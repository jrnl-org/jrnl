#!/usr/bin/env python
# encoding: utf-8
import os
import tempfile
import parsedatetime.parsedatetime as pdt
import parsedatetime.parsedatetime_consts as pdc
import subprocess
import re
import argparse
from datetime import datetime
import time
try: import simplejson as json
except ImportError: import json
import sys
import readline, glob
from Crypto.Cipher import AES
from Crypto.Random import random, atfork
import hashlib
import getpass
try:
    import clint
    CLINT = True
except ImportError:
    CLINT = False

default_config = {
    'journal': os.path.expanduser("~/journal.txt"),
    'editor': "",
    'encrypt': False,
    'password': "",
    'default_hour': 9,
    'default_minute': 0,
    'timeformat': "%Y-%m-%d %H:%M",
    'tagsymbols': '@',
    'highlight': True,
}

CONFIG_PATH = os.path.expanduser('~/.jrnl_config')

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

class Journal:
    def __init__(self, config, **kwargs):
        config.update(kwargs)
        self.config = config

        # Set up date parser
        consts = pdc.Constants()
        consts.DOWParseStyle = -1 # "Monday" will be either today or the last Monday
        self.dateparse = pdt.Calendar(consts)
        self.key = None # used to decrypt and encrypt the journal

        journal_txt = self.open()
        self.entries = self.parse(journal_txt)
        self.sort()

    def _colorize(self, string, color='red'):
        if CLINT:
            return str(clint.textui.colored.ColoredString(color.upper(), string))
        else:
            return string

    def _decrypt(self, cipher):
        """Decrypts a cipher string using self.key as the key and the first 16 byte of the cipher as the IV"""
        if not cipher:
            return ""
        crypto = AES.new(self.key, AES.MODE_CBC, cipher[:16])
        plain = crypto.decrypt(cipher[16:])
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

        for line in journal.split(os.linesep):
            if line:
                try:
                    new_date = datetime.fromtimestamp(time.mktime(time.strptime(line[:date_length], self.config['timeformat'])))
                    # make a journal entry of the current stuff first
                    if new_date and current_entry:
                        entries.append(current_entry)
                    # Start constructing current entry
                    current_entry = Entry(self, date=new_date, title=line[date_length+1:])
                except ValueError:
                    # Happens when we can't parse the start of the line as an date.
                    # In this case, just append line to our body.
                    current_entry.body += line
        # Append last entry
        if current_entry:
            entries.append(current_entry)
        for entry in entries:
            entry.parse_tags()
        return entries

    def __str__(self):
        """Prettyprints the journal's entries"""
        sep = "-"*60+"\n"
        pp = sep.join([str(e) for e in self.entries])
        if self.config['highlight']: # highlight tags
            if hasattr(self, 'search_tags'):
                for tag in self.search_tags:
                    pp = pp.replace(tag, self._colorize(tag))
            else:
                pp = re.sub(r"([%s]\w+)" % self.config['tagsymbols'],
                            lambda match: self._colorize(match.group(0), 'cyan'),
                            pp)
        return pp

    def to_json(self):
        """Returns a JSON representation of the Journal."""
        return json.dumps([e.to_dict() for e in self.entries], indent=2)

    def to_md(self):
        """Returns a markdown representation of the Journal"""
        out = []
        year, month = -1, -1
        for e in self.entries:
            if not e.date.year == year:
                year = e.date.year
                out.append(str(year))
                out.append("=" * len(str(year)) + "\n")
            if not e.date.month == month:
                month = e.date.month
                out.append(e.date.strftime("%B"))
                out.append('-' * len(e.date.strftime("%B")) + "\n")
            out.append(e.to_md())
        return "\n".join(out)

    def __repr__(self):
        return "<Journal with %d entries>" % len(self.entries)

    def write(self, filename = None):
        """Dumps the journal into the config file, overwriting it"""
        filename = filename or self.config['journal']
        journal = os.linesep.join([str(e) for e in self.entries])
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

        return date

    def new_entry(self, raw, date=None):
        """Constructs a new entry from some raw text input.
        If a date is given, it will parse and use this, otherwise scan for a date in the input first."""
        if not date:
            if raw.find(":") > 0:
                date = self.parse_date(raw[:raw.find(":")])
                if date: # Parsed successfully, strip that from the raw text
                    raw = raw[raw.find(":")+1:].strip()

        if not date: # Still nothing? Meh, just live in the moment.
            date = self.parse_date("now")

        # Split raw text into title and body
        body = ""
        title_end = len(raw)
        for separator in ".?!":
            sep_pos = raw.find(separator)
            if 1 < sep_pos < title_end:
                title_end = sep_pos
        title = raw[:title_end+1]
        body = raw[title_end+1:].strip()
        self.entries.append(Entry(self, date, title, body))
        self.sort()

    def save_config(self, config_path = CONFIG_PATH):
        with open(config_path, 'w') as f:
            json.dump(self.config, f, indent=2)

