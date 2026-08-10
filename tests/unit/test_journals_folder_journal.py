# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import datetime
import pathlib
from unittest import mock

import pytest

from jrnl.journals.Entry import Entry
from jrnl.journals.FolderJournal import Folder


@pytest.mark.parametrize(
    "inputs_and_outputs",
    [
        [
            "/2020/01",
            ["02.txt", "03.txt", "31.txt"],
            ["/2020/01/02.txt", "/2020/01/03.txt", "/2020/01/31.txt"],
        ],
        [
            "/2020/02",  # leap year
            ["02.txt", "03.txt", "28.txt", "29.txt", "31.txt", "39.txt"],
            [
                "/2020/02/02.txt",
                "/2020/02/03.txt",
                "/2020/02/28.txt",
                "/2020/02/29.txt",
            ],
        ],
        [
            "/2100/02",  # not a leap year
            ["01.txt", "28.txt", "29.txt", "39.txt"],
            ["/2100/02/01.txt", "/2100/02/28.txt"],
        ],
        [
            "/2023/04",
            ["29.txt", "30.txt", "31.txt", "39.txt"],
            ["/2023/04/29.txt", "/2023/04/30.txt"],
        ],
    ],
)
def test_get_day_files_expected_filtering(inputs_and_outputs):
    year_month_path, glob_filenames, expected_output = inputs_and_outputs

    year_month_path = pathlib.Path(year_month_path)

    glob_files = map(lambda x: year_month_path / x, glob_filenames)
    expected_output = list(map(lambda x: str(pathlib.PurePath(x)), expected_output))

    with (
        mock.patch("pathlib.Path.glob", return_value=glob_files),
        mock.patch.object(pathlib.Path, "is_file", return_value=True),
    ):
        actual_output = list(Folder._get_day_files(year_month_path, ".txt"))
        actual_output.sort()

        expected_output.sort()

        assert actual_output == expected_output


def test_dateless_timeformat_preserves_same_day_entries(tmp_path):
    # Regression for #2006: with a timeformat that carries no date component
    # (e.g. "%H:%M"), a second entry added on the same day must not overwrite
    # the earlier one. The folder path (YYYY/MM/DD) is authoritative for the
    # date, so entries must round-trip regardless of the timeformat.
    kwargs = {"journal": str(tmp_path / "journal"), "timeformat": "%H:%M"}

    journal = Folder("test", **kwargs)
    morning = Entry(
        journal, date=datetime.datetime(2020, 1, 15, 9, 0), text="Morning entry"
    )
    morning.modified = True
    journal.entries = [morning]
    journal.write()

    journal = Folder("test", **kwargs).open()
    evening = Entry(
        journal, date=datetime.datetime(2020, 1, 15, 17, 0), text="Evening entry"
    )
    evening.modified = True
    journal.entries.append(evening)
    journal.write()

    journal = Folder("test", **kwargs).open()
    texts = " ".join(e.text for e in journal.entries)
    assert len(journal.entries) == 2
    assert "Morning entry" in texts
    assert "Evening entry" in texts
