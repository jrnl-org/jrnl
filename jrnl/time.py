# Copyright © 2012-2022 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import datetime

FAKE_YEAR = 9999
DEFAULT_FUTURE = datetime.datetime(FAKE_YEAR, 12, 31, 23, 59, 59)
DEFAULT_PAST = datetime.datetime(FAKE_YEAR, 1, 1, 0, 0)


def __get_pdt_calendar():
    try:
        import parsedatetime.parsedatetime_consts as pdt
    except ImportError:
        import parsedatetime as pdt

    consts = pdt.Constants(usePyICU=False)
    consts.DOWParseStyle = -1  # "Monday" will be either today or the last Monday
    calendar = pdt.Calendar(consts)

    return calendar


def parse(
    date_str, inclusive=False, default_hour=None, default_minute=None, bracketed=False
):
    """Parses a string containing a fuzzy date and returns a datetime.datetime object"""
    if not date_str:
        return None
    elif isinstance(date_str, datetime.datetime):
        return date_str

    # Don't try to parse anything with 6 or less characters and was parsed from the existing journal.
    # It's probably a markdown footnote
    if len(date_str) <= 6 and bracketed:
        return None

    default_date = DEFAULT_FUTURE if inclusive else DEFAULT_PAST
    date = None
    year_present = False
    while not date:
        try:
            from dateutil.parser import parse as dateparse

            date = dateparse(date_str, default=default_date)
            if date.year == FAKE_YEAR:
                date = datetime.datetime(
                    datetime.datetime.now().year, date.timetuple()[1:6]
                )
            else:
                year_present = True
            flag = 1 if date.hour == date.minute == 0 else 2
            date = date.timetuple()
        except Exception as e:
            if e.args[0] == "day is out of range for month":
                y, m, d, H, M, S = default_date.timetuple()[:6]
                default_date = datetime.datetime(y, m, d - 1, H, M, S)
            else:
                calendar = __get_pdt_calendar()
                date, flag = calendar.parse(date_str)

    if not flag:  # Oops, unparsable.
        try:  # Try and parse this as a single year
            year = int(date_str)
            return datetime.datetime(year, 1, 1)
        except ValueError:
            return None
        except TypeError:
            return None

    if flag == 1:  # Date found, but no time. Use the default time.
        date = datetime.datetime(
            *date[:3],
            hour=23 if inclusive else default_hour or 0,
            minute=59 if inclusive else default_minute or 0,
            second=59 if inclusive else 0
        )
    else:
        date = datetime.datetime(*date[:6])

    # Ugly heuristic: if the date is more than 4 weeks in the future, we got the year wrong.
    # Rather then this, we would like to see parsedatetime patched so we can tell it to prefer
    # past dates
    dt = datetime.datetime.now() - date
    if dt.days < -28 and not year_present:
        date = date.replace(date.year - 1)
    return date
