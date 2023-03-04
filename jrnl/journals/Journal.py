# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import datetime
import logging
import os
import re

from jrnl import time
from jrnl.config import validate_journal_name
from jrnl.encryption import determine_encryption_method
from jrnl.messages import Message
from jrnl.messages import MsgStyle
from jrnl.messages import MsgText
from jrnl.output import print_msg
from jrnl.path import expand_path
from jrnl.prompt import yesno

from .Entry import Entry


class Tag:
    def __init__(self, name, count=0):
        self.name = name
        self.count = count

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<Tag '{self.name}'>"


class Journal:
    def __init__(self, name="default", **kwargs):
        self.config = {
            "journal": "journal.txt",
            "encrypt": False,
            "default_hour": 9,
            "default_minute": 0,
            "timeformat": "%Y-%m-%d %H:%M",
            "tagsymbols": "@",
            "highlight": True,
            "linewrap": 80,
            "indent_character": "|",
        }
        self.config.update(kwargs)
        # Set up date parser
        self.search_tags = None  # Store tags we're highlighting
        self.name = name
        self.entries = []
        self.encryption_method = None

        # Track changes to journal in session. Modified is tracked in Entry
        self.added_entry_count = 0
        self.deleted_entry_count = 0

    def __len__(self):
        """Returns the number of entries"""
        return len(self.entries)

    def __iter__(self):
        """Iterates over the journal's entries."""
        return (entry for entry in self.entries)

    @classmethod
    def from_journal(cls, other: "Journal") -> "Journal":
        """Creates a new journal by copying configuration and entries from
        another journal object"""
        new_journal = cls(other.name, **other.config)
        new_journal.entries = other.entries
        logging.debug(
            "Imported %d entries from %s to %s",
            len(new_journal),
            other.__class__.__name__,
            cls.__name__,
        )
        return new_journal

    def import_(self, other_journal_txt: str) -> None:
        imported_entries = self._parse(other_journal_txt)
        for entry in imported_entries:
            entry.modified = True

        self.entries = list(frozenset(self.entries) | frozenset(imported_entries))
        self.sort()

    def _get_encryption_method(self) -> None:
        encryption_method = determine_encryption_method(self.config["encrypt"])
        self.encryption_method = encryption_method(self.name, self.config)

    def _decrypt(self, text: bytes) -> str:
        if self.encryption_method is None:
            self._get_encryption_method()

        return self.encryption_method.decrypt(text)

    def _encrypt(self, text: str) -> bytes:
        if self.encryption_method is None:
            self._get_encryption_method()

        return self.encryption_method.encrypt(text)

    def open(self, filename: str | None = None) -> "Journal":
        """Opens the journal file defined in the config and parses it into a list of Entries.
        Entries have the form (date, title, body)."""
        filename = filename or self.config["journal"]
        dirname = os.path.dirname(filename)
        if not os.path.exists(filename):
            if not os.path.isdir(dirname):
                os.makedirs(dirname)
                print_msg(
                    Message(
                        MsgText.DirectoryCreated,
                        MsgStyle.NORMAL,
                        {"directory_name": dirname},
                    )
                )
            self.create_file(filename)
            print_msg(
                Message(
                    MsgText.JournalCreated,
                    MsgStyle.NORMAL,
                    {
                        "journal_name": self.name,
                        "filename": filename,
                    },
                )
            )
            self.write()

        text = self._load(filename)
        text = self._decrypt(text)
        self.entries = self._parse(text)
        self.sort()
        logging.debug("opened %s with %d entries", self.__class__.__name__, len(self))
        return self

    def write(self, filename: str | None = None) -> None:
        """Dumps the journal into the config file, overwriting it"""
        filename = filename or self.config["journal"]
        text = self._to_text()
        text = self._encrypt(text)
        self._store(filename, text)

    def validate_parsing(self) -> bool:
        """Confirms that the jrnl is still parsed correctly after being dumped to text."""
        new_entries = self._parse(self._to_text())
        return all(entry == new_entries[i] for i, entry in enumerate(self.entries))

    @staticmethod
    def create_file(filename: str) -> None:
        with open(filename, "w"):
            pass

    def _to_text(self) -> str:
        return "\n".join([str(e) for e in self.entries])

    def _load(self, filename: str) -> bytes:
        with open(filename, "rb") as f:
            return f.read()

    def _store(self, filename: str, text: bytes) -> None:
        with open(filename, "wb") as f:
            f.write(text)

    def _parse(self, journal_txt: str) -> list[Entry]:
        """Parses a journal that's stored in a string and returns a list of entries"""

        # Return empty array if the journal is blank
        if not journal_txt:
            return []

        # Initialise our current entry
        entries = []

        date_blob_re = re.compile("(?:^|\n)\\[([^\\]]+)\\] ")
        last_entry_pos = 0
        for match in date_blob_re.finditer(journal_txt):
            date_blob = match.groups()[0]
            try:
                new_date = datetime.datetime.strptime(
                    date_blob, self.config["timeformat"]
                )
            except ValueError:
                # Passing in a date that had brackets around it
                new_date = time.parse(date_blob, bracketed=True)

            if new_date:
                if entries:
                    entries[-1].text = journal_txt[last_entry_pos : match.start()]
                last_entry_pos = match.end()
                entries.append(Entry(self, date=new_date))

        # If no entries were found, treat all the existing text as an entry made now
        if not entries:
            entries.append(Entry(self, date=time.parse("now")))

        # Fill in the text of the last entry
        entries[-1].text = journal_txt[last_entry_pos:]

        for entry in entries:
            entry._parse_text()
        return entries

    def pprint(self, short: bool = False) -> str:
        """Prettyprints the journal's entries"""
        return "\n".join([e.pprint(short=short) for e in self.entries])

    def __str__(self):
        return self.pprint()

    def __repr__(self):
        return f"<Journal with {len(self.entries)} entries>"

    def sort(self) -> None:
        """Sorts the Journal's entries by date"""
        self.entries = sorted(self.entries, key=lambda entry: entry.date)

    def limit(self, n: int | None = None) -> None:
        """Removes all but the last n entries"""
        if n:
            self.entries = self.entries[-n:]

    @property
    def tags(self) -> list[Tag]:
        """Returns a set of tuples (count, tag) for all tags present in the journal."""
        # Astute reader: should the following line leave you as puzzled as me the first time
        # I came across this construction, worry not and embrace the ensuing moment of enlightment.
        tags = [tag for entry in self.entries for tag in set(entry.tags)]
        # To be read: [for entry in journal.entries: for tag in set(entry.tags): tag]
        tag_counts = {(tags.count(tag), tag) for tag in tags}
        return [Tag(tag, count=count) for count, tag in sorted(tag_counts)]

    def filter(
        self,
        tags=[],
        month=None,
        day=None,
        year=None,
        start_date=None,
        end_date=None,
        starred=False,
        tagged=False,
        exclude_starred=False,
        exclude_tagged=False,
        strict=False,
        contains=None,
        exclude=[],
    ):
        """Removes all entries from the journal that don't match the filter.

        tags is a list of tags, each being a string that starts with one of the
        tag symbols defined in the config, e.g. ["@John", "#WorldDomination"].

        start_date and end_date define a timespan by which to filter.

        starred limits journal to starred entries

        If strict is True, all tags must be present in an entry. If false, the

        exclude is a list of the tags which should not appear in the results.
        entry is kept if any tag is present, unless they appear in exclude."""
        self.search_tags = {tag.lower() for tag in tags}
        excluded_tags = {tag.lower() for tag in exclude}
        end_date = time.parse(end_date, inclusive=True)
        start_date = time.parse(start_date)

        # If strict mode is on, all tags have to be present in entry
        has_tags = (
            self.search_tags.issubset if strict else self.search_tags.intersection
        )

        def excluded(tags):
            return 0 < len([tag for tag in tags if tag in excluded_tags])

        if contains:
            contains_lower = contains.casefold()

        # Create datetime object for comparison below
        # this approach allows various formats
        if month or day or year:
            compare_d = time.parse(f"{month or 1}.{day or 1}.{year or 1}")

        result = [
            entry
            for entry in self.entries
            if (not tags or has_tags(entry.tags))
            and (not (starred or exclude_starred) or entry.starred == starred)
            and (not (tagged or exclude_tagged) or bool(entry.tags) == tagged)
            and (not month or entry.date.month == compare_d.month)
            and (not day or entry.date.day == compare_d.day)
            and (not year or entry.date.year == compare_d.year)
            and (not start_date or entry.date >= start_date)
            and (not end_date or entry.date <= end_date)
            and (not exclude or not excluded(entry.tags))
            and (
                not contains
                or (
                    contains_lower in entry.title.casefold()
                    or contains_lower in entry.body.casefold()
                )
            )
        ]

        self.entries = result

    def delete_entries(self, entries_to_delete: list[Entry]) -> None:
        """Deletes specific entries from a journal."""
        for entry in entries_to_delete:
            self.entries.remove(entry)
            self.deleted_entry_count += 1

    def change_date_entries(
        self, date: datetime.datetime, entries_to_change: list[Entry]
    ) -> None:
        """Changes entry dates to given date."""
        date = time.parse(date)

        for entry in entries_to_change:
            entry.date = date
            entry.modified = True

    def prompt_action_entries(self, msg: MsgText) -> list[Entry]:
        """Prompts for action for each entry in a journal, using given message.
        Returns the entries the user wishes to apply the action on."""
        to_act = []

        def ask_action(entry):
            return yesno(
                Message(
                    msg,
                    params={"entry_title": entry.pprint(short=True)},
                ),
                default=False,
            )

        for entry in self.entries:
            if ask_action(entry):
                to_act.append(entry)

        return to_act

    def new_entry(self, raw: str, date=None, sort: bool = True) -> Entry:
        """Constructs a new entry from some raw text input.
        If a date is given, it will parse and use this, otherwise scan for a date in the input first.
        """

        raw = raw.replace("\\n ", "\n").replace("\\n", "\n")
        # Split raw text into title and body
        sep = re.search(r"\n|[?!.]+ +\n?", raw)
        first_line = raw[: sep.end()].strip() if sep else raw
        starred = False

        if not date:
            colon_pos = first_line.find(": ")
            if colon_pos > 0:
                date = time.parse(
                    raw[:colon_pos],
                    default_hour=self.config["default_hour"],
                    default_minute=self.config["default_minute"],
                )
                if date:  # Parsed successfully, strip that from the raw text
                    starred = raw[:colon_pos].strip().endswith("*")
                    raw = raw[colon_pos + 1 :].strip()
        starred = (
            starred
            or first_line.startswith("*")
            or first_line.endswith("*")
            or raw.startswith("*")
        )
        if not date:  # Still nothing? Meh, just live in the moment.
            date = time.parse("now")
        entry = Entry(self, date, raw, starred=starred)
        entry.modified = True
        self.entries.append(entry)
        if sort:
            self.sort()
        return entry

    def editable_str(self) -> str:
        """Turns the journal into a string of entries that can be edited
        manually and later be parsed with self.parse_editable_str."""
        return "\n".join([str(e) for e in self.entries])

    def parse_editable_str(self, edited: str) -> None:
        """Parses the output of self.editable_str and updates it's entries."""
        mod_entries = self._parse(edited)
        # Match those entries that can be found in self.entries and set
        # these to modified, so we can get a count of how many entries got
        # modified and how many got deleted later.
        for entry in mod_entries:
            entry.modified = not any(entry == old_entry for old_entry in self.entries)

        self.increment_change_counts_by_edit(mod_entries)

        self.entries = mod_entries

    def increment_change_counts_by_edit(self, mod_entries: Entry) -> None:
        if len(mod_entries) > len(self.entries):
            self.added_entry_count += len(mod_entries) - len(self.entries)
        else:
            self.deleted_entry_count += len(self.entries) - len(mod_entries)

    def get_change_counts(self) -> dict:
        return {
            "added": self.added_entry_count,
            "deleted": self.deleted_entry_count,
            "modified": len([e for e in self.entries if e.modified]),
        }


