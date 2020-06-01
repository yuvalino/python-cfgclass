import re
import clex
import tokenize


from .cfgfile import File
from .cfgclass import Class
from .cfgscope import Scope


class ParseError(Exception):
    """
    Raised when a parsing error is encountered and cannot be recovered from.
    """
    pass


class TryParseError(ParseError):
    """
    Raised when a parsing error is encountered but should be caught in the call stack and continued.
    Any parsing state should be reset when this exception goes up the call stack.
    """
    pass

class Parser(object):
    """
    Base parser.
    """
    def __init__(self, clex_object):
        """
        :type clex_object: clex.clex
        """
        self._clex = clex_object

    def parse(self, scope):
        """
        Parse an instance of parser's type.
        :type scope: Scope
        :raise ParseError: When a fatal error occurs.
        :raise TryParseError: When a non-fatal parsing error occurs (clex state is restored).
        """
        raise NotImplementedError

    @property
    def clex(self):
        return self._clex


class StringParser(Parser):

    def parse(self, scope):
        value =

class ArrayParser(object):
    pass

class ScopeParser(Parser):
    def __init__(self, clex_object, parent):
        """
        :type clex_object: clex.clex
        """
        super(ScopeParser, self).__init__(clex_object, parent)

    def _parse_property(self):

        parsed_property = None
        for inner_type in (ClassParser, PrimitiveParser, ArrayParser):
            try:
                parsed_property = inner_type(self.clex, self.parent)
            except TryParseError:
                continue




class ClassParser(object):

    def __init__(self, clex_object, parent=None):
        """
        :type clex_object: clex.clex
        """
        self._clex = clex_object
        self._class = Class(parent=parent)

    def parse(self):
        """
        Parse class (from clex object).
        :rtype: any
        """
        # Get `class` token
        class_token = self._clex.get_token()
        if 'class' != class_token:
            self._clex.push_token(class_token)
            raise TryParseError

        # Get class name
        class_name = self._clex.get_token()
        if not re.match(tokenize.Name, class_name):
            raise ParseError
        self._class.name = class_name

        # Get class opening
        if '{' != self._clex.get_token():
            raise ParseError

        # Get inners
        while True:
            token = self._clex.get_token()
            if self._clex.eof == token:
                raise ParseError
            if '}' == token:
                break
            self._clex.push_token(token)
            self.parse_inner()

        # Get semicolon
        if ';' != self._clex.get_token():
            raise ParseError

        return self._class

    def parse_inner(self):
        raise NotImplementedError


class FileParser(object):

    def __init__(self, clex_object, filename=None):
        """
        :type clex_object: clex.clex
        """
        self._clex = clex_object
        self._file = File(filename=filename)

    def parse(self):
        """
        Parse file (from clex object) until end is reached.
        :rtype: File
        """
        while True:
            token = self._clex.get_token()
            if self._clex.eof == token:
                break
            self._clex.push_token(token)
            self.parse_inner()

        return self._file

    def parse_inner(self):
        inner = None

        for inner_type in [ClassParser]:
            try:
                inner = inner_type(self._clex, self).parse()
            except TryParseError:
                continue

        if inner is None:
            raise ParseError

        self._file.


def parse_file(instream, filename=None):
    """
    Parse a config file.
    May optionally provide filename.
    """
    parsed_file = FileParser(clex.clex(instream)).parse()
    return parsed_file
