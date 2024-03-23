# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import pathlib
from unittest import mock

import pytest

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
