# Copyright © 2012-2023 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

import datetime

FAKE_YEAR = 9999
DEFAULT_FUTURE = datetime.datetime(FAKE_YEAR, 12, 31, 23, 59, 59)
DEFAULT_PAST = datetime.datetime(FAKE_YEAR, 1, 1, 0, 0)


def __get_pdt_calendar():
    import parsedatetime as pdt

    consts = pdt.Constants(usePyICU=False)
    consts.DOWParseStyle = -1  # "Monday" will be either today or the last Monday
    calendar = pdt.Calendar(consts, version=pdt.VERSION_CONTEXT_STYLE)

    return calendar


def parse(
    date_str: str | datetime.datetime,
    inclusive: bool = False,
    default_hour: int | None = None,
    default_minute: int | None = None,
    bracketed: bool = False,
) -> datetime.datetime | None:
    """Parses a string containing a fuzzy date and returns a datetime.datetime object"""
    if not date_str:
        logger.info(f'Condition in body log is: (not date_str) is True') # STRUDEL_LOG tedc
        return None
    elif isinstance(date_str, datetime.datetime):
        logger.info(f'Condition in body log is: isinstance( date_str datetime.datetime)') # STRUDEL_LOG idcg
        return date_str

    # Don't try to parse anything with 6 or fewer characters and was parsed from the
    # existing journal. It's probably a markdown footnote
    if len(date_str) <= 6 and bracketed:
        logger.info(f'Condition in body log is: len( date_str) <= 6 BoolOp bracketed') # STRUDEL_LOG nujw
        return None

    default_date = DEFAULT_FUTURE if inclusive else DEFAULT_PAST
    date = None
    year_present = False

    hasTime = False
    hasDate = False

    while not date:
        try:
            from dateutil.parser import parse as dateparse

            date = dateparse(date_str, default=default_date)
            if date.year == FAKE_YEAR:
                logger.info(f'Condition in body log is: date.year = FAKE_YEAR') # STRUDEL_LOG axfv
                date = datetime.datetime(
                    datetime.datetime.now().year, date.timetuple()[1:6]
                )
            else:
                year_present = True
            hasTime = not (date.hour == date.minute == 0)
            hasDate = True
            date = date.timetuple()
        except Exception as e:
            if e.args[0] == "day is out of range for month":
                logger.info(f'Condition in body log is: e.args[0] = "day is out of range for month"') # STRUDEL_LOG janj
                y, m, d, H, M, S = default_date.timetuple()[:6]
                default_date = datetime.datetime(y, m, d - 1, H, M, S)
            else:
                calendar = __get_pdt_calendar()
                date, parse_context = calendar.parse(date_str)
                hasTime = parse_context.hasTime
                hasDate = parse_context.hasDate

    if not hasDate and not hasTime:
        logger.info(f'Condition in body log is: (not hasDate) is True BoolOp (not hasTime) is True') # STRUDEL_LOG onqx
        try:  # Try and parse this as a single year
            year = int(date_str)
            return datetime.datetime(year, 1, 1)
        except ValueError:
            return None
        except TypeError:
            return None

    if hasDate and not hasTime:
        logger.info(f'Condition in body log is: hasDate BoolOp (not hasTime) is True') # STRUDEL_LOG uzyb
        date = datetime.datetime(  # Use the default time
            *date[:3],
            hour=23 if inclusive else default_hour or 0,
            minute=59 if inclusive else default_minute or 0,
            second=59 if inclusive else 0
        )
    else:
        date = datetime.datetime(*date[:6])

    # Ugly heuristic: if the date is more than 4 weeks in the future, we got the year
    # wrong. Rather than this, we would like to see parsedatetime patched so we can
    # tell it to prefer past dates
    dt = datetime.datetime.now() - date
    if dt.days < -28 and not year_present:
        logger.info(f'Condition in body log is: dt.days < UnaryOp 28 BoolOp (not year_present) is True') # STRUDEL_LOG eodx
        date = date.replace(date.year - 1)
    return date


def is_valid_date(year: int, month: int, day: int) -> bool:
    try:
        datetime.datetime(year, month, day)
        return True
    except ValueError:
        return False