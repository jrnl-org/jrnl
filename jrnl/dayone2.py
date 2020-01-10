import json

from datetime import datetime

from .Entry import Entry
from . import Journal


class DayOne2(Journal.PlainJournal):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _parse(self, json_data):

        entries = []

        json_string = json.loads(json_data)

        for entry in json_string["entries"]:
            entries.append(
                Entry(
                    self,
                    date=datetime.strptime(entry["creationDate"], "%Y-%m-%dT%H:%M:%SZ"),
                    text=entry["text"],
                    starred=entry["starred"],
                )
            )

        return entries
