#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import
from . import Entry
from . import util
import codecs
import os
try:
    import parsedatetime.parsedatetime_consts as pdt
except ImportError:
    import parsedatetime as pdt
import re
from datetime import timedelta
from datetime import datetime
import dateutil
import time
import sys
try:
    from Crypto.Cipher import AES
    from Crypto import Random
    crypto_installed = True
except ImportError:
    crypto_installed = False
import hashlib
import plistlib
import pytz
import uuid
import tzlocal


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
        consts = pdt.Constants(usePyICU=False)
        consts.DOWParseStyle = -1  # "Monday" will be either today or the last Monday
        self.dateparse = pdt.Calendar(consts)
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
        padding = " ".encode("utf-8")
        if not plain.endswith(padding):  # Journals are always padded
            return None
        else:
            return plain.decode("utf-8")

    def _encrypt(self, plain):
        """Encrypt a plaintext string using self.key as the key"""
        if not crypto_installed:
            sys.exit("Error: PyCrypto is not installed.")
        Random.atfork()  # A seed for PyCrypto
        iv = Random.new().read(AES.block_size)
        crypto = AES.new(self.key, AES.MODE_CBC, iv)
        plain = plain.encode("utf-8")
        plain += b" " * (AES.block_size - len(plain) % AES.block_size)
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
        end_date = self.parse_date(end_date, end_flag="to")
        start_date = self.parse_date(start_date, end_flag="from")
        # If strict mode is on, all tags have to be present in entry
        tagged = self.search_tags.issubset if strict else self.search_tags.intersection
        result = [
            entry for entry in self.entries
            if (not tags or tagged(entry.tags))
            and (not starred or entry.starred)
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
                            res.append('{0} {1} ..'.format(date, excerpt))
                    e.body = "\n".join(res)
            else:
                for e in self.entries:
                    e.body = ''
        self.entries = result

    def parse_date(self, date_str, end_flag=None):
        """Parses a string containing a fuzzy date and returns a datetime.datetime object"""
        if not date_str:
            return None
        elif isinstance(date_str, datetime):
            return date_str

        if re.match(r'^\d{4}$', date_str):
            # i.e. if we're just given a year
            if end_flag == "from":
                date = datetime(year=int(date_str), month=1, day=1, hour=0, minute=0)
            elif end_flag == "to":
                date = datetime(year=int(date_str), month=12, day=31, hour=23, minute=59, second=59)
            else:
                # Use the default time.
                date = datetime(year=int(date_str), month=1, day=1, hour=self.config['default_hour'], minute=self.config['default_minute'])
        else:
            # clean up some misunderstood dates
            replacements = (u"september", u"sep"), (u"sept", u"sep"), (u"tuesday", u"tue"), \
                                (u"tues", u"tue"), (u"thursday", u"thu"), (u"thurs", u"thu"), \
                                (u" o'clock", u":00")
            date_str = util.multiple_replace(date_str.lower(), *replacements)

            # determine if we've been given just a month, or just a year and month
            replacements2 = ("january", "01"), ("february", "02"), ("march", "03"), \
                            ("april", "04"), ("may", "05"), ("june", "06"), \
                            ("july", "07"), ("august", "08"), \
                            ("october", "10"), ("november", "11"), ("december", "12"), \
                            ("jan", "01"), ("feb", "02"), ("mar", "03"), ("apr", "04"), \
                                           ("jun", "06"), ("jul", "07"), ("aug", "08"), \
                            ("sep", "09"), ("oct", "10"), ("nov", "11"), ("dec", "12")
            date_str2 = util.multiple_replace(date_str.lower(), *replacements2)
            year_month_only = False;
            matches = re.match(r'^(\d{4})[ \\/-](\d{2})$', date_str2)
            if matches:
                myYear = matches.group(1)
                myMonth = matches.group(2)
                year_month_only = True
            else:
                matches2 = re.match(r'^(\d{2})[ \\/-](\d{4})$', date_str2)
                if matches2:
                    myYear = matches2.group(2)
                    myMonth = matches2.group(1)
                    year_month_only = True
                else:
                    matches3 = re.match(r'^(\d{2})$', date_str2)
                    if matches3:
                        myYear = datetime.today().year
                        myMonth = matches3.group(0)

                        # if given (just) a month and it's not this month or next, assume it was last year
                        dt = datetime.now() - datetime(year=int(myYear), month=int(myMonth), day=1)
                        if dt.days < -32:
                            myYear = myYear - 1
                        year_month_only = True

            if year_month_only == True:
                if end_flag == "from":
                    date = datetime(year=int(myYear), month=int(myMonth), day=1, hour=0, minute=0)
                elif end_flag == "to":
                    # get the last day of the month
                    if myMonth == 12:
                        date = datetime(year=int(myYear), month=int(myMonth), day=31, hour=23, minute=59, second=59)
                    else:
                        date = datetime(year=int(myYear), month=int(myMonth)+1, day=1, hour=23, minute=59, second=59) - timedelta (days = 1)
                else:
                    # Use the default time.
                    date = datetime(year=int(myYear), month=int(myMonth), day=1, hour=self.config['default_hour'], minute=self.config['default_minute'])

            else:
                try:
                    date = dateutil.parser.parse(date_str)
                    flag = 1 if date.hour == 0 and date.minute == 0 else 2
                    date = date.timetuple()
                except:
                    date, flag = self.dateparse.parse(date_str)

                if not flag:  # Oops, unparsable.
                    try:  # Try and parse this as a single year
                        year = int(date_str)
                        return datetime(year, 1, 1)
                    except ValueError:
                        return None
                    except TypeError:
                        return None

                if flag is 1:  # Date found, but no time.
                    if end_flag == "from":
                        date = datetime(*date[:3], hour=0, minute=0)
                    elif end_flag == "to":
                        date = datetime(*date[:3], hour=23, minute=59, second=59)
                    else:
                        # Use the default time.
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
        starred = False
        # Split raw text into title and body
        sep = re.search("\n|[\?.]+", raw)
        title, body = (raw[:sep.end()], raw[sep.end():]) if sep else (raw, "")
        starred = False
        if not date:
            if title.find(": ") > 0:
                starred = "*" in title[:title.find(": ")]
                date = self.parse_date(title[:title.find(": ")])
                if date or starred:  # Parsed successfully, strip that from the raw text
                    title = title[title.find(": ")+1:].strip()
            elif title.strip().startswith("*"):
                starred = True
                title = title[1:].strip()
            elif title.strip().endswith("*"):
                starred = True
                title = title[:-1].strip()
        if not date:  # Still nothing? Meh, just live in the moment.
            date = self.parse_date("now")
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


class DayOne(Journal):
    """A special Journal handling DayOne files"""
    def __init__(self, **kwargs):
        self.entries = []
        self._deleted_entries = []
        super(DayOne, self).__init__(**kwargs)

    def open(self):
        filenames = [os.path.join(self.config['journal'], "entries", f) for f in os.listdir(os.path.join(self.config['journal'], "entries"))]
        self.entries = []
        for filename in filenames:
            with open(filename, 'rb') as plist_entry:
                dict_entry = plistlib.readPlist(plist_entry)
                try:
                    timezone = pytz.timezone(dict_entry['Time Zone'])
                except (KeyError, pytz.exceptions.UnknownTimeZoneError):
                    timezone = tzlocal.get_localzone()
                date = dict_entry['Creation Date']
                date = date + timezone.utcoffset(date)
                raw = dict_entry['Entry Text']
                sep = re.search("[\n!?.]+", raw)
                title, body = (raw[:sep.end()], raw[sep.end():]) if sep else (raw, "")
                entry = Entry.Entry(self, date, title, body, starred=dict_entry["Starred"])
                entry.uuid = dict_entry["UUID"]
                entry.tags = [self.config['tagsymbols'][0] + tag for tag in dict_entry.get("Tags", [])]
                self.entries.append(entry)
        self.sort()

    def write(self):
        """Writes only the entries that have been modified into plist files."""
        for entry in self.entries:
            if entry.modified:
                if not hasattr(entry, "uuid"):
                    entry.uuid = uuid.uuid1().hex
                utc_time = datetime.utcfromtimestamp(time.mktime(entry.date.timetuple()))
                filename = os.path.join(self.config['journal'], "entries", entry.uuid + ".doentry")
                entry_plist = {
                    'Creation Date': utc_time,
                    'Starred': entry.starred if hasattr(entry, 'starred') else False,
                    'Entry Text': entry.title+"\n"+entry.body,
                    'Time Zone': str(tzlocal.get_localzone()),
                    'UUID': entry.uuid,
                    'Tags': [tag.strip(self.config['tagsymbols']) for tag in entry.tags]
                }
                plistlib.writePlist(entry_plist, filename)
        for entry in self._deleted_entries:
            filename = os.path.join(self.config['journal'], "entries", entry.uuid+".doentry")
            os.remove(filename)

    def editable_str(self):
        """Turns the journal into a string of entries that can be edited
        manually and later be parsed with eslf.parse_editable_str."""
        return u"\n".join([u"# {0}\n{1}".format(e.uuid, e.__unicode__()) for e in self.entries])

    def parse_editable_str(self, edited):
        """Parses the output of self.editable_str and updates it's entries."""
        # Method: create a new list of entries from the edited text, then match
        # UUIDs of the new entries against self.entries, updating the entries
        # if the edited entries differ, and deleting entries from self.entries
        # if they don't show up in the edited entries anymore.
        date_length = len(datetime.today().strftime(self.config['timeformat']))

        # Initialise our current entry
        entries = []
        current_entry = None

        for line in edited.splitlines():
            # try to parse line as UUID => new entry begins
            line = line.rstrip()
            m = re.match("# *([a-f0-9]+) *$", line.lower())
            if m:
                if current_entry:
                    entries.append(current_entry)
                current_entry = Entry.Entry(self)
                current_entry.modified = False
                current_entry.uuid = m.group(1).lower()
            else:
                try:
                    new_date = datetime.strptime(line[:date_length], self.config['timeformat'])
                    if line.endswith("*"):
                        current_entry.starred = True
                        line = line[:-1]
                    current_entry.title = line[date_length+1:]
                    current_entry.date = new_date
                except ValueError:
                    if current_entry:
                        current_entry.body += line + "\n"

        # Append last entry
        if current_entry:
            entries.append(current_entry)

        # Now, update our current entries if they changed
        for entry in entries:
            entry.parse_tags()
            matched_entries = [e for e in self.entries if e.uuid.lower() == entry.uuid]
            if matched_entries:
                # This entry is an existing entry
                match = matched_entries[0]
                if match != entry:
                    self.entries.remove(match)
                    entry.modified = True
                    self.entries.append(entry)
            else:
                # This entry seems to be new... save it.
                entry.modified = True
                self.entries.append(entry)
        # Remove deleted entries
        edited_uuids = [e.uuid for e in entries]
        self._deleted_entries = [e for e in self.entries if e.uuid not in edited_uuids]
        self.entries[:] = [e for e in self.entries if e.uuid in edited_uuids]
        return entries
