#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import re
import textwrap
from datetime import datetime


class Entry:
    def __init__(self, journal, date=None, title="", body="", starred=False):
        self.journal = journal  # Reference to journal mainly to access it's config
        self.date = date or datetime.now()
        self.title = title.rstrip("\n ")
        self.body = body.rstrip("\n ")
        self.tags = self.parse_tags()
        self.starred = starred
        self.modified = False

    @staticmethod
    def tag_regex(tagsymbols):
        pattern = r'(?u)\s([{tags}][-+*#/\w]+)'.format(tags=tagsymbols)
        return re.compile( pattern, re.UNICODE )

    def parse_tags(self):
        fulltext =  " " + " ".join([self.title, self.body]).lower()
        tagsymbols = self.journal.config['tagsymbols']
        tags = re.findall( Entry.tag_regex(tagsymbols), fulltext )
        self.tags = tags
        return set(tags)

    def __unicode__(self):
        """Returns a string representation of the entry to be written into a journal file."""
        date_str = self.date.strftime(self.journal.config['timeformat'])
        title = date_str + " " + self.title.rstrip("\n ")
        if self.starred:
            title += " *"
        return "{title}{sep}{body}\n".format(
            title=title,
            sep="\n" if self.body.rstrip("\n ") else "",
            body=self.body.rstrip("\n ")
        )

    def pprint(self, short=False):
        """Returns a pretty-printed version of the entry.
        If short is true, only print the title."""
        date_str = self.date.strftime(self.journal.config['timeformat'])
        if not short and self.journal.config['linewrap']:
            title = textwrap.fill(date_str + " " + self.title, self.journal.config['linewrap'])
            body = "\n".join([
                    textwrap.fill((line + " ") if (len(line) == 0) else line,
                        self.journal.config['linewrap'],
                        initial_indent="| ",
                        subsequent_indent="| ",
                        drop_whitespace=False)
                    for line in self.body.rstrip(" \n").splitlines()
                ])
        else:
            title = date_str + " " + self.title.rstrip("\n ")
            body = self.body.rstrip("\n ")

        # Suppress bodies that are just blanks and new lines.
        has_body = len(self.body) > 20 or not all(char in (" ", "\n") for char in self.body)

        if short:
            return title
        else:
            return "{title}{sep}{body}\n".format(
                title=title,
                sep="\n" if has_body else "",
                body=body if has_body else "",
            )

    def __repr__(self):
        return "<Entry '{0}' on {1}>".format(self.title.strip(), self.date.strftime("%Y-%m-%d %H:%M"))

    def __eq__(self, other):
        if not isinstance(other, Entry) \
           or self.title.strip() != other.title.strip() \
           or self.body.rstrip() != other.body.rstrip() \
           or self.date != other.date \
           or self.starred != other.starred:
           return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def to_dict(self):
        return {
            'title': self.title,
            'body': self.body,
            'date': self.date.strftime("%Y-%m-%d"),
            'time': self.date.strftime("%H:%M"),
            'starred': self.starred
        }

    def to_md(self):
        date_str = self.date.strftime(self.journal.config['timeformat'])
        body_wrapper = "\n\n" if self.body else ""
        body = body_wrapper + self.body
        space = "\n"
        md_head = "###"

        return "{md} {date}, {title} {body} {space}".format(
            md=md_head,
            date=date_str,
            title=self.title,
            body=body,
            space=space
        )

    def to_html(self):
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
        # date time title body
        html +="\t\t\t\t<h2>" + self.date.strftime(self.journal.config['timeformat']) + "\t" + str(self.title) + "</h2>\n"
        html +="\t\t\t\t<p class=\"tab\">" + str(self.body) + "</p>\n\t\t\t<br>\n\t\t\t<br>\n"
        html +="\t\t</font>\n"
        html +="\t</body>\n"
        html +="</html>"
        return html
