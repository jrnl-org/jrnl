# Copyright (C) 2012-2021 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import ast
import os
from collections import defaultdict
from keyring import backend
from keyring import set_keyring
from keyring import errors
import re
import shutil
import tempfile
from unittest.mock import patch

from pytest_bdd import given
from pytest_bdd import then
from pytest_bdd import when
from pytest_bdd.parsers import parse
from pytest import fixture
import toml

from jrnl import __version__
from jrnl.cli import cli
from jrnl.config import load_config
from jrnl.os_compat import split_args


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
    """
    A keyring that cannot be retrieved.
    """

    priority = 2

    def set_password(self, servicename, username, password):
        raise errors.KeyringError

    def get_password(self, servicename, username):
        raise errors.KeyringError

    def delete_password(self, servicename, username):
        raise errors.KeyringError


# ----- UTILS ----- #
def failed_msg(msg, expected, actual):
    return f"{msg}\nExpected:\n{expected}\n---end---\nActual:\n{actual}\n---end---\n"


def read_value_from_string(string):
    if string[0] == "{":
        # Handle value being a dictionary
        return ast.literal_eval(string)

    # Takes strings like "bool:true" or "int:32" and coerces them into proper type
    t, value = string.split(":")
    value = {"bool": lambda v: v.lower() == "true", "int": int, "str": str}[t](value)
    return value


# ----- FIXTURES ----- #
@fixture
def cli_run():
    return {"status": 0, "stdout": None, "stderr": None}


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
def password():
    return ""


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
def keyring():
    set_keyring(NoKeyring())


@fixture
def keyring_type():
    return "default"


@fixture
def config_data(config_path):
    return load_config(config_path)


@fixture
def journal_name():
    return None


@fixture
def which_output_stream():
    return None


# ----- STEPS ----- #
@given("we have a keyring", target_fixture="keyring")
@given(parse("we have a {keyring_type} keyring"), target_fixture="keyring")
def we_have_type_of_keyring(keyring_type):
    if keyring_type == "failed":
        set_keyring(FailedKeyring())
    else:
        set_keyring(TestKeyring())


@given(parse('we use the config "{config_file}"'), target_fixture="config_path")
@given('we use the config "<config_file>"', target_fixture="config_path")
def we_use_the_config(config_file, temp_dir, working_dir):
    # Move into temp dir as cwd
    os.chdir(temp_dir.name)

    # Copy the config file over
    config_source = os.path.join(working_dir, "data", "configs", config_file)
    config_dest = os.path.join(temp_dir.name, config_file)
    shutil.copy2(config_source, config_dest)

    # @todo make this only copy some journals over
    # Copy all of the journals over
    journal_source = os.path.join(working_dir, "data", "journals")
    journal_dest = os.path.join(temp_dir.name, "features", "journals")
    shutil.copytree(journal_source, journal_dest)

    # @todo get rid of this by using default config values
    # merge in version number
    if config_file.endswith("yaml") and os.path.exists(config_dest):
        # Add jrnl version to file for 2.x journals
        with open(config_dest, "a") as cf:
            cf.write("version: {}".format(__version__))

    return config_dest


@given(parse('we use the password "{pw}" if prompted'), target_fixture="password")
def use_password_forever(pw):
    return pw


@when(parse('we run "jrnl {command}"'))
@when('we run "jrnl <command>"')
@when('we run "jrnl"')
@when(parse('we run "jrnl" and enter "{user_input}"'))
@when(parse('we run "jrnl {command}" and enter\n{user_input}'))
def we_run(command, config_path, user_input, cli_run, capsys, password, keyring):
    args = split_args(command)
    status = 0

    if user_input:
        user_input = user_input.splitlines()

    if password:
        password = password.splitlines()

    if not password and user_input:
        password = user_input

    # fmt: off
    # see: https://github.com/psf/black/issues/664
    with \
        patch("sys.argv", ['jrnl'] + args), \
        patch("sys.stdin.read", side_effect=user_input) as mock_stdin, \
        patch("builtins.input", side_effect=user_input) as mock_input, \
        patch("getpass.getpass", side_effect=password) as mock_getpass, \
        patch("jrnl.install.get_config_path", return_value=config_path), \
        patch("jrnl.config.get_config_path", return_value=config_path) \
    : # @TODO: single point of truth for get_config_path (move from all calls from install to config)
        try:
            cli(args)
        except StopIteration:
            # This happens when input is expected, but don't have any input left
            pass
        except SystemExit as e:
            status = e.code
    # fmt: on

    captured = capsys.readouterr()

    cli_run["status"] = status
    cli_run["stdout"] = captured.out
    cli_run["stderr"] = captured.err
    cli_run["mocks"] = {
        "stdin": mock_stdin,
        "input": mock_input,
        "getpass": mock_getpass,
    }


