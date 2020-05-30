from .cfgproperty import Property


class DuplicateError(NameError):
    pass


class Scope(object):
    """
    Basic config scope with inner properties.
    Can describe a file or a class for example.
    """
    def __init__(self):
        self._properties = dict()

    def add_property(self, new_property):
        """
        :type new_property: Property
        """
        if new_property.name in self._properties:
            raise DuplicateError(new_property.name)
        self._properties[new_property.name] = new_property
