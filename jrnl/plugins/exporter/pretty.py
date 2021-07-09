#!/usr/bin/env python
# encoding: utf-8
# Copyright (C) 2012-2021 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from jrnl import __version__
from jrnl.plugins.base import BaseExporter


class Exporter(BaseExporter):
    """Pretty print journal"""

    names = ["pretty", "default"]
    extension = "txt"
    version = __version__

    @classmethod
    def export_journal(cls, journal):
        return journal.pprint()