@then("we should get no error")
def should_get_no_error(cli_run):
    assert cli_run["status"] == 0, cli_run["status"]


@then(parse('the output should match "{regex}"'))
def output_should_match(regex, cli_run):
    out = cli_run["stdout"]
    matches = re.findall(regex, out)
    assert matches, f"\nRegex didn't match:\n{regex}\n{str(out)}\n{str(matches)}"


@then(parse("the output should contain\n{output}"))
@then(parse('the output should contain "{output}"'))
@then('the output should contain "<output>"')
@then(parse("the {which_output_stream} output should contain\n{output}"))
@then(parse('the {which_output_stream} output should contain "{output}"'))
def output_should_contain(output, which_output_stream, cli_run):
    assert output
    if which_output_stream is None:
        assert (output in cli_run["stdout"]) or (output in cli_run["stderr"])

    elif which_output_stream == "standard":
        assert output in cli_run["stdout"]

    elif which_output_stream == "error":
        assert output in cli_run["stderr"]

    else:
        assert output in cli_run[which_output_stream]


@then(parse("the output should not contain\n{output}"))
@then(parse('the output should not contain "{output}"'))
@then('the output should not contain "<output>"')
def output_should_not_contain(output, cli_run):
    assert output not in cli_run["stdout"]


@then(parse("the output should be\n{output}"))
@then(parse('the output should be "{output}"'))
@then('the output should be "<output>"')
def output_should_be(output, cli_run):
    actual_out = cli_run["stdout"].strip()
    output = output.strip()
    assert output and output == actual_out, failed_msg(
        "Output does not match.", output, actual_out
    )


@then('the output should contain the date "<date>"')
def output_should_contain_date(output, cli_run):
    assert output and output in cli_run["stdout"]


@then("the output should contain pyproject.toml version")
def output_should_contain_version(cli_run, toml_version):
    out = cli_run["stdout"]
    assert toml_version in out, toml_version


@then(parse('we should see the message "{text}"'))
def should_see_the_message(text, cli_run):
    out = cli_run["stderr"]
    assert text in out, [text, out]


@then(parse('the config should have "{key}" set to\n{str_value}'))
@then(parse('the config should have "{key}" set to "{str_value}"'))
@then(
    parse(
        'the config for journal "{journal_name}" should have "{key}" set to "{str_value}"'
    )
)
@then(parse('the config should {should_not} have "{key}" set'))
@then(parse('the config should {should_not} have "{key}" set'))
@then(
    parse(
        'the config for journal "{journal_name}" should {should_not} have "{key}" set'
    )
)
def config_var(config_data, key, str_value, journal_name, should_not):
    str_value = read_value_from_string(str_value) if len(str_value) else str_value

    configuration = config_data
    if journal_name:
        configuration = configuration["journals"][journal_name]

    # is the config a string?
    # @todo this should probably be a function
    if type(configuration) is str:
        configuration = {"journal": configuration}

    if should_not:
        assert key not in configuration
    else:
        assert key in configuration
        assert configuration[key] == str_value


@then("we should be prompted for a password")
def password_was_called(cli_run):
    assert cli_run["mocks"]["getpass"].called


@then("we should not be prompted for a password")
def password_was_not_called(cli_run):
    assert not cli_run["mocks"]["getpass"].called
