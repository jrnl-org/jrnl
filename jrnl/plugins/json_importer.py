import json
import os

from abc import abstractmethod
from pathlib import Path

from jrnl.Journal import PlainJournal
from jrnl.plugins.text_exporter import TextExporter


class JSONImporter(PlainJournal, TextExporter):
    """This importer reads a JSON file and returns a dict. """

    def __init__(self):
        PlainJournal.__init__(self)
        self.journal = PlainJournal()
        self.path = self.path[0]
        self.filename = os.path.splitext(self.path)[0]
        self.json = self.import_file()

    def __str__(self):
        return f"{self.type} journal with {len(self.journal)} " \
               f"entries located at {self.path}"

    def _convert(self):
        if self.validate_schema():
            self.data = self.parse_json()
            self.create_file(self.filename + '.txt')
            return self.export(self.journal, self.filename + '.txt')

    def import_file(self):
        """Reads a JSON file and returns a dict."""
        if os.path.exists(self.path):
            try:
                with open(self.path) as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"{self.path} is not valid JSON.")
        elif Path(self.path).suffix != '.json':
            print(f"{self.path} must be a JSON file.")
        else:
            print(f"{self.path} does not exist.")

    @abstractmethod
    def parse_json(self):
        raise NotImplementedError

    @abstractmethod
    def validate_schema(self):
        raise NotImplementedError
