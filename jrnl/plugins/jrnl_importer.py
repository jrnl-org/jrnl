# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import sys
from typing import TYPE_CHECKING

from jrnl.exception import JrnlException
from jrnl.messages import Message
from jrnl.messages import MsgStyle
from jrnl.messages import MsgText
from jrnl.output import print_msg

if TYPE_CHECKING:
    from jrnl.journals import Journal


class JRNLImporter:
    """This plugin imports entries from other jrnl files."""

    names = ["jrnl"]

    @staticmethod
    def import_(journal: "Journal", input: str | None = None) -> None:
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
                    Message(MsgText.KeyboardInterruptMsg, MsgStyle.ERROR_ON_NEW_LINE),
                    Message(MsgText.ImportAborted, MsgStyle.WARNING),
                )

        journal.import_(other_journal_txt)
        new_cnt = len(journal.entries)
        journal.write()
        print_msg(
            Message(
                MsgText.ImportSummary,
                MsgStyle.NORMAL,
                {
                    "count": new_cnt - old_cnt,
                    "journal_name": journal.name,
                },
            )
        )
