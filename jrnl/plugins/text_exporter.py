# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import errno
import os
import re
import unicodedata

from jrnl.messages import Message
from jrnl.messages import MsgStyle
from jrnl.messages import MsgText
from jrnl.output import print_msg


class TextExporter:
    """This Exporter can convert entries and journals into text files."""

    names = ["text", "txt"]
    extension = "txt"

    @classmethod
    def export_entry(cls, entry):
        """Returns a string representation of a single entry."""
        return str(entry)

    @classmethod
    def export_journal(cls, journal):
        """Returns a string representation of an entire journal."""
        return "\n".join(cls.export_entry(entry) for entry in journal)

    @classmethod
    def write_file(cls, journal, path):
        """Exports a journal into a single file."""
        export_str = cls.export_journal(journal)
        with open(path, "w", encoding="utf-8") as f:
            f.write(export_str)
        print_msg(
            Message(
                MsgText.JournalExportedTo,
                MsgStyle.NORMAL,
                {
                    "path": path,
                },
            )
        )
        return ""

    @classmethod
    def make_filename(cls, entry):
        return entry.date.strftime("%Y-%m-%d") + "_{}.{}".format(
            cls._slugify(str(entry.title)), cls.extension
        )

    @classmethod
    def write_files(cls, journal, path):
        """Exports a journal into individual files for each entry."""
        for entry in journal.entries:
            entry_is_written = False
            while not entry_is_written:
                full_path = os.path.join(path, cls.make_filename(entry))
                try:
                    with open(full_path, "w", encoding="utf-8") as f:
                        f.write(cls.export_entry(entry))
                        entry_is_written = True
                except OSError as oserr:
                    title_length = len(str(entry.title))
                    if (
                        oserr.errno == errno.ENAMETOOLONG
                        or oserr.errno == errno.ENOENT
                        or oserr.errno == errno.EINVAL
                    ) and title_length > 1:
                        shorter_file_length = title_length // 2
                        entry.title = str(entry.title)[:shorter_file_length]
                    else:
                        raise
        print_msg(
            Message(
                MsgText.JournalExportedTo,
                MsgStyle.NORMAL,
                {"path": path},
            )
        )
        return ""

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
