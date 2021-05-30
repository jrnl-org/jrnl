# encoding: utf-8
# Copyright (C) 2012-2021 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

"""
Base class for Importers and Exporters.
"""


import os
import re
import unicodedata

from jrnl.color import ERROR_COLOR
from jrnl.color import RESET_COLOR


class BaseImporter:
    """Base Importer class (to sub-class)"""

    # names = ["jrnl"]
    # version = __version__

    @classmethod
    def class_path(cls):
        return cls.__module__

    @staticmethod
    def import_(journal, input=None):
        raise NotImplementedError


class BaseExporter:
    """Base Exporter class (to sub-class)"""

    # names = ["text", "txt"]
    # extension = "txt"
    # version = __version__

    @classmethod
    def class_path(cls):
        return cls.__module__

    @classmethod
    def export_entry(cls, entry):
        """Returns a string representation of a single entry."""
        raise NotImplementedError

    @classmethod
    def export_journal(cls, journal):
        """Returns a string representation of an entire journal."""
        return "\n".join(cls.export_entry(entry) for entry in journal)

    @classmethod
    def write_file(cls, journal, path):
        """Exports a journal into a single file."""
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(cls.export_journal(journal))
                return (
                    f"[Journal '{journal.name}' exported (as a single file) to {path}]"
                )
        except IOError as e:
            return f"[{ERROR_COLOR}ERROR{RESET_COLOR}: {e.filename} {e.strerror}]"
        except NotImplementedError:
            return (
                f"[{ERROR_COLOR}ERROR{RESET_COLOR}: This exporter doesn't support "
                "exporting as a single file.]"
            )

    @classmethod
    def make_filename(cls, entry):
        return entry.date.strftime("%Y-%m-%d") + "_{}.{}".format(
            cls._slugify(str(entry.title)), cls.extension
        )

    @classmethod
    def write_files(cls, journal, path):
        """Exports a journal into individual files for each entry."""
        try:
            for entry in journal.entries:
                try:
                    full_path = os.path.join(path, cls.make_filename(entry))
                    with open(full_path, "w", encoding="utf-8") as f:
                        f.write(cls.export_entry(entry))
                except IOError as e:
                    return "[{2}ERROR{3}: {0} {1}]".format(
                        e.filename, e.strerror, ERROR_COLOR, RESET_COLOR
                    )
        except NotImplementedError:
            return (
                f"[{ERROR_COLOR}ERROR{RESET_COLOR}: This exporter doesn't support "
                "exporting as individual files.]"
            )
        else:
            return f"[Journal '{journal.name}' exported (as multiple files) to {path}]"

    def _slugify(string):
        """Slugifies a string.
        Based on public domain code from https://github.com/zacharyvoase/slugify
        """
        normalized_string = str(unicodedata.normalize("NFKD", string))
        no_punctuation = re.sub(r"[^\w\s-]", "", normalized_string).strip().lower()
        slug = re.sub(r"[-\s]+", "-", no_punctuation)
        return slug

    @classmethod
    def export(cls, journal, output=None):
        """Exports to individual files if output is an existing path, or into
        a single file if output is a file name, or returns the exporter's
        representation as string if output is None."""
        if output and os.path.isdir(output):  # multiple files
            return cls.write_files(journal, output)
        elif output:  # single file
            return cls.write_file(journal, output)
        else:
            return cls.export_journal(journal)
