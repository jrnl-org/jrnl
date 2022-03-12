# encoding: utf-8
# Copyright (C) 2012-2021 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import sys

from jrnl.exception import JrnlException
from jrnl.messages import Message
from jrnl.messages import MsgText
from jrnl.messages import MsgType


class JRNLImporter:
    """This plugin imports entries from other jrnl files."""

    names = ["jrnl"]

    @staticmethod
    def import_(journal, input=None):
        """Imports from an existing file if input is specified, and
        standard input otherwise."""
        old_cnt = len(journal.entries)
        if input:
            with open(input, "r", encoding="utf-8") as f:
                other_journal_txt = f.read()
        else:
            try:
                other_journal_txt = sys.stdin.read()
            except KeyboardInterrupt:
                raise JrnlException(
                    Message(MsgText.KeyboardInterruptMsg, MsgType.ERROR),
                    Message(MsgText.ImportAborted, MsgType.WARNING),
                )

        journal.import_(other_journal_txt)
        new_cnt = len(journal.entries)
        print(
            "[{} imported to {} journal]".format(new_cnt - old_cnt, journal.name),
            file=sys.stderr,
        )
        journal.write()
