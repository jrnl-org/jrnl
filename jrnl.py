#!/usr/bin/python
# encoding: utf-8

import parsedatetime.parsedatetime as pdt
import parsedatetime.parsedatetime_consts as pdc
import re
import argparse
from datetime import datetime
import time

config = {
    'journal': "/home/manuel/Dropbox/Notes/journal.txt",
    'default_hour': 9,
    'default_minute': 0,
    'timeformat': "%Y-%m-%d %H:%M",
    'tagsymbols': '#@'
}

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


class Journal:
    def __init__(self, config):
        self.config = config

        # Set up date parser
        consts = pdc.Constants()
        consts.DOWParseStyle = -1 # "Monday" will be either today or the last Monday
        self.dateparse = pdt.Calendar(consts)

        self.entries = self.open()
        self.sort()

    def open(self, filename=None):
        """Opens the journal file defined in the config and parses it into a list of Entries.
        Entries have the form (date, title, body)."""
        filename = filename or self.config['journal']

        # Entries start with a line that looks like 'date title' - let's figure out how
        # long the date will be by constructing one
        date_length = len(datetime.today().strftime(self.config['timeformat']))

        # Initialise our current entry
        entries = []
        current_entry = None

        journal_file = open(filename)
        for line in journal_file.readlines():
            if line:
                try:
                    new_date = datetime.fromtimestamp(time.mktime(time.strptime(line[:date_length], config['timeformat'])))
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
        entries.append(current_entry)
        journal_file.close()
        for entry in entries:
            entry.parse_tags()
        return entries

    def __str__(self):
        """Prettyprints the journal's entries"""
        sep = "-"*60+"\n"
        return sep.join([str(e) for e in self.entries])

    def __repr__(self):
        return "<Journal with %d entries>" % len(self.entries)

    def write(self, filename = None):
        """Dumps the journal into the config file, overwriting it"""
        filename = filename or self.config['journal']
        journal_file = open(filename, 'w')
        for entry in self.entries:
            journal_file.write(str(entry)+"\n")
        journal_file.close()

    def sort(self):
        """Sorts the Journal's entries by date"""
        self.entries = sorted(self.entries, key=lambda entry: entry.date)

    def limit(self, n=None):
        """Removes all but the last n entries"""
        if n:
            self.entries = self.entries[-n:]

    def filter(self, tags=[], start_date=None, end_date=None, strict=False):
        """Removes all entries from the journal that don't match the filter.
        
        tags is a list of tags, each being a string that starts with one of the
        tag symbols defined in the config, e.g. ["@John", "#WorldDomination"].

        start_date and end_date define a timespan by which to filter.

        If strict is True, all tags must be present in an entry. If false, the 
        entry is kept if any tag is present."""
        search_tags = set(tags)
        end_date = self.parse_date(end_date)
        start_date = self.parse_date(start_date)
        # If strict mode is on, all tags have to be present in entry
        tagged = search_tags.issubset if strict else search_tags.intersection
        result = [
            entry for entry in self.entries
            if (not tags or tagged(entry.tags))
            and (not start_date or entry.date > start_date)
            and (not end_date or entry.date < end_date)
        ]
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    composing = parser.add_argument_group('Composing', 'Will make an entry out of whatever follows as arguments')
    composing.add_argument('-date', dest='date', help='Date, e.g. "yesterday at 5pm"')
    composing.add_argument('text', metavar='text', nargs="*",  help='Log entry')

    reading = parser.add_argument_group('Reading', 'Specifying either of these parameters will display posts of your journal')
    reading.add_argument('-from', dest='start_date', metavar="date", help='View entries after this date')
    reading.add_argument('-to', dest='end_date', metavar="date", help='View entries before this date')
    reading.add_argument('-n', dest='limit', default=None, metavar="N", help='Shows the last n entries matching the filter', nargs="?", type=int)
    args = parser.parse_args()

    # open journal
    journal = Journal(config=config)

    # Guess mode
    compose = True
    if args.start_date or args.end_date or args.limit:
        # Any sign of displaying stuff?
        compose = False
    elif not args.date and args.text and all(word[0] in config['tagsymbols'] for word in args.text):
        # No date and only tags?
        compose = False

    # No text? Query
    if compose and not args.text:
        raw = raw_input("Compose Entry: ")
        if raw:
            args.text = [raw]
        else:
            compose = False

    # Writing mode
    if compose:
        raw = " ".join(args.text).strip()    
        journal.new_entry(raw, args.date)
        print journal
        journal.write()

    else: # read mode
        journal.filter(tags=args.text, start_date=args.start_date, end_date=args.end_date)
        journal.limit(args.limit)
        print journal
