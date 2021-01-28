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


def _mock_time_parse(context):
    original_parse = jrnl.time.parse
    if "now" not in context:
        return original_parse

    def wrapper(input, *args, **kwargs):
        input = context.now if input == "now" else input
        return original_parse(input, *args, **kwargs)

    return wrapper


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

    def _mock_callback(**args):
        print("callback executed")

    # fmt: off
    try: 
        with \
        mock.patch("jrnl.jrnl.search_mode"), \
        mock.patch.object(jrnl.override,"_recursively_apply",wraps=jrnl.override._recursively_apply) as mock_recurse, \
        mock.patch('jrnl.install.load_or_install_jrnl', return_value=context.cfg), \
        mock.patch('jrnl.time.parse', side_effect=_mock_time_parse(context)), \
        mock.patch("jrnl.config.get_config_path", side_effect=lambda: context.config_path), \
        mock.patch("jrnl.install.get_config_path", side_effect=lambda: context.config_path) \
        : 
            run(context.parser)
        runtime_cfg = mock_recurse.call_args_list[0][0][0]
        
        for k in key_as_vec: 
            runtime_cfg = runtime_cfg['%s'%k]

        assert runtime_cfg == override_value
    except SystemExit as e :
        context.exit_status = e.code
    # fmt: on


@then("the editor {editor} should have been called")
def editor_override(context, editor):
    def _mock_write_in_editor(config):
        editor = config['editor']
        journal = 'features/journals/journal.jrnl'
        context.tmpfile = journal
        print("%s has been launched" % editor)
        return journal

    # fmt: off
    # see: https://github.com/psf/black/issues/664
    with \
        mock.patch("jrnl.jrnl._write_in_editor", side_effect=_mock_write_in_editor(context.cfg)) as mock_write_in_editor, \
        mock.patch("sys.stdin.isatty", return_value=True), \
        mock.patch("jrnl.time.parse", side_effect = _mock_time_parse(context)), \
        mock.patch("jrnl.config.get_config_path", side_effect=lambda: context.config_path), \
        mock.patch("jrnl.install.get_config_path", side_effect=lambda: context.config_path) \
    :
        try :
                run(context.parser)
                context.exit_status = 0
                context.editor = mock_write_in_editor
                expected_config = context.cfg
                expected_config['editor'] = '%s'%editor 
                expected_config['journal'] ='features/journals/journal.jrnl'

                assert mock_write_in_editor.call_count == 1
                assert mock_write_in_editor.call_args[0][0]['editor']==editor
        except SystemExit as e:
            context.exit_status = e.code
    # fmt: on


    try: 
        with \
        mock.patch('sys.stdin.read', return_value='Zwei peanuts walk into a bar und one of zem was a-salted')as mock_stdin_read, \
        mock.patch("jrnl.install.load_or_install_jrnl", return_value=context.cfg), \
        mock.patch("jrnl.Journal.open_journal", spec=False, return_value='features/journals/journal.jrnl'):
            run(context.parser)
            context.exit_status = 0
        mock_stdin_read.assert_called_once()

    except SystemExit as e:
        context.exit_status = e.code
