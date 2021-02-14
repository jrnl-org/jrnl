import argparse
import jrnl
import pytest
from unittest import mock
from jrnl.jrnl import _export_journal


# fmt: off
# see: https://github.com/psf/black/issues/664
@pytest.mark.parametrize("export_format", [ "pretty", "short",])
#fmt: on
@mock.patch.object(argparse, "Namespace", return_value={"export": None, "filename": None})
def test_export_format(mock_args, export_format):

    test_journal = jrnl.Journal.Journal
    mock_args.export = export_format
    # fmt: off
    # see: https://github.com/psf/black/issues/664
    with mock.patch("builtins.print") as print_spy, mock.patch("jrnl.Journal.Journal.pprint") as mock_pprint:
        _export_journal(mock_args, test_journal)
    print_spy.call_args_list = mock_pprint
    # fmt: on


@mock.patch.object(argparse, "Namespace", return_value={"export": None, "filename": None})
def test_export_plugin(mock_args):
    export_format = "markdown"

    test_journal = jrnl.Journal.Journal
    mock_args.export = export_format
    mock_args.filename = "foo.jrnl"

    # fmt: off
    # see: https://github.com/psf/black/issues/664
    with mock.patch("builtins.print") as print_spy, \
    mock.patch("jrnl.plugins.get_exporter") as mock_get_exporter, \
    mock.patch("jrnl.Journal.Journal.pprint") as mock_pprint:
        _export_journal(mock_args, test_journal)
    # fmt: on
    
    print_spy.call_args_list = mock_pprint
    mock_get_exporter.assert_called_once_with(export_format)
