#!/usr/bin/env python
# encoding: utf-8


"""
jrnl is a simple journal application for your command line.
"""
from __future__ import absolute_import

__title__ = 'jrnl'
__version__ = '1.9.2'
__author__ = 'Manuel Ebert'
__license__ = 'MIT License'
__copyright__ = 'Copyright 2013 - 2014 Manuel Ebert'

from . import Journal
from . import cli
from .cli import run
