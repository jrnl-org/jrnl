# Copyright (C) 2012-2021 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from datetime import datetime
import json
import os
import random
import shutil
import string
from unittest.mock import MagicMock
from unittest.mock import patch
from xml.etree import ElementTree

from pytest_bdd import given
from pytest_bdd.parsers import parse

from jrnl import __version__
from jrnl.time import __get_pdt_calendar

from .fixtures import FailedKeyring
from .fixtures import TestKeyring
from .helpers import get_fixture


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


@given(parse('now is "{date_str}"'))
def now_is_str(date_str, mock_factories):
    class DatetimeMagicMock(MagicMock):
        # needed because jrnl does some reflection on datetime
        def __instancecheck__(self, subclass):
            return isinstance(subclass, datetime)

    def mocked_now(tz=None):
        now = datetime.strptime(date_str, "%Y-%m-%d %I:%M:%S %p")

        if tz:
            time_zone = datetime.utcnow().astimezone().tzinfo
            now = now.replace(tzinfo=time_zone)

        return now

    # jrnl uses two different classes to parse dates, so both must be mocked
    datetime_mock = DatetimeMagicMock(wraps=datetime)
    datetime_mock.now.side_effect = mocked_now

    pdt = __get_pdt_calendar()
    calendar_mock = MagicMock(wraps=pdt)
    calendar_mock.parse.side_effect = lambda date_str_input: pdt.parse(
        date_str_input, mocked_now()
    )

    mock_factories["datetime"] = lambda: patch("datetime.datetime", new=datetime_mock)
    mock_factories["calendar_parse"] = lambda: patch(
        "jrnl.time.__get_pdt_calendar", return_value=calendar_mock
    )


@given("we have a keyring", target_fixture="keyring")
@given(parse("we have a {keyring_type} keyring"), target_fixture="keyring")
def we_have_type_of_keyring(keyring_type):
    if keyring_type == "failed":
        return FailedKeyring()
    else:
        return TestKeyring()


@given(parse('we use the config "{config_file}"'), target_fixture="config_path")
@given(parse("we use no config"), target_fixture="config_path")
def we_use_the_config(request, temp_dir, working_dir):
    config_file = get_fixture(request, "config_file")

    # Move into temp dir as cwd
    os.chdir(temp_dir.name)

    if not config_file:
        return os.path.join(temp_dir.name, "non_existing_config.yaml")

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
    if (
        config_file.endswith("yaml")
        and os.path.exists(config_dest)
        and os.path.getsize(config_dest) > 0
    ):
        # Add jrnl version to file for 2.x journals
        with open(config_dest, "a") as cf:
            cf.write("version: {}".format(__version__))

    return config_dest


@given(parse('the config "{config_file}" exists'), target_fixture="config_path")
def config_exists(config_file, temp_dir, working_dir):
    config_source = os.path.join(working_dir, "data", "configs", config_file)
    config_dest = os.path.join(temp_dir.name, config_file)
    shutil.copy2(config_source, config_dest)


@given(parse('we use the password "{password}" if prompted'))
def use_password_forever(password):
    return password


@given("we create a cache directory", target_fixture="cache_dir")
def create_cache_dir(temp_dir):
    random_str = "".join(random.choices(string.ascii_uppercase + string.digits, k=20))

    dir_path = os.path.join(temp_dir.name, "cache_" + random_str)
    os.mkdir(dir_path)
    return {"exists": True, "path": dir_path}


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
