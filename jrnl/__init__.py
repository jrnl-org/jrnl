#!/usr/bin/env python
# encoding: utf-8


"""
jrnl is a simple journal application for your command line.
"""

__title__ = 'jrnl'
__version__ = '1.7.5'
__author__ = 'Manuel Ebert'
__license__ = 'MIT License'
__copyright__ = 'Copyright 2013 - 2014 Manuel Ebert'

from . import Journal
from . import cli
from .cli import run
