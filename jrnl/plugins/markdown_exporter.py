#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, unicode_literals
from .text_exporter import TextExporter


class MarkdownExporter(TextExporter):
    """This Exporter can convert entries and journals into Markdown."""
    names = ["md", "markdown"]
    extension = "md"

    @classmethod
    def export_entry(cls, entry, to_multifile=True):
        """Returns a markdown representation of a single entry."""
        date_str = entry.date.strftime(entry.journal.config['timeformat'])
        body_wrapper = "\n" if entry.body else ""
        body = body_wrapper + entry.body

        if to_multifile is True:
            heading = '#'
        else:
            heading = '###'

        return "{md} {date} {title} {body} {space}".format(
            md=heading,
            date=date_str,
            title=entry.title,
            body=body,
            space=""
        )

    @classmethod
    def export_journal(cls, journal):
        """Returns a Markdown representation of an entire journal."""
        out = []
        year, month = -1, -1
        for e in journal.entries:
            if not e.date.year == year:
                year = e.date.year
                out.append(str(year))
                out.append("=" * len(str(year)) + "\n")
            if not e.date.month == month:
                month = e.date.month
                out.append(e.date.strftime("%B"))
                out.append('-' * len(e.date.strftime("%B")) + "\n")
            out.append(cls.export_entry(e, False))
        result = "\n".join(out)
        return result
