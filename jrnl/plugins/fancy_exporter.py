# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import logging
import os
from textwrap import TextWrapper

from jrnl.exception import JrnlException
from jrnl.messages import Message
from jrnl.messages import MsgStyle
from jrnl.messages import MsgText
from jrnl.plugins.text_exporter import TextExporter


class FancyExporter(TextExporter):
    """This Exporter can convert entries and journals into text with unicode box drawing characters."""

    names = ["fancy", "boxed"]
    extension = "txt"

    # Top border of the card
    border_a = "┎"
    border_b = "─"
    border_c = "╮"
    border_d = "╘"
    border_e = "═"
    border_f = "╕"

    border_g = "┃"
    border_h = "│"
    border_i = "┠"
    border_j = "╌"
    border_k = "┤"
    border_l = "┖"
    border_m = "┘"

    @classmethod
    def export_entry(cls, entry):
        """Returns a fancy unicode representation of a single entry."""
        date_str = entry.date.strftime(entry.journal.config["timeformat"])

        if entry.journal.config["linewrap"]:
            linewrap = entry.journal.config["linewrap"]

            if linewrap == "auto":
                try:
                    linewrap = os.get_terminal_size().columns
                except OSError:
                    logging.debug(
                        "Can't determine terminal size automatically 'linewrap': '%s'",
                        entry.journal.config["linewrap"],
                    )
                    linewrap = 79
        else:
            linewrap = 79

        initial_linewrap = max((1, linewrap - len(date_str) - 2))
        body_linewrap = linewrap - 2
        card = [
            cls.border_a + cls.border_b * (initial_linewrap) + cls.border_c + date_str
        ]
        check_provided_linewrap_viability(linewrap, card, entry.journal.name)

        w = TextWrapper(
            width=initial_linewrap,
            initial_indent=cls.border_g + " ",
            subsequent_indent=cls.border_g + " ",
        )

        title_lines = w.wrap(entry.title) or [""]
        card.append(
            title_lines[0].ljust(initial_linewrap + 1)
            + cls.border_d
            + cls.border_e * (len(date_str) - 1)
            + cls.border_f
        )
        w.width = body_linewrap
        if len(title_lines) > 1:
            for line in w.wrap(
                " ".join(
                    [
                        title_line[len(w.subsequent_indent) :]
                        for title_line in title_lines[1:]
                    ]
                )
            ):
                card.append(line.ljust(body_linewrap + 1) + cls.border_h)
        if entry.body:
            card.append(cls.border_i + cls.border_j * body_linewrap + cls.border_k)
            for line in entry.body.splitlines():
                body_lines = w.wrap(line) or [cls.border_g]
                for body_line in body_lines:
                    card.append(body_line.ljust(body_linewrap + 1) + cls.border_h)
        card.append(cls.border_l + cls.border_b * body_linewrap + cls.border_m)
        return "\n".join(card)

    @classmethod
    def export_journal(cls, journal):
        """Returns a unicode representation of an entire journal."""
        return "\n".join(cls.export_entry(entry) for entry in journal)


def check_provided_linewrap_viability(linewrap, card, journal):
    if len(card[0]) > linewrap:
        width_violation = len(card[0]) - linewrap
        raise JrnlException(
            Message(
                MsgText.LineWrapTooSmallForDateFormat,
                MsgStyle.NORMAL,
                {
                    "config_linewrap": linewrap,
                    "columns": width_violation,
                    "journal": journal,
                },
            )
        )
