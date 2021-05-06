#!/usr/bin/env python 
# encoding: utf-8
# Copyright (C) 2012-2021 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

"""
Exporter for testing and experimentation purposes 
"""

from jrnl import __version__
from jrnl.plugins.base import BaseExporter

class Exporter(BaseExporter):
    names=["testing","test"]
    version= 'v0.0.1'