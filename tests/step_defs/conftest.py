# Copyright (C) 2012-2021 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import ast
import json
import os
from datetime import datetime
from collections import defaultdict
from keyring import backend
from keyring import set_keyring
from keyring import errors
from pathlib import Path
import random
import string
import re
import shutil
import tempfile
from unittest.mock import patch
from unittest.mock import MagicMock
from xml.etree import ElementTree

from pytest_bdd import given
from pytest_bdd import then
from pytest_bdd import when
from pytest_bdd.parsers import parse
from pytest_bdd import parsers
from pytest import fixture
from pytest import mark
import toml

from jrnl import __version__
from jrnl.cli import cli
from jrnl.config import load_config
from jrnl.config import scope_config
from jrnl.os_compat import split_args
from jrnl.os_compat import on_windows
from jrnl.time import __get_pdt_calendar


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


# ----- MARKERS ----- #
def pytest_bdd_apply_tag(tag, function):
    if tag == "skip_win":
        marker = mark.skipif(on_windows, reason="Skip test on Windows")
    elif tag == "skip_editor":
        marker = mark.skip(
            reason="Skipping editor-related test. We should come back to this!"
        )
    else:
        # Fall back to pytest-bdd's default behavior
        return None

    marker(function)
    return True


# ----- UTILS ----- #
def read_value_from_string(string):
    if string[0] == "{":
        # Handle value being a dictionary
        return ast.literal_eval(string)

    # Takes strings like "bool:true" or "int:32" and coerces them into proper type
    t, value = string.split(":")
    value = {"bool": lambda v: v.lower() == "true", "int": int, "str": str}[t](value)
    return value

def assert_directory_contains_files(file_list, directory_path):
    assert os.path.isdir(directory_path), "Directory path is not a directory"

    for file in file_list.split("\n"):
        fullpath = directory_path + '/' + file
        assert os.path.isfile(fullpath)


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
def now_date():
    return {"datetime": datetime, "calendar_parse": __get_pdt_calendar()}


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


# ----- STEPS ----- #
@given(parse("we {editor_method} to the editor if opened\n{editor_input}"))
@given(parse("we {editor_method} nothing to the editor if opened"))
def we_enter_editor(editor_method, editor_input, editor_state):
    file_method = editor_state["intent"]["method"]
    if editor_method == "write":
        file_method = "w+"
    elif editor_method == "append":
        file_method = "a+"
    else:
        assert False, f"Method '{editor_method}' not supported"

    editor_state["intent"] = {"method": file_method, "input": editor_input}


@given(parse('now is "<date_str>"'), target_fixture="now_date")
@given(parse('now is "{date_str}"'), target_fixture="now_date")
def now_is_str(date_str):
    class DatetimeMagicMock(MagicMock):
        # needed because jrnl does some reflection on datetime
        def __instancecheck__(self, subclass):
            return isinstance(subclass, datetime)

    my_date = datetime.strptime(date_str, "%Y-%m-%d %I:%M:%S %p")

    # jrnl uses two different classes to parse dates, so both must be mocked
    datetime_mock = DatetimeMagicMock(wraps=datetime)
    datetime_mock.now.return_value = my_date

    pdt = __get_pdt_calendar()
    calendar_mock = MagicMock(wraps=pdt)
    calendar_mock.parse.side_effect = lambda date_str_input: pdt.parse(
        date_str_input, my_date
    )

    return {"datetime": datetime_mock, "calendar_parse": calendar_mock}


@then(parse("the editor should have been called"))
@then(parse("the editor should have been called with {num_args} arguments"))
def count_editor_args(num_args, cli_run, editor_state):
    assert cli_run["mocks"]["editor"].called

    if isinstance(num_args, int):
        assert len(editor_state["command"]) == int(num_args)


@then(parse('the editor file content should {comparison} "{str_value}"'))
@then(parse("the editor file content should {comparison} empty"))
@then(parse("the editor file content should {comparison}\n{str_value}"))
def contains_editor_file(comparison, str_value, editor_state):
    content = editor_state["tmpfile"]["content"]
    # content = f'\n"""\n{content}\n"""\n'
    if comparison == "be":
        assert content == str_value
    elif comparison == "contain":
        assert str_value in content
    else:
        assert False, f"Comparison '{comparison}' not supported"


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


