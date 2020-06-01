import re
import tokenize

from .parsable import Parsable, ParseError, UnexpectedEOFError, TryParseError
from .cfgvalue import String, Number, Bool, Array
from .cfgscope import Class


class Property(Parsable):
    def __init__(self, parent, name, value):
        super(Property, self).__init__(parent)
        self._name = name
        self._value = value

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    @classmethod
    def parse(cls, clex_object, parent):
        parsed_property = cls(parent, None, None)
        parse_types = [String, Number, Bool]

        # Get first token
        token = clex_object.get_token()
        if token == clex_object.eof:
            raise UnexpectedEOFError(clex_object)

        # If class, set parse type and read name as next token
        if 'class' == token:
            parse_types = [Class]
            token = clex_object.get_token()
            if token == clex_object.eof:
                raise UnexpectedEOFError(clex_object)

        # Property name
        if not re.match(tokenize.Name, token):
            raise ParseError(clex_object, 'invalid property name')
        parsed_property._name = token

        # If a non-class value is being parsed, get operator
        if parse_types != [Class]:
            operator = clex_object.get_token()
            if operator == '[':
                if ']' != clex_object.get_token():
                    raise ParseError(clex_object, 'expected ]')
                parse_types = [Array]

            if '=' != clex_object.get_token():
                raise ParseError(clex_object, 'expected =')

        # Try parse property value by type
        for parse_type in parse_types:
            try:
                parsed_property._value = parse_type.parse(clex_object, parsed_property)
            except TryParseError:
                continue
            break

        # If no property was parsed, raise
        if parsed_property._value is None:
            raise ParseError(clex_object, 'could not parse value')

        # Parse semicolon
        if ';' != clex_object.get_token():
            raise ParseError(clex_object, 'expected ;')

        return parsed_property
