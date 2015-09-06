#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, unicode_literals
from . import Entry
from . import Journal
import os
import re
from datetime import datetime
import time
import plistlib
import pytz
import uuid
import tzlocal
import base64
from xml.parsers.expat import ExpatError


class DayOne(Journal.Journal):
    """A special Journal handling DayOne files"""

    # InvalidFileException was added to plistlib in Python3.4
    PLIST_EXCEPTIONS = (ExpatError, plistlib.InvalidFileException) if hasattr(plistlib, "InvalidFileException") else ExpatError
    DAY_ONE_EXTRA_DATA_MARKER = "## DAY_ONE_DATA: "

    def __init__(self, **kwargs):
        self.entries = []
        self._deleted_entries = []
        super(DayOne, self).__init__(**kwargs)

    def open(self):
        filenames = [os.path.join(self.config['journal'], "entries", f) for f in os.listdir(os.path.join(self.config['journal'], "entries"))]
        self.entries = []
        for filename in filenames:
            with open(filename, 'rb') as plist_entry:
                try:
                    dict_entry = plistlib.readPlist(plist_entry)
                except self.PLIST_EXCEPTIONS:
                    pass
                else:
                    try:
                        timezone = pytz.timezone(dict_entry['Time Zone'])
                    except (KeyError, pytz.exceptions.UnknownTimeZoneError):
                        timezone = tzlocal.get_localzone()
                    do_to_jrnl_field_map = {
                        'Creation Date': 'date',
                        'Entry Text': 'title',
                        'Starred': 'starred',
                        'UUID': 'uuid'
                    }
                    date = dict_entry['Creation Date']
                    date = date + timezone.utcoffset(date, is_dst=False)
                    raw = dict_entry['Entry Text']
                    sep = re.search("\n|[\?!.]+ +\n?", raw)
                    title, body = (raw[:sep.end()], raw[sep.end():]) if sep else (raw, "")
                    extra_data = {k: v for k, v in dict_entry.iteritems() if k not in do_to_jrnl_field_map.keys()}
                    entry = Entry.DayOneEntry(self, date, title, body, starred=dict_entry["Starred"],
                                              extra_data=extra_data)
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
                # make sure to upper() the uuid since uuid.uuid1 returns a lowercase string by default
                # while dayone uses uppercase by default. On fully case preserving filesystems (e.g.
                # linux) this results in duplicated entries when we save the file
                filename = os.path.join(self.config['journal'], "entries", entry.uuid.upper() + ".doentry")
                entry_plist = {
                    'Creation Date': utc_time,
                    'Starred': entry.starred if hasattr(entry, 'starred') else False,
                    'Entry Text': entry.title + "\n" + entry.body,
                    'Time Zone': str(tzlocal.get_localzone()),
                    'UUID': entry.uuid,
                    'Tags': [tag.strip(self.config['tagsymbols']).replace("_", " ") for tag in entry.tags]
                }
                if entry.extra_data:
                    entry_plist.update(entry.extra_data)
                plistlib.writePlist(entry_plist, filename)
        for entry in self._deleted_entries:
            filename = os.path.join(self.config['journal'], "entries", entry.uuid + ".doentry")
            os.remove(filename)

    def editable_str(self):
        """Turns the journal into a string of entries that can be edited
        manually and later be parsed with eslf.parse_editable_str."""
        output_str = ""
        for entry in self.entries:
            # use base64 and zlib encoding to compress the extra data and minimize
            # non-human readable gibberish in the output
            day_one_data = base64.encodestring(
                plistlib.writePlistToString(entry.extra_data).encode("zlib")).replace('\n', '')
            output_str += "# {uuid}\n{body}\n\n{day_one_marker}{day_one_data}\n".format(
                uuid=entry.uuid, body=entry.__unicode__(), day_one_marker=self.DAY_ONE_EXTRA_DATA_MARKER,
                day_one_data=day_one_data)
        return output_str

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
                current_entry = Entry.DayOneEntry(self)
                current_entry.modified = False
                current_entry.uuid = m.group(1).lower()
            else:
                try:
                    new_date = datetime.strptime(line[:date_length], self.config['timeformat'])
                    if line.endswith("*"):
                        current_entry.starred = True
                        line = line[:-1]
                    current_entry.title = line[date_length + 1:]
                    current_entry.date = new_date
                except ValueError:
                    # strptime failed to parse a date, so assume this line is part of the journal
                    # entry
                    if current_entry:
                        if line.startswith(self.DAY_ONE_EXTRA_DATA_MARKER):
                            data = line[len(self.DAY_ONE_EXTRA_DATA_MARKER):]
                            current_entry.extra_data = plistlib.readPlistFromString(base64.decodestring(data).decode("zlib"))
                        else:
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
