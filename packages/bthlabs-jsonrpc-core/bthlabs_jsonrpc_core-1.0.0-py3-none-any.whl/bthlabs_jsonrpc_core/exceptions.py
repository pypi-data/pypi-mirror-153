# -*- coding: utf-8
# django-jsonrpc-core | (c) 2022-present Tomek Wójcik | MIT License
class BaseJSONRPCError(Exception):
    """
    Base class for JSONRPC exceptions.

    If *data* is provided, it'll be added to the exception's response payload.
    """

    #: Error code
    ERROR_CODE: int = -32001

    #: Error message
    ERROR_MESSAGE: str = 'JSONRPC Error'

    def __init__(self, data=None):
        self.data = data

    def to_rpc(self) -> dict:
        """Returns payload for :py:class:`JSONRPCSerializer`."""
        result = {
            'code': self.ERROR_CODE,
            'message': self.ERROR_MESSAGE,
        }

        if self.data:
            result['data'] = self.data

        return result


class JSONRPCParseError(BaseJSONRPCError):
    """Parse error"""

    #: Error code
    ERROR_CODE = -32700

    #: Error message
    ERROR_MESSAGE = 'Parse error'


class JSONRPCInvalidRequestError(BaseJSONRPCError):
    """Invalid request error"""

    #: Error code
    ERROR_CODE = -32600

    #: Error message
    ERROR_MESSAGE = 'Invalid Request'


class JSONRPCMethodNotFoundError(BaseJSONRPCError):
    """Method not found error"""

    #: Error code
    ERROR_CODE = -32601

    #: Error message
    ERROR_MESSAGE = 'Method not found'


class JSONRPCInvalidParamsError(BaseJSONRPCError):
    """Invalid params error"""

    #: Error code
    ERROR_CODE = -32602

    #: Error message
    ERROR_MESSAGE = 'Invalid params'


class JSONRPCInternalError(BaseJSONRPCError):
    """Internal error"""

    #: Error code
    ERROR_CODE = -32603

    #: Error message
    ERROR_MESSAGE = 'Internal error'


class JSONRPCSerializerError(BaseJSONRPCError):
    """Serializer error"""

    #: Error code
    ERROR_CODE = -32002

    #: Error message
    ERROR_MESSAGE = 'JSONRPCSerializer error'


class JSONRPCAccessDeniedError(BaseJSONRPCError):
    """Access denied error"""

    #: Error code
    ERROR_CODE = -32003

    #: Error message
    ERROR_MESSAGE = 'Access denied'
