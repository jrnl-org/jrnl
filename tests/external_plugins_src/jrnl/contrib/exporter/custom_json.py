# pelican\contrib\exporter\custom_json.py
import json

from jrnl.plugins.base import BaseExporter

__version__ = "v1.0.0"


class Exporter(BaseExporter):
    """
    This basic Exporter can convert entries and journals into JSON.
    """

    names = ["json"]
    extension = "json"
    version = __version__

    @classmethod
    def entry_to_dict(cls, entry):
        return {
            "title": entry.title,
            "body": entry.body,
            "date": entry.date.strftime("%Y-%m-%d"),
        }

    @classmethod
    def export_entry(cls, entry):
        """Returns a json representation of a single entry."""
        return json.dumps(cls.entry_to_dict(entry), indent=2) + "\n"

    @classmethod
    def export_journal(cls, journal):
        """Returns a json representation of an entire journal."""
        result = {
            "entries": [cls.entry_to_dict(e) for e in journal.entries],
        }
        return json.dumps(result, indent=2)
