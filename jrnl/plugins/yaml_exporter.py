#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, unicode_literals, print_function
from .text_exporter import TextExporter
import re
import sys


class YAMLExporter(TextExporter):
    """This Exporter can convert entries and journals into Markdown with YAML front matter."""
    names = ["yaml"]
    extension = "md"

    @classmethod
    def export_entry(cls, entry, to_multifile=True):
        """Returns a markdown representation of a single entry, with YAML front matter."""
        if to_multifile is False:
            print("{}ERROR{}: YAML export must be to individual files. Please specify a directory to export to.".format("\033[31m", "\033[0m", file=sys.stderr))
            return

        date_str = entry.date.strftime(entry.journal.config['timeformat'])
        body_wrapper = "\n" if entry.body else ""
        body = body_wrapper + entry.body

        tagsymbols = entry.journal.config['tagsymbols']
        # see also Entry.Entry.rag_regex
        multi_tag_regex = re.compile(r'(?u)^\s*([{tags}][-+*#/\w]+\s*)+$'.format(tags=tagsymbols), re.UNICODE)

        '''Increase heading levels in body text'''
        newbody = ''
        heading = '#'
        previous_line = ''
        warn_on_heading_level = False
        for line in entry.body.splitlines(True):
            if re.match(r"#+ ", line):
                """ATX style headings"""
                newbody = newbody + previous_line + heading + line
                if re.match(r"#######+ ", heading + line):
                    warn_on_heading_level = True
                line = ''
            elif re.match(r"=+$", line) and not re.match(r"^$", previous_line):
                """Setext style H1"""
                newbody = newbody + heading + "# " + previous_line
                line = ''
            elif re.match(r"-+$", line) and not re.match(r"^$", previous_line):
                """Setext style H2"""
                newbody = newbody + heading + "## " + previous_line
                line = ''
            elif multi_tag_regex.match(line):
                """Tag only lines"""
                line = ''
            else:
                newbody = newbody + previous_line
            previous_line = line
        newbody = newbody + previous_line   # add very last line

        if warn_on_heading_level is True:
            print("{}WARNING{}: Headings increased past H6 on export - {} {}".format("\033[33m", "\033[0m", date_str, entry.title), file=sys.stderr)

        return "title: {title}\ndate: {date}\nstared: {stared}\ntags: {tags}\n{body} {space}".format(
            date=date_str,
            title=entry.title,
            stared=entry.starred,
            tags=', '.join([tag[1:] for tag in entry.tags]),
            body=newbody,
            space=""
        )

    @classmethod
    def export_journal(cls, journal):
        """Returns an error, as YAML export requires a directory as a target."""
        print("{}ERROR{}: YAML export must be to individual files. Please specify a directory to export to.".format("\033[31m", "\033[0m", file=sys.stderr))
        return
