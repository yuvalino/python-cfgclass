from .parsable import Parsable, ParseError, UnexpectedEOFError, TryParseError


class DuplicateError(NameError):
    pass


class Scope(Parsable):
    """
    Basic config scope with inner properties.
    Can describe a file or a class.
    """
    def __init__(self, parent):
        super(Scope, self).__init__(parent)
        self._properties = dict()

    def add_property(self, new_property):
        if new_property.name in self._properties:
            raise DuplicateError(new_property.name)
        self._properties[new_property.name] = new_property

    @classmethod
    def parse(cls, clex_object, parent):
        scope = cls(parent)
        token = clex_object.get_token()
        if token == clex_object.eof:
            raise UnexpectedEOFError(clex_object)




class Class(Scope):

    def __init__(self, parent, defined, base_class):