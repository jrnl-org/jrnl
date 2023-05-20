# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import os
import tempfile
from collections import defaultdict
from collections.abc import Iterable
from pathlib import Path
from unittest.mock import Mock
from unittest.mock import patch

import toml
from keyring import backend
from keyring import errors
from pytest import fixture
from rich.console import Console

from jrnl.config import load_config
from jrnl.os_compat import split_args
from tests.lib.helpers import get_fixture


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
    mock_default_journal_path,
    mock_default_templates_path,
):
    # Check if we need more mocks
    mock_factories.update(mock_args)
    mock_factories.update(mock_is_tty)
    mock_factories.update(mock_overrides)
    mock_factories.update(mock_editor)
    mock_factories.update(mock_config_path)
    mock_factories.update(mock_user_input)
    mock_factories.update(mock_default_journal_path)
    mock_factories.update(mock_default_templates_path)

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
            "jrnl.controller.apply_overrides", side_effect=my_overrides
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
def mock_default_journal_path(temp_dir):
    journal_path = os.path.join(temp_dir.name, "journal.txt")
    return {
        "default_journal_path_install": lambda: patch(
            "jrnl.install.get_default_journal_path", return_value=journal_path
        ),
        "default_journal_path_config": lambda: patch(
            "jrnl.config.get_default_journal_path", return_value=journal_path
        ),
    }


@fixture
def mock_default_templates_path(temp_dir):
    templates_path = os.path.join(temp_dir.name, "templates")
    return {
        "get_templates_path": lambda: patch(
            "jrnl.editor.get_templates_path", return_value=templates_path
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
def input_method():
    return ""


@fixture
def all_input():
    return ""


@fixture
def command():
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
def mock_user_input(request, password_input, stdin_input):
    def _mock_user_input():
        # user_input needs to be here because we don't know it until cli_run starts
        user_input = get_fixture(request, "all_input", None)

        if user_input is None:
            user_input = Exception("Unexpected call for user input")
        else:
            user_input = iter(user_input.splitlines())

        def mock_console_input(**kwargs):
            pw = kwargs.get("password", False)
            if pw and not isinstance(password_input, Exception):
                return password_input

            if isinstance(user_input, Iterable):
                input_line = next(user_input)
                # A raw newline is used to indicate deliberate empty input
                return "" if input_line == r"\n" else input_line

            # exceptions
            return user_input if not pw else password_input

        mock_console = Mock(wraps=Console(stderr=True))
        mock_console.input = Mock(side_effect=mock_console_input)

        return patch("jrnl.output._get_console", return_value=mock_console)

    return {
        "user_input": _mock_user_input,
        "stdin_input": lambda: patch("sys.stdin.read", side_effect=stdin_input),
    }


@fixture
def password_input(request):
    password_input = get_fixture(request, "password", None)
    if password_input is None:
        password_input = Exception("Unexpected call for password input")
    return password_input


@fixture
def stdin_input(request, is_tty):
    stdin_input = get_fixture(request, "all_input", None)
    if stdin_input is None or is_tty:
        stdin_input = Exception("Unexpected call for stdin input")
    else:
        stdin_input = [stdin_input]
    return stdin_input


@fixture
def is_tty(input_method):
    assert input_method in ["", "enter", "pipe", "type"]
    return input_method not in ["pipe", "type"]


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
