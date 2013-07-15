#!/usr/bin/env python
# encoding: utf-8
import sys
import os
from tzlocal import get_localzone

__cached_tz = None

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
    global __cached_tz
    if not __cached_tz and "darwin" in sys.platform:
        __cached_tz = os.popen("systemsetup -gettimezone").read().replace("Time Zone: ", "").strip()
    elif not __cached_tz:
        __cached_tz = str(get_localzone())
    return __cached_tz
