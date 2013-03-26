#!/usr/bin/env python
# encoding: utf-8

import re
import os
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

def to_files(journal, directory, extension):
    """Turns your journal into separate files for each entry."""
    if extension:
        ext = "." + extension
    else:
        ext = ''

    if not os.path.exists(directory):
        os.makedirs(directory)

    for e in journal.entries:
        date = e.date.strftime('%Y-%m-%d')
        title = re.sub('[^\w-]', '', re.sub(' ', '-', e.title.lower()))
        filename = date + '-' + title + ext
        f = open(directory + "/" + filename, 'w+')
        if extension == 'md':
            f.write(str(e.to_md()))
        else:
            f.write(str(e))
        f.close()
    return ("Journal exported to directory '" + directory + "' as <filename>" + ext)
