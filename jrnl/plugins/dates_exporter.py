# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from collections import Counter

from jrnl.plugins.text_exporter import TextExporter


class DatesExporter(TextExporter):
    """This Exporter lists dates and their respective counts, for heatingmapping etc."""

    names = ["dates"]
    extension = "dates"

    @classmethod
    def export_entry(cls, entry):
        raise NotImplementedError

    @classmethod
    def export_journal(cls, journal):
        """Returns dates and their frequencies for an entire journal."""
        date_counts = Counter()
        for entry in journal.entries:
            # entry.date.date() gets date without time
            date = str(entry.date.date())
            date_counts[date] += 1
        result = "\n".join(f"{date}, {count}" for date, count in date_counts.items())
        return result