@when(parse('we run "jrnl {command}" and enter\n{user_input}'))
@when(parsers.re('we run "jrnl (?P<command>[^"]+)" and enter "(?P<user_input>[^"]+)"'))
@when(parse('we run "jrnl {command}"'))
@when(parse('we run "jrnl" and enter "{user_input}"'))
@when('we run "jrnl <command>"')
@when('we run "jrnl"')
def we_run(
    command,
    config_path,
    user_input,
    cli_run,
    capsys,
    password,
    cache_dir,
    editor,
    now_date,
    keyring
):
    if cache_dir["exists"]:
        command = command.format(cache_dir=cache_dir["path"])

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
        patch("datetime.datetime", new=now_date["datetime"]), \
        patch("jrnl.time.__get_pdt_calendar", return_value=now_date["calendar_parse"]), \
        patch("jrnl.install.get_config_path", return_value=config_path), \
        patch("jrnl.config.get_config_path", return_value=config_path), \
        patch("subprocess.call", side_effect=editor) as mock_editor \
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
        "editor": mock_editor,
    }


@then("we should get no error")
def should_get_no_error(cli_run):
    assert cli_run["status"] == 0, cli_run["status"]


@then(parse('the output should match "{regex}"'))
def output_should_match(regex, cli_run):
    out = cli_run["stdout"]
    matches = re.findall(regex, out)
    assert matches, f"\nRegex didn't match:\n{regex}\n{str(out)}\n{str(matches)}"


@then(parse("the output should contain\n{expected_output}"))
@then(parse('the output should contain "{expected_output}"'))
@then('the output should contain "<expected_output>"')
@then(parse("the {which_output_stream} output should contain\n{expected_output}"))
@then(parse('the {which_output_stream} output should contain "{expected_output}"'))
def output_should_contain(expected_output, which_output_stream, cli_run):
    assert expected_output
    if which_output_stream is None:
        assert (expected_output in cli_run["stdout"]) or (
            expected_output in cli_run["stderr"]
        )

    elif which_output_stream == "standard":
        assert expected_output in cli_run["stdout"]

    elif which_output_stream == "error":
        assert expected_output in cli_run["stderr"]

    else:
        assert expected_output in cli_run[which_output_stream]


@then(parse("the output should not contain\n{expected_output}"))
@then(parse('the output should not contain "{expected_output}"'))
@then('the output should not contain "<expected_output>"')
def output_should_not_contain(expected_output, cli_run):
    assert expected_output not in cli_run["stdout"]


@then(parse("the output should be\n{expected_output}"))
@then(parse('the output should be "{expected_output}"'))
@then('the output should be "<expected_output>"')
def output_should_be(expected_output, cli_run):
    actual = cli_run["stdout"].strip()
    expected = expected_output.strip()
    assert expected == actual


@then("the output should be empty")
def output_should_be_empty(cli_run):
    actual = cli_run["stdout"].strip()
    assert actual == ""


@then('the output should contain the date "<date>"')
def output_should_contain_date(date, cli_run):
    assert date and date in cli_run["stdout"]


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


@then(parse("the cache directory should contain the files\n{file_list}"))
def assert_dir_contains_files(file_list, cache_dir):
    assert_directory_contains_files(file_list, cache_dir["path"])

@then(parse("the journal directory should contain\n{file_list}"))
def journal_directory_should_contain(config_data, file_list, journal_name):
    if not journal_name:
        journal_name = "default"

    scoped_config = scope_config(config_data, journal_name)
    journal_path = scoped_config["journal"]

    assert_directory_contains_files(file_list, journal_path)

@given("we create a cache directory", target_fixture="cache_dir")
def create_cache_dir(temp_dir):
    random_str = "".join(random.choices(string.ascii_uppercase + string.digits, k=20))

    dir_path = os.path.join(temp_dir.name, "cache_" + random_str)
    os.mkdir(dir_path)
    return {"exists": True, "path": dir_path}


@then(parse('the content of file "{file_path}" in the cache should be\n{file_content}'))
def content_of_file_should_be(file_path, file_content, cache_dir):
    assert cache_dir["exists"]
    expected_content = file_content.strip().splitlines()

    with open(os.path.join(cache_dir["path"], file_path), "r") as f:
        actual_content = f.read().strip().splitlines()

    for actual_line, expected_line in zip(actual_content, expected_content):
        if actual_line.startswith("tags: ") and expected_line.startswith("tags: "):
            assert_equal_tags_ignoring_order(
                actual_line, expected_line, actual_content, expected_content
            )
        else:
            assert actual_line.strip() == expected_line.strip(), [
                [actual_line.strip(), expected_line.strip()],
                [actual_content, expected_content],
            ]


