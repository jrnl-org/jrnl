#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, unicode_literals

from .text_exporter import TextExporter
from .template import Template
import os
from glob import glob


class GenericTemplateExporter(TextExporter):
    """This Exporter can convert entries and journals into text files."""

    @classmethod
    def export_entry(cls, entry):
        """Returns a unicode representation of a single entry."""
        vars = {
            'entry': entry,
            'tags': entry.tags
        }
        return cls.template.render_block("entry", **vars)

    @classmethod
    def export_journal(cls, journal):
        """Returns a unicode representation of an entire journal."""
        vars = {
            'journal': journal,
            'entries': journal.entries,
            'tags': journal.tags
        }
        return cls.template.render_block("journal", **vars)


def __exporter_from_file(template_file):
    """Create a template class from a file"""
    name = os.path.basename(template_file).replace(".template", "")
    template = Template.from_file(template_file)
    return type(str("{}Exporter".format(name.title())), (GenericTemplateExporter, ), {
        "names": [name],
        "extension": template.extension,
        "template": template
    })

__all__ = []

# Factory pattern to create Exporter classes for all available templates
for template_file in glob("jrnl/templates/*.template"):
    __all__.append(__exporter_from_file(template_file))
