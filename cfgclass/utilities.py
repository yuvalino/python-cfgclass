from .cfgnamespace import Namespace
from .parsing import parse_file


def load(fp):
    """
    Load config namespace from file.
    """
    ns = Namespace()
    ns.add_file(parse_file(fp))
    return ns
