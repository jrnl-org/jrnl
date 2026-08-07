# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import datetime

import pytest

from jrnl import time


def test_default_hour_is_added():
    assert time.parse(
        "2020-06-20", inclusive=False, default_hour=9, default_minute=0, bracketed=False
    ) == datetime.datetime(2020, 6, 20, 9)


def test_default_minute_is_added():
    assert time.parse(
        "2020-06-20",
        inclusive=False,
        default_hour=0,
        default_minute=30,
        bracketed=False,
    ) == datetime.datetime(2020, 6, 20, 0, 30)


@pytest.mark.parametrize(
    "inputs",
    [
        [2000, 2, 29, True],
        [2023, 1, 0, False],
        [2023, 1, 1, True],
        [2023, 4, 31, False],
        [2023, 12, 31, True],
        [2023, 12, 32, False],
        [2023, 13, 1, False],
        [2100, 2, 27, True],
        [2100, 2, 28, True],
        [2100, 2, 29, False],
    ],
)
def test_is_valid_date(inputs):
    year, month, day, expected_result = inputs
    assert time.is_valid_date(year, month, day) == expected_result


@pytest.mark.parametrize(
    "inputs",
    [
        [datetime.timedelta(seconds=30), "just now"],
        [datetime.timedelta(minutes=1), "1 minute ago"],
        [datetime.timedelta(minutes=5), "5 minutes ago"],
        [datetime.timedelta(hours=1), "1 hour ago"],
        [datetime.timedelta(hours=3), "3 hours ago"],
        [datetime.timedelta(days=1), "1 day ago"],
        [datetime.timedelta(days=6), "6 days ago"],
        [datetime.timedelta(weeks=1), "1 week ago"],
        [datetime.timedelta(weeks=3), "3 weeks ago"],
        [datetime.timedelta(days=30), "1 month ago"],
        [datetime.timedelta(days=365), "1 year ago"],
        [datetime.timedelta(days=730), "2 years ago"],
    ],
)
def test_relative_time_past(inputs):
    delta, expected_result = inputs
    now = datetime.datetime(2023, 6, 15, 12, 0, 0)
    assert time.relative_time(now - delta, now=now) == expected_result


@pytest.mark.parametrize(
    "inputs",
    [
        [datetime.timedelta(seconds=30), "just now"],
        [datetime.timedelta(minutes=5), "in 5 minutes"],
        [datetime.timedelta(hours=3), "in 3 hours"],
        [datetime.timedelta(days=1), "in 1 day"],
        [datetime.timedelta(days=365), "in 1 year"],
    ],
)
def test_relative_time_future(inputs):
    delta, expected_result = inputs
    now = datetime.datetime(2023, 6, 15, 12, 0, 0)
    assert time.relative_time(now + delta, now=now) == expected_result
