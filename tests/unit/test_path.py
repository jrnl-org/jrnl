import pytest
from os import path

from jrnl.path import home_dir
from jrnl.path import expand_path
from jrnl.path import absolute_path


@pytest.fixture
def home_dir_str(monkeypatch):
    username = "username"
    monkeypatch.setenv("USERPROFILE", username)  # for windows
    monkeypatch.setenv("HOME", username)  # for *nix
    return username


@pytest.fixture
def expand_path_test_data(monkeypatch, home_dir_str):
    monkeypatch.setenv("VAR", "var")
    return [
        ["~", home_dir_str],
        [path.join("~", "${VAR}", "$VAR"), path.join(home_dir_str, "var", "var")],
    ]


@pytest.fixture
def absolute_path_test_data(monkeypatch, expand_path_test_data):
    cwd = "currentdir"
    monkeypatch.setattr("jrnl.path.os.getcwd", lambda: cwd)
    test_data = [
        [".", cwd],
        [path.join(".", "dir"), path.join(cwd, "dir")],
        [".dot_file", path.join(cwd, ".dot_file")],
    ]
    for inpath, outpath in expand_path_test_data:
        test_data.append([inpath, path.join(cwd, outpath)])
    return test_data


def test_home_dir(home_dir_str):
    assert home_dir() == home_dir_str


def test_expand_path(expand_path_test_data):
    for inpath, outpath in expand_path_test_data:
        assert expand_path(inpath) == outpath


def test_absolute_path(absolute_path_test_data):
    for inpath, outpath in absolute_path_test_data:
        assert absolute_path(inpath) == outpath
