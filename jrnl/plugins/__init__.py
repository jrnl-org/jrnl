#!/usr/bin/env python
# encoding: utf-8

from .text_exporter import TextExporter
from .jrnl_importer import JRNLImporter
from .json_exporter import JSONExporter
from .markdown_exporter import MarkdownExporter
from .tag_exporter import TagExporter
from .xml_exporter import XMLExporter
from .yaml_exporter import YAMLExporter
from .template_exporter import __all__ as template_exporters
from .fancy_exporter import FancyExporter

__exporters = [
    JSONExporter,
    MarkdownExporter,
    TagExporter,
    TextExporter,
    XMLExporter,
    YAMLExporter,
    FancyExporter,
] + template_exporters
__importers = [JRNLImporter]

__exporter_types = {name: plugin for plugin in __exporters for name in plugin.names}
__importer_types = {name: plugin for plugin in __importers for name in plugin.names}

EXPORT_FORMATS = sorted(__exporter_types.keys())
IMPORT_FORMATS = sorted(__importer_types.keys())


def get_exporter(format):
    for exporter in __exporters:
        if hasattr(exporter, "names") and format in exporter.names:
            return exporter
    return None


def get_importer(format):
    for importer in __importers:
        if hasattr(importer, "names") and format in importer.names:
            return importer
    return None
