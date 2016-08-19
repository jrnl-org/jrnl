#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, unicode_literals
import codecs
import sys
from .. import util

class JRNLImporter(object):
    """This plugin imports entries from other jrnl files."""
    names = ["jrnl"]

    @staticmethod
    def import_(journal, input=None):
        """Imports from an existing file if input is specified, and
        standard input otherwise."""
        old_cnt = len(journal.entries)
        old_entries = journal.entries
        if input:
            with codecs.open(input, "r", "utf-8") as f:
                other_journal_txt = f.read()
        else:
            try:
                other_journal_txt = util.py23_read()
            except KeyboardInterrupt:
                util.prompt("[Entries NOT imported into journal.]")
                sys.exit(0)
        journal.import_(other_journal_txt)
        new_cnt = len(journal.entries)
        util.prompt("[{0} imported to {1} journal]".format(new_cnt - old_cnt, journal.name))
        journal.write()
