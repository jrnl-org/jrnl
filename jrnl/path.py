import os.path


def home_dir():
    return os.path.expanduser("~")


def expand_path(path):
    return os.path.expanduser(os.path.expandvars(path))


def absolute_path(path):
    return os.path.abspath(expand_path(path))
