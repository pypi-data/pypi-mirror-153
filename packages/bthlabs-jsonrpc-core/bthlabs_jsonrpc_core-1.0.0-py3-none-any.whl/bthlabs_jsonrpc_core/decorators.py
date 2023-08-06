# -*- coding: utf-8 -*-
# django-jsonrpc-core | (c) 2022-present Tomek Wójcik | MIT License
import typing

from bthlabs_jsonrpc_core.registry import MethodRegistry


def register_method(method: str,
                    namespace: typing.Optional[str] = None,
                    ) -> typing.Callable:
    """
    Registers the decorated function as JSONRPC *method* in *namespace*.
    If *namespace* is omitted, the function will be registered in the default
    namespace.

    Example:

    .. code-block:: python

        @register_method('example')
        def example(a, b):
            return a + b
    """
    if namespace is None:
        namespace = MethodRegistry.DEFAULT_NAMESPACE

    def decorator(handler: typing.Callable) -> typing.Callable:
        registry = MethodRegistry.shared_registry()
        registry.register_method(namespace, method, handler)

        handler.jsonrpc_method = method
        handler.jsonrpc_namespace = namespace
        return handler

    return decorator
