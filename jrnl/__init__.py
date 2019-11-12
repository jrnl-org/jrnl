#!/usr/bin/env python

import pkg_resources

dist = pkg_resources.get_distribution('jrnl')
__title__ = dist.project_name
__version__ = dist.version

