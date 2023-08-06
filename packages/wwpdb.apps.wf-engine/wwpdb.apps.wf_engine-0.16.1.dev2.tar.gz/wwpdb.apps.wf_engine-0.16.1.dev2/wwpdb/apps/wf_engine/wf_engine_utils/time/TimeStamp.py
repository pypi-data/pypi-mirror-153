##
# File: TimeStamp.py
# Date: 4-Mar-2015
#
# Updates:
#   13-Apr-2015 - Added daylight time offset to correct for this.
#                 The manner of TZ incorporation does
#
#
##
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.07"

import time
import datetime
from dateutil import tz
from decimal import Decimal


class TimeStamp(object):
    def __init__(self, refDate="2000-01-01 00:00:00"):
        self.__useTz = True
        self.__refDate = refDate

        datetime_obj = datetime.datetime.strptime(self.__refDate, "%Y-%m-%d %H:%M:%S")

        if self.__useTz:
            utctz = tz.tzutc()
            self.__referenceDate = datetime_obj.replace(tzinfo=utctz)
        else:
            self.__referenceDate = datetime_obj

        self.__dstOffset = -self.__isDST() * 3600.0

    def __isDST(self):
        """Return 1 if the local TZ is on daylight time or 0 otherwise."""
        return time.localtime().tm_isdst

    def getTimeReference(self):
        """Return the datetime object for the time reference"""
        return self.__referenceDate

    def getSecondsFromReference(self):
        """Return the number of seconds since the time reference with micosecond precision."""
        if self.__useTz:
            utctz = tz.tzutc()
            tNow = datetime.datetime.utcnow().replace(tzinfo=utctz)
        else:
            tNow = datetime.datetime.utcnow()
        c = tNow - self.__referenceDate
        seconds = ((c.days * 24 * 60 * 60 + c.seconds) * 1000000 + c.microseconds) / 1000000.0
        return Decimal(repr(seconds))

    def getSecondsFromEpoc(self, secondsFromReference):
        """Return the number of seconds since the Epoc.

        Input: microseconds since the reference date (self.__referenceDate)
        """

        ref = time.mktime(self.__referenceDate.timetuple())
        d = float(ref) + float(secondsFromReference)
        return d

    def getTimeStringUTC(self, secondsFromReference):
        """Return the formatted time string in the UTC

        Input: seconds since the reference date (self.__referenceDate)
        """
        if secondsFromReference is None:
            return ""
        ref = time.mktime(self.__referenceDate.timetuple())

        fmt = "%Y-%m-%d %H:%M:%S %Z%z"

        d = float(ref) + float(secondsFromReference) + self.__dstOffset
        return datetime.datetime.fromtimestamp(int(d)).strftime(fmt)

    def getTimeStringLocal(self, secondsFromReference):
        """Return the formatted time string in the local time zone.

        Input: seconds since the reference date (self.__referenceDate)
        """
        if secondsFromReference is None:
            return ""
        ltz = tz.tzlocal()
        utctz = tz.tzutc()
        ref = time.mktime(self.__referenceDate.timetuple())

        fmt = "%Y-%m-%d %H:%M:%S %Z%z"

        d = float(ref) + float(secondsFromReference) + self.__dstOffset
        dt = datetime.datetime.fromtimestamp(int(d))
        dt = dt.replace(tzinfo=utctz)
        return dt.astimezone(ltz).strftime(fmt)

    def getTimeFromEpoc(self, secondsFromEpoc):
        """Return the formatted time string (UTC).

        Input: seconds since the epoc.
        """
        if secondsFromEpoc is None:
            return ""
        fmt = "%Y-%m-%d %H:%M:%S %Z%z"

        d = float(secondsFromEpoc)
        return datetime.datetime.fromtimestamp(int(d)).strftime(fmt)


if __name__ == "__main__":
    #
    tS = TimeStamp()
    print("getSecondsFromReference() %s" % tS.getSecondsFromReference())
    print("UTC (0)  %s" % tS.getTimeStringUTC(0.0))
    print("UTC (now)  %s" % tS.getTimeStringUTC(tS.getSecondsFromReference()))
    print("Local now  %s" % tS.getTimeStringLocal(tS.getSecondsFromReference()))
    #
    tS = TimeStamp()
    print("getSecondsFromReference() %s" % tS.getSecondsFromReference())
    print("getSecondsFromEpoc() %s" % tS.getSecondsFromEpoc(tS.getSecondsFromReference()))
    #
    print("tS.getTimeStringLocal(0) %s" % tS.getTimeStringLocal(0))
    print("tS.getTimeStringLocal(3600*24) %s" % tS.getTimeStringLocal(3600 * 24))
    print("")
    print("tS.getTimeStringUTC(0) %s" % tS.getTimeStringUTC(0))
    print("tS.getTimeStringUTC(3600*24) %s" % tS.getTimeStringUTC(3600 * 24))
