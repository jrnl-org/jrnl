# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from jrnl.plugins.dates_exporter import DatesExporter
from jrnl.plugins.fancy_exporter import FancyExporter
from jrnl.plugins.jrnl_importer import JRNLImporter
from jrnl.plugins.json_exporter import JSONExporter
from jrnl.plugins.markdown_exporter import MarkdownExporter
from jrnl.plugins.tag_exporter import TagExporter
from jrnl.plugins.text_exporter import TextExporter
from jrnl.plugins.xml_exporter import XMLExporter
from jrnl.plugins.yaml_exporter import YAMLExporter

__exporters = [
    JSONExporter,
    MarkdownExporter,
    TagExporter,
    DatesExporter,
    TextExporter,
    XMLExporter,
    YAMLExporter,
    FancyExporter,
]
__importers = [JRNLImporter]

__exporter_types = {name: plugin for plugin in __exporters for name in plugin.names}
__exporter_types["pretty"] = None
__exporter_types["short"] = None
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
