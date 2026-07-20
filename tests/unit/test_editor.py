# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import io
import os
from unittest.mock import Mock
from unittest.mock import mock_open
from unittest.mock import patch

import pytest

from jrnl.editor import get_template_path
from jrnl.editor import read_stdin_text
from jrnl.editor import read_template_file
from jrnl.exception import JrnlException


@patch(
    "os.getcwd", side_effect="/"
)  # prevent failures in CI if current directory has been deleted
@patch("builtins.open", side_effect=FileNotFoundError())
def test_read_template_file_with_no_file_raises_exception(mock_open, mock_getcwd):
    with pytest.raises(JrnlException) as ex:
        read_template_file("invalid_file.txt")
        assert isinstance(ex.value, JrnlException)


@patch(
    "os.getcwd", side_effect="/"
)  # prevent failures in CI if current directory has been deleted
@patch("builtins.open", new_callable=mock_open, read_data="template text")
def test_read_template_file_with_valid_file_returns_text(mock_file, mock_getcwd):
    assert read_template_file("valid_file.txt") == "template text"


def test_get_template_path_when_exists_returns_correct_path():
    with patch("os.path.exists", return_value=True):
        output = get_template_path("template", "templatepath")

    assert output == os.path.join("templatepath", "template")


@patch("jrnl.editor.absolute_path")
def test_get_template_path_when_doesnt_exist_returns_correct_path(mock_absolute_paths):
    with patch("os.path.exists", return_value=False):
        output = get_template_path("template", "templatepath")

    assert output == mock_absolute_paths.return_value


def test_read_stdin_text_with_invalid_utf8_does_not_raise():
    # Regression test for https://github.com/jrnl-org/jrnl/issues/2082
    # A backspace over a multi-byte character (e.g. ß) in a canonical-mode
    # terminal only erases one byte, leaving stray invalid UTF-8 like this.
    raw_bytes = b"I saw Elvis. " + bytes([0xC3]) + b"ss"
    stdin = io.TextIOWrapper(io.BytesIO(raw_bytes), encoding="utf-8")

    with patch("sys.stdin", stdin):
        read_stdin_text()  # should not raise UnicodeDecodeError


def test_read_stdin_text_replaces_invalid_utf8_with_replacement_character():
    raw_bytes = b"I saw Elvis. " + bytes([0xC3]) + b"ss"
    stdin = io.TextIOWrapper(io.BytesIO(raw_bytes), encoding="utf-8")

    with patch("sys.stdin", stdin):
        result = read_stdin_text()

    assert result == "I saw Elvis. \ufffdss"


def test_read_stdin_text_when_stdin_does_not_support_reconfigure():
    # Some stdin replacements (e.g. pytest-xdist's captured stdin) don't
    # support reconfigure(); reading should still work in that case.
    stdin = Mock(spec=["read"])
    stdin.read.return_value = "I saw Elvis."

    with patch("sys.stdin", stdin):
        result = read_stdin_text()

    assert result == "I saw Elvis."
