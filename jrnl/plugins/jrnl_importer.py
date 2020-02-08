#!/usr/bin/env python
# encoding: utf-8

import sys
from .. import util


class JRNLImporter:
    """This plugin imports entries from other jrnl files."""

    names = ["jrnl"]

    @staticmethod
    def import_(journal, input=None):
        """Imports from an existing file if input is specified, and
        standard input otherwise."""
        old_cnt = len(journal.entries)
        old_entries = journal.entries
        if input:
            with open(input, "r", encoding="utf-8") as f:
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
