# Copyright (C) 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from unittest import mock

import pytest

from jrnl.os_compat import on_posix
from jrnl.os_compat import on_windows
from jrnl.os_compat import split_args


@pytest.mark.parametrize(
    "systems",
    [
        ["linux", False],
        ["win32", True],
        ["cygwin", False],
        ["msys", False],
        ["darwin", False],
        ["os2", False],
        ["os2emx", False],
        ["riscos", False],
        ["atheos", False],
        ["freebsd7", False],
        ["freebsd8", False],
        ["freebsdN", False],
        ["openbsd6", False],
    ],
)
def test_on_windows(systems):
    osname, expected_on_windows = systems[0], systems[1]
    with mock.patch("jrnl.os_compat.platform", osname):
        assert on_windows() == expected_on_windows


@pytest.mark.parametrize(
    "systems",
    [
        ["linux", True],
        ["win32", False],
        ["cygwin", True],
        ["msys", True],
        ["darwin", True],
        ["os2", True],
        ["os2emx", True],
        ["riscos", True],
        ["atheos", True],
        ["freebsd7", True],
        ["freebsd8", True],
        ["freebsdN", True],
        ["openbsd6", True],
    ],
)
def test_on_posix(systems):
    osname, expected_on_posix = systems[0], systems[1]
    with mock.patch("jrnl.os_compat.platform", osname):
        assert on_posix() == expected_on_posix


@pytest.mark.parametrize(
    "args",
    [
        ["notepad", ["notepad"]],
        ["subl -w", ["subl", "-w"]],
        [
            '"C:\\Program Files\\Sublime Text 3\\subl.exe" -w',
            ['"C:\\Program Files\\Sublime Text 3\\subl.exe"', "-w"],
        ],
    ],
)
def test_split_args_on_windows(args):
    input_arguments, expected_split_args = args[0], args[1]
    with mock.patch("jrnl.os_compat.on_windows", lambda: True):
        assert split_args(input_arguments) == expected_split_args


@pytest.mark.parametrize(
    "args",
    [
        ["vim", ["vim"]],
        [
            'vim -f +Goyo +Limelight "+set spell linebreak"',
            ["vim", "-f", "+Goyo", "+Limelight", '"+set spell linebreak"'],
        ],
    ],
)
def test_split_args_on_not_windows(args):
    input_arguments, expected_split_args = args[0], args[1]
    with mock.patch("jrnl.os_compat.on_windows", lambda: True):
        assert split_args(input_arguments) == expected_split_args
