#!/usr/bin/env python
# encoding: utf-8

from Entry import Entry
import os
import parsedatetime.parsedatetime as pdt
import re
from datetime import datetime
import time
try: import simplejson as json
except ImportError: import json
import sys
import readline, glob
try:
    from Crypto.Cipher import AES
    from Crypto.Random import random, atfork
except ImportError:
    pass
import hashlib
import getpass
try:
    import clint
except ImportError:
    clint = None
import plistlib
import uuid

class Journal(object):
    def __init__(self, **kwargs):
        self.config = {
            'journal': "journal.txt",
            'encrypt': False,
            'password': "",
            'default_hour': 9,
            'default_minute': 0,
            'timeformat': "%Y-%m-%d %H:%M",
            'tagsymbols': '@',
            'highlight': True,
            'linewrap': 80,
        }
        self.config.update(kwargs)

        # Set up date parser
        consts = pdt.Constants()
        consts.DOWParseStyle = -1 # "Monday" will be either today or the last Monday
        self.dateparse = pdt.Calendar(consts)
        self.key = None # used to decrypt and encrypt the journal

        journal_txt = self.open()
        self.entries = self.parse(journal_txt)
        self.sort()

    def _colorize(self, string, color='red'):
        if clint:
            return str(clint.textui.colored.ColoredString(color.upper(), string))
        else:
            return string

    def _decrypt(self, cipher):
        """Decrypts a cipher string using self.key as the key and the first 16 byte of the cipher as the IV"""
        if not cipher:
            return ""
        crypto = AES.new(self.key, AES.MODE_CBC, cipher[:16])
        try:
            plain = crypto.decrypt(cipher[16:])
        except ValueError:
            print("ERROR: Your journal file seems to be corrupted. You do have a backup, don't you?")
            sys.exit(-1)
        if plain[-1] != " ": # Journals are always padded
            return None
        else:
            return plain

    def _encrypt(self, plain):
        """Encrypt a plaintext string using self.key as the key"""
        atfork() # A seed for PyCrypto
        iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
        crypto = AES.new(self.key, AES.MODE_CBC, iv)
        if len(plain) % 16 != 0:
            plain += " " * (16 - len(plain) % 16)
        else: # Always pad so we can detect properly decrypted files :)
            plain += " " * 16
        return iv + crypto.encrypt(plain)

    def make_key(self, prompt="Password: "):
        """Creates an encryption key from the default password or prompts for a new password."""
        password = self.config['password'] or getpass.getpass(prompt)
        self.key = hashlib.sha256(password).digest()

    def open(self, filename=None):
        """Opens the journal file defined in the config and parses it into a list of Entries.
        Entries have the form (date, title, body)."""
        filename = filename or self.config['journal']
        journal = None
        with open(filename) as f:
            journal = f.read()
        if self.config['encrypt']:
            decrypted = None
            attempts = 0
            while decrypted is None:
                self.make_key()
                decrypted = self._decrypt(journal)
                if decrypted is None:
                    attempts += 1
                    self.config['password'] = None # This password doesn't work.
                    if attempts < 3:
                        print("Wrong password, try again.")
                    else:
                        print("Extremely wrong password.")
                        sys.exit(-1)
            journal = decrypted
        return journal

    def parse(self, journal):
        """Parses a journal that's stored in a string and returns a list of entries"""

        # Entries start with a line that looks like 'date title' - let's figure out how
        # long the date will be by constructing one
        date_length = len(datetime.today().strftime(self.config['timeformat']))

        # Initialise our current entry
        entries = []
        current_entry = None

        for line in journal.splitlines():
            try:
                # try to parse line as date => new entry begins
                new_date = datetime.strptime(line[:date_length], self.config['timeformat'])

                # parsing successfull => save old entry and create new one
                if new_date and current_entry:
                    entries.append(current_entry)
                current_entry = Entry(self, date=new_date, title=line[date_length+1:])
            except ValueError:
                # Happens when we can't parse the start of the line as an date.
                # In this case, just append line to our body.
                current_entry.body += line + "\n"

        # Append last entry
        if current_entry:
            entries.append(current_entry)
        for entry in entries:
            entry.parse_tags()
        return entries

    def __str__(self):
        """Prettyprints the journal's entries"""
        sep = "\n"
        pp = sep.join([e.pprint() for e in self.entries])
        if self.config['highlight']: # highlight tags
            if self.search_tags:
                for tag in self.search_tags:
                    tagre = re.compile(re.escape(tag), re.IGNORECASE)
                    pp = re.sub(tagre,
                                lambda match: self._colorize(match.group(0), 'cyan'),
                                pp)
            else:
                pp = re.sub(r"([%s]\w+)" % self.config['tagsymbols'],
                            lambda match: self._colorize(match.group(0), 'cyan'),
                            pp)
        return pp

    def __repr__(self):
        return "<Journal with %d entries>" % len(self.entries)

    def write(self, filename = None):
        """Dumps the journal into the config file, overwriting it"""
        filename = filename or self.config['journal']
        journal = "\n".join([str(e) for e in self.entries])
        if self.config['encrypt']:
            journal = self._encrypt(journal)
        with open(filename, 'w') as journal_file:
                journal_file.write(journal)

    def sort(self):
        """Sorts the Journal's entries by date"""
        self.entries = sorted(self.entries, key=lambda entry: entry.date)

    def limit(self, n=None):
        """Removes all but the last n entries"""
        if n:
            self.entries = self.entries[-n:]

    def filter(self, tags=[], start_date=None, end_date=None, strict=False, short=False):
        """Removes all entries from the journal that don't match the filter.

        tags is a list of tags, each being a string that starts with one of the
        tag symbols defined in the config, e.g. ["@John", "#WorldDomination"].

        start_date and end_date define a timespan by which to filter.

        If strict is True, all tags must be present in an entry. If false, the
        entry is kept if any tag is present."""
        self.search_tags = set([tag.lower() for tag in tags])
        end_date = self.parse_date(end_date)
        start_date = self.parse_date(start_date)
        # If strict mode is on, all tags have to be present in entry
        tagged = self.search_tags.issubset if strict else self.search_tags.intersection
        result = [
            entry for entry in self.entries
            if (not tags or tagged(entry.tags))
            and (not start_date or entry.date > start_date)
            and (not end_date or entry.date < end_date)
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
                            res.append('%s %s ..' % (date, excerpt))
                    e.body = "\n".join(res)
            else:
                for e in self.entries:
                    e.body = ''
        self.entries = result

    def parse_date(self, date):
        """Parses a string containing a fuzzy date and returns a datetime.datetime object"""
        if not date:
            return None
        elif type(date) is datetime:
            return date

        date, flag = self.dateparse.parse(date)

        if not flag: # Oops, unparsable.
            return None

        if flag is 1: # Date found, but no time. Use the default time.
            date = datetime(*date[:3], hour=self.config['default_hour'], minute=self.config['default_minute'])
        else:
            date = datetime(*date[:6])

        # Ugly heuristic: if the date is more than 4 weeks in the future, we got the year wrong.
        # Rather then this, we would like to see parsedatetime patched so we can tell it to prefer
        # past dates
        dt = datetime.now() - date
        if dt.days < -28:
            date = date.replace(date.year - 1)

        return date

    def new_entry(self, raw, date=None, sort=True):
        """Constructs a new entry from some raw text input.
        If a date is given, it will parse and use this, otherwise scan for a date in the input first."""

        raw = raw.replace('\\n ', '\n').replace('\\n', '\n')

        # Split raw text into title and body
        title_end = len(raw)
        for separator in ".?!\n":
            sep_pos = raw.find(separator)
            if 1 < sep_pos < title_end:
                title_end = sep_pos
        title = raw[:title_end+1]
        body = raw[title_end+1:].strip()
        if not date:
            if title.find(":") > 0:
                date = self.parse_date(title[:title.find(":")])
                if date: # Parsed successfully, strip that from the raw text
                    title = title[title.find(":")+1:].strip()
        if not date: # Still nothing? Meh, just live in the moment.
            date = self.parse_date("now")

        entry = Entry(self, date, title, body)
        self.entries.append(entry)
        if sort:
            self.sort()
        return entry

class DayOne(Journal):
    """A special Journal handling DayOne files"""
    def __init__(self, **kwargs):
        self.entries = []
        super(DayOne, self).__init__(**kwargs)

    def open(self):
        files = [os.path.join(self.config['journal'], "entries", f) for f in os.listdir(os.path.join(self.config['journal'], "entries"))]
        return files

    def parse(self, filenames):
        """Instead of parsing a string into an entry, this method will take a list
        of filenames, interpret each as a plist file and create a new entry from that."""
        self.entries = []
        for filename in filenames:
            with open(filename) as plist_entry:
                dict_entry = plistlib.readPlist(plist_entry)
                entry = self.new_entry(raw=dict_entry['Entry Text'], date=dict_entry['Creation Date'], sort=False)
                entry.starred = dict_entry["Starred"]
                entry.uuid = dict_entry["UUID"]
        # We're using new_entry to create the Entry object, which adds the entry
        # to self.entries already. However, in the original Journal.__init__, this
        # method is expected to return a list of newly created entries, which is why
        # we're returning the obvious.
        return self.entries


    def write(self):
        """Writes only the entries that have been modified into plist files."""
        for entry in self.entries:
            # Assumption: since jrnl can not manipulate existing entries, all entries
            # that have a uuid will be old ones, and only the one that doesn't will
            # have a new one!
            if not hasattr(entry, "uuid"):
                new_uuid = uuid.uuid1().hex
                filename = os.path.join(self.config['journal'], "entries", new_uuid+".doentry")
                entry_plist = {
                    'Creation Date': entry.date,
                    'Starred': entry.starred if hasattr(entry, 'starred') else False,
                    'Entry Text': entry.title+"\n"+entry.body,
                    'UUID': new_uuid
                }
                plistlib.writePlist(entry_plist, filename)

