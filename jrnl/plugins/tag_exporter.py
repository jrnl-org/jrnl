#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, unicode_literals
from .text_exporter import TextExporter
from .util import get_tags_count


class TagExporter(TextExporter):
    """This Exporter can convert entries and journals into json."""
    names = ["tags"]
    extension = "tags"

    @classmethod
    def export_entry(cls, entry):
        """Returns a markdown representation of a single entry."""
        return ", ".join(entry.tags)

    @classmethod
    def export_journal(cls, journal):
        """Returns a json representation of an entire journal."""
        tag_counts = get_tags_count(journal)
        result = ""
        if not tag_counts:
            return '[No tags found in journal.]'
        elif min(tag_counts)[0] == 0:
            tag_counts = filter(lambda x: x[0] > 1, tag_counts)
            result += '[Removed tags that appear only once.]\n'
        result += "\n".join("{0:20} : {1}".format(tag, n) for n, tag in sorted(tag_counts, reverse=True))
        return result
