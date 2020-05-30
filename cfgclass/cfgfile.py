from .cfgscope import Scope


class File(Scope):
    """
    Config file.
    """

    def __init__(self, filename):
        super(File, self).__init__()
        self._filename = filename
