# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import os
from contextlib import ExitStack

from pytest_bdd import when
from pytest_bdd.parsers import parse
from pytest_bdd.parsers import re

from jrnl.cli import cli


@when(parse('we change directory to "{directory_name}"'))
def when_we_change_directory(directory_name):
    if not os.path.isdir(directory_name):
        os.mkdir(directory_name)

    os.chdir(directory_name)


# These variables are used in the `@when(re(...))` section below
command = '(?P<command>[^"]*)'
input_method = "(?P<input_method>enter|pipe|type)"
all_input = '("(?P<all_input>[^"]*)")'
# Note: A line with only a raw newline r'\n' is treated as
# an empty line of input internally for testing purposes.


@when(parse('we run "jrnl {command}" and {input_method}\n{all_input}'))
@when(re(f'we run "jrnl ?{command}" and {input_method} {all_input}'))
@when(parse('we run "jrnl {command}"'))
@when('we run "jrnl"')
def we_run_jrnl(cli_run, capsys, keyring):
    from keyring import set_keyring

    set_keyring(keyring)

    with ExitStack() as stack:
        mocks = cli_run["mocks"]
        factories = cli_run["mock_factories"]

        for id in factories:
            mocks[id] = stack.enter_context(factories[id]())

        try:
            cli_run["status"] = cli() or 0
        except StopIteration:
            # This happens when input is expected, but don't have any input left
            pass
        except SystemExit as e:
            cli_run["status"] = e.code

    captured = capsys.readouterr()

    cli_run["stdout"] = captured.out
    cli_run["stderr"] = captured.err
