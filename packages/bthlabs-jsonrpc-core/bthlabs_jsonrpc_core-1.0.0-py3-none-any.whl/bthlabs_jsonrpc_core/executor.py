# -*- coding: utf-8 -*-
# django-jsonrpc-core | (c) 2022-present Tomek Wójcik | MIT License
from contextlib import contextmanager
from dataclasses import dataclass
import json
import logging
import typing

from bthlabs_jsonrpc_core.exceptions import (
    BaseJSONRPCError,
    JSONRPCInternalError,
    JSONRPCInvalidParamsError,
    JSONRPCInvalidRequestError,
    JSONRPCMethodNotFoundError,
    JSONRPCParseError,
)
from bthlabs_jsonrpc_core.registry import MethodRegistry
from bthlabs_jsonrpc_core.serializer import JSONRPCSerializer

LOGGER = logging.getLogger('bthlabs_jsonrpc.core.executor')


class Executor:
    """
    *Executor* is the main interface for the integrations. It processes the
    JSONRPC request, executes the calls and returns the responses.

    *namespace* will be used to look up called methods in the registry. If
    omitted, it'll fall back to the default namespace.

    Example:

    .. code-block:: python

        def rpc_handler(request):
            executor = Executor()
            serializer = executor.execute(request.body)

            return JSONResponse(serializer.data)
    """

    # pragma mark - Private class attributes

    # Supported internal methods.
    # These methods will be resolved and handled internally.
    INTERNAL_METHODS = ('system.list_methods',)

    # The method registry class to use for handler lookups.
    registry = MethodRegistry

    # The serializer registry class to use for response serialization.
    serializer = JSONRPCSerializer

    @dataclass
    class CallContext:
        """
        The context of a single call.

        :meta private:
        """

        #: Method
        method: str

        #: Handler
        handler: typing.Callable

        #: Call args
        args: list[typing.Any]

        #: Call kwargs
        kwargs: dict

        #: Call result
        result: typing.Optional[typing.Any] = None

        @classmethod
        def invalid_context(cls):
            return cls(None, None, None, None)

        @property
        def is_valid(self) -> bool:
            """Returns ``True`` if the context is valid."""
            return all((
                self.method is not None,
                self.handler is not None,
                self.args is not None,
                self.kwargs is not None,
            ))

    @dataclass
    class ExecuteContext:
        """
        The context of an execute call.

        :meta private:
        """

        #: List of call results.
        results: list

        #: The serializer instance.
        serializer: typing.Optional[JSONRPCSerializer] = None

    # pragma mark - Private interface

    def __init__(self, namespace=None):
        self.namespace = namespace or MethodRegistry.DEFAULT_NAMESPACE

    def get_internal_handler(self, method: str) -> typing.Callable:
        """
        Returns the internal handler for *method* or raises
        ``JSONRPCMethodNotFoundError``.

        :meta private:
        """
        match method:
            case 'system.list_methods':
                return self.list_methods

            case _:
                raise JSONRPCMethodNotFoundError()

    def get_calls(self, data: typing.Union[dict, list]) -> list:
        """
        Returns the list of calls.

        If *data* is a list, it's returned verbatim. If it's a dict, it's
        wrapped in a list.

        Raises ``JSONRPCInvalidRequestError`` if the effective list of calls
        is empty:

        :meta private:
        """
        result = list()
        if isinstance(data, list):
            result = data
        else:
            result.append(data)

        if len(result) == 0:
            raise JSONRPCInvalidRequestError()

        return result

    def get_call_spec(self,
                      call: typing.Any,
                      ) -> tuple[str, typing.Callable, list, dict]:
        """
        Validates and pre-processes the *call*.

        Returns tuple of *method*, *handler*, *args*, *kwargs*.

        :meta private:
        """
        method = None
        handler = None
        args = []
        kwargs = {}

        try:
            assert isinstance(call, dict), JSONRPCInvalidRequestError
            assert call.get('jsonrpc', None) == '2.0', JSONRPCInvalidRequestError

            method = call.get('method', None)
            assert method is not None, JSONRPCInvalidRequestError

            if method in self.INTERNAL_METHODS:
                handler = self.get_internal_handler(method)
            else:
                handler = self.registry.shared_registry().get_handler(
                    self.namespace, method,
                )

            assert handler is not None, JSONRPCMethodNotFoundError
        except AssertionError as exception:
            klass = exception.args[0]
            raise klass()

        call_params = call.get('params', None)
        if call_params is not None:
            if isinstance(call_params, list):
                args = call_params
            elif isinstance(call_params, dict):
                kwargs = call_params
            else:
                raise JSONRPCInvalidParamsError()

        args = self.enrich_args(args)
        kwargs = self.enrich_kwargs(kwargs)

        return method, handler, args, kwargs

    def process_results(self,
                        results: list,
                        ) -> typing.Optional[typing.Union[list, dict]]:
        """
        Post-processes the *results* and returns responses.

        If *results* is a single-element list, the result is a single
        response object. Otherwise, it's a list of response objects.

        If the effective response is empty (e.g. all the calls were
        notifications), returns ``None``.

        :meta private:
        """
        responses = []
        for result in results:
            call, call_result = result

            response: dict[str, typing.Any] = {
                'jsonrpc': '2.0',
            }

            if call is None:
                response['id'] = None
                response['error'] = call_result
            elif call.get('id', None) is not None:
                response['id'] = call['id']

                if isinstance(call_result, BaseJSONRPCError):
                    response['error'] = call_result
                else:
                    response['result'] = call_result
            else:
                continue

            responses.append(response)

        if len(responses) == 0:
            return None
        elif len(responses) == 1:
            return responses[0]

        return responses

    @contextmanager
    def call_context(self, execute_context: ExecuteContext, call: dict):
        """
        The call context manager. Yields ``CallContext``, which can be
        invalid invalid if there was en error processing the call.

        Handles errors and the call result accordingly.

        :meta private:
        """
        method = None
        error = None

        try:
            context = self.CallContext.invalid_context()
            try:
                method, handler, args, kwargs = self.get_call_spec(call)
                context = self.CallContext(method, handler, args, kwargs)
            except BaseJSONRPCError as exception:
                error = exception

            yield context
        except Exception as exception:
            if isinstance(exception, BaseJSONRPCError):
                error = exception
            else:
                LOGGER.error(
                    f'Error handling RPC method: {method}!',
                    exc_info=exception,
                )
                error = JSONRPCInternalError(str(exception))
        finally:
            if error is not None:
                execute_context.results.append((call, error))
            else:
                execute_context.results.append((call, context.result))

    @contextmanager
    def execute_context(self):
        """
        The execution context. Yields ``ExecuteContext``.

        Handles errors and manages the serializer post execution.

        :meta private:
        """
        try:
            context = self.ExecuteContext([])
            yield context
        except Exception as exc:
            if isinstance(exc, BaseJSONRPCError):
                context.results = [(None, exc)]
            else:
                raise

        responses = self.process_results(context.results)
        if responses is not None:
            context.serializer = self.serializer(responses)

    # pragma mark - Public interface

    def deserialize_data(self, data: bytes) -> typing.Any:
        """
        Deserializes *data* and returns the result.

        Raises :py:exc:`JSONRPCParseError` if there was an error in the process.
        Subclasses should also raise this exception, so it can be resulting
        response object conforms to the spec.
        """
        try:
            return json.loads(data)
        except Exception as exception:
            LOGGER.error('Error deserializing RPC call!', exc_info=exception)
            raise JSONRPCParseError() from exception

    def list_methods(self, *args, **kwargs) -> list[str]:
        """
        The handler for ``system.list_methods`` internal method.

        Returns list of methods this *Executor* can handle.
        """
        result = list(self.INTERNAL_METHODS)
        result.extend(MethodRegistry.shared_registry().get_methods(
            self.namespace,
        ))

        return result

    def enrich_args(self, args: list) -> list:
        """
        Hook for subclasses to pass additional args to the handler. The default
        implementation returns the *args* verbatim.

        Example:

        .. code-block:: python

            class ExampleExecutor(Executor):
                def enrich_args(self, args):
                    return ['spam', *args]
        """
        return [*args]

    def enrich_kwargs(self, kwargs: dict) -> dict:
        """
        Hook for subclasses to pass additional kwaargs to the handler.
        The default implementation returns the *kwargs* verbatim.

        Example:

        .. code-block:: python

            class ExampleExecutor(Executor):
                def enrich_kwargs(self, kwargs):
                    return {'spam': True, **kwargs}
        """
        return {**kwargs}

    def before_call(self, method: str, args: list, kwargs: dict):
        """
        Hook for subclasses to perform additional operations before executing
        the call.

        If this method raises a subclass of
        :py:exc:`BaseJSONRPCError`, it'll be used to construct the response
        object directly. Any other exception will be wrapped in
        :py:exc:`JSONRPCInternalError`.

        The default implementation does nothing.
        """
        pass

    def execute(self,
                payload: typing.Any,
                ) -> typing.Optional[JSONRPCSerializer]:
        """
        Executes the JSONRPC request in *payload*.

        Returns an instance of :py:class:`JSONRPCSerializer` or ``None`` if
        the list of responses is empty.
        """
        with self.execute_context() as execute_context:
            data = self.deserialize_data(payload)

            calls = self.get_calls(data)
            for call in calls:
                with self.call_context(execute_context, call) as call_context:
                    if call_context.is_valid is True:
                        self.before_call(
                            call_context.method,
                            call_context.args,
                            call_context.kwargs,
                        )

                        call_context.result = call_context.handler(
                            *call_context.args, **call_context.kwargs,
                        )

        return execute_context.serializer
