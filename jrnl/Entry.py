# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import datetime
import logging
import os
import re

import ansiwrap

from .color import colorize
from .color import highlight_tags_with_background_color


class Entry:
    def __init__(self, journal, date=None, text="", starred=False):
        self.journal = journal  # Reference to journal mainly to access its config
        self.date = date or datetime.datetime.now()
        self.text = text
        self._title = None
        self._body = None
        self._tags = None
        self.starred = starred
        self.modified = False

    @property
    def fulltext(self):
        return self.title + " " + self.body

    def _parse_text(self):
        raw_text = self.text
        lines = raw_text.splitlines()
        if lines and lines[0].strip().endswith("*"):
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

    @title.setter
    def title(self, x):
        self._title = x

    @property
    def body(self):
        if self._body is None:
            self._parse_text()
        return self._body

    @body.setter
    def body(self, x):
        self._body = x

    @property
    def tags(self):
        if self._tags is None:
            self._parse_text()
        return self._tags

    @tags.setter
    def tags(self, x):
        self._tags = x

    @staticmethod
    def tag_regex(tagsymbols):
        pattern = rf"(?<!\S)([{tagsymbols}][-+*#/\w]+)"
        return re.compile(pattern)

    def _parse_tags(self):
        tagsymbols = self.journal.config["tagsymbols"]
        return {
            tag.lower() for tag in re.findall(Entry.tag_regex(tagsymbols), self.text)
        }

    def __str__(self):
        """Returns a string representation of the entry to be written into a journal file."""
        date_str = self.date.strftime(self.journal.config["timeformat"])
        title = "[{}] {}".format(date_str, self.title.rstrip("\n "))
        if self.starred:
            title += " *"
        return "{title}{sep}{body}\n".format(
            title=title,
            sep="\n" if self.body.rstrip("\n ") else "",
            body=self.body.rstrip("\n "),
        )

    def pprint(self, short=False):
        """Returns a pretty-printed version of the entry.
        If short is true, only print the title."""
        # Handle indentation
        if self.journal.config["indent_character"]:
            indent = self.journal.config["indent_character"].rstrip() + " "
        else:
            indent = ""

        date_str = colorize(
            self.date.strftime(self.journal.config["timeformat"]),
            self.journal.config["colors"]["date"],
            bold=True,
        )

        if not short and self.journal.config["linewrap"]:
            columns = self.journal.config["linewrap"]

            if columns == "auto":
                try:
                    columns = os.get_terminal_size().columns
                except OSError:
                    logging.debug(
                        "Can't determine terminal size automatically 'linewrap': '%s'",
                        self.journal.config["linewrap"],
                    )
                    columns = 79

            # Color date / title and bold title
            title = ansiwrap.fill(
                date_str
                + " "
                + highlight_tags_with_background_color(
                    self,
                    self.title,
                    self.journal.config["colors"]["title"],
                    is_title=True,
                ),
                columns,
            )
            body = highlight_tags_with_background_color(
                self, self.body.rstrip(" \n"), self.journal.config["colors"]["body"]
            )
            body_text = [
                colorize(
                    ansiwrap.fill(
                        line,
                        columns,
                        initial_indent=indent,
                        subsequent_indent=indent,
                        drop_whitespace=True,
                    ),
                    self.journal.config["colors"]["body"],
                )
                or indent
                for line in body.rstrip(" \n").splitlines()
            ]

            # ansiwrap doesn't handle lines with only the "\n" character and some
            # ANSI escapes properly, so we have this hack here to make sure the
            # beginning of each line has the indent character and it's colored
            # properly. textwrap doesn't have this issue, however, it doesn't wrap
            # the strings properly as it counts ANSI escapes as literal characters.
            # TL;DR: I'm sorry.
            body = "\n".join(
                [
                    colorize(indent, self.journal.config["colors"]["body"]) + line
                    if not ansiwrap.strip_color(line).startswith(indent)
                    else line
                    for line in body_text
                ]
            )
        else:
            title = (
                date_str
                + " "
                + highlight_tags_with_background_color(
                    self,
                    self.title.rstrip("\n"),
                    self.journal.config["colors"]["title"],
                    is_title=True,
                )
            )
            body = highlight_tags_with_background_color(
                self, self.body.rstrip("\n "), self.journal.config["colors"]["body"]
            )

        # Suppress bodies that are just blanks and new lines.
        has_body = len(self.body) > 20 or not all(
            char in (" ", "\n") for char in self.body
        )

        if short:
            return title
        else:
            return "{title}{sep}{body}\n".format(
                title=title, sep="\n" if has_body else "", body=body if has_body else ""
            )

    def __repr__(self):
        return "<Entry '{}' on {}>".format(
            self.title.strip(), self.date.strftime("%Y-%m-%d %H:%M")
        )

    def __hash__(self):
        return hash(self.__repr__())

    def __eq__(self, other):
        if (
            not isinstance(other, Entry)
            or self.title.strip() != other.title.strip()
            or self.body.rstrip() != other.body.rstrip()
            or self.date != other.date
            or self.starred != other.starred
        ):
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)


# Based on Segtok by Florian Leitner
# https://github.com/fnl/segtok
SENTENCE_SPLITTER = re.compile(
    r"""
    (
    [.!?\u2026\u203C\u203D\u2047\u2048\u2049\u22EF\uFE52\uFE57] # Sequence starting with a sentence terminal,
    [\'\u2019\"\u201D]? # an optional right quote,
    [\]\)]*             # optional closing bracket
    \s+                 # AND a sequence of required spaces.
    )
    |[\uFF01\uFF0E\uFF1F\uFF61\u3002] # CJK full/half width terminals usually do not have following spaces.
    """,
    re.VERBOSE,
)

SENTENCE_SPLITTER_ONLY_NEWLINE = re.compile("\n")


def split_title(text):
    """Splits the first sentence off from a text."""
    sep = SENTENCE_SPLITTER_ONLY_NEWLINE.search(text.lstrip())
    if not sep:
        sep = SENTENCE_SPLITTER.search(text)
        if not sep:
            return text, ""
    return text[: sep.end()].strip(), text[sep.end() :].strip()
