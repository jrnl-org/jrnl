#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, unicode_literals
from .util import ERROR_COLOR, RESET_COLOR
from .util import slugify, u
from .template import Template
import os
import codecs


class Exporter(object):
    """This Exporter can convert entries and journals into text files."""
    def __init__(self, format):
        with open("jrnl/templates/" + format + ".template") as f:
            front_matter, body = f.read().strip("-\n").split("---", 2)
            self.template = Template(body)

    def export_entry(self, entry):
        """Returns a unicode representation of a single entry."""
        return entry.__unicode__()

    def _get_vars(self, journal):
        return {
            'journal': journal,
            'entries': journal.entries,
            'tags': journal.tags
        }

    def export_journal(self, journal):
        """Returns a unicode representation of an entire journal."""
        return self.template.render_block("journal", **self._get_vars(journal))

    def write_file(self, journal, path):
        """Exports a journal into a single file."""
        try:
            with codecs.open(path, "w", "utf-8") as f:
                f.write(self.export_journal(journal))
                return "[Journal exported to {0}]".format(path)
        except IOError as e:
            return "[{2}ERROR{3}: {0} {1}]".format(e.filename, e.strerror, ERROR_COLOR, RESET_COLOR)

    def make_filename(self, entry):
        return entry.date.strftime("%Y-%m-%d_{0}.{1}".format(slugify(u(entry.title)), self.extension))

    def write_files(self, journal, path):
        """Exports a journal into individual files for each entry."""
        for entry in journal.entries:
            try:
                full_path = os.path.join(path, self.make_filename(entry))
                with codecs.open(full_path, "w", "utf-8") as f:
                    f.write(self.export_entry(entry))
            except IOError as e:
                return "[{2}ERROR{3}: {0} {1}]".format(e.filename, e.strerror, ERROR_COLOR, RESET_COLOR)
        return "[Journal exported to {0}]".format(path)

    def export(self, journal, format="text", output=None):
        """Exports to individual files if output is an existing path, or into
        a single file if output is a file name, or returns the exporter's
        representation as unicode if output is None."""
        if output and os.path.isdir(output):  # multiple files
            return self.write_files(journal, output)
        elif output:                          # single file
            return self.write_file(journal, output)
        else:
            return self.export_journal(journal)
