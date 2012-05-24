#!/usr/bin/env python
# encoding: utf-8

import re

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
        date_str = self.date.strftime(self.journal.config['timeformat'])
        body_wrapper = "\n" if self.body else ""
        body = body_wrapper + self.body.strip()
        space = "\n"

        return "%(date)s %(title)s %(body)s %(space)s" % {
            'date': date_str,
            'title': self.title,
            'body': body,
            'space': space
        }

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

        return "%(md)s %(date)s, %(title)s %(body)s %(space)s" % {
            'md': md_head,
            'date': date_str,
            'title': self.title,
            'body': body,
            'space': space
        }