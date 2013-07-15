#!/usr/bin/env python
# encoding: utf-8
import sys
import os
from tzlocal import get_localzone

def py23_input(msg):
    if sys.version_info[0] == 3:
        try: return input(msg)
        except SyntaxError: return ""
    else:
        return raw_input(msg)

def get_local_timezone():
    """Returns the Olson identifier of the local timezone.
    In a happy world, tzlocal.get_localzone would do this, but there's a bug on OS X
    that prevents that right now: https://github.com/regebro/tzlocal/issues/6"""
    if "darwin" in sys.platform:
        return os.popen("systemsetup -gettimezone").read().replace("Time Zone: ", "").strip()
    else:
        return str(get_localzone())
