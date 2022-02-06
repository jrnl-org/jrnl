import pytest

from jrnl.exception import JrnlException
from jrnl.exception import JrnlExceptionMessage
from jrnl.plugins.fancy_exporter import check_provided_linewrap_viability


@pytest.fixture()
def datestr():
    yield "2020-10-20 16:59"


def build_card_header(datestr):
    top_left_corner = "┎─╮"
    content = top_left_corner + datestr
    return content


class TestFancy:
    def test_too_small_linewrap(self, datestr):

        journal = "test_journal"
        content = build_card_header(datestr)

        total_linewrap = 12

        with pytest.raises(JrnlException) as e:
            check_provided_linewrap_viability(total_linewrap, [content], journal)
        assert (
            e.value.exception_msg == JrnlExceptionMessage.LineWrapTooSmallForDateFormat
        )
