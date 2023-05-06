# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from jrnl.main import run


def test_whatever():
    expected_output = """
        a: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
        b: {c: 1, d: 2}
    """.strip()
    assert run() == expected_output
