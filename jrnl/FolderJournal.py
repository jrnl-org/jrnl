#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, unicode_literals
from . import Entry
from . import Journal
import codecs
import os
import fnmatch


def get_files(journal_config):
    """Searches through sub directories starting with journal_config and find all text files"""
    filenames = []
    for root, dirnames, f in os.walk(journal_config):
        for filename in fnmatch.filter(f, "*.txt"):
            filenames.append(os.path.join(root, filename))
    return filenames


class Folder(Journal.Journal):
    """A Journal handling multiple files in a folder"""

    def __init__(self, **kwargs):
        self.entries = []
        self._diff_entry_dates = []
        super(Folder, self).__init__(**kwargs)

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
                if e.date not in seen_dates:
                    modified_dates.append(e.date)
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
                # print("empty file: {}".format(filename))
                os.remove(filename)

    def parse_editable_str(self, edited):
        """Parses the output of self.editable_str and updates it's entries."""
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
