#!/usr/bin/env python
# encoding: utf-8

import re
import os
try: from slugify import slugify
except ImportError: import slugify
try: import simplejson as json
except ImportError: import json

def to_json(journal, output):
    """Returns a JSON representation of the Journal."""
    result = json.dumps([e.to_dict() for e in journal.entries], indent=2)
    if output is not False:
        write_file(result, output)
    return result

def to_md(journal, output):
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
    result = "\n".join(out)
    if output is not False:
        write_file(result, output)
    return result

def to_txt(journal, output):
    """Returns the complete text of the Journal."""
    if output is not False:
        write_file(str(journal), output)
    return journal

def to_files(journal, output):
    """Turns your journal into separate files for each entry."""
    if output is False:
        output = os.path.expanduser('~/journal/*.txt') # default path
    path, extension = os.path.splitext(os.path.expanduser(output))
    head, tail = os.path.split(path)
    if tail == '*': # if wildcard is specified
        path = head + '/'
    if not os.path.exists(path): # if the folder doesn't exist, create it
        os.makedirs(path)
    for e in journal.entries:
        date = e.date.strftime('%Y-%m-%d')
        title = slugify(e.title)
        filename = date + '-' + title
        result = str(e)
        fullpath = path + filename + extension
        print fullpath
        write_file(result, fullpath)
    return ("Journal exported to '" + path + "'")

def write_file(content, path):
    """Writes content to the file provided"""
    f = open(path, 'w+')
    f.write(content)
    f.close()
