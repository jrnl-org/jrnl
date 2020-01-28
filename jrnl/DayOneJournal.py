#!/usr/bin/env python

from . import Entry
from . import Journal
from . import time as jrnl_time
import os
import re
from datetime import datetime
import time
import fnmatch
import plistlib
import pytz
import uuid
import tzlocal
from xml.parsers.expat import ExpatError


class DayOne(Journal.Journal):
    """A special Journal handling DayOne files"""

    # InvalidFileException was added to plistlib in Python3.4
    PLIST_EXCEPTIONS = (
        (ExpatError, plistlib.InvalidFileException)
        if hasattr(plistlib, "InvalidFileException")
        else ExpatError
    )

    def __init__(self, **kwargs):
        self.entries = []
        self._deleted_entries = []
        super().__init__(**kwargs)

    def open(self):
        filenames = [
            os.path.join(self.config["journal"], "entries", f)
            for f in os.listdir(os.path.join(self.config["journal"], "entries"))
        ]
        filenames = []
        for root, dirnames, f in os.walk(self.config["journal"]):
            for filename in fnmatch.filter(f, "*.doentry"):
                filenames.append(os.path.join(root, filename))
        self.entries = []
        for filename in filenames:
            with open(filename, "rb") as plist_entry:
                try:
                    dict_entry = plistlib.readPlist(plist_entry)
                except self.PLIST_EXCEPTIONS:
                    pass
                else:
                    try:
                        timezone = pytz.timezone(dict_entry["Time Zone"])
                    except (KeyError, pytz.exceptions.UnknownTimeZoneError):
                        timezone = tzlocal.get_localzone()
                    date = dict_entry["Creation Date"]
                    # convert the date to UTC rather than keep messing with
                    # timezones
                    if timezone.zone != "UTC":
                        date = date + timezone.utcoffset(date, is_dst=False)

                    entry = Entry.Entry(
                        self,
                        date,
                        text=dict_entry["Entry Text"],
                        starred=dict_entry["Starred"],
                    )
                    entry.uuid = dict_entry["UUID"]
                    entry._tags = [
                        self.config["tagsymbols"][0] + tag.lower()
                        for tag in dict_entry.get("Tags", [])
                    ]

                    self.entries.append(entry)
        self.sort()
        return self

    def write(self):
        """Writes only the entries that have been modified into plist files."""
        for entry in self.entries:
            if entry.modified:
                utc_time = datetime.utcfromtimestamp(
                    time.mktime(entry.date.timetuple())
                )

                if not hasattr(entry, "uuid"):
                    entry.uuid = uuid.uuid1().hex

                filename = os.path.join(
                    self.config["journal"], "entries", entry.uuid.upper() + ".doentry"
                )

                entry_plist = {
                    "Creation Date": utc_time,
                    "Starred": entry.starred if hasattr(entry, "starred") else False,
                    "Entry Text": entry.title + "\n" + entry.body,
                    "Time Zone": str(tzlocal.get_localzone()),
                    "UUID": entry.uuid.upper(),
                    "Tags": [
                        tag.strip(self.config["tagsymbols"]).replace("_", " ")
                        for tag in entry.tags
                    ],
                }
                plistlib.writePlist(entry_plist, filename)
        for entry in self._deleted_entries:
            filename = os.path.join(
                self.config["journal"], "entries", entry.uuid + ".doentry"
            )
            os.remove(filename)

    def editable_str(self):
        """Turns the journal into a string of entries that can be edited
        manually and later be parsed with eslf.parse_editable_str."""
        return "\n".join([f"# {e.uuid}\n{str(e)}" for e in self.entries])

    def parse_editable_str(self, edited):
        """Parses the output of self.editable_str and updates its entries."""
        # Method: create a new list of entries from the edited text, then match
        # UUIDs of the new entries against self.entries, updating the entries
        # if the edited entries differ, and deleting entries from self.entries
        # if they don't show up in the edited entries anymore.

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
                date_blob_re = re.compile("^\\[[^\\]]+\\] ")
                date_blob = date_blob_re.findall(line)
                if date_blob:
                    date_blob = date_blob[0]
                    new_date = jrnl_time.parse(date_blob.strip(" []"))
                    if line.endswith("*"):
                        current_entry.starred = True
                        line = line[:-1]
                    current_entry.title = line[len(date_blob) - 1 :]
                    current_entry.date = new_date
                elif current_entry:
                    current_entry.body += line + "\n"

        # Append last entry
        if current_entry:
            entries.append(current_entry)

        # Now, update our current entries if they changed
        for entry in entries:
            entry._parse_text()
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
