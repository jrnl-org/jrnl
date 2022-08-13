# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from pytest import mark
from pytest import skip

from jrnl.os_compat import on_posix
from jrnl.os_compat import on_windows

pytest_plugins = [
    "tests.lib.fixtures",
    "tests.lib.given_steps",
    "tests.lib.when_steps",
    "tests.lib.then_steps",
]


def pytest_bdd_apply_tag(tag, function):
    # skip markers
    if tag == "skip_win":
        marker = mark.skipif(on_windows(), reason="Skip test on Windows")
    elif tag == "skip_posix":
        marker = mark.skipif(on_posix(), reason="Skip test on Mac/Linux")

    # only on OS markers
    elif tag == "on_win":
        marker = mark.skipif(not on_windows(), reason="Skip test not on Windows")
    elif tag == "on_posix":
        marker = mark.skipif(not on_posix(), reason="Skip test not on Mac/Linux")
    else:
        # Fall back to pytest-bdd's default behavior
        return None

    marker(function)
    return True


def pytest_runtest_setup(item):
    markers = [mark.name for mark in item.iter_markers()]

    on_win = on_windows()
    on_nix = on_posix()

    if "skip_win" in markers and on_win:
        skip("Skip test on Windows")

    if "skip_posix" in markers and on_nix:
        skip("Skip test on Mac/Linux")

    if "on_win" in markers and not on_win:
        skip("Skip test not on Windows")

    if "on_posix" in markers and not on_nix:
        skip("Skip test not on Mac/Linux")
