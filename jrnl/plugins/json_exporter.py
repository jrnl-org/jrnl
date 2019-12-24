#!/usr/bin/env python
# encoding: utf-8

from .text_exporter import TextExporter
import json
from .util import get_tags_count


class JSONExporter(TextExporter):
    """This Exporter can convert entries and journals into json."""

    names = ["json"]
    extension = "json"

    @classmethod
    def entry_to_dict(cls, entry):
        entry_dict = {
            "title": entry.title,
            "body": entry.body,
            "date": entry.date.strftime("%Y-%m-%d"),
            "time": entry.date.strftime("%H:%M"),
            "starred": entry.starred,
        }
        if hasattr(entry, "uuid"):
            entry_dict["uuid"] = entry.uuid
        return entry_dict

    @classmethod
    def export_entry(cls, entry):
        """Returns a json representation of a single entry."""
        return json.dumps(cls.entry_to_dict(entry), indent=2) + "\n"

    @classmethod
    def export_journal(cls, journal):
        """Returns a json representation of an entire journal."""
        tags = get_tags_count(journal)
        result = {
            "tags": {tag: count for count, tag in tags},
            "entries": [cls.entry_to_dict(e) for e in journal.entries],
        }
        return json.dumps(result, indent=2)
