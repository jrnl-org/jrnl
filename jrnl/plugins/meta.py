#!/usr/bin/env python
# encoding: utf-8

import importlib
import pkgutil

import jrnl.contrib.exporter
import jrnl.contrib.importer
import jrnl.plugins.exporter
import jrnl.plugins.importer

__exporters_builtin = list(
    pkgutil.iter_modules(
        jrnl.plugins.exporter.__path__, jrnl.plugins.exporter.__name__ + "."
    )
)
__exporters_contrib = list(
    pkgutil.iter_modules(
        jrnl.contrib.exporter.__path__, jrnl.contrib.exporter.__name__ + "."
    )
)

__importers_builtin = list(
    pkgutil.iter_modules(
        jrnl.plugins.importer.__path__, jrnl.plugins.importer.__name__ + "."
    )
)
__importers_contrib = list(
    pkgutil.iter_modules(
        jrnl.contrib.importer.__path__, jrnl.contrib.importer.__name__ + "."
    )
)

__exporter_types_builtin = {
    name: importlib.import_module(plugin.name)
    for plugin in __exporters_builtin
    for name in importlib.import_module(plugin.name).Exporter.names
}
__exporter_types_contrib = {
    name: importlib.import_module(plugin.name)
    for plugin in __exporters_contrib
    for name in importlib.import_module(plugin.name).Exporter.names
}


__importer_types_builtin = {
    name: importlib.import_module(plugin.name)
    for plugin in __importers_builtin
    for name in importlib.import_module(plugin.name).Importer.names
}
__importer_types_contrib = {
    name: importlib.import_module(plugin.name)
    for plugin in __importers_contrib
    for name in importlib.import_module(plugin.name).Importer.names
}

__exporter_types = {
    **__exporter_types_builtin,
    **__exporter_types_contrib,
}
__importer_types = {**__importer_types_builtin, **__importer_types_contrib}

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
