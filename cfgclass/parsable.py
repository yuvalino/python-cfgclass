import clex


class ParseError(RuntimeError):
    def __init__(self, clex_object, what=None):
        self._clex = clex_object
        super(ParseError, self).__init__(what)


class UnexpectedEOFError(ParseError):
    def __init__(self, clex_object, what=None):
        super(UnexpectedEOFError, self).__init__(clex_object, what if what is not None else 'unexpected eof')


class TryParseError(ParseError):
    pass


class Parsable(object):
    """
    Base parsable config object.
    By design, all parsable objects have a linked parent (either an array, class or file)
    """
    def __init__(self, parent):
        self._parent = parent

    @property
    def parent(self):
        return self._parent

    @classmethod
    def parse(cls, clex_object, parent):
        """
        :type clex_object: clex.clex
        :rtype: Parsable

        :raises ParseError: Fatal error that cannot allow parsing to continue.
        :raises TryParseError: Error that allows parsing to continue incase another parsable may be parsed instead.
        """
        raise NotImplementedError
