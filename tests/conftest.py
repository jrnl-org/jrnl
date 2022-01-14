# Copyright (C) 2012-2021 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from pytest import mark

from jrnl.os_compat import on_windows


pytest_plugins = [
    "tests.lib.fixtures",
    "tests.lib.given_steps",
    "tests.lib.when_steps",
    "tests.lib.then_steps",
]


def pytest_bdd_apply_tag(tag, function):
    if tag == "skip_win":
        marker = mark.skipif(on_windows(), reason="Skip test on Windows")
    else:
        # Fall back to pytest-bdd's default behavior
        return None

    marker(function)
    return True
