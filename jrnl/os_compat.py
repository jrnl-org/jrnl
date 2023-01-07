# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import shlex
from sys import platform


def on_windows() -> bool:
    return "win32" in platform


def on_posix() -> bool:
    return not on_windows()


def split_args(args: str) -> list[str]:
    """Split arguments and add escape characters as appropriate for the OS"""
    return shlex.split(args, posix=on_posix())
