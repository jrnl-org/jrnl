# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html


def get_tags_count(journal):
    """Returns a set of tuples (count, tag) for all tags present in the journal."""
    # Astute reader: should the following line leave you as puzzled as me the first time
    # I came across this construction, worry not and embrace the ensuing moment of enlightment.
    tags = [tag for entry in journal.entries for tag in set(entry.tags)]
    # To be read: [for entry in journal.entries: for tag in set(entry.tags): tag]
    tag_counts = {(tags.count(tag), tag) for tag in tags}
    return tag_counts


def oxford_list(lst):
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
