#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import
import os
import json
from .util import u, slugify
import codecs
from xml.dom import minidom


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
    result += "\n".join(u"{0:20} : {1}".format(tag, n) for n, tag in sorted(tag_counts, reverse=True))
    return result


def entry_to_dict(entry):
    return {
        'title': entry.title,
        'body': entry.body,
        'date': entry.date.strftime("%Y-%m-%d"),
        'time': entry.date.strftime("%H:%M"),
        'starred': entry.starred
    }


def to_json(journal):
    """Returns a JSON representation of the Journal."""
    tags = get_tags_count(journal)
    result = {
        "tags": dict((tag, count) for count, tag in tags),
        "entries": [entry_to_dict(e) for e in journal.entries]
    }
    return json.dumps(result, indent=2)


def entry_to_xml(entry, doc=None):
    """Turns an entry into an XML representation.
    If doc is not given, it will return a full XML document.
    Otherwise, it will only return a new 'entry' elemtent for
    a given doc."""
    doc_el = doc or minidom.Document()
    entry_el = doc_el.createElement('entry')
    for key, value in entry_to_dict(entry).items():
        elem = doc_el.createElement(key)
        elem.appendChild(doc_el.createTextNode(u(value)))
        entry_el.appendChild(elem)
    if not doc:
        doc_el.appendChild(entry_el)
        return doc_el.toprettyxml()
    else:
        return entry_el


def to_xml(journal):
    """Returns a XML representation of the Journal."""
    tags = get_tags_count(journal)
    doc = minidom.Document()
    xml = doc.createElement('journal')
    tags_el = doc.createElement('tags')
    entries_el = doc.createElement('entries')
    for tag in tags:
        tag_el = doc.createElement('tag')
        tag_el.setAttribute('name', tag[1])
        count_node = doc.createTextNode(u(tag[0]))
        tag.appendChild(count_node)
        tags_el.appendChild(tag)
    for entry in journal.entries:
        entries_el.appendChild(entry_to_xml(entry, doc))
    xml.appendChild(entries_el)
    xml.appendChild(tags_el)
    doc.appendChild(xml)
    return doc.toprettyxml()


def entry_to_md(entry):
    date_str = entry.date.strftime(entry.journal.config['timeformat'])
    body_wrapper = "\n\n" if entry.body else ""
    body = body_wrapper + entry.body
    space = "\n"
    md_head = "###"

    return u"{md} {date}, {title} {body} {space}".format(
        md=md_head,
        date=date_str,
        title=entry.title,
        body=body,
        space=space
    )


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
        out.append(entry_to_md(e))
    result = "\n".join(out)
    return result


def to_txt(journal):
    """Returns the complete text of the Journal."""
    return journal.pprint()


def export(journal, format, output=None):
    """Exports the journal to various formats.
    format should be one of json, xml, txt, text, md, markdown.
    If output is None, returns a unicode representation of the output.
    If output is a directory, exports entries into individual files.
    Otherwise, exports to the given output file.
    """
    maps = {
        "json": to_json,
        "xml": to_xml,
        "txt": to_txt,
        "text": to_txt,
        "md": to_md,
        "markdown": to_md
    }
    if format not in maps:
        return u"[ERROR: can't export to '{0}'. Valid options are 'md', 'txt', 'xml', and 'json']".format(format)
    if output and os.path.isdir(output):  # multiple files
        return write_files(journal, output, format)
    else:
        content = maps[format](journal)
        if output:
            try:
                with codecs.open(output, "w", "utf-8") as f:
                    f.write(content)
                return u"[Journal exported to {0}]".format(output)
            except IOError as e:
                return u"[ERROR: {0} {1}]".format(e.filename, e.strerror)
        else:
            return content


def write_files(journal, path, format):
    """Turns your journal into separate files for each entry.
    Format should be either json, xml, md or txt."""
    make_filename = lambda entry: e.date.strftime("%C-%m-%d_{0}.{1}".format(slugify(u(e.title)), format))
    for e in journal.entries:
        full_path = os.path.join(path, make_filename(e))
        if format == 'json':
            content = json.dumps(entry_to_dict(e), indent=2) + "\n"
        elif format in ('md', 'markdown'):
            content = entry_to_md(e)
        elif format in 'xml':
            content = entry_to_xml(e)
        elif format in ('txt', 'text'):
            content = e.__unicode__()
        with codecs.open(full_path, "w", "utf-8") as f:
            f.write(content)
    return u"[Journal exported individual files in {0}]".format(path)
