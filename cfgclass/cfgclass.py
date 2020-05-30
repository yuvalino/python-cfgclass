

class Class(object):
    """
    Config class.
    """

    def __init__(self, parent=None, name=None):
        self._parent = parent
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
