#!/usr/bin/env python
# encoding: utf-8

import re
import textwrap
from datetime import datetime

class Entry:
    def __init__(self, journal, date=None, title="", body="", starred=False):
        self.journal = journal # Reference to journal mainly to access it's config
        self.date = date or datetime.now()
        self.title = title.strip()
        self.body = body.strip()
        self.tags = self.parse_tags()
        self.starred = starred

    def parse_tags(self):
        fulltext = " ".join([self.title, self.body]).lower()
        tags = re.findall(r'(?u)([{tags}]\w+)'.format(tags=self.journal.config['tagsymbols']), fulltext, re.UNICODE)
        self.tags = tags
        return set(tags)

    def __unicode__(self):
        """Returns a string representation of the entry to be written into a journal file."""
        date_str = self.date.strftime(self.journal.config['timeformat'])
        title = date_str + " " + self.title
        if self.starred:
            title += " *"
        body = self.body.strip()

        return u"{title}{sep}{body}\n".format(
            title=title,
            sep="\n" if self.body else "",
            body=body
        )

    def pprint(self, short=False):
        """Returns a pretty-printed version of the entry.
        If short is true, only print the title."""
        date_str = self.date.strftime(self.journal.config['timeformat'])
        if not short and self.journal.config['linewrap']:
            title = textwrap.fill(date_str + " " + self.title, self.journal.config['linewrap'])
            body = "\n".join([
                    textwrap.fill(line+" ",
                        self.journal.config['linewrap'],
                        initial_indent="| ",
                        subsequent_indent="| ",
                        drop_whitespace=False).replace('  ', ' ')
                    for line in self.body.strip().splitlines()
                ])
        else:
            title = date_str + " " + self.title
            body = self.body.strip()

        # Suppress bodies that are just blanks and new lines.
        has_body = len(self.body) > 20 or not all(char in (" ", "\n") for char in self.body)

        if short:
            return title
        else:
            return u"{title}{sep}{body}\n".format(
                title=title,
                sep="\n" if has_body else "",
                body=body if has_body else "",
            )

    def __repr__(self):
        return "<Entry '{0}' on {1}>".format(self.title.strip(), self.date.strftime("%Y-%m-%d %H:%M"))

    def to_dict(self):
        return {
            'title': self.title.strip(),
            'body': self.body.strip(),
            'date': self.date.strftime("%Y-%m-%d"),
            'time': self.date.strftime("%H:%M"),
            'starred': self.starred
        }

    def to_md(self):
        date_str = self.date.strftime(self.journal.config['timeformat'])
        body_wrapper = "\n\n" if self.body.strip() else ""
        body = body_wrapper + self.body.strip()
        space = "\n"
        md_head = "###"

        return u"{md} {date}, {title} {body} {space}".format(
            md=md_head,
            date=date_str,
            title=self.title,
            body=body,
            space=space
        )
