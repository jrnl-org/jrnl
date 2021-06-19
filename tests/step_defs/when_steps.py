# Copyright (C) 2012-2021 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import os
from contextlib import ExitStack
from unittest.mock import patch

from pytest_bdd import when
from pytest_bdd.parsers import parse
from pytest_bdd import parsers

from jrnl.cli import cli
from jrnl.os_compat import split_args


@when(parse('we change directory to "{directory_name}"'))
def when_we_change_directory(directory_name):
    if not os.path.isdir(directory_name):
        os.mkdir(directory_name)

    os.chdir(directory_name)


@when(parse('we run "jrnl {command}" and {input_method}\n{user_input}'))
@when(
    parsers.re(
        'we run "jrnl (?P<command>[^"]+)" and (?P<input_method>enter|pipe) "(?P<user_input>[^"]+)"'
    )
)
@when(parse('we run "jrnl" and {input_method} "{user_input}"'))
@when(parse('we run "jrnl {command}"'))
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
    keyring,
    input_method,
    mocks,
):
    assert input_method in ["", "enter", "pipe"]
    is_tty = input_method != "pipe"

    if cache_dir["exists"]:
        command = command.format(cache_dir=cache_dir["path"])

    args = split_args(command)
    status = 0

    if user_input:
        user_input = user_input.splitlines() if is_tty else [user_input]

    if password:
        password = password.splitlines()

    if not password and user_input:
        password = user_input

    with ExitStack() as stack:

        stack.enter_context(patch("sys.argv", ["jrnl"] + args))

        mock_stdin = stack.enter_context(
            patch("sys.stdin.read", side_effect=user_input)
        )
        stack.enter_context(patch("sys.stdin.isatty", return_value=is_tty))
        mock_input = stack.enter_context(
            patch("builtins.input", side_effect=user_input)
        )
        mock_getpass = stack.enter_context(
            patch("getpass.getpass", side_effect=password)
        )

        if "datetime" in mocks:
            stack.enter_context(mocks["datetime"])
            stack.enter_context(mocks["calendar_parse"])

            # stack.enter_context(patch("datetime.datetime", new=mocks["datetime"]))
            # stack.enter_context(patch("jrnl.time.__get_pdt_calendar", return_value=mocks["calendar_parse"]))

        stack.enter_context(
            patch("jrnl.install.get_config_path", return_value=config_path)
        )
        stack.enter_context(
            patch("jrnl.config.get_config_path", return_value=config_path)
        )
        mock_editor = stack.enter_context(patch("subprocess.call", side_effect=editor))

        try:
            cli(args)
        except StopIteration:
            # This happens when input is expected, but don't have any input left
            pass
        except SystemExit as e:
            status = e.code

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
