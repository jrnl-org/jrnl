#!/usr/bin/env python
# encoding: utf-8

import sys

from pathlib import Path
from jrnl import util


class JRNLImporter:
    """This plugin imports entries from other jrnl files."""

    names = ["jrnl"]

    def __init__(self, path, root_config, journal):
        self.path = Path(path[0])
        self.root_config = root_config
        self.journal = journal
        self.import_(self.journal)

    def import_(self, journal):
        """Imports from an existing file if input is specified, and
        standard input otherwise."""
        old_cnt = len(journal.entries)
        old_entries = journal.entries
        if self.journal:
            with open(self.path, "r", encoding="utf-8") as f:
                other_journal_txt = f.read()
        else:
            try:
                other_journal_txt = sys.stdin.read()
            except KeyboardInterrupt:
                print("[Entries NOT imported into journal.]", file=sys.stderr)
                sys.exit(0)
        journal.import_(other_journal_txt)
        new_cnt = len(journal.entries)
        print(
            "[{} imported to {} journal]".format(new_cnt - old_cnt, journal.name),
            file=sys.stderr,
        )
        journal.write()
