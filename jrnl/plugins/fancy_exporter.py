#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, unicode_literals, print_function
from .text_exporter import TextExporter
from textwrap import TextWrapper


class FancyExporter(TextExporter):
    """This Exporter can convert entries and journals into text with unicode box drawing characters."""

    names = ["fancy", "boxed"]
    extension = "txt"

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
        linewrap = entry.journal.config["linewrap"] or 78
        initial_linewrap = linewrap - len(date_str) - 2
        body_linewrap = linewrap - 2
        card = [
            cls.border_a + cls.border_b * (initial_linewrap) + cls.border_c + date_str
        ]
        w = TextWrapper(
            width=initial_linewrap,
            initial_indent=cls.border_g + " ",
            subsequent_indent=cls.border_g + " ",
        )
        title_lines = w.wrap(entry.title)
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
