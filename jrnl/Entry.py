#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import re
import textwrap
from datetime import datetime
from .util import split_title


class Entry:
    def __init__(self, journal, date=None, text="", starred=False):
        self.journal = journal  # Reference to journal mainly to access its config
        self.date = date or datetime.now()
        self.text = text
        self._title = self._body = self._tags = None
        self.starred = starred
        self.modified = False

    @property
    def fulltext(self):
        return self.title + " " + self.body

    def _parse_text(self):
        raw_text = self.text
        lines = raw_text.splitlines()
        if lines[0].strip().endswith("*"):
            self.starred = True
            raw_text = lines[0].strip("\n *") + "\n" + "\n".join(lines[1:])
        self._title, self._body = split_title(raw_text)
        if self._tags is None:
            self._tags = list(self._parse_tags())

    @property
    def title(self):
        if self._title is None:
            self._parse_text()
        return self._title

    @property
    def body(self):
        if self._body is None:
            self._parse_text()
        return self._body

    @property
    def tags(self):
        if self._tags is None:
            self._parse_text()
        return self._tags

    @staticmethod
    def tag_regex(tagsymbols):
        pattern = r'(?u)(?:^|\s)([{tags}][-+*#/\w]+)'.format(tags=tagsymbols)
        return re.compile(pattern, re.UNICODE)

    def _parse_tags(self):
        tagsymbols = self.journal.config['tagsymbols']
        return set(tag.lower() for tag in re.findall(Entry.tag_regex(tagsymbols), self.text))

    def __unicode__(self):
        """Returns a string representation of the entry to be written into a journal file."""
        date_str = self.date.strftime(self.journal.config['timeformat'])
        title = "[{}] {}".format(date_str, self.title.rstrip("\n "))
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
        if self.journal.config['indent_character']:
            indent = self.journal.config['indent_character'].rstrip() + " "
        else:
            indent = ""
        if not short and self.journal.config['linewrap']:
            title = textwrap.fill(date_str + " " + self.title, self.journal.config['linewrap'])
            body = "\n".join([
                textwrap.fill(
                    line,
                    self.journal.config['linewrap'],
                    initial_indent=indent,
                    subsequent_indent=indent,
                    drop_whitespace=True) or indent
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

    def __hash__(self):
        return hash(self.__repr__())

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
<<<<<<< HEAD
=======

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
>>>>>>> master
