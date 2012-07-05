#!/usr/bin/env python
# encoding: utf-8

try: import simplejson as json
except ImportError: import json

def to_json(journal):
    """Returns a JSON representation of the Journal."""
    return json.dumps([e.to_dict() for e in journal.entries], indent=2)

def to_md(journal):
    """Returns a markdown representation of the Journal"""
    out = []
    year, month = -1, -1
    for e in journal.entries:
        if not e.date.year == year:
            year = e.date.year
            out.append(str(year))
            out.append("=" * len(str(year)) + "\n")
        if not e.date.month == month:
            month = e.date.month
            out.append(e.date.strftime("%B"))
            out.append('-' * len(e.date.strftime("%B")) + "\n")
        out.append(e.to_md())
    return "\n".join(out)
