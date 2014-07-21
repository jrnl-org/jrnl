#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import
from . import Entry
from . import util
from . import time
import codecs
import re
from datetime import datetime
import sys
try:
    from Crypto.Cipher import AES
    from Crypto import Random
    crypto_installed = True
except ImportError:
    crypto_installed = False
import hashlib


class Journal(object):
    def __init__(self, name='default', **kwargs):
        self.config = {
            'journal': "journal.txt",
            'encrypt': False,
            'default_hour': 9,
            'default_minute': 0,
            'timeformat': "%Y-%m-%d %H:%M",
            'tagsymbols': '@',
            'highlight': True,
            'linewrap': 80,
        }
        self.config.update(kwargs)
        # Set up date parser
        self.key = None  # used to decrypt and encrypt the journal
        self.search_tags = None  # Store tags we're highlighting
        self.name = name

        self.open()

    def __len__(self):
        """Returns the number of entries"""
        return len(self.entries)

    def _decrypt(self, cipher):
        """Decrypts a cipher string using self.key as the key and the first 16 byte of the cipher as the IV"""
        if not crypto_installed:
            sys.exit("Error: PyCrypto is not installed.")
        if not cipher:
            return ""
        crypto = AES.new(self.key, AES.MODE_CBC, cipher[:16])
        try:
            plain = crypto.decrypt(cipher[16:])
        except ValueError:
            util.prompt("ERROR: Your journal file seems to be corrupted. You do have a backup, don't you?")
            sys.exit(1)

        padding_length = util.byte2int(plain[-1])
        if padding_length > AES.block_size and padding_length != 32:
            # 32 is the space character and is kept for backwards compatibility
            return None
        elif padding_length == 32:
            plain = plain.strip()
        elif plain[-padding_length:] != util.int2byte(padding_length) * padding_length:
            # Invalid padding!
            return None
        else:
            plain = plain[:-padding_length]
        return plain.decode("utf-8")

    def _encrypt(self, plain):
        """Encrypt a plaintext string using self.key as the key"""
        if not crypto_installed:
            sys.exit("Error: PyCrypto is not installed.")
        Random.atfork()  # A seed for PyCrypto
        iv = Random.new().read(AES.block_size)
        crypto = AES.new(self.key, AES.MODE_CBC, iv)
        plain = plain.encode("utf-8")
        padding_length = AES.block_size - len(plain) % AES.block_size
        plain += util.int2byte(padding_length) * padding_length
        return iv + crypto.encrypt(plain)

    def make_key(self, password):
        """Creates an encryption key from the default password or prompts for a new password."""
        self.key = hashlib.sha256(password.encode("utf-8")).digest()

    def open(self, filename=None):
        """Opens the journal file defined in the config and parses it into a list of Entries.
        Entries have the form (date, title, body)."""
        filename = filename or self.config['journal']

        if self.config['encrypt']:
            with open(filename, "rb") as f:
                journal_encrypted = f.read()

            def validate_password(password):
                self.make_key(password)
                return self._decrypt(journal_encrypted)

            # Soft-deprecated:
            journal = None
            if 'password' in self.config:
                journal = validate_password(self.config['password'])
            if journal is None:
                journal = util.get_password(keychain=self.name, validator=validate_password)
        else:
            with codecs.open(filename, "r", "utf-8") as f:
                journal = f.read()
        self.entries = self._parse(journal)
        self.sort()

    def _parse(self, journal_txt):
        """Parses a journal that's stored in a string and returns a list of entries"""

        # Entries start with a line that looks like 'date title' - let's figure out how
        # long the date will be by constructing one
        date_length = len(datetime.today().strftime(self.config['timeformat']))

        # Initialise our current entry
        entries = []
        current_entry = None

        for line in journal_txt.splitlines():
            line = line.rstrip()
            try:
                # try to parse line as date => new entry begins
                new_date = datetime.strptime(line[:date_length], self.config['timeformat'])

                # parsing successful => save old entry and create new one
                if new_date and current_entry:
                    entries.append(current_entry)

                if line.endswith("*"):
                    starred = True
                    line = line[:-1]
                else:
                    starred = False

                current_entry = Entry.Entry(self, date=new_date, title=line[date_length+1:], starred=starred)
            except ValueError:
                # Happens when we can't parse the start of the line as an date.
                # In this case, just append line to our body.
                if current_entry:
                    current_entry.body += line + "\n"

        # Append last entry
        if current_entry:
            entries.append(current_entry)
        for entry in entries:
            entry.parse_tags()
        return entries

    def __unicode__(self):
        return self.pprint()

    def pprint(self, short=False):
        """Prettyprints the journal's entries"""
        sep = "\n"
        pp = sep.join([e.pprint(short=short) for e in self.entries])
        if self.config['highlight']:  # highlight tags
            if self.search_tags:
                for tag in self.search_tags:
                    tagre = re.compile(re.escape(tag), re.IGNORECASE)
                    pp = re.sub(tagre,
                                lambda match: util.colorize(match.group(0)),
                                pp, re.UNICODE)
            else:
                pp = re.sub(r"(?u)([{tags}]\w+)".format(tags=self.config['tagsymbols']),
                            lambda match: util.colorize(match.group(0)),
                            pp)
        return pp

    def __repr__(self):
        return "<Journal with {0} entries>".format(len(self.entries))

    def write(self, filename=None):
        """Dumps the journal into the config file, overwriting it"""
        filename = filename or self.config['journal']
        journal = u"\n".join([e.__unicode__() for e in self.entries])
        if self.config['encrypt']:
            journal = self._encrypt(journal)
            with open(filename, 'wb') as journal_file:
                journal_file.write(journal)
        else:
            with codecs.open(filename, 'w', "utf-8") as journal_file:
                journal_file.write(journal)

    def sort(self):
        """Sorts the Journal's entries by date"""
        self.entries = sorted(self.entries, key=lambda entry: entry.date)

    def limit(self, n=None):
        """Removes all but the last n entries"""
        if n:
            self.entries = self.entries[-n:]

    def filter(self, tags=[], start_date=None, end_date=None, starred=False, strict=False, short=False):
        """Removes all entries from the journal that don't match the filter.

        tags is a list of tags, each being a string that starts with one of the
        tag symbols defined in the config, e.g. ["@John", "#WorldDomination"].

        start_date and end_date define a timespan by which to filter.

        starred limits journal to starred entries

        If strict is True, all tags must be present in an entry. If false, the
        entry is kept if any tag is present."""
        self.search_tags = set([tag.lower() for tag in tags])
        end_date = time.parse(end_date, inclusive=True)
        start_date = time.parse(start_date)

        # If strict mode is on, all tags have to be present in entry
        tagged = self.search_tags.issubset if strict else self.search_tags.intersection
        result = [
            entry for entry in self.entries
            if (not tags or tagged(entry.tags))
            and (not starred or entry.starred)
            and (not start_date or entry.date >= start_date)
            and (not end_date or entry.date <= end_date)
        ]
        if short:
            if tags:
                for e in self.entries:
                    res = []
                    for tag in tags:
                        matches = [m for m in re.finditer(tag, e.body)]
                        for m in matches:
                            date = e.date.strftime(self.config['timeformat'])
                            excerpt = e.body[m.start():min(len(e.body), m.end()+60)]
                            res.append('{0} {1} ..'.format(date, excerpt))
                    e.body = "\n".join(res)
            else:
                for e in self.entries:
                    e.body = ''
        self.entries = result

    def new_entry(self, raw, date=None, sort=True):
        """Constructs a new entry from some raw text input.
        If a date is given, it will parse and use this, otherwise scan for a date in the input first."""

        raw = raw.replace('\\n ', '\n').replace('\\n', '\n')
        starred = False
        # Split raw text into title and body
        sep = re.search("\n|[\?!.]+ +\n?", raw)
        title, body = (raw[:sep.end()], raw[sep.end():]) if sep else (raw, "")
        starred = False
        if not date:
            if title.find(": ") > 0:
                starred = "*" in title[:title.find(": ")]
                date = time.parse(title[:title.find(": ")], default_hour=self.config['default_hour'], default_minute=self.config['default_minute'])
                if date or starred:  # Parsed successfully, strip that from the raw text
                    title = title[title.find(": ")+1:].strip()
            elif title.strip().startswith("*"):
                starred = True
                title = title[1:].strip()
            elif title.strip().endswith("*"):
                starred = True
                title = title[:-1].strip()
        if not date:  # Still nothing? Meh, just live in the moment.
            date = time.parse("now")
        entry = Entry.Entry(self, date, title, body, starred=starred)
        entry.modified = True
        self.entries.append(entry)
        if sort:
            self.sort()
        return entry

    def editable_str(self):
        """Turns the journal into a string of entries that can be edited
        manually and later be parsed with eslf.parse_editable_str."""
        return u"\n".join([e.__unicode__() for e in self.entries])

    def parse_editable_str(self, edited):
        """Parses the output of self.editable_str and updates it's entries."""
        mod_entries = self._parse(edited)
        # Match those entries that can be found in self.entries and set
        # these to modified, so we can get a count of how many entries got
        # modified and how many got deleted later.
        for entry in mod_entries:
            entry.modified = not any(entry == old_entry for old_entry in self.entries)
        self.entries = mod_entries
