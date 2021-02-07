import argparse
import jrnl
import pytest 
import mock
from jrnl.jrnl import _export_journal, _display_search_results
@pytest.mark.parametrize(
    "export_format",
    [
        "pretty",
        "short",
        "markdown",
        "json"
    ]
)
@mock.patch.object(argparse,'Namespace',autospec=True)
@mock.patch.object(jrnl,'Journal',autospec=True)
def test_export_format(mock_journal, mock_args, export_format): 
    mock_args.export = export_format
    mock_args.filename = "foo.jrnl"
    with mock.patch('builtins.print', wraps=print) as print_spy:
        _export_journal(mock_args,mock_journal)
    print_spy.assert_called_once()
    