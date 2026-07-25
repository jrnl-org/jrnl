# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import pytest

from jrnl.journals.DayOneJournal import DayOne


@pytest.mark.parametrize("tagsymbol", ["#", "@"])
def test_filter_matches_any_configured_tagsymbol(tagsymbol):
    journal = DayOne(
        name="dayone",
        journal="tests/data/journals/dayone.dayone",
        tagsymbols="#@",
    )
    journal.open()
    journal.filter(tags=[tagsymbol + "work"])

    assert len(journal.entries) == 1