def setup():
    def autocomplete(text, state):
        expansions = glob.glob(os.path.expanduser(text)+'*')
        expansions = [e+"/" if os.path.isdir(e) else e for e in expansions]
        expansions.append(None)
        return expansions[state]
    readline.set_completer_delims(' \t\n;')
    readline.parse_and_bind("tab: complete")
    readline.set_completer(autocomplete)

    # Where to create the journal?
    path_query = 'Path to your journal file (leave blank for ~/journal.txt): '
    journal_path = raw_input(path_query).strip() or os.path.expanduser('~/journal.txt')
    default_config['journal'] = os.path.expanduser(journal_path)

    # Encrypt it?
    password = getpass.getpass("Enter password for journal (leave blank for no encryption): ")
    if password:
        default_config['encrypt'] = True
        print("Journal will be encrypted.")
        print("If you want to, you can store your password in .jrnl_config and will never be bothered about it again.")

    # Use highlighting:
    if not CLINT:
        print("clint not found. To turn on highlighting, install clint and set highlight to true in your .jrnl_conf.")
        default_config['highlight'] = False

    open(default_config['journal'], 'a').close() # Touch to make sure it's there

    # Write config to ~/.jrnl_conf
    with open(CONFIG_PATH, 'w') as f:
        json.dump(default_config, f, indent=2)
    config = default_config
    if password:
        config['password'] = password
    return config

if __name__ == "__main__":

    if not os.path.exists(CONFIG_PATH):
        config = setup()
    else:
        with open(CONFIG_PATH) as f:
            config = json.load(f)

        # update config file with settings introduced in a later version
        missing_keys = set(default_config).difference(config)
        if missing_keys:
            for key in missing_keys:
                config[key] = default_config[key]
            with open(CONFIG_PATH, 'w') as f:
                json.dump(config, f, indent=2)

    parser = argparse.ArgumentParser()
    composing = parser.add_argument_group('Composing', 'Will make an entry out of whatever follows as arguments')
    composing.add_argument('-date', dest='date', help='Date, e.g. "yesterday at 5pm"')
    composing.add_argument('text', metavar='text', nargs="*",  help='Log entry (or tags by which to filter in viewing mode)')

    reading = parser.add_argument_group('Reading', 'Specifying either of these parameters will display posts of your journal')
    reading.add_argument('-from', dest='start_date', metavar="DATE", help='View entries after this date')
    reading.add_argument('-to', dest='end_date', metavar="DATE", help='View entries before this date')
    reading.add_argument('-and', dest='strict', action="store_true", help='Filter by tags using AND (default: OR)')
    reading.add_argument('-n', dest='limit', default=None, metavar="N", help='Shows the last n entries matching the filter', nargs="?", type=int)
    reading.add_argument('-short', dest='short', action="store_true", help='Show only titles or line containing the search tags')

    exporting = parser.add_argument_group('Export / Import', 'Options for transmogrifying your journal')
    exporting.add_argument('--tags', dest='tags', action="store_true", help='Returns a list of all tags and number of occurences')
    exporting.add_argument('--json', dest='json', action="store_true", help='Returns a JSON-encoded version of the Journal')
    exporting.add_argument('--markdown', dest='markdown', action="store_true", help='Returns a Markdown-formated version of the Journal')
    exporting.add_argument('--encrypt', dest='encrypt', action="store_true", help='Encrypts your existing journal with a new password')
    exporting.add_argument('--decrypt', dest='decrypt', action="store_true", help='Decrypts your journal and stores it in plain text')

    args = parser.parse_args()

    # Guess mode
    compose = True
    export = False
    if args.json or args.decrypt or args.encrypt or args.markdown or args.tags:
        compose = False
        export = True
    elif args.start_date or args.end_date or args.limit or args.strict or args.short:
        # Any sign of displaying stuff?
        compose = False
    elif not args.date and args.text and all(word[0] in config['tagsymbols'] for word in args.text):
        # No date and only tags?
        compose = False

    # No text? Query
    if compose and not args.text:
        if config['editor']:
            tmpfile = os.path.join(tempfile.gettempdir(), "jrnl")
            subprocess.call(config['editor'].split() + [tmpfile])
            if os.path.exists(tmpfile):
                with open(tmpfile) as f:
                    raw = f.read()
                os.remove(tmpfile)
            else:
                print('nothing saved to file')
                raw = ''
        else:
            raw = raw_input("Compose Entry: ")

        if raw:
            args.text = [raw]
        else:
            compose = False

    # open journal
    journal = Journal(config=config)

    # Writing mode
    if compose:
        raw = " ".join(args.text).strip()
        journal.new_entry(raw, args.date)
        print("Entry added.")
        journal.write()

    elif not export: # read mode
        journal.filter(tags=args.text,
                       start_date=args.start_date, end_date=args.end_date,
                       strict=args.strict,
                       short=args.short)
        journal.limit(args.limit)
        print(journal)

    elif args.tags: # get all tags
        # Astute reader: should the following line leave you as puzzled as me the first time
        # I came across this construction, worry not and embrace the ensuing moment of enlightment.
        tags = [tag 
            for entry in journal.entries 
            for tag in set(entry.tags)
        ]
        # To be read: [for entry in journal.entries: for tag in set(entry.tags): tag]
        tag_counts = {(tags.count(tag), tag) for tag in tags}
        for n, tag in sorted(tag_counts, reverse=True):
            print "%-20s : %d" % (tag, n)

    elif args.json: # export to json
        print(journal.to_json())

    elif args.markdown: # export to json
        print(journal.to_md())

    elif args.encrypt:
        journal.config['encrypt'] = True
        journal.config['password'] = ""
        journal.make_key(prompt="Enter new password:")
        journal.write()
        journal.save_config()
        print("Journal encrypted to %s." % journal.config['journal'])

    elif args.decrypt:
        journal.config['encrypt'] = False
        journal.config['password'] = ""
        journal.write()
        journal.save_config()
        print("Journal decrypted to %s." % journal.config['journal'])

