#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, unicode_literals, print_function

import sys
import re

from .text_exporter import TextExporter
from ..util import WARNING_COLOR, ERROR_COLOR, RESET_COLOR


class PrjctExporter(TextExporter):
    """This Exporter can convert entries and journals into Markdown formatted
    text with front matter usable by the Ablog extention for Sphinx."""
    names = ["prjct"]
    extension = "md"

    @classmethod
    def export_entry(cls, entry, to_multifile=True):
        """Returns a markdown representation of a single entry, with Ablog front matter."""
        if to_multifile is False:
            print("{}ERROR{}: Prjct export must be to individual files. Please \
                specify a directory to export to.".format(ERROR_COLOR, RESET_COLOR, file=sys.stderr))
            return

        date_str = entry.date.strftime(entry.journal.config['timeformat'])
        body_wrapper = "\n" if entry.body else ""
        body = body_wrapper + entry.body

        tagsymbols = entry.journal.config['tagsymbols']
        # see also Entry.Entry.rag_regex
        multi_tag_regex = re.compile(r'(?u)^\s*([{tags}][-+*#/\w]+\s*)+$'.format(tags=tagsymbols), re.UNICODE)

        newbody = ''
        for line in body.splitlines(True):
            if multi_tag_regex.match(line):
                """Tag only lines"""
                line = ''
            newbody = newbody + line

        # pass headings as is

        if len(entry.tags) > 0:
            tags_str = '   :tags: ' + ', '.join([tag[1:] for tag in entry.tags]) + '\n'
        else:
            tags_str = ''

        if hasattr(entry, 'location'):
            location_str = '   :location: {}\n'.format(entry.location.get('Locality', ''))
        else:
            location_str = ''

        # source directory is  entry.journal.config['journal']
        # output directory is...?

        return "# {title}\n\n```eval_rst\n.. post:: {date}\n{tags}{category}{author}{location}{language}```\n\n{body}{space}" \
            .format(
                date=date_str,
                title=entry.title,
                tags=tags_str,
                category="   :category: jrnl\n",
                author="",
                location=location_str,
                language="",
                body=newbody,
                space="\n"
            )

    @classmethod
    def export_journal(cls, journal):
        """Returns an error, as Prjct export requires a directory as a target."""
        print("{}ERROR{}: Prjct export must be to individual files. \
            Please specify a directory to export to.".format(ERROR_COLOR, RESET_COLOR), file=sys.stderr)
        return
