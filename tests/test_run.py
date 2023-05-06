# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from jrnl.main import run


def test_passes():
    num = 80
    assert run(num) == "a: " + ("a" * num) +  "\nb:\n  c: 1\n  d: 2\n"


def test_fails():
    num = 81
    assert run(num) == "a: " + ("a" * num) +  "\nb:\n  c: 1\n  d: 2\n"

