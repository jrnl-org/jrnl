from datetime import datetime

from jrnl.Entry import Entry
from jrnl.plugins.json_importer import JSONImporter


class DayOne2Importer(JSONImporter):

    names = ["dayone2"]
    extension = "json"

    def __init__(self, path, root_config, journal):
        self.type = "dayone2"
        self.path = path
        self.keys = [
            "audios",
            "creationDate",
            "photos",
            "starred",
            "tags",
            "text",
            "timeZone",
            "uuid",
        ]
        self.root_config = root_config
        JSONImporter.__init__(self)
        self.convert_journal()

    def convert_journal(self):
        self._convert()

    def validate_schema(self):
        try:
            for key in self.json["entries"][0]:
                try:
                    assert key in self.keys
                except AssertionError:
                    print(f"{self.path} is not the expected Day One 2 format.")
            return True

        except KeyError:
            print(f"{self.path} is not the expected Day One 2 format.")

    def parse_json(self):
        entries = []
        for entry in self.json["entries"]:
            tags = " ".join(["@" + t for t in entry["tags"]])

            entries.append(
                Entry(
                    self,
                    date=datetime.strptime(entry["creationDate"], "%Y-%m-%dT%H:%M:%SZ"),
                    text=f"{entry['text']} {tags}",
                    starred=entry["starred"],
                )
            )
        self.journal.entries = entries
        return entries
