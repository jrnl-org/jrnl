#!/usr/bin/env python
# encoding: utf-8
# Copyright (C) 2012-2021 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

"""
Code relating to the collecting of plugins and distributing calls to them.

In particular, the code here collects the list of imports and exporters, both
internal and external, and tells the main program which plugins are available.
Actual calling of the plugins is done directly and works because given plugin
functions are importable/callable at predetermined (code) locations.

Internal plugins are located in the `jrnl.plugins` namespace, and external
plugins are located in the `jrnl.contrib` namespace.

This file was originally called "meta", using that title in the reflexive sense;
i.e. it is the collection of code that allows plugins to deal with themselves.
"""

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
"""list of stings: all available export formats."""
IMPORT_FORMATS = sorted(__importer_types.keys())
"""list of stings: all available import formats."""


def get_exporter(format):
    """
    Given an export format, returns the (callable) class of the corresponding exporter.
    """
    try:
        return __exporter_types[format].Exporter
    except (AttributeError, KeyError):
        return None

def get_importer(format):
    """
    Given an import format, returns the (callable) class of the corresponding importer.
    """
    try:
        return __importer_types[format].Importer
    except (AttributeError, KeyError):
        return None
