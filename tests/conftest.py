# Copyright © 2012-2023 jrnl contributors
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
        logger.info(f'Condition in body log is: tag({tag}) = "skip_win"') # STRUDEL_LOG ured
        marker = mark.skipif(on_windows(), reason="Skip test on Windows")
    elif tag == "skip_posix":
        logger.info(f'Condition in body log is: tag({tag}) = "skip_posix"') # STRUDEL_LOG ddbs
        marker = mark.skipif(on_posix(), reason="Skip test on Mac/Linux")

    # only on OS markers
    elif tag == "on_win":
        logger.info(f'Condition in body log is: tag({tag}) = "on_win"') # STRUDEL_LOG zjqp
        marker = mark.skipif(not on_windows(), reason="Skip test not on Windows")
    elif tag == "on_posix":
        logger.info(f'Condition in body log is: tag({tag}) = "on_posix"') # STRUDEL_LOG zgja
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
        logger.info(f'Condition in body log is: "skip_win" in markers BoolOp on_win') # STRUDEL_LOG iabq
        skip("Skip test on Windows")

    if "skip_posix" in markers and on_nix:
        logger.info(f'Condition in body log is: "skip_posix" in markers BoolOp on_nix') # STRUDEL_LOG asee
        skip("Skip test on Mac/Linux")

    if "on_win" in markers and not on_win:
        logger.info(f'Condition in body log is: "on_win" in markers BoolOp (not on_win) is True') # STRUDEL_LOG gknf
        skip("Skip test not on Windows")

    if "on_posix" in markers and not on_nix:
        logger.info(f'Condition in body log is: "on_posix" in markers BoolOp (not on_nix) is True') # STRUDEL_LOG ojpo
        skip("Skip test not on Mac/Linux")