#!/usr/bin/env python
# encoding: utf-8

import os

__title__ = "jrnl"
__version__ = "source"

version_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "VERSION.txt")
if os.path.exists(version_path):
    with open(version_path) as version_file:
        __version__ = version_file.read()
