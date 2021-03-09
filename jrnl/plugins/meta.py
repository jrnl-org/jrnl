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
__importer_types = {
    **__importer_types_builtin,
    **__importer_types_contrib,
}

EXPORT_FORMATS = sorted(__exporter_types.keys())
IMPORT_FORMATS = sorted(__importer_types.keys())


def get_exporter(format):
    # print('get_exporter')
    # print(__exporter_types)
    for exporter_name, exporter_class in __exporter_types.items():
        # print(exporter_class, exporter_class.Exporter.names)
        if (
            hasattr(exporter_class, "Exporter")
            and hasattr(exporter_class.Exporter, "names")
            and format in exporter_class.Exporter.names
        ):
            return exporter_class.Exporter
    return None


def get_importer(format):
    for importer_name, importer_class in __importer_types.items():
        if (
            hasattr(importer_class, "Importer")
            and hasattr(importer_class.Importer, "names")
            and format in importer_class.Importer.names
        ):
            return importer_class.Importer
    return None
