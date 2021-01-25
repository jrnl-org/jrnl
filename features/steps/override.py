from jrnl.os_compat import split_args
from unittest import mock

# from __future__ import with_statement
from jrnl.args import parse_args
import os
from behave import given, when, then
import yaml
from yaml.loader import FullLoader

import jrnl
from jrnl.override import apply_overrides, _recursively_apply
from jrnl.cli import cli
from jrnl.jrnl import run


@given("we use the config {config_file}")
def load_config(context, config_file):
    filepath = os.path.join("features/configs", config_file)
    context.config_path = os.path.abspath(filepath)
    with open(context.config_path) as cfg:
        context.config = yaml.load(cfg, Loader=FullLoader)


@when("we run jrnl with {args}")
def run_command(context, args):
    context.args = split_args("%s" % args)
    context.parser = parse_args(context.args)


@then("the runtime config should have {key_as_dots} set to {override_value}")
def config_override(context, key_as_dots: str, override_value: str):
    with open(context.config_path) as f:
        loaded_cfg = yaml.load(f, Loader=yaml.FullLoader)
        loaded_cfg["journal"] = "features/journals/simple.journal"
    # base_cfg = loaded_cfg.copy()

    def _mock_callback(**args):
        print("callback executed")

    # fmt: off
    try: 
        with \
        mock.patch.object(jrnl.override,"recursively_apply",wraps=jrnl.override.recursively_apply) as mock_recurse, \
        mock.patch("jrnl.config.get_config_path", side_effect=lambda: context.config_path), \
        mock.patch("jrnl.install.get_config_path", side_effect=lambda: context.config_path) \
        : 
            cli(['-1','--config-override', '{"%s": "%s"}'%(key_as_dots,override_value)])
        mock_recurse.assert_called()
            
        
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
