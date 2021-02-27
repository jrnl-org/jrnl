import argparse
import jrnl
import pytest
from unittest import mock
from jrnl.jrnl import _display_search_results, _export_journal


# fmt: off
# see: https://github.com/psf/black/issues/664
@pytest.mark.parametrize("export_format", [ "pretty", "short",])
#fmt: on
@mock.patch.object(argparse, "Namespace", return_value={"export": "markdown", "filename": "irrele.vant"})
def test_export_format(mock_args, export_format):

    test_journal = jrnl.Journal.Journal
    mock_args.export = export_format
    #fmt: off
    # see: https://github.com/psf/black/issues/664
    with mock.patch("builtins.print") as mock_spy_print, \
    mock.patch('jrnl.Journal.Journal.pprint') as mock_pprint:
        _display_search_results(mock_args, test_journal)
    mock_spy_print.assert_called_once_with(mock_pprint())
    #fmt: on


@mock.patch.object(argparse, "Namespace", return_value={"export": "markdown", "filename": "foo.jrnl"})
def test_export_plugin(mock_args):
    export_format =  mock_args.return_value["export"]

    test_journal = jrnl.Journal.Journal
    mock_args.export = export_format
    mock_args.filename = mock_args.return_value['filename']

    # fmt: off
    # see: https://github.com/psf/black/issues/664
    with mock.patch("builtins.print") as print_spy, \
    mock.patch("jrnl.plugins.get_exporter") as mock_get_exporter, \
    mock.patch("jrnl.Journal.Journal.pprint") :
        _export_journal(mock_args, test_journal)
    # fmt: on
    mock_get_exporter.assert_called_once_with(export_format)
    print_spy.assert_called_once_with(mock_get_exporter().export(test_journal,mock_args.filename))
