from unittest import mock

from behave import then

from jrnl.args import parse_args
from jrnl.behave_testing import _mock_getpass
from jrnl.behave_testing import _mock_time_parse
from jrnl.jrnl import run


@then("the editor {editor} should have been called")
@then("No editor should have been called")
def editor_override(context, editor=None):
    def _mock_write_in_editor(config):
        editor = config["editor"]
        journal = "features/journals/journal.jrnl"
        context.tmpfile = journal
        print("%s has been launched" % editor)
        return journal

    if "password" in context:
        password = context.password
    else:
        password = ""
    # fmt: off
    # see: https://github.com/psf/black/issues/664
    with \
        mock.patch("jrnl.jrnl._write_in_editor", side_effect=_mock_write_in_editor(context.jrnl_config)) as mock_write_in_editor, \
        mock.patch("sys.stdin.isatty", return_value=True), \
        mock.patch('getpass.getpass',side_effect=_mock_getpass(password)), \
        mock.patch("jrnl.time.parse", side_effect = _mock_time_parse(context)), \
        mock.patch("jrnl.config.get_config_path", side_effect=lambda: context.config_path), \
        mock.patch("jrnl.install.get_config_path", side_effect=lambda: context.config_path) \
    :
        try :
                parsed_args = parse_args(context.args)
                run(parsed_args)
                context.exit_status = 0
                context.editor = mock_write_in_editor
                expected_config = context.jrnl_config
                expected_config['editor'] = '%s'%editor 
                expected_config['journal'] ='features/journals/journal.jrnl'

                if editor is not None:
                    assert mock_write_in_editor.call_count == 1
                    assert mock_write_in_editor.call_args[0][0]['editor']==editor
                else: 
                    # Expect that editor is *never* called
                    mock_write_in_editor.assert_not_called() 
        except SystemExit as e:
            context.exit_status = e.code
    # fmt: on


@then("the stdin prompt should have been called")
def override_editor_to_use_stdin(context):

    try:
        with mock.patch(
            "sys.stdin.read",
            return_value="Zwei peanuts walk into a bar und one of zem was a-salted",
        ) as mock_stdin_read, mock.patch(
            "jrnl.install.load_or_install_jrnl", return_value=context.jrnl_config
        ), mock.patch(
            "jrnl.Journal.open_journal",
            spec=False,
            return_value="features/journals/journal.jrnl",
        ), mock.patch(
            "getpass.getpass", side_effect=_mock_getpass("test")
        ):
            parsed_args = parse_args(context.args)
            run(parsed_args)
            context.exit_status = 0
        mock_stdin_read.assert_called_once()

    except SystemExit as e:
        context.exit_status = e.code
