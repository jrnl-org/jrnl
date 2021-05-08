import codecs

from jrnl.plugins.base import BaseExporter

__version__ = "1.0.0"

class Exporter(BaseExporter):
    names = ["rot13"]
    extension = "txt"
    version = __version__

    @classmethod
    def export_entry(cls, entry):
        return codecs.encode(str(entry), "rot_13")
