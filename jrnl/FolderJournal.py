# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import codecs
import fnmatch
import os

from jrnl import Journal
from jrnl import time


def get_files(journal_config):
    """Searches through sub directories starting with journal_config and find all text files"""
    filenames = []
    for root, dirnames, f in os.walk(journal_config):
        for filename in fnmatch.filter(f, "*.txt"):
            filenames.append(os.path.join(root, filename))
    return filenames


class Folder(Journal.Journal):
    """A Journal handling multiple files in a folder"""

    def __init__(self, name="default", **kwargs):
        self.entries = []
        self._diff_entry_dates = []
        self.can_be_encrypted = False
        super().__init__(name, **kwargs)

    def open(self):
        filenames = []
        self.entries = []
        filenames = get_files(self.config["journal"])
        for filename in filenames:
            with codecs.open(filename, "r", "utf-8") as f:
                journal = f.read()
                self.entries.extend(self._parse(journal))
        self.sort()
        return self

    def write(self):
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
        filenames = get_files(self.config["journal"])
        for filename in filenames:
            if os.stat(filename).st_size <= 0:
                os.remove(filename)

    def delete_entries(self, entries_to_delete):
        """Deletes specific entries from a journal."""
        for entry in entries_to_delete:
            self.entries.remove(entry)
            self._diff_entry_dates.append(entry.date)

    def change_date_entries(self, date):
        """Changes entry dates to given date."""

        date = time.parse(date)

        self._diff_entry_dates.append(date)

        for entry in self.entries:
            self._diff_entry_dates.append(entry.date)
            entry.date = date

    def parse_editable_str(self, edited):
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
        self.entries = mod_entries
