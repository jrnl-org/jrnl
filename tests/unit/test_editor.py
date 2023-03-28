# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import os
from unittest.mock import mock_open
from unittest.mock import patch

import pytest

from jrnl.editor import get_template_path
from jrnl.editor import read_template_file
from jrnl.exception import JrnlException


@patch("builtins.open", side_effect=FileNotFoundError())
def test_read_template_file_with_no_file_raises_exception(mock_open):
    with pytest.raises(JrnlException) as ex:
        read_template_file("invalid_file.txt")
        assert isinstance(ex.value, JrnlException)


@patch("builtins.open", new_callable=mock_open, read_data="template text")
def test_read_template_file_with_valid_file_returns_text(mock_file):
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
