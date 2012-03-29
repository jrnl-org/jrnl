#!/usr/bin/python
# encoding: utf-8

import parsedatetime.parsedatetime as pdt
import parsedatetime.parsedatetime_consts as pdc
import argparse
from datetime import datetime
import time

config = {
    'journal': "/home/manuel/Dropbox/Notes/journal.txt",
    'default_hour': 9,
    'default_minute': 0,
    'timeformat': "%Y-%m-%d %H:%M",
}

def read_file(filename=None):
    filename = filename or config['journal']
    f = open(filename)
    journal = []

    date_length = len(datetime.today().strftime(config['timeformat']))
    date = None
    body = ""
    title = ""
    for line in f.readlines():
        if line:
            try:
                new_date = datetime.fromtimestamp(time.mktime(time.strptime(line[:date_length], config['timeformat'])))
                # make a journal entry of the current stuff first
                if date:
                    journal.append((date, title.strip(), body.strip()))
                # Start constructing current entry
                title = line[date_length+1:]
                body = ""
                date = new_date
            except ValueError:
                body += line
    journal.append((date, title.strip(), body.strip()))
    f.close()
    return journal

def print_journal(journal):
    for date, title, body in sorted(journal):
        print "Date:", date.strftime(config['timeformat'])
        print "Title:", title
        if body: print "Body:", body
        print "-------------------------------------------"

def write_file(journal, filename=None):
    filename = filename or config['journal']
    f = open(filename, 'w')
    for date, title, body in sorted(journal):
        body = ("\n%s\n\n" % body if body else "\n\n")
        f.write("%(date)s %(title)s %(body)s" % {
            'date': date.strftime(config['timeformat']), 
            'title': title,
            'body': body,
        })
    f.close()

def parse_entry(log, date=None):
    # Set up date parser
    consts = pdc.Constants()
    consts.DOWParseStyle = -1 # "Monday" will be either today or the last Monday
    dateparse = pdt.Calendar(consts)

    if not date:
        #see whether we find anything in the beginning of our log
        if log.find(":") > 0:
            date = log[:log.find(":")]
            dtest, flag = dateparse.parse(date)
            if flag: # can parse successfully
                log = log[log.find(":")+1:].strip()
        else:
            date = "now"

    # Parse date
    date, flag = dateparse.parse(date)
    if flag is 1: # set to 9 am
        date = datetime(*date[:3], hour=config['default_hour'], minute=config['default_minute'])
    else:
        date = datetime(*date[:6])

    # Split log into title and body
    body = ""
    title_end = len(log)
    for separator in ".?!":
        sep_pos = log.find(separator)
        if 1 < sep_pos < title_end:
            title_end = sep_pos
    title = log[:title_end+1]
    body = log[title_end+1:].strip()
    return date, title, body

def filter_journal(journal, tags=[], people=[]):
    tags = [tag[1:].lower() if tag.startswith("#") else tag.lower() for tag in tags]
    people = [person[:1].lower() if person.startswith("@") else person.lower() for person in people]

    def _has_tag(entry, tags, symbol="@"):
        date, title, body = entry
        fulltext = " ".join([title, body]).lower()
        has = False
        for tag in tags:
            if symbol+tag in fulltext:
                has = True
        return has

    result = [entry for entry in journal
        if _has_tag(entry, people) 
        or _has_tag(entry, tags, symbol="#")
    ]
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    composing = parser.add_argument_group('Composing', 'Will make an entry out of whatever follows as arguments')
    composing.add_argument('-date', dest='date', help='Date, e.g. "yesterday at 5pm"')
    composing.add_argument('log', metavar='text', nargs="*",  help='Log entry')

    reading = parser.add_argument_group('Reading', 'Specifying either of these parameters will display posts of your journal')
    reading.add_argument('-tags', dest='tags', metavar="#tag", default=[], help='Tags by which to filter', nargs="*")
    reading.add_argument('-people', dest='people', metavar="@person", default=[], help='People by which to filter', nargs="+")
    reading.add_argument('-n', dest='limit', metavar="N", help='Shows the last n entries matching the filter', nargs="?", type=int)
    args = parser.parse_args()

    # open journal
    journal = read_file()
    # Writing mode
    if not args.log and not args.people and not args.limit and not args.tags:
        args.log = [raw_input("Compose Entry: ")]
    elif args.log: # Write mode
        raw = " ".join(args.log).strip()    
        entry = parse_entry(log=raw, date=args.date)
        journal.append(entry)
        print_journal(journal)
        write_file(journal)
    else: # read mode
        journal = filter_journal(journal, tags=args.tags, people=args.people)
        if args.limit:
            journal = journal[:-limit]
        print_journal(journal)
