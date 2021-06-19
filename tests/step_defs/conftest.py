# Copyright (C) 2012-2021 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from jrnl.os_compat import on_windows
from pytest import mark

from .fixtures import *
from .given_steps import *
from .when_steps import *
from .then_steps import *


def pytest_bdd_apply_tag(tag, function):
    if tag == "skip_win":
        marker = mark.skipif(on_windows(), reason="Skip test on Windows")
    elif tag == "skip_editor":
        marker = mark.skip(
            reason="Skipping editor-related test. We should come back to this!"
        )
    else:
        # Fall back to pytest-bdd's default behavior
        return None

    marker(function)
    return True
