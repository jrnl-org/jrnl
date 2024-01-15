# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import codecs
import os
import pathlib
from typing import TYPE_CHECKING

from jrnl import time

from .Journal import Journal

if TYPE_CHECKING:
    from jrnl.journals import Entry

# glob search patterns for folder/file structure
DIGIT_PATTERN = "[0123456789]"
YEAR_PATTERN = DIGIT_PATTERN * 4
MONTH_PATTERN = "[01]" + DIGIT_PATTERN
DAY_PATTERN = "[0123]" + DIGIT_PATTERN + ".txt"


class Folder(Journal):
    """A Journal handling multiple files in a folder"""

    def __init__(self, name: str = "default", **kwargs):
        self.entries = []
        self._diff_entry_dates = []
        self.can_be_encrypted = False
        super().__init__(name, **kwargs)

    def open(self) -> "Folder":
        filenames = []
        self.entries = []

        if os.path.exists(self.config["journal"]):
            filenames = Folder._get_files(self.config["journal"])
            for filename in filenames:
                with codecs.open(filename, "r", "utf-8") as f:
                    journal = f.read()
                    self.entries.extend(self._parse(journal))
            self.sort()

        return self

    def write(self) -> None:
        """Writes only the entries that have been modified into proper files."""
        # Create a list of dates of modified entries. Start with diff_entry_dates
        modified_dates = self._diff_entry_dates
        seen_dates = set(self._diff_entry_dates)

        for e in self.entries:
            if e.modified:
                if e.date not in modified_dates:
                    modified_dates.append(e.date)
                if e.date not in seen_dates:
                    seen_dates.add(e.date)

        # For every date that had a modified entry, write to a file
        for d in modified_dates:
            write_entries = []
            filename = os.path.join(
                self.config["journal"],
                d.strftime("%Y"),
                d.strftime("%m"),
                d.strftime("%d") + ".txt",
            )
            dirname = os.path.dirname(filename)
            # create directory if it doesn't exist
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            for e in self.entries:
                if (
                    e.date.year == d.year
                    and e.date.month == d.month
                    and e.date.day == d.day
                ):
                    write_entries.append(e)
            journal = "\n".join([e.__str__() for e in write_entries])
            with codecs.open(filename, "w", "utf-8") as journal_file:
                journal_file.write(journal)
        # look for and delete empty files
        filenames = []
        filenames = Folder._get_files(self.config["journal"])
        for filename in filenames:
            if os.stat(filename).st_size <= 0:
                os.remove(filename)

    def delete_entries(self, entries_to_delete: list["Entry"]) -> None:
        """Deletes specific entries from a journal."""
        for entry in entries_to_delete:
            self.entries.remove(entry)
            self._diff_entry_dates.append(entry.date)
            self.deleted_entry_count += 1

    def change_date_entries(self, date: str, entries_to_change: list["Entry"]) -> None:
        """Changes entry dates to given date."""

        date = time.parse(date)

        self._diff_entry_dates.append(date)

        for entry in entries_to_change:
            self._diff_entry_dates.append(entry.date)
            entry.date = date
            entry.modified = True

    def parse_editable_str(self, edited: str) -> None:
        """Parses the output of self.editable_str and updates its entries."""
        mod_entries = self._parse(edited)
        diff_entries = set(self.entries) - set(mod_entries)
        for e in diff_entries:
            self._diff_entry_dates.append(e.date)
        # Match those entries that can be found in self.entries and set
        # these to modified, so we can get a count of how many entries got
        # modified and how many got deleted later.
        for entry in mod_entries:
            entry.modified = not any(entry == old_entry for old_entry in self.entries)

        self.increment_change_counts_by_edit(mod_entries)
        self.entries = mod_entries

    @staticmethod
    def _get_files(journal_path: str) -> list[str]:
        """Searches through sub directories starting with journal_path and find all text
        files that look like entries"""
        for year_folder in Folder._get_year_folders(pathlib.Path(journal_path)):
            for month_folder in Folder._get_month_folders(year_folder):
                yield from Folder._get_day_files(month_folder)

    @staticmethod
    def _get_year_folders(path: pathlib.Path) -> list[pathlib.Path]:
        for child in path.glob(YEAR_PATTERN):
            if child.is_dir():
                yield child
        return

    @staticmethod
    def _get_month_folders(path: pathlib.Path) -> list[pathlib.Path]:
        for child in path.glob(MONTH_PATTERN):
            if int(child.name) > 0 and int(child.name) <= 12 and path.is_dir():
                yield child
        return

    @staticmethod
    def _get_day_files(path: pathlib.Path) -> list[str]:
        for child in path.glob(DAY_PATTERN):
            if (
                int(child.stem) > 0
                and int(child.stem) <= 31
                and time.is_valid_date(
                    year=int(path.parent.name),
                    month=int(path.name),
                    day=int(child.stem),
                )
                and child.is_file()
            ):
                yield str(child)
