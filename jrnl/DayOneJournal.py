# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import datetime
import fnmatch
import os
import platform
import plistlib
import re
import socket
import time
import uuid
import zoneinfo
from pathlib import Path
from xml.parsers.expat import ExpatError

import tzlocal

from jrnl import Entry
from jrnl import Journal
from jrnl import __title__
from jrnl import __version__


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
        self.can_be_encrypted = False
        super().__init__(**kwargs)

    def open(self):
        filenames = []
        for root, dirnames, f in os.walk(self.config["journal"]):
            for filename in fnmatch.filter(f, "*.doentry"):
                filenames.append(os.path.join(root, filename))
        self.entries = []
        for filename in filenames:
            with open(filename, "rb") as plist_entry:
                try:
                    dict_entry = plistlib.load(plist_entry, fmt=plistlib.FMT_XML)
                except self.PLIST_EXCEPTIONS:
                    pass
                else:
                    try:
                        timezone = zoneinfo.ZoneInfo(dict_entry["Time Zone"])
                    except KeyError:
                        timezone_name = str(tzlocal.get_localzone())
                        timezone = zoneinfo.ZoneInfo(timezone_name)
                    date = dict_entry["Creation Date"]
                    # convert the date to UTC rather than keep messing with
                    # timezones
                    if timezone.key != "UTC":
                        date = date.replace(fold=1) + timezone.utcoffset(date)

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

                    """Extended DayOne attributes"""
                    try:
                        entry.creator_device_agent = dict_entry["Creator"][
                            "Device Agent"
                        ]
                    except:  # noqa: E722
                        pass
                    try:
                        entry.creator_generation_date = dict_entry["Creator"][
                            "Generation Date"
                        ]
                    except:  # noqa: E722
                        entry.creator_generation_date = date
                    try:
                        entry.creator_host_name = dict_entry["Creator"]["Host Name"]
                    except:  # noqa: E722
                        pass
                    try:
                        entry.creator_os_agent = dict_entry["Creator"]["OS Agent"]
                    except:  # noqa: E722
                        pass
                    try:
                        entry.creator_software_agent = dict_entry["Creator"][
                            "Software Agent"
                        ]
                    except:  # noqa: E722
                        pass
                    try:
                        entry.location = dict_entry["Location"]
                    except:  # noqa: E722
                        pass
                    try:
                        entry.weather = dict_entry["Weather"]
                    except:  # noqa: E722
                        pass
                    self.entries.append(entry)
        self.sort()
        return self

    def write(self):
        """Writes only the entries that have been modified into plist files."""
        for entry in self.entries:
            if entry.modified:
                utc_time = datetime.datetime.utcfromtimestamp(
                    time.mktime(entry.date.timetuple())
                )

                if not hasattr(entry, "uuid"):
                    entry.uuid = uuid.uuid1().hex
                if not hasattr(entry, "creator_device_agent"):
                    entry.creator_device_agent = ""  # iPhone/iPhone5,3
                if not hasattr(entry, "creator_generation_date"):
                    entry.creator_generation_date = utc_time
                if not hasattr(entry, "creator_host_name"):
                    entry.creator_host_name = socket.gethostname()
                if not hasattr(entry, "creator_os_agent"):
                    entry.creator_os_agent = "{}/{}".format(
                        platform.system(), platform.release()
                    )
                if not hasattr(entry, "creator_software_agent"):
                    entry.creator_software_agent = "{}/{}".format(
                        __title__, __version__
                    )

                fn = (
                    Path(self.config["journal"])
                    / "entries"
                    / (entry.uuid.upper() + ".doentry")
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
                    "Creator": {
                        "Device Agent": entry.creator_device_agent,
                        "Generation Date": entry.creator_generation_date,
                        "Host Name": entry.creator_host_name,
                        "OS Agent": entry.creator_os_agent,
                        "Software Agent": entry.creator_software_agent,
                    },
                }
                if hasattr(entry, "location"):
                    entry_plist["Location"] = entry.location
                if hasattr(entry, "weather"):
                    entry_plist["Weather"] = entry.weather

                # plistlib expects a binary object
                with fn.open(mode="wb") as f:
                    plistlib.dump(entry_plist, f, fmt=plistlib.FMT_XML, sort_keys=False)

        for entry in self._deleted_entries:
            filename = os.path.join(
                self.config["journal"], "entries", entry.uuid + ".doentry"
            )
            os.remove(filename)

    def editable_str(self):
        """Turns the journal into a string of entries that can be edited
        manually and later be parsed with eslf.parse_editable_str."""
        return "\n".join([f"{str(e)}\n# {e.uuid}\n" for e in self.entries])

    def _update_old_entry(self, entry, new_entry):
        for attr in ("title", "body", "date"):
            old_attr = getattr(entry, attr)
            new_attr = getattr(new_entry, attr)
            if old_attr != new_attr:
                entry.modified = True
                setattr(entry, attr, new_attr)

    def _get_and_remove_uuid_from_entry(self, entry):
        uuid_regex = "^ *?# ([a-zA-Z0-9]+) *?$"
        m = re.search(uuid_regex, entry.body, re.MULTILINE)
        entry.uuid = m.group(1) if m else None

        # remove the uuid from the body
        entry.body = re.sub(uuid_regex, "", entry.body, flags=re.MULTILINE, count=1)
        entry.body = entry.body.rstrip()

        return entry

    def parse_editable_str(self, edited):
        """Parses the output of self.editable_str and updates its entries."""
        # Method: create a new list of entries from the edited text, then match
        # UUIDs of the new entries against self.entries, updating the entries
        # if the edited entries differ, and deleting entries from self.entries
        # if they don't show up in the edited entries anymore.
        entries_from_editor = self._parse(edited)

        for entry in entries_from_editor:
            entry = self._get_and_remove_uuid_from_entry(entry)

        # Remove deleted entries
        edited_uuids = [e.uuid for e in entries_from_editor]
        self._deleted_entries = [e for e in self.entries if e.uuid not in edited_uuids]
        self.entries[:] = [e for e in self.entries if e.uuid in edited_uuids]

        for entry in entries_from_editor:
            for old_entry in self.entries:
                if entry.uuid == old_entry.uuid:
                    self._update_old_entry(old_entry, entry)
                    break
