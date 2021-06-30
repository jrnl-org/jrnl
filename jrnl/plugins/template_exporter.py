# encoding: utf-8
# Copyright (C) 2012-2021 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from glob import glob
import os

from .template import Template
from .text_exporter import TextExporter


class GenericTemplateExporter(TextExporter):
    """This Exporter can convert entries and journals into text files."""

    @classmethod
    def export_entry(cls, entry):
        """Returns a string representation of a single entry."""
        vars = {"entry": entry, "tags": entry.tags}
        return cls.template.render_block("entry", **vars)

    @classmethod
    def export_journal(cls, journal):
        """Returns a string representation of an entire journal."""
        vars = {"journal": journal, "entries": journal.entries, "tags": journal.tags}
        return cls.template.render_block("journal", **vars)


def __exporter_from_file(template_file):
    """Create a template class from a file"""
    name = os.path.basename(template_file).replace(".template", "")
    template = Template.from_file(template_file)
    return type(
        str(f"{name.title()}Exporter"),
        (GenericTemplateExporter,),
        {"names": [name], "extension": template.extension, "template": template},
    )


__all__ = []

# Factory pattern to create Exporter classes for all available templates
for template_file in glob("jrnl/templates/*.template"):
    __all__.append(__exporter_from_file(template_file))
