# pelican\contrib\importer\sample_json.py
import json
import sys

from jrnl import Entry
from jrnl.plugins.base import BaseImporter

__version__ = "v1.0.0"


class Importer(BaseImporter):
    """JSON Importer for jrnl."""

    names = ["json"]
    version = __version__

    @staticmethod
    def import_(journal, input=None):
        """
        Given a nicely formatted JSON file, will add the
        contained Entries to the journal.
        """

        old_cnt = len(journal.entries)
        if input:
            with open(input, "r", encoding="utf-8") as f:
                data = json.loads(f)
        else:
            try:
                data = sys.stdin.read()
            except KeyboardInterrupt:
                print(
                    "[Entries NOT imported into journal.]",
                    file=sys.stderr,
                )
                sys.exit(0)

        for json_entry in data:
            raw = json_entry["title"] + "/n" + json_entry["body"]
            date = json_entry["date"]
            entry = Entry.Entry(journal, date, raw)
            journal.entries.append(entry)

        new_cnt = len(journal.entries)
        print(
            "[{} entries imported to '{}' journal]".format(
                new_cnt - old_cnt, journal.name
            ),
            file=sys.stderr,
        )
