#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, unicode_literals
import os
import json
from .util import u, slugify
import codecs


def get_tags_count(journal):
    """Returns a set of tuples (count, tag) for all tags present in the journal."""
    # Astute reader: should the following line leave you as puzzled as me the first time
    # I came across this construction, worry not and embrace the ensuing moment of enlightment.
    tags = [tag
            for entry in journal.entries
            for tag in set(entry.tags)]
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
    result += "\n".join("{0:20} : {1}".format(tag, n) for n, tag in sorted(tag_counts, reverse=True))
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
    result = "\n".join(out)
    return result


def to_txt(journal):
    """Returns the complete text of the Journal."""
    return journal.pprint()


def to_html(journal):
    html = "<!DOCTYPE html>\n"
    html += "<html>\n"
    html += "\t<head>\n"
    html += "\t\t<style>\n"
    html += "\t\t\tp{margin:0;}\n"
    html += "\t\t\th2{margin:0}\n"
    html += "\t\t\tbody{\n"
    html += "\t\t\t\tbackground: #252a32;\n"
    html += "\t\t\t\tmargin-top:5%;\n"
    html += "\t\t\t\tmargin-bottom:5%;\n"
    html += "\t\t\t\tmargin-left:5%;\n"
    html += "\t\t\t\tmargin-right:5%;\n"
    html += "\t\t\t}\n"
    html += "\t\t</style>\n"
    html += "\t</head>\n\n"
    html += "\t<body>\n"
    html += "\t\t<font color=\"white\">\n"
    html += "\t\t\t<h1>Journal</h1>\n"
    html += "\t\t\t<br>\n"
    for element in journal.entries:
        # date time title body
        html += "\t\t\t\t<h2>" + str(element.date) + "\t" + element.title + "</h2>\n"
        html += "\t\t\t\t<p class=\"tab\">" + element.body + "</p>\n\t\t\t<br>\n\t\t\t<br>\n"
    html += "\t\t</font>\n"
    html += "\t</body>\n"
    html += "</html>"
    return html

def export(journal, format, output=None):
    """Exports the journal to various formats.
    format should be one of json, txt, text, md, markdown, html.
    If output is None, returns a unicode representation of the output.
    If output is a directory, exports entries into individual files.
    Otherwise, exports to the given output file.
    """
    maps = {
        "json": to_json,
        "txt": to_txt,
        "text": to_txt,
        "md": to_md,
        "markdown": to_md,
        "html": to_html
    }
    if format not in maps:
        return "[ERROR: can't export to '{0}'. Valid options are 'md', 'txt', 'html', and 'json']".format(format)
    if output and os.path.isdir(output):  # multiple files
        return write_files(journal, output, format)
    else:
        content = maps[format](journal)
        if output:
            try:
                with codecs.open(output, "w", "utf-8") as f:
                    f.write(content)
                return "[Journal exported to {0}]".format(output)
            except IOError as e:
                return "[ERROR: {0} {1}]".format(e.filename, e.strerror)
        else:
            return content


def write_files(journal, path, format):
    """Turns your journal into separate files for each entry.
    Format should be either json, md or txt."""
    make_filename = lambda entry: e.date.strftime("%Y-%m-%d_{0}.{1}".format(slugify(u(e.title)), format))
    for e in journal.entries:
        full_path = os.path.join(path, make_filename(e))
        if format == 'json':
            content = json.dumps(e.to_dict(), indent=2) + "\n"
        elif format in ('md', 'markdown'):
            content = e.to_md()
        elif format in ('txt', 'text'):
            content = e.__unicode__()
        elif format == 'html':
            content = e.to_html()
        with codecs.open(full_path, "w", "utf-8") as f:
            f.write(content)
    return "[Journal exported individual files in {0}]".format(path)
