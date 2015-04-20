#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, unicode_literals
import glob
import os
import importlib


class PluginMeta(type):

    def __init__(cls, name, bases, attrs):
        """Called when a Plugin derived class is imported"""
        if not hasattr(cls, 'PLUGINS'):
            cls.PLUGINS = []
            cls.PLUGIN_NAMES = []
        else:
            cls.__register_plugin(cls)

    def __register_plugin(cls, plugin):
        """Add the plugin to the plugin list and perform any registration logic"""
        cls.PLUGINS.append(plugin)
        cls.PLUGIN_NAMES.extend(plugin.names)

    def get_plugin_types_string(cls):
        plugin_names = sorted(cls.PLUGIN_NAMES)
        if not plugin_names:
            return "(nothing)"
        elif len(plugin_names) == 1:
            return plugin_names[0]
        elif len(plugin_names) == 2:
            return plugin_names[0] + " or " + plugin_names[1]
        else:
            return ', '.join(plugin_names[:-1]) + ", or " + plugin_names[-1]

# This looks a bit arcane, but is basically bilingual speak for defining a
# class with meta class 'PluginMeta' for both Python 2 and 3.
BaseExporter = PluginMeta(str('BaseExporter'), (), {'names': []})
BaseImporter = PluginMeta(str('BaseImporter'), (), {'names': []})


for module in glob.glob(os.path.dirname(__file__) + "/*.py"):
    importlib.import_module("." + os.path.basename(module)[:-3], "jrnl.plugins")
del module


def get_exporter(format):
    for exporter in BaseExporter.PLUGINS:
        if hasattr(exporter, "names") and format in exporter.names:
            return exporter
    return None


def get_importer(format):
    for importer in BaseImporter.PLUGINS:
        if hasattr(importer, "names") and format in importer.names:
            return importer
    return None
