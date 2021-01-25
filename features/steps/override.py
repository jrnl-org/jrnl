from jrnl.jrnl import run
from jrnl.os_compat import split_args
from unittest import mock

# from __future__ import with_statement
from jrnl.args import parse_args
import os
from behave import given, when, then
import yaml
from yaml.loader import FullLoader

import jrnl
from jrnl.cli import cli


@given("we use the config {config_file}")
def load_config(context, config_file):
    filepath = os.path.join("features/configs", config_file)
    context.config_path = os.path.abspath(filepath)


@when("we run jrnl with {args}")
def run_command(context, args):
    context.args = split_args("%s" % args)
    context.parser = parse_args(context.args)
    with open(context.config_path, "r") as f:
        cfg = yaml.load(f, Loader=FullLoader)
    context.cfg = cfg


@then("the runtime config should have {key_as_dots} set to {override_value}")
def config_override(context, key_as_dots: str, override_value: str):
    key_as_vec = key_as_dots.split(".")
    expected_call_args_list = [
        (context.cfg, key_as_vec, override_value),
        (context.cfg[key_as_vec[0]], key_as_vec[1], override_value),
    ]
    with open(context.config_path) as f:
        loaded_cfg = yaml.load(f, Loader=yaml.FullLoader)
        loaded_cfg["journal"] = "features/journals/simple.journal"

    def _mock_callback(**args):
        print("callback executed")

    # fmt: off
    try: 
        with \
        mock.patch.object(jrnl.override,"_recursively_apply",wraps=jrnl.override._recursively_apply) as mock_recurse, \
        mock.patch('jrnl.install.load_or_install_jrnl', return_value=context.cfg), \
        mock.patch("jrnl.config.get_config_path", side_effect=lambda: context.config_path), \
        mock.patch("jrnl.install.get_config_path", side_effect=lambda: context.config_path) \
        : 
            run(context.parser)
        
        assert mock_recurse.call_count == 2
        mock_recurse.call_args_list = expected_call_args_list
        
    except SystemExit as e :
        context.exit_status = e.code
    # fmt: on


@then("the editor {editor} should have been called")
def editor_override(context, editor):
    def _mock_editor(command_and_journal_file):
        editor = command_and_journal_file[0]
        tmpfile = command_and_journal_file[-1]
        context.tmpfile = tmpfile
        print("%s has been launched" % editor)
        return tmpfile

    # fmt: off
    # see: https://github.com/psf/black/issues/664
    with \
        mock.patch("subprocess.call", side_effect=_mock_editor) as mock_editor, \
        mock.patch("sys.stdin.isatty", return_value=True), \
        mock.patch("jrnl.time.parse"), \
        mock.patch("jrnl.config.get_config_path", side_effect=lambda: context.config_path), \
        mock.patch("jrnl.install.get_config_path", side_effect=lambda: context.config_path) \
    :
        try :
                cli(['--config-override','{"editor": "%s"}'%editor])
                context.exit_status = 0
                context.editor = mock_editor
                assert mock_editor.assert_called_once_with(editor, context.tmpfile)
        except SystemExit as e:
            context.exit_status = e.code
    # fmt: on
