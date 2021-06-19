# Copyright (C) 2012-2021 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import os
from collections import defaultdict
from keyring import backend
from keyring import set_keyring
from keyring import errors
from pathlib import Path
import tempfile

from pytest import fixture
import toml

from jrnl.config import load_config


# --- Keyring --- #
@fixture
def keyring():
    set_keyring(NoKeyring())


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
    """ A keyring that cannot be retrieved.  """

    priority = 2

    def set_password(self, servicename, username, password):
        raise errors.KeyringError

    def get_password(self, servicename, username):
        raise errors.KeyringError

    def delete_password(self, servicename, username):
        raise errors.KeyringError


# ----- Misc ----- #
@fixture
def cli_run():
    return {"status": 0, "stdout": None, "stderr": None}


@fixture
def mocks():
    return dict()


@fixture
def temp_dir():
    return tempfile.TemporaryDirectory()


@fixture
def working_dir(request):
    return os.path.join(request.config.rootpath, "tests")


@fixture
def config_path(temp_dir):
    os.chdir(temp_dir.name)
    return temp_dir.name + "/jrnl.yaml"


@fixture
def toml_version(working_dir):
    pyproject = os.path.join(working_dir, "..", "pyproject.toml")
    pyproject_contents = toml.load(pyproject)
    return pyproject_contents["tool"]["poetry"]["version"]


@fixture
def password():
    return ""


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
def command():
    return ""


@fixture
def should_not():
    return False


@fixture
def user_input():
    return ""


@fixture
def config_data(config_path):
    return load_config(config_path)


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
def editor(editor_state):
    def _mock_editor(editor_command):
        tmpfile = editor_command[-1]

        editor_state["command"] = editor_command
        editor_state["tmpfile"]["name"] = tmpfile

        Path(tmpfile).touch()
        with open(tmpfile, editor_state["intent"]["method"]) as f:
            # Touch the file so jrnl knows it was edited
            if editor_state["intent"]["input"] != None:
                f.write(editor_state["intent"]["input"])

            file_content = f.read()
            editor_state["tmpfile"]["content"] = file_content

    return _mock_editor

