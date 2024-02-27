# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from collections import Counter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from jrnl.journals import Journal


"""https://stackoverflow.com/a/74873621/8740440"""
class NestedDict(dict):
    def __missing__(self, x):
        self[x] = NestedDict()
        return self[x]


def get_tags_count(journal: "Journal") -> set[tuple[int, str]]:
    """Returns a set of tuples (count, tag) for all tags present in the journal."""
    # Astute reader: should the following line leave you as puzzled as me the first time
    # I came across this construction, worry not and embrace the ensuing moment of
    # enlightment.
    tags = [tag for entry in journal.entries for tag in set(entry.tags)]
    # To be read: [for entry in journal.entries: for tag in set(entry.tags): tag]
    tag_counts = {(tags.count(tag), tag) for tag in tags}
    return tag_counts


def oxford_list(lst: list) -> str:
    """Return Human-readable list of things obeying the object comma)"""
    lst = sorted(lst)
    if not lst:
        return "(nothing)"
    elif len(lst) == 1:
        return lst[0]
    elif len(lst) == 2:
        return lst[0] + " or " + lst[1]
    else:
        return ", ".join(lst[:-1]) + ", or " + lst[-1]


def get_journal_frequency_nested(journal: "Journal") -> NestedDict:
    """Returns a NestedDict of the form {year: {month: {day: count}}}"""
    journal_frequency = NestedDict()
    for entry in journal.entries:
        date = entry.date.date()
        if date.day in journal_frequency[date.year][date.month]:
            journal_frequency[date.year][date.month][date.day] += 1
        else:
            journal_frequency[date.year][date.month][date.day] = 1

    return journal_frequency


def get_journal_frequency_one_level(journal: "Journal") -> Counter:
    """Returns a Counter of the form {date (YYYY-MM-DD): count}"""
    date_counts = Counter()
    for entry in journal.entries:
        # entry.date.date() gets date without time
        date = str(entry.date.date())
        date_counts[date] += 1
    return date_counts
