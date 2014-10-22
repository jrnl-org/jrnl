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
        if not cls.PLUGIN_NAMES:
            return "(nothing)"
        elif len(cls.PLUGIN_NAMES) == 1:
            return cls.PLUGIN_NAMES[0]
        elif len(cls.PLUGIN_NAMES) == 2:
            return cls.PLUGIN_NAMES[0] + " or " + cls.PLUGIN_NAMES[1]
        else:
            return ', '.join(cls.PLUGIN_NAMES[:-1]) + ", or " + cls.PLUGIN_NAMES[-1]


class BaseExporter(object):
    __metaclass__ = PluginMeta
    names = []


class BaseImporter(object):
    __metaclass__ = PluginMeta
    names = []


for module in glob.glob(os.path.dirname(__file__) + "/*.py"):
    importlib.import_module("." + os.path.basename(module)[:-3], "jrnl.plugins")
del module


def get_exporter(format):
    for exporter in BaseExporter.PLUGINS:
        if hasattr(exporter, "names") and format in exporter.names:
            return exporter
    return None
