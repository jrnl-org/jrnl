# Copyright (C) 2012-2021 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from collections import defaultdict
import os
from pathlib import Path
import tempfile

from keyring import backend
from keyring import errors
from pytest import fixture
from unittest.mock import patch
from .helpers import get_fixture
import toml

from jrnl.config import load_config
from jrnl.os_compat import split_args


# --- Keyring --- #
@fixture
def keyring():
    return NoKeyring()


@fixture
def keyring_type():
    return "default"


class TestKeyring(backend.KeyringBackend):
    """A test keyring that just stores its values in a hash"""

    priority = 1
    keys = defaultdict(dict)

    def set_password(self, servicename, username, password):
        self.keys[servicename][username] = password

    def get_password(self, servicename, username):
        return self.keys[servicename].get(username)

    def delete_password(self, servicename, username):
        self.keys[servicename][username] = None


class NoKeyring(backend.KeyringBackend):
    """A keyring that simulated an environment with no keyring backend."""

    priority = 2
    keys = defaultdict(dict)

    def set_password(self, servicename, username, password):
        raise errors.NoKeyringError

    def get_password(self, servicename, username):
        raise errors.NoKeyringError

    def delete_password(self, servicename, username):
        raise errors.NoKeyringError


class FailedKeyring(backend.KeyringBackend):
    """A keyring that cannot be retrieved."""

    priority = 2

    def set_password(self, servicename, username, password):
        raise errors.KeyringError

    def get_password(self, servicename, username):
        raise errors.KeyringError

    def delete_password(self, servicename, username):
        raise errors.KeyringError


# ----- Misc ----- #
@fixture
def cli_run(
    mock_factories,
    mock_args,
    mock_is_tty,
    mock_config_path,
    mock_editor,
    mock_user_input,
    mock_overrides,
    mock_password,
):
    # Check if we need more mocks
    mock_factories.update(mock_args)
    mock_factories.update(mock_is_tty)
    mock_factories.update(mock_overrides)
    mock_factories.update(mock_editor)
    mock_factories.update(mock_config_path)
    mock_factories.update(mock_user_input)
    mock_factories.update(mock_password)

    return {
        "status": 0,
        "stdout": None,
        "stderr": None,
        "mocks": {},
        "mock_factories": mock_factories,
    }


@fixture
def mock_factories():
    return {}


@fixture
def mock_args(cache_dir, request):
    def _mock_args():
        command = get_fixture(request, "command", "")

        if cache_dir["exists"]:
            command = command.format(cache_dir=cache_dir["path"])

        args = split_args(command)

        return patch("sys.argv", ["jrnl"] + args)

    return {"args": _mock_args}


@fixture
def mock_is_tty(is_tty):
    return {"is_tty": lambda: patch("sys.stdin.isatty", return_value=is_tty)}


@fixture
def mock_overrides(config_in_memory):
    from jrnl.override import apply_overrides

    def my_overrides(*args, **kwargs):
        result = apply_overrides(*args, **kwargs)
        config_in_memory["overrides"] = result
        return result

    return {
        "overrides": lambda: patch(
            "jrnl.jrnl.apply_overrides", side_effect=my_overrides
        )
    }


@fixture
def mock_config_path(request):
    config_path = get_fixture(request, "config_path")

    if not config_path:
        return {}

    return {
        "config_path_install": lambda: patch(
            "jrnl.install.get_config_path", return_value=config_path
        ),
        "config_path_config": lambda: patch(
            "jrnl.config.get_config_path", return_value=config_path
        ),
    }


@fixture
def temp_dir():
    return tempfile.TemporaryDirectory()


@fixture
def working_dir(request):
    return os.path.join(request.config.rootpath, "tests")


@fixture
def toml_version(working_dir):
    pyproject = os.path.join(working_dir, "..", "pyproject.toml")
    pyproject_contents = toml.load(pyproject)
    return pyproject_contents["tool"]["poetry"]["version"]


@fixture
def mock_password(request):
    def _mock_password():
        password = get_fixture(request, "password")
        user_input = get_fixture(request, "user_input")

        if password:
            password = password.splitlines()

        elif user_input:
            password = user_input.splitlines()

        if not password:
            password = Exception("Unexpected call for password")

        return patch("getpass.getpass", side_effect=password)

    return {"getpass": _mock_password}


@fixture
def input_method():
    return ""


@fixture
def cache_dir():
    return {"exists": False, "path": ""}


@fixture
def str_value():
    return ""


@fixture
def should_not():
    return False


@fixture
def mock_user_input(request, is_tty):
    def _generator(target):
        def _mock_user_input():
            user_input = get_fixture(request, "user_input", "")
            user_input = user_input.splitlines() if is_tty else [user_input]

            if not user_input:
                user_input = Exception("Unexpected call for user input")

            return patch(target, side_effect=user_input)

        return _mock_user_input

    return {
        "stdin": _generator("sys.stdin.read"),
        "input": _generator("builtins.input"),
    }


@fixture
def is_tty(input_method):
    assert input_method in ["", "enter", "pipe"]
    return input_method != "pipe"


@fixture
def config_on_disk(config_path):
    return load_config(config_path)


@fixture
def config_in_memory():
    return dict()


@fixture
def journal_name():
    return None


@fixture
def which_output_stream():
    return None


@fixture
def editor_input():
    return None


@fixture
def num_args():
    return None


@fixture
def parsed_output():
    return {"lang": None, "obj": None}


@fixture
def editor_state():
    return {
        "command": "",
        "intent": {"method": "r", "input": None},
        "tmpfile": {"name": None, "content": None},
    }


@fixture
def mock_editor(editor_state):
    def _mock_editor(editor_command):
        tmpfile = editor_command[-1]

        editor_state["command"] = editor_command
        editor_state["tmpfile"]["name"] = tmpfile

        Path(tmpfile).touch()
        with open(tmpfile, editor_state["intent"]["method"]) as f:
            # Touch the file so jrnl knows it was edited
            if editor_state["intent"]["input"] is not None:
                f.write(editor_state["intent"]["input"])

            file_content = f.read()
            editor_state["tmpfile"]["content"] = file_content

    return {"editor": lambda: patch("subprocess.call", side_effect=_mock_editor)}
