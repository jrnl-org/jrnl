#!/usr/bin/env python
# encoding: utf-8

import re
import textwrap

class Entry:
    def __init__(self, journal, date=None, title="", body=""):
        self.journal = journal # Reference to journal mainly to access it's config
        self.date = date
        self.title = title.strip()
        self.body = body.strip()
        self.tags = self.parse_tags()

    def parse_tags(self):
        fulltext = " ".join([self.title, self.body]).lower()
        tags = re.findall(r"([%s]\w+)" % self.journal.config['tagsymbols'], fulltext)
        self.tags = set(tags)

    def __str__(self):
        """Returns a string representation of the entry to be written into a journal file."""
        date_str = self.date.strftime(self.journal.config['timeformat'])
        title = date_str + " " + self.title
        body = self.body.strip()

        return "{title}{sep}{body}\n".format(
            title=title,
            sep="\n" if self.body else "",
            body=body
        )

    def pprint(self):
        """Returns a pretty-printed version of the entry."""
        date_str = self.date.strftime(self.journal.config['timeformat'])
        if self.journal.config['linewrap']:
            title = textwrap.fill(date_str + " " + self.title, self.journal.config['linewrap'])
            body = "\n".join([
                    textwrap.fill(line+" ", 
                        self.journal.config['linewrap'], 
                        initial_indent="| ", 
                        subsequent_indent="| ",
                        drop_whitespace=False)
                    for line in self.body.splitlines()
                ])
        else:
            title = date_str + " " + self.title
            body = self.body.strip()

        return "{title}{sep}{body}\n".format(
            title=title,
            sep="\n" if self.body else "",
            body=body
        )

    def __repr__(self):
        return str(self)

    def to_dict(self):
        return {
            'title': self.title.strip(),
            'body': self.body.strip(),
            'date': self.date.strftime("%Y-%m-%d"),
            'time': self.date.strftime("%H:%M")
        }

    def to_md(self):
        date_str = self.date.strftime(self.journal.config['timeformat'])
        body_wrapper = "\n\n" if self.body.strip() else ""
        body = body_wrapper + self.body.strip()
        space = "\n"
        md_head = "###"

        return "{md} {date}, {title} {body} {space}".format(
            md=md_head,
            date=date_str,
            title=self.title,
            body=body,
            space=space
        )