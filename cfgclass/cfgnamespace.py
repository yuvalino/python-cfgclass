

class Namespace(object):
    """
    Namespace for config files.
    All external inheritance between files is resolved within this namespace.
    """

    def __init__(self):
        pass

    def add_file(self, file):
        """
        Adds a file to the namespace.
        """
        raise NotImplementedError

    def to_dict(self):
        """
        Convert the namespace to a dictionary (irreversible).
        """
        raise NotImplementedError
