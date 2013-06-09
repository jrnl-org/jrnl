#!/usr/bin/env python
# encoding: utf-8

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
    """Prints a list of all tags and the number of occurances."""
    tag_counts = get_tags_count(journal)
    result = ""
    if not tag_counts:
        return '[No tags found in journal.]'
    elif min(tag_counts)[0] == 0:
        tag_counts = filter(lambda x: x[0] > 1, tag_counts)
        result += '[Removed tags that appear only once.]\n'
    result += "\n".join("{0:20} : {1}".format(tag, n) for n, tag in sorted(tag_counts, reverse=False))
    return result

def to_json(journal):
    """Returns a JSON representation of the Journal."""
    tags = get_tags_count(journal)
    result = {
        "tags": dict((tag, count) for count, tag in tags),
        "entries": [e.to_dict() for e in journal.entries]
    }
    return json.dumps(result, indent=2)

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
