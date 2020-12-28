# Copyright (C) 2012-2021 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import shutil
import os
import re

import pytest
from pytest_bdd import given
from pytest_bdd import then
from pytest_bdd import when
from pytest_bdd.parsers import parse
from unittest.mock import patch

from jrnl import __version__
from jrnl.os_compat import split_args
from jrnl.cli import cli

WORKING_DIR = ''
TEMP_DIR = ''

# ----- FIXTURES ----- #
@pytest.fixture
def cli_run():
    return dict(status=0, stdout=None, stderr=None)


def get_working_dirs(request):
    CWD = request.config.rootpath
    return os.path.join(CWD, 'tests', '.current_test'), CWD


# ----- HOOKS ----- #
def pytest_bdd_before_scenario(request, feature, scenario):
    """Before each scenario, backup all config and journal test data."""
    global TEMP_DIR
    global WORKING_DIR
    TEMP_DIR, WORKING_DIR = get_working_dirs(request)

    if not os.path.exists(TEMP_DIR):
        os.mkdir(TEMP_DIR)


def pytest_bdd_after_scenario(request, feature, scenario):
    """After each scenario, restore all test data and remove working_dirs."""
    TEMP_DIR, WORKING_DIR = get_working_dirs(request)

    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)


# ----- STEPS ----- #
@given(parse('we use the config "{config_file}"'), target_fixture="config_path")
def set_config(config_file):
    # Copy the config file over
    config_source = os.path.join(WORKING_DIR, 'features', 'data', 'configs', config_file)
    config_dest = os.path.join(TEMP_DIR, config_file)
    shutil.copy2(config_source, config_dest)

    # @todo make this only copy some journals over
    # Copy all of the journals over
    journal_source = os.path.join(WORKING_DIR, 'features', 'data', 'journals')
    journal_dest = os.path.join(TEMP_DIR, 'features', 'journals')
    shutil.copytree(journal_source, journal_dest, dirs_exist_ok=True)

    # @todo get rid of this by using default config values
    # merge in version number
    if config_file.endswith("yaml") and os.path.exists(config_dest):
        # Add jrnl version to file for 2.x journals
        with open(config_dest, "a") as cf:
            cf.write("version: {}".format(__version__))

    return config_dest


@when(parse('we run "{command}"'))
def run(command, config_path, cli_run, capsys):
    args = split_args(command)
    status = 0

    # fmt: off
    # see: https://github.com/psf/black/issues/664
    with \
        patch("sys.argv", args), \
        patch("jrnl.config.get_config_path", side_effect=lambda: config_path), \
        patch("jrnl.install.get_config_path", side_effect=lambda: config_path) \
    :
        try:
            cli(args[1:])
        except SystemExit as e:
            status = e.code
    # fmt: on

    cli_run['status'] = status
    captured = capsys.readouterr()
    cli_run['stdout'] = captured.out
    cli_run['stderr'] = captured.err


@then("we should get no error")
def no_error(cli_run):
    assert cli_run['status'] == 0, cli_run['status']


@then(parse('the output should match "{regex}"'))
def matches_std_output(regex, cli_run):
    out = cli_run['stdout']
    matches = re.findall(regex, out)
    assert (
        matches
    ), f"\nRegex didn't match:\n{regex}\n{str(out)}\n{str(matches)}"
