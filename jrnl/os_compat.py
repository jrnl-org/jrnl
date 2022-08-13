# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import shlex
from sys import platform


def on_windows():
    return "win32" in platform


def on_posix():
    return not on_windows()


def split_args(args):
    """Split arguments and add escape characters as appropriate for the OS"""
    return shlex.split(args, posix=on_posix())
