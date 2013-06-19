#!/usr/bin/env python
# encoding: utf-8
import sys

def py23_input(msg):
    if sys.version_info[0] == 3:
        try: return input(msg)
        except SyntaxError: return ""
    else:
        return raw_input(msg)
