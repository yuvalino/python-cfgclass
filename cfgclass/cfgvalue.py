import ast
import six

import json

from .parsable import Parsable, ParseError, UnexpectedEOFError, TryParseError


class Value(Parsable):
    """
    Base cfgclass value.
    """
    def __init__(self, parent, value):
        super(Value, self).__init__(parent)
        self.validate(value)
        self._value = value

    def get(self):
        """
        Get the pythonic value.
        """
        return self._value

    @classmethod
    def validate(cls, value):
        """
        Validate the given value.
        """
        raise NotImplementedError


class String(Value):
    @classmethod
    def validate(cls, value):
        if not isinstance(value, six.text_type):
            raise TypeError(type(value).__name__)

    @classmethod
    def parse(cls, clex_object, parent):
        token = clex_object.get_token()
        if token == clex_object.eof:
            raise UnexpectedEOFError(clex_object)

        try:
            literal = ast.literal_eval(token)
            cls.validate(literal)
            return cls(parent, literal)
        except:
            clex_object.push_token(token)
            raise TryParseError(clex_object)


class Number(Value):
    @classmethod
    def validate(cls, value):
        if not isinstance(value, (float, six.integer_types)):
            raise TypeError(type(value).__name__)

    @classmethod
    def parse(cls, clex_object, parent):
        token = clex_object.get_token()
        if token == clex_object.eof:
            raise UnexpectedEOFError(clex_object)

        try:
            literal = ast.literal_eval(token)
            cls.validate(literal)
            return cls(parent, literal)
        except:
            clex_object.push_token(token)
            raise TryParseError(clex_object)


class Bool(Value):
    @classmethod
    def validate(cls, value):
        if not isinstance(value, bool):
            raise TypeError(type(value).__name__)

    @classmethod
    def parse(cls, clex_object, parent):
        token = clex_object.get_token()
        if token == clex_object.eof:
            raise UnexpectedEOFError(clex_object)

        try:
            literal = json.loads(token)
            cls.validate(literal)
            return cls(parent, literal)
        except:
            clex_object.push_token(token)
            raise TryParseError(clex_object)


class Array(Value):
    @staticmethod
    def _supported_types():
        return String, Number, Bool, Array

    @classmethod
    def validate(cls, value):
        if not isinstance(value, list):
            raise TypeError(type(value).__name__)
        for inner_value in value:
            if not isinstance(inner_value, cls._supported_types()):
                raise TypeError(type(inner_value).__name__)

    @classmethod
    def parse(cls, clex_object, parent):
        token = clex_object.get_token()
        if token == clex_object.eof:
            raise UnexpectedEOFError(clex_object)

        if '{' != token:
            clex_object.push_token(token)
            raise TryParseError

        value = cls(parent, list())
        while True:
            token = clex_object.get_token()
            if token == clex_object.eof:
                raise UnexpectedEOFError(clex_object)
            if '}' == token:
                break

            item = None
            for item_type in cls._supported_types():
                try:
                    item = item_type.parse(clex_object, value)
                except TryParseError:
                    continue
                break

            if item is None:
                raise ParseError(clex_object, 'could not parse item')

            value.get().append(item)
        return value
