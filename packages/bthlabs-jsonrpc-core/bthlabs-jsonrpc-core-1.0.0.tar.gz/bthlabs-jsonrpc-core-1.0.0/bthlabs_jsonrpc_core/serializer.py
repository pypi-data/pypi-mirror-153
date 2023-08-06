# -*- coding: utf-8 -*-
# django-jsonrpc-core | (c) 2022-present Tomek Wójcik | MIT License
import datetime
import decimal
import typing
import uuid

from bthlabs_jsonrpc_core.exceptions import JSONRPCSerializerError


class JSONRPCSerializer:
    """
    Serializer for JSONRPC responses.

    This class is responsible for making the respones JSON-serializable.
    Sequence types are all converted to lists. Dict-like types are all
    converted to plain dicts. Simple types (``bool``, ``float``, ``int`` and
    ``str``) and ``None`` are returned as they are.

    Datetime values are converted to strings using the ISO format. ``UUID`` and
    ``Decimal`` values are explicitly coerced to strings.

    For values of other types, the serializer will try to invoke their
    ``to_rpc()`` method. If that fails, the serializer will raise
    :py:exc:`JSONRPCSerializerError`.

    Example:

    .. code-block:: python

        spam = ['eggs', {'spam': False}, Decimal('42.0')]
        serializer = JSONRPCSerializer(spam)
        print(serializer.data)

    Example with ``to_rpc()``:

    .. code-block:: python

        class Spam:
            def to_rpc(self):
                return {
                    'spam': True
                }

        spam = ['eggs', Spam(), Decimal('42.0')]
        serializer = JSONRPCSerializer(spam)
        print(serializer.data)
    """

    # Datetime types
    DATETIME_TYPES = (datetime.date, datetime.datetime, datetime.time)

    # Sequence types
    SEQUENCE_TYPES = (set,)

    # Simple types
    SIMPLE_TYPES = (bool, float, int, str)

    # Types that can be coerced to string
    STRING_COERCIBLE_TYPES = (uuid.UUID, decimal.Decimal)

    def __init__(self, data):
        self._data = data

    def is_simple_value(self, value: typing.Any) -> bool:
        """
        Returns ``True`` if *value* is a simple value.

        :meta private:
        """
        value_type = type(value)
        return (
            value is None or value_type in self.SIMPLE_TYPES
        )

    def is_datetime_value(self, value: typing.Any) -> bool:
        """
        Returns ``True`` if *value* is a datetime value.

        :meta private:
        """
        return type(value) in self.DATETIME_TYPES

    def is_sequence_value(self, value: typing.Any) -> bool:
        """
        Returns ``True`` if *value* is a sequence value.

        :meta private:
        """
        return any((
            isinstance(value, typing.Sequence),
            isinstance(value, typing.Generator),
            type(value) in self.SEQUENCE_TYPES,
        ))

    def is_dict_value(self, value: typing.Any) -> bool:
        """
        Returns ``True`` if *value* is a simple value.

        :meta private:
        """
        return isinstance(value, typing.Dict)

    def is_string_coercible_value(self, value: typing.Any) -> bool:
        """
        Returns ``True`` if *value* is a coercible to string.

        :meta private:
        """
        return type(value) in self.STRING_COERCIBLE_TYPES

    def serialize_datetime(self, value: typing.Any) -> typing.Any:
        """
        Serializes a datetime value.

        :meta private:
        """
        return value.isoformat()

    def serialize_sequence(self, value: typing.Any) -> typing.Any:
        """
        Serializes a sequence value.

        :meta private:
        """
        return [self.serialize_value(item) for item in value]

    def serialize_dict(self, value: typing.Any) -> typing.Any:
        """
        Serializes a dict-like value.

        :meta private:
        """
        return {
            key: self.serialize_value(item) for key, item in value.items()
        }

    def serialize_string_coercible(self, value: typing.Any) -> typing.Any:
        """
        Serializes a string-coercible value.

        :meta private:
        """
        return str(value)

    def serialize_value(self, value: typing.Any) -> typing.Any:
        """
        Serializes *value* and returns the result.

        :meta private:
        """
        if isinstance(value, JSONRPCSerializer):
            return value.data
        elif self.is_simple_value(value):
            return value
        if self.is_datetime_value(value):
            return self.serialize_datetime(value)
        elif self.is_sequence_value(value):
            return self.serialize_sequence(value)
        elif self.is_dict_value(value):
            return self.serialize_dict(value)
        elif self.is_string_coercible_value(value):
            return self.serialize_string_coercible(value)
        elif hasattr(value, 'to_rpc'):
            return self.serialize_value(value.to_rpc())
        else:
            raise JSONRPCSerializerError(
                'Object of type {type} is not RPC serializable'.format(
                    type=type(value),
                ),
            )

        return value

    @property
    def data(self) -> typing.Any:
        """The serialized data."""
        if not hasattr(self, '_serialized_data'):
            self._serialized_data = self.serialize_value(self._data)

        return self._serialized_data
