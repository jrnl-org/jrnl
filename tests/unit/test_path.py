# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import random
import string
from os import getenv
from unittest.mock import patch

import pytest

from jrnl.path import absolute_path
from jrnl.path import expand_path
from jrnl.path import home_dir


@pytest.fixture
def home_dir_str(monkeypatch):
    username = "username"
    monkeypatch.setenv("USERPROFILE", username)  # for windows
    monkeypatch.setenv("HOME", username)  # for *nix
    return username


@pytest.fixture
def random_test_var(monkeypatch):
    name = f"JRNL_TEST_{''.join(random.sample(string.ascii_uppercase, 10))}"
    val = "".join(random.sample(string.ascii_lowercase, 25))
    monkeypatch.setenv(name, val)
    return (name, val)


def test_home_dir(home_dir_str):
    assert home_dir() == home_dir_str


@pytest.mark.on_posix
@pytest.mark.parametrize(
    "path",
    ["~"],
)
def test_expand_path_actually_expands_mac_linux(path):
    # makes sure that path isn't being returns as-is
    assert expand_path(path) != path


@pytest.mark.on_win
@pytest.mark.parametrize(
    "path",
    ["~", "%USERPROFILE%"],
)
def test_expand_path_actually_expands_windows(path):
    # makes sure that path isn't being returns as-is
    assert expand_path(path) != path


@pytest.mark.on_posix
@pytest.mark.parametrize(
    "paths",
    [
        ["~", "HOME"],
    ],
)
def test_expand_path_expands_into_correct_value_mac_linux(paths):
    input_path, expected_path = paths[0], paths[1]
    assert expand_path(input_path) == getenv(expected_path)


@pytest.mark.on_win
@pytest.mark.parametrize(
    "paths",
    [
        ["~", "USERPROFILE"],
        ["%USERPROFILE%", "USERPROFILE"],
    ],
)
def test_expand_path_expands_into_correct_value_windows(paths):
    input_path, expected_path = paths[0], paths[1]
    assert expand_path(input_path) == getenv(expected_path)


@pytest.mark.on_posix
@pytest.mark.parametrize("_", range(25))
def test_expand_path_expands_into_random_env_value_mac_linux(_, random_test_var):
    var_name, var_value = random_test_var[0], random_test_var[1]
    assert expand_path(var_name) == var_name
    assert expand_path(f"${var_name}") == var_value  # mac & linux
    assert expand_path(f"${var_name}") == getenv(var_name)


@pytest.mark.on_win
@pytest.mark.parametrize("_", range(25))
def test_expand_path_expands_into_random_env_value_windows(_, random_test_var):
    var_name, var_value = random_test_var[0], random_test_var[1]
    assert expand_path(var_name) == var_name
    assert expand_path(f"%{var_name}%") == var_value  # windows
    assert expand_path(f"%{var_name}%") == getenv(var_name)


@patch("jrnl.path.expand_path")
@patch("os.path.abspath")
def test_absolute_path(mock_abspath, mock_expand_path):
    test_val = "test_value"

    assert absolute_path(test_val) == mock_abspath.return_value
    mock_expand_path.assert_called_with(test_val)
    mock_abspath.assert_called_with(mock_expand_path.return_value)