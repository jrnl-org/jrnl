#!/usr/bin/env python
# encoding: utf-8
# Copyright (C) 2012-2021 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from .text_exporter import TextExporter
from .util import get_date_counts


class DatecountExporter(TextExporter):
    """This Exporter can lists the tags for entries and journals, exported as a plain text file."""

    names = ["datecount"]
    extension = "datecount"

    @classmethod
    def export_entry(cls, entry):
        raise NotImplementedError

    @classmethod
    def export_journal(cls, journal):
        """Returns dates and their frequencies for an entire journal."""
        date_counts = get_date_counts(journal)
        if not date_counts:
            return "[No dates found in journal.]"
        result = "\n".join(f"{date}, {count}" for date, count in date_counts.items())
        return result
