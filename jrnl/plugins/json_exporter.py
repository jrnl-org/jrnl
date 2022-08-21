# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import json

from jrnl.plugins.text_exporter import TextExporter
from jrnl.plugins.util import get_tags_count


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
            "tags": entry.tags,
            "starred": entry.starred,
        }
        if hasattr(entry, "uuid"):
            entry_dict["uuid"] = entry.uuid
        if (
            hasattr(entry, "creator_device_agent")
            or hasattr(entry, "creator_generation_date")
            or hasattr(entry, "creator_host_name")
            or hasattr(entry, "creator_os_agent")
            or hasattr(entry, "creator_software_agent")
        ):
            entry_dict["creator"] = {}
            if hasattr(entry, "creator_device_agent"):
                entry_dict["creator"]["device_agent"] = entry.creator_device_agent
            if hasattr(entry, "creator_generation_date"):
                entry_dict["creator"]["generation_date"] = str(
                    entry.creator_generation_date
                )
            if hasattr(entry, "creator_host_name"):
                entry_dict["creator"]["host_name"] = entry.creator_host_name
            if hasattr(entry, "creator_os_agent"):
                entry_dict["creator"]["os_agent"] = entry.creator_os_agent
            if hasattr(entry, "creator_software_agent"):
                entry_dict["creator"]["software_agent"] = entry.creator_software_agent

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
