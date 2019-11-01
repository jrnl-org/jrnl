#!/usr/bin/env python

from .util import ERROR_COLOR, RESET_COLOR
from .util import slugify
from .plugins.template import Template
import os


class Exporter:
    """This Exporter can convert entries and journals into text files."""
    def __init__(self, format):
        with open("jrnl/templates/" + format + ".template") as f:
            front_matter, body = f.read().strip("-\n").split("---", 2)
            self.template = Template(body)

    def export_entry(self, entry):
        """Returns a string representation of a single entry."""
        return str(entry)

    def _get_vars(self, journal):
        return {
            'journal': journal,
            'entries': journal.entries,
            'tags': journal.tags
        }

    def export_journal(self, journal):
        """Returns a string representation of an entire journal."""
        return self.template.render_block("journal", **self._get_vars(journal))

    def write_file(self, journal, path):
        """Exports a journal into a single file."""
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.export_journal(journal))
                return f"[Journal exported to {path}]"
        except OSError as e:
            return f"[{ERROR_COLOR}ERROR{RESET_COLOR}: {e.filename} {e.strerror}]"

    def make_filename(self, entry):
        return entry.date.strftime("%Y-%m-%d_{}.{}".format(slugify(entry.title), self.extension))

    def write_files(self, journal, path):
        """Exports a journal into individual files for each entry."""
        for entry in journal.entries:
            try:
                full_path = os.path.join(path, self.make_filename(entry))
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(self.export_entry(entry))
            except OSError as e:
                return f"[{ERROR_COLOR}ERROR{RESET_COLOR}: {e.filename} {e.strerror}]"
        return f"[Journal exported to {path}]"

    def export(self, journal, format="text", output=None):
        """Exports to individual files if output is an existing path, or into
        a single file if output is a file name, or returns the exporter's
        representation as string if output is None."""
        if output and os.path.isdir(output):  # multiple files
            return self.write_files(journal, output)
        elif output:                          # single file
            return self.write_file(journal, output)
        else:
            return self.export_journal(journal)