def assert_equal_tags_ignoring_order(
    actual_line, expected_line, actual_content, expected_content
):
    actual_tags = set(tag.strip() for tag in actual_line[len("tags: ") :].split(","))
    expected_tags = set(
        tag.strip() for tag in expected_line[len("tags: ") :].split(",")
    )
    assert actual_tags == expected_tags, [
        [actual_tags, expected_tags],
        [expected_content, actual_content],
    ]


@then(parse("the cache should contain the files\n{file_list}"))
def cache_dir_contains_files(file_list, cache_dir):
    assert cache_dir["exists"]

    actual_files = os.listdir(cache_dir["path"])
    expected_files = file_list.split("\n")

    # sort to deal with inconsistent default file ordering on different OS's
    actual_files.sort()
    expected_files.sort()

    assert actual_files == expected_files, [actual_files, expected_files]


@then(parse("the output should be valid {language_name}"))
def assert_output_is_valid_language(cli_run, language_name):
    language_name = language_name.upper()
    if language_name == "XML":
        xml_tree = ElementTree.fromstring(cli_run["stdout"])
        assert xml_tree, "Invalid XML"
    elif language_name == "JSON":
        assert json.loads(cli_run["stdout"]), "Invalid JSON"
    else:
        assert False, f"Language name {language_name} not recognized"


@given(parse("we parse the output as {language_name}"), target_fixture="parsed_output")
def parse_output_as_language(cli_run, language_name):
    language_name = language_name.upper()
    actual_output = cli_run["stdout"]

    if language_name == "XML":
        parsed_output = ElementTree.fromstring(actual_output)
    elif language_name == "JSON":
        parsed_output = json.loads(actual_output)
    else:
        assert False, f"Language name {language_name} not recognized"

    return {"lang": language_name, "obj": parsed_output}


@then(parse('"{node_name}" in the parsed output should have {number:d} elements'))
def assert_parsed_output_item_count(node_name, number, parsed_output):
    lang = parsed_output["lang"]
    obj = parsed_output["obj"]

    if lang == "XML":
        xml_node_names = (node.tag for node in obj)
        assert node_name in xml_node_names, str(list(xml_node_names))

        actual_entry_count = len(obj.find(node_name))
        assert actual_entry_count == number, actual_entry_count

    elif lang == "JSON":
        my_obj = obj

        for node in node_name.split("."):
            try:
                my_obj = my_obj[int(node)]
            except ValueError:
                assert node in my_obj
                my_obj = my_obj[node]

        assert len(my_obj) == number, len(my_obj)

    else:
        assert False, f"Language name {lang} not recognized"


@then(parse('"{field_name}" in the parsed output should {comparison}\n{expected_keys}'))
def assert_output_field_content(
    field_name, comparison, expected_keys, cli_run, parsed_output
):
    lang = parsed_output["lang"]
    obj = parsed_output["obj"]
    expected_keys = expected_keys.split("\n")
    if len(expected_keys) == 1:
        expected_keys = expected_keys[0]

    if lang == "XML":
        xml_node_names = (node.tag for node in obj)
        assert field_name in xml_node_names, str(list(xml_node_names))

        if field_name == "tags":
            actual_tags = set(t.attrib["name"] for t in obj.find("tags"))
            assert set(actual_tags) == set(expected_keys), [
                actual_tags,
                set(expected_keys),
            ]
        else:
            assert False, "This test only works for tags in XML"

    elif lang == "JSON":
        my_obj = obj

        for node in field_name.split("."):
            try:
                my_obj = my_obj[int(node)]
            except ValueError:
                assert node in my_obj, [my_obj.keys(), node]
                my_obj = my_obj[node]

        if comparison == "be":
            if type(my_obj) is str:
                assert expected_keys == my_obj, [my_obj, expected_keys]
            else:
                assert set(expected_keys) == set(my_obj), [
                    set(my_obj),
                    set(expected_keys),
                ]
        elif comparison == "contain":
            if type(my_obj) is str:
                assert expected_keys in my_obj, [my_obj, expected_keys]
            else:
                assert all(elem in my_obj for elem in expected_keys), [
                    my_obj,
                    expected_keys,
                ]
    else:
        assert False, f"Language name {lang} not recognized"


@then(parse('there should be {number:d} "{item}" elements'))
def count_elements(number, item, cli_run):
    actual_output = cli_run["stdout"]
    xml_tree = ElementTree.fromstring(actual_output)
    assert len(xml_tree.findall(".//" + item)) == number

