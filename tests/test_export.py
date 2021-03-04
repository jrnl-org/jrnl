from jrnl.exception import JrnlError
from jrnl.plugins.fancy_exporter import FancyExporter


import pytest


@pytest.fixture()
def datestr():

    yield "2020-10-20 16:59"


from textwrap import TextWrapper


def provide_date_wrapper(initial_linewrap):
    wrapper = TextWrapper(
        width=initial_linewrap, initial_indent=" ", subsequent_indent=" "
    )
    return wrapper


def build_card_header(datestr):
    top_left_corner = "┎─╮"
    content = top_left_corner + datestr
    return content


class TestFancy:
    def test_too_small_linewrap(self, datestr):

        content = build_card_header(datestr)

        total_linewrap = 12

        with pytest.raises(JrnlError) as e:
            FancyExporter.check_linewrap(total_linewrap, [content])
        assert e.value.error_type == "LineWrapTooSmallForDateFormat"
