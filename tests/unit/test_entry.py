# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from unittest.mock import Mock

from jrnl.journals import Entry


def _entry(text: str, tagsymbols: str = "#@") -> Entry:
    journal = Mock()
    journal.config = {"tagsymbols": tagsymbols}
    return Entry(journal, text=text)


def test_tags_ignores_runs_made_up_only_of_tagsymbols():
    # A markdown heading such as "###" is punctuation, not a tag.
    entry = _entry("@@\n##\n@#@\n#@#\n#@#@#\n@#@#@\n###\n@@@\n####")
    assert entry.tags == []


def test_tags_parses_real_tags_alongside_tagsymbol_runs():
    entry = _entry("## Notes\nTalked about #python with @alice")
    assert sorted(entry.tags) == ["#python", "@alice"]


def test_tags_keeps_tags_that_merely_contain_a_tagsymbol():
    entry = _entry("Filed under #abc#def")
    assert entry.tags == ["#abc#def"]
