import ast
from collections import defaultdict
import os
from pathlib import Path
import re
import shlex
import time
from unittest.mock import patch

from behave import given
from behave import then
from behave import when
import keyring
import toml
import yaml

from jrnl import Journal
from jrnl import __version__
from jrnl import install
from jrnl import plugins
from jrnl.cli import cli
from jrnl.config import load_config
from jrnl.os_compat import on_windows

try:
    import parsedatetime.parsedatetime_consts as pdt
except ImportError:
    import parsedatetime as pdt

consts = pdt.Constants(usePyICU=False)
consts.DOWParseStyle = -1  # Prefers past weekdays
CALENDAR = pdt.Calendar(consts)


class TestKeyring(keyring.backend.KeyringBackend):
    """A test keyring that just stores its values in a hash"""

    priority = 1
    keys = defaultdict(dict)

    def set_password(self, servicename, username, password):
        self.keys[servicename][username] = password

    def get_password(self, servicename, username):
        return self.keys[servicename].get(username)

    def delete_password(self, servicename, username):
        self.keys[servicename][username] = None


class NoKeyring(keyring.backend.KeyringBackend):
    """A keyring that simulated an environment with no keyring backend."""

    priority = 2
    keys = defaultdict(dict)

    def set_password(self, servicename, username, password):
        raise keyring.errors.NoKeyringError

    def get_password(self, servicename, username):
        raise keyring.errors.NoKeyringError

    def delete_password(self, servicename, username):
        raise keyring.errors.NoKeyringError


class FailedKeyring(keyring.backend.KeyringBackend):
    """
    A keyring that simulates an environment with a keyring that has passwords, but fails
    to return them.
    """

    priority = 2
    keys = defaultdict(dict)


    def set_password(self, servicename, username, password):
        self.keys[servicename][username] = password

    def get_password(self, servicename, username):
        raise keyring.errors.NoKeyringError

    def delete_password(self, servicename, username):
        self.keys[servicename][username] = None


def ushlex(command):
    return shlex.split(command, posix=not on_windows)


def read_journal(journal_name="default"):
    config = load_config(install.CONFIG_FILE_PATH)
    with open(config["journals"][journal_name]) as journal_file:
        journal = journal_file.read()
    return journal


def open_journal(journal_name="default"):
    config = load_config(install.CONFIG_FILE_PATH)
    journal_conf = config["journals"][journal_name]

    # We can override the default config on a by-journal basis
    if type(journal_conf) is dict:
        config.update(journal_conf)
    # But also just give them a string to point to the journal file
    else:
        config["journal"] = journal_conf

    return Journal.open_journal(journal_name, config)


def read_value_from_string(string):
    if string[0] == "{":
        # Handle value being a dictionary
        return ast.literal_eval(string)

    # Takes strings like "bool:true" or "int:32" and coerces them into proper type
    t, value = string.split(":")
    value = {"bool": lambda v: v.lower() == "true", "int": int, "str": str}[t](
        value
    )
    return value

@given('we use the config "{config_file}"')
def set_config(context, config_file):
    full_path = os.path.join("features/configs", config_file)
    install.CONFIG_FILE_PATH = os.path.abspath(full_path)
    if config_file.endswith("yaml"):
        # Add jrnl version to file for 2.x journals
        with open(install.CONFIG_FILE_PATH, "a") as cf:
            cf.write("version: {}".format(__version__))


@given('we have a keyring')
def set_keyring(context):
    keyring.set_keyring(TestKeyring())


@given('we do not have a keyring')
def disable_keyring(context):
    keyring.core.set_keyring(NoKeyring())


@when('we change directory to "{path}"')
def move_up_dir(context, path):
    os.chdir(path)


@when("we open the editor and {method}")
@when('we open the editor and {method} "{text}"')
@when("we open the editor and {method} nothing")
@when("we open the editor and {method} nothing")
def open_editor_and_enter(context, method, text=""):
    text = text or context.text or ""

    if method == "enter":
        file_method = "w+"
    elif method == "append":
        file_method = "a"
    else:
        file_method = "r+"

    def _mock_editor(command):
        context.editor_command = command
        tmpfile = command[-1]
        with open(tmpfile, file_method) as f:
            f.write(text)

        return tmpfile

    # fmt: off
    # see: https://github.com/psf/black/issues/664
    with \
        patch("subprocess.call", side_effect=_mock_editor) as mock_editor, \
        patch("sys.stdin.isatty", return_value=True) \
    :
        context.editor = mock_editor
        cli(["--edit"])
    # fmt: on


