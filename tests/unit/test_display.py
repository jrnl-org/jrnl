import argparse
from unittest import mock

import pytest

import jrnl
from jrnl.jrnl import _display_search_results


# fmt: off
# see: https://github.com/psf/black/issues/664
@pytest.mark.parametrize("export_format", [ "pretty", "short","markdown"])
#fmt: on
@mock.patch.object(argparse, "Namespace", return_value={"export": "markdown", "filename": "irrele.vant"})
def test_export_format(mock_args, export_format):

    test_journal = jrnl.Journal.Journal
    mock_args.export = export_format
    mock_args.tags = None
    #fmt: off
    # see: https://github.com/psf/black/issues/664
    with mock.patch("builtins.print") as mock_spy_print, \
    mock.patch('jrnl.Journal.Journal.pprint') as mock_pprint:
        _display_search_results(mock_args, test_journal)
    mock_spy_print.assert_called_once_with(mock_pprint())
    #fmt: on
