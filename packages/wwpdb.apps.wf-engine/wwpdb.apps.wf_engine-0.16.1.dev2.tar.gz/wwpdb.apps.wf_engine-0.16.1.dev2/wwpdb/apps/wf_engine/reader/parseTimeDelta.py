#
# Regular expression to parse a timedelta
#
# Taken from https://stackoverflow.com/questions/12075562/how-to-deal-with-time-values-over-24-hours-in-python
# Updated http://kbyanc.blogspot.com/2007/08/python-reconstructing-timedeltas-from.html
#
#
import re
from datetime import timedelta


def parseTimeDelta(s):
    """Create timedelta object representing time delta
       expressed in a string

    Takes a string in the format produced by calling str() on
    a python timedelta object and returns a timedelta instancee
    that would produce that string.

    Acceptable formats are: "X days, HH:MM:SS" or "HH:MM:SS".
    """
    if s is None:
        return None
    d = re.match(r"((?P<days>\d+) days, )?(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d+)", str(s)).groupdict(0)
    return timedelta(**dict(((key, int(value)) for key, value in d.items())))


if __name__ == "__main__":
    print(parseTimeDelta("24:00:00"))
    print(parseTimeDelta("24:00:00").total_seconds())
    print(parseTimeDelta("28:32:12"))