@then("the editor should have been called")
@then("the editor should have been called with {num} arguments")
def count_editor_args(context, num=None):
    assert context.editor.called

    if isinstance(num, int):
        assert len(context.editor_command) == int(num)


@then("the editor should not have been called")
def no_editor_called(context, num=None):
    assert "editor" not in context or not context.editor.called


@then('one editor argument should be "{arg}"')
def contains_editor_arg(context, arg):
    args = context.editor_command
    assert (
        arg in args and args.count(arg) == 1
    ), f"\narg not in args exactly 1 time:\n{arg}\n{str(args)}"


@then('one editor argument should match "{regex}"')
def matches_editor_arg(context, regex):
    args = context.editor_command
    matches = list(filter(lambda x: re.match(regex, x), args))
    assert (
        len(matches) == 1
    ), f"\nRegex didn't match exactly 1 time:\n{regex}\n{str(args)}"


def _mock_getpass(inputs):
    def prompt_return(prompt="Password: "):
        print(prompt)
        try:
            return next(inputs)
        except StopIteration:
            raise KeyboardInterrupt

    return prompt_return


def _mock_input(inputs):
    def prompt_return(prompt=""):
        try:
            val = next(inputs)
            print(prompt, val)
            return val
        except StopIteration:
            raise KeyboardInterrupt

    return prompt_return


@when('we run "{command}" and enter')
@when('we run "{command}" and enter nothing')
@when('we run "{command}" and enter "{inputs}"')
def run_with_input(context, command, inputs=""):
    # create an iterator through all inputs. These inputs will be fed one by one
    # to the mocked calls for 'input()', 'util.getpass()' and 'sys.stdin.read()'
    if context.text:
        text = iter(context.text.split("\n"))
    else:
        text = iter([inputs])

    args = ushlex(command)[1:]

    def _mock_editor(command):
        context.editor_command = command
        tmpfile = command[-1]
        context.editor_file = tmpfile
        Path(tmpfile).touch()

    # fmt: off
    # see: https://github.com/psf/black/issues/664
    with \
        patch("builtins.input", side_effect=_mock_input(text)) as mock_input, \
        patch("getpass.getpass", side_effect=_mock_getpass(text)) as mock_getpass, \
        patch("sys.stdin.read", side_effect=text) as mock_read, \
        patch("subprocess.call", side_effect=_mock_editor) as mock_editor \
    :
        try:
            cli(args or [])
            context.exit_status = 0
        except SystemExit as e:
            context.exit_status = e.code

        # put mocks into context so they can be checked later in "then" statements
        context.editor = mock_editor
        context.input = mock_input
        context.getpass = mock_getpass
        context.read = mock_read
        context.iter_text = text

        context.execute_steps('''
            Then all input was used
            And at least one input method was called
        ''')

    # fmt: on


@then("at least one input method was called")
def inputs_were_called(context):
    assert (
        context.input.called
        or context.getpass.called
        or context.read.called
        or context.editor.called
    )


@then("we should be prompted for a password")
def password_was_called(context):
    assert context.getpass.called


@then("we should not be prompted for a password")
def password_was_not_called(context):
    assert not context.getpass.called


@then("all input was used")
def all_input_was_used(context):
    # all inputs were used (ignore if empty string)
    for temp in context.iter_text:
        assert "" == temp, "Not all inputs were consumed"


@when('we run "{command}"')
@when('we run "{command}" and pipe')
@when('we run "{command}" and pipe "{text}"')
@when('we run "{command}" with cache directory "{cache_dir}"')
def run(context, command, text="", cache_dir=None):
    text = text or context.text or ""

    if cache_dir is not None:
        cache_dir = os.path.join("features", "cache", cache_dir)
        command = command.format(cache_dir=cache_dir)

    args = ushlex(command)

    def _mock_editor(command):
        context.editor_command = command

    try:
        with patch("sys.argv", args), patch(
            "subprocess.call", side_effect=_mock_editor
        ), patch("sys.stdin.read", side_effect=lambda: text):
            cli(args[1:])
            context.exit_status = 0
    except SystemExit as e:
        context.exit_status = e.code


@given('we load template "{filename}"')
def load_template(context, filename):
    full_path = os.path.join("features/data/templates", filename)
    exporter = plugins.template_exporter.__exporter_from_file(full_path)
    plugins.__exporter_types[exporter.names[0]] = exporter


@when('we set the keyring password of "{journal}" to "{password}"')
def set_keyring(context, journal, password):
    keyring.set_password("jrnl", journal, password)


@then("we should get an error")
def has_error(context):
    assert context.exit_status != 0, context.exit_status


@then("we should get no error")
def no_error(context):
    assert context.exit_status == 0, context.exit_status