class LegacyJournal(Journal):
    """Legacy class to support opening journals formatted with the jrnl 1.x
    standard. Main difference here is that in 1.x, timestamps were not cuddled
    by square brackets. You'll not be able to save these journals anymore."""

    def _parse(self, journal_txt: str) -> list[Entry]:
        """Parses a journal that's stored in a string and returns a list of entries"""
        # Entries start with a line that looks like 'date title' - let's figure out how
        # long the date will be by constructing one
        date_length = len(datetime.datetime.today().strftime(self.config["timeformat"]))

        # Initialise our current entry
        entries = []
        current_entry = None
        new_date_format_regex = re.compile(r"(^\[[^\]]+\].*?$)")
        for line in journal_txt.splitlines():
            line = line.rstrip()
            try:
                # try to parse line as date => new entry begins
                new_date = datetime.datetime.strptime(
                    line[:date_length], self.config["timeformat"]
                )

                # parsing successful => save old entry and create new one
                if new_date and current_entry:
                    entries.append(current_entry)

                if line.endswith("*"):
                    starred = True
                    line = line[:-1]
                else:
                    starred = False

                current_entry = Entry(
                    self, date=new_date, text=line[date_length + 1 :], starred=starred
                )
            except ValueError:
                # Happens when we can't parse the start of the line as an date.
                # In this case, just append line to our body (after some
                # escaping for the new format).
                line = new_date_format_regex.sub(r" \1", line)
                if current_entry:
                    current_entry.text += line + "\n"

        # Append last entry
        if current_entry:
            entries.append(current_entry)
        for entry in entries:
            entry._parse_text()
        return entries


