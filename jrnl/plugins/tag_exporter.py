# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from typing import TYPE_CHECKING

from jrnl.plugins.text_exporter import TextExporter
from jrnl.plugins.util import get_tags_count

if TYPE_CHECKING:
    from jrnl.journals import Entry
    from jrnl.journals import Journal


class TagExporter(TextExporter):
    """This Exporter can lists the tags for entries and journals, exported as a plain text file."""

    names = ["tags"]
    extension = "tags"

    @classmethod
    def export_entry(cls, entry: "Entry") -> str:
        """Returns a list of tags for a single entry."""
        return ", ".join(entry.tags)

    @classmethod
    def export_journal(cls, journal: "Journal") -> str:
        """Returns a list of tags and their frequency for an entire journal."""
        tag_counts = get_tags_count(journal)
        result = ""
        if not tag_counts:
            return "[No tags found in journal.]"
        elif min(tag_counts)[0] == 0:
            tag_counts = filter(lambda x: x[0] > 1, tag_counts)
            result += "[Removed tags that appear only once.]\n"
        result += "\n".join(
            "{:20} : {}".format(tag, n) for n, tag in sorted(tag_counts, reverse=True)
        )
        return result