@then("the output should be")
@then("the output should be empty")
@then('the output should be "{text}"')
def check_output(context, text=None):
    text = (text or context.text or "").strip().splitlines()
    out = context.stdout_capture.getvalue().strip().splitlines()
    assert len(text) == len(out), "Output has {} lines (expected: {})".format(
        len(out), len(text)
    )
    for line_text, line_out in zip(text, out):
        assert line_text.strip() == line_out.strip(), [
            line_text.strip(),
            line_out.strip(),
        ]


@then('the output should contain "{text}" in the local time')
def check_output_time_inline(context, text):
    out = context.stdout_capture.getvalue()
    date, flag = CALENDAR.parse(text)
    output_date = time.strftime("%Y-%m-%d %H:%M", date)
    assert output_date in out, output_date


@then("the output should contain pyproject.toml version")
def check_output_version_inline(context):
    out = context.stdout_capture.getvalue()
    pyproject = (Path(__file__) / ".." / ".." / ".." / "pyproject.toml").resolve()
    pyproject_contents = toml.load(pyproject)
    pyproject_version = pyproject_contents["tool"]["poetry"]["version"]
    assert pyproject_version in out, pyproject_version


@then("the output should contain")
@then('the output should contain "{text}"')
@then('the output should contain "{text}" or "{text2}"')
def check_output_inline(context, text=None, text2=None):
    text = text or context.text
    out = context.stdout_capture.getvalue()
    assert (text and text in out) or (text2 and text2 in out)


@then("the error output should contain")
@then('the error output should contain "{text}"')
@then('the error output should contain "{text}" or "{text2}"')
def check_error_output_inline(context, text=None, text2=None):
    text = text or context.text
    out = context.stderr_capture.getvalue()
    assert text in out or text2 in out, text or text2


@then('the output should not contain "{text}"')
def check_output_not_inline(context, text):
    out = context.stdout_capture.getvalue()
    assert text not in out


@then('we should see the message "{text}"')
def check_message(context, text):
    out = context.stderr_capture.getvalue()
    assert text in out, [text, out]


@then('we should not see the message "{text}"')
def check_not_message(context, text):
    out = context.stderr_capture.getvalue()
    assert text not in out, [text, out]


@then('the journal should contain "{text}"')
@then('journal "{journal_name}" should contain "{text}"')
def check_journal_content(context, text, journal_name="default"):
    journal = read_journal(journal_name)
    assert text in journal, journal


@then('the journal should not contain "{text}"')
@then('journal "{journal_name}" should not contain "{text}"')
def check_not_journal_content(context, text, journal_name="default"):
    journal = read_journal(journal_name)
    assert text not in journal, journal


@then('journal "{journal_name}" should not exist')
def journal_doesnt_exist(context, journal_name="default"):
    config = load_config(install.CONFIG_FILE_PATH)

    journal_path = config["journals"][journal_name]
    assert not os.path.exists(journal_path)


@then('the config should have "{key}" set to')
@then('the config should have "{key}" set to "{value}"')
@then('the config for journal "{journal}" should have "{key}" set to "{value}"')
def config_var(context, key, value="", journal=None):
    value = read_value_from_string(value or context.text or "")
    config = load_config(install.CONFIG_FILE_PATH)

    if journal:
        config = config["journals"][journal]

    assert key in config
    assert config[key] == value


@then('the config for journal "{journal}" should not have "{key}" set')
def config_var(context, key, value="", journal=None):
    config = load_config(install.CONFIG_FILE_PATH)

    if journal:
        config = config["journals"][journal]

    assert key not in config


@then("the journal should have {number:d} entries")
@then("the journal should have {number:d} entry")
@then('journal "{journal_name}" should have {number:d} entries')
@then('journal "{journal_name}" should have {number:d} entry')
def check_journal_entries(context, number, journal_name="default"):
    journal = open_journal(journal_name)
    assert len(journal.entries) == number


@when("the journal directory is listed")
def list_journal_directory(context, journal="default"):
    with open(install.CONFIG_FILE_PATH) as config_file:
        config = yaml.load(config_file, Loader=yaml.FullLoader)
    journal_path = config["journals"][journal]
    for root, dirnames, f in os.walk(journal_path):
        for file in f:
            print(os.path.join(root, file))


@then("the Python version warning should appear if our version is below {version}")
def check_python_warning_if_version_low_enough(context, version):
    import platform

    import packaging.version

    if packaging.version.parse(platform.python_version()) < packaging.version.parse(
        version
    ):
        out = context.stderr_capture.getvalue()
        assert "WARNING: Python versions" in out
    else:
        assert True


@then("fail")
def debug_fail(context):
    assert False
