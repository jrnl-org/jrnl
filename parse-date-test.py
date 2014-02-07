"""Parses a string containing a fuzzy date and returns a datetime.datetime object"""

from datetime import datetime
import dateutil
import argparse
try: import parsedatetime.parsedatetime_consts as pdt
except ImportError: import parsedatetime as pdt

parser = argparse.ArgumentParser()
parser.add_argument('-i', default='today')
parser.add_argument('-f', default=None)
args = parser.parse_args()
print "args: " + str(args)
date_str = args.i
end_flag = args.f

# Set up date parser
consts = pdt.Constants(usePyICU=False)
consts.DOWParseStyle = -1  # "Monday" will be either today or the last Monday
dateparse = pdt.Calendar(consts)

if not date_str:
    print "Nothing supplied"
    # return None
elif isinstance(date_str, datetime):
    print date_str
    # return date_str

try:
    date = dateutil.parser.parse(date_str)
    flag = 1 if date.hour == 0 and date.minute == 0 else 2
    date = date.timetuple()
except:
    date, flag = dateparse.parse(date_str)

if not flag:  # Oops, unparsable.
    try:  # Try and parse this as a single year
        year = int(date_str)
        print datetime(year, 1, 1)
        # return datetime(year, 1, 1)
    except ValueError:
        print "return None"
        # return None
    except TypeError:
        print "return None"
        # return None

if flag is 1:  # Date found, but no time. Use the default time.
    if end_flag == "from":
        date = datetime(*date[:3], hour=0, minute=0)
    elif end_flag == "to":
        date = datetime(*date[:3], hour=23, minute=59, second=59)
    else:
        # Use the default time.
        date = datetime(*date[:3], hour=9, minute=1)
else:
    date = datetime(*date[:6])

# Ugly heuristic: if the date is more than 4 weeks in the future, we got the year wrong.
# Rather then this, we would like to see parsedatetime patched so we can tell it to prefer
# past dates
dt = datetime.now() - date
if dt.days < -28:
    date = date.replace(date.year - 1)

print date
# return date