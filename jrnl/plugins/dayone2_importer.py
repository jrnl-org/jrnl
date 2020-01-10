from datetime import datetime

from jrnl.Entry import Entry
from jrnl.plugins.json_importer import JSONImporter


class DayOne2Importer(JSONImporter):

    names = ["dayone2"]
    extension = "json"

    def __init__(self, path):
        self.type = 'Day One 2'
        self.path = path
        self.keys = ['audios', 'creationDate', 'photos',
                     'starred', 'tags', 'text', 'timeZone', 'uuid']
        JSONImporter.__init__(self)
        self.convert_journal()

    def convert_journal(self):
        print(self._convert())

    def validate_schema(self):
        for key in self.json['entries'][0]:
            try:
                assert key in self.keys

            except AssertionError:
                raise KeyError(f"{self.path} is not the expected Day One 2 format.")
        print(f"{self.path} validated as Day One 2.")
        return True

    def parse_json(self):
        entries = []
        for entry in self.json["entries"]:
            entries.append(
                Entry(
                    self,
                    date=datetime.strptime(entry["creationDate"], "%Y-%m-%dT%H:%M:%SZ"),
                    text=entry["text"],
                    starred=entry["starred"],
                )
            )
        self.journal.entries = entries
        return entries
