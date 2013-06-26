#!/usr/bin/env python
# encoding: utf-8

import os
import string
try: from slugify import slugify
except ImportError: import slugify
try: import simplejson as json
except ImportError: import json

def get_tags_count(journal):
    """Returns a set of tuples (count, tag) for all tags present in the journal."""
    # Astute reader: should the following line leave you as puzzled as me the first time
    # I came across this construction, worry not and embrace the ensuing moment of enlightment.
    tags = [tag
        for entry in journal.entries
        for tag in set(entry.tags)
    ]
    # To be read: [for entry in journal.entries: for tag in set(entry.tags): tag]
    tag_counts = set([(tags.count(tag), tag) for tag in tags])
    return tag_counts

def to_tag_list(journal):
    """Prints a list of all tags and the number of occurrences."""
    tag_counts = get_tags_count(journal)
    result = ""
    if not tag_counts:
        return '[No tags found in journal.]'
    elif min(tag_counts)[0] == 0:
        tag_counts = filter(lambda x: x[0] > 1, tag_counts)
        result += '[Removed tags that appear only once.]\n'
    result += "\n".join(u"{0:20} : {1}".format(tag, n) for n, tag in sorted(tag_counts, reverse=False))
    return result

def to_json(journal, output):
    """Returns a JSON representation of the Journal."""
    tags = get_tags_count(journal)
    result = {
        "tags": dict((tag, count) for count, tag in tags),
        "entries": [e.to_dict() for e in journal.entries]
    }
    if output is not False:
        path = output_path('json', output)
        if not is_globable(path):
            message = write_file(json.dumps(result, indent=2), path)
        else:
            message = to_files(journal, path)
        return message
    else:
        return json.dumps(result, indent=2)

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
        path = output_path('md', output)
        if not is_globable(path):
            message = write_file(result, path)
        else:
            message = to_files(journal, path)
        return message
    else:
        return result

def to_txt(journal, output):
    """Returns the complete text of the Journal."""
    if output is not False:
        path = output_path('txt', output)
        if not is_globable(path):
            message = write_file(unicode(journal), path)
        else:
            message = to_files(journal, path)
        return message
    else:
        return unicode(journal)

def to_files(journal, output):
    """Turns your journal into separate files for each entry."""
    path, extension = os.path.splitext(os.path.expanduser(output))

    for e in journal.entries:
        content = ""
        date = e.date.strftime('%C-%m-%d')
        title = slugify(unicode(e.title))

        filename = string.replace(path, "%C-%m-%d", date)
        filename = string.replace(filename, "slug", title)

        fullpath = filename + extension

        if extension == '.json':
            content = json.dumps(e.to_dict(), indent=2)
        elif extension == '.md':
            content = e.to_md()
        elif extension == '.txt':
            content = unicode(e)
        write_file(content, fullpath)

    return ("Journal exported.")

def is_globable(output):
    path, extension = os.path.splitext(os.path.expanduser(output))
    head, tail = os.path.split(path)

    if tail == "%C-%m-%d_slug":
        return True
    else:
        return False

def output_path(file_ext, output):
    path, extension = os.path.splitext(os.path.expanduser(output))

    head, tail = os.path.split(path)
    if head != '':
        if not os.path.exists(head): # if the folder doesn't exist, create it
            os.makedirs(head)
        fullpath = head + '/' + tail + '.' + file_ext
    else:
        fullpath = tail + '.' + file_ext

    return fullpath

def write_file(content, path):
    """Writes content to the file provided"""

    f = open(path, 'w+')
    f.write(content)
    f.close()

    return ("File exported to " + path)
