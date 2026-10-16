# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from datetime import datetime
from types import SimpleNamespace
from unittest import mock

import pytest

from jrnl.exception import JrnlException
from jrnl.plugins.fancy_exporter import check_provided_linewrap_viability
from jrnl.plugins.markdown_exporter import MarkdownExporter
from jrnl.plugins.yaml_exporter import YAMLExporter


@pytest.fixture()
def datestr():
    yield "2020-10-20 16:59"


def build_card_header(datestr):
    top_left_corner = "┎─╮"
    content = top_left_corner + datestr
    return content


class TestFancy:
    def test_too_small_linewrap(self, datestr):
        journal = "test_journal"
        content = build_card_header(datestr)

        total_linewrap = 12

        with pytest.raises(JrnlException):
            check_provided_linewrap_viability(total_linewrap, [content], journal)


class TestYaml:
    @mock.patch("builtins.open")
    def test_export_to_nonexisting_folder(self, mock_open):
        with pytest.raises(JrnlException):
            YAMLExporter.write_file("journal", "non-existing-path")
        mock_open.assert_not_called()


class TestMarkdown:
    @pytest.mark.parametrize("years", [(2024, 2025), (2025, 2024)])
    def test_same_month_in_different_years_has_both_headings(self, years):
        journal = SimpleNamespace(config={"timeformat": "%Y-%m-%d"})
        journal.entries = [
            SimpleNamespace(
                date=datetime(year, 1, 2), title="Entry", body="", journal=journal
            )
            for year in years
        ]
        output = MarkdownExporter.export_journal(journal)
        headings = [
            line
            for line in output.splitlines()
            if line.startswith("# ") or line.startswith("## ")
        ]
        month = journal.entries[0].date.strftime("%B")
        assert headings == [
            f"# {years[0]}",
            f"## {month}",
            f"# {years[1]}",
            f"## {month}",
        ]

    def test_same_year_and_month_does_not_repeat_heading(self):
        journal = SimpleNamespace(config={"timeformat": "%Y-%m-%d"})
        journal.entries = [
            SimpleNamespace(
                date=datetime(2024, 1, day), title="Entry", body="", journal=journal
            )
            for day in (2, 3)
        ]
        output = MarkdownExporter.export_journal(journal)
        month = journal.entries[0].date.strftime("%B")
        assert output.count(f"## {month}\n") == 1