def open_journal(journal_name: str, config: dict, legacy: bool = False) -> Journal:
    """
    Creates a normal, encrypted or DayOne journal based on the passed config.
    If legacy is True, it will open Journals with legacy classes build for
    backwards compatibility with jrnl 1.x
    """
    logging.debug(f"open_journal '{journal_name}'")
    validate_journal_name(journal_name, config)
    config = config.copy()
    config["journal"] = expand_path(config["journal"])

    if os.path.isdir(config["journal"]):
        if config["encrypt"]:
            print_msg(
                Message(
                    MsgText.ConfigEncryptedForUnencryptableJournalType,
                    MsgStyle.WARNING,
                    {
                        "journal_name": journal_name,
                    },
                )
            )

        if config["journal"].strip("/").endswith(".dayone") or "entries" in os.listdir(
            config["journal"]
        ):
            from jrnl.journals import DayOne

            return DayOne(**config).open()
        else:
            from jrnl.journals import Folder

            return Folder(journal_name, **config).open()

    if not config["encrypt"]:
        if legacy:
            return LegacyJournal(journal_name, **config).open()
        if config["journal"].endswith(os.sep):
            from jrnl.journals import Folder

            return Folder(journal_name, **config).open()
        return Journal(journal_name, **config).open()

    if legacy:
        config["encrypt"] = "jrnlv1"
        return LegacyJournal(journal_name, **config).open()
    return Journal(journal_name, **config).open()
