# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import datetime

from jrnl.journals import Journal


def test_text_above_first_entry_is_kept():
    journal = Journal()

    entries = journal._parse("buy milk\n\n[2026-10-10 01:15] test\n")

    assert [entry.title for entry in entries] == ["buy milk", "test"]
    assert entries[0].date.date() == datetime.date.today()
