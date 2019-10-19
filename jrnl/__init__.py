#!/usr/bin/env python
# encoding: utf-8

import pkg_resources

dist = pkg_resources.get_distribution('jrnl')
__title__ = dist.project_name
__version__ = dist.version

