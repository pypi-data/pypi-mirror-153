##
# File:    TaskComparitor.py
#
# Updates:
#
#  3-May-2015   jdw rewritten  -
#
##

"""
TaskComparitor() handles comparisons for SwitchTask()
"""

import sys


class TaskComparitor(object):
    def __init__(self, debug=0, prt=sys.stderr):  # pylint: disable=unused-argument

        self.__dataId = None
        self.min = 0
        self.max = 0
        self.lower = ">"
        self.upper = "<"
        self.logical = False
        self.string = None
        self.__compareCode = None
        self.__compareAs = None

        self.debug = debug
        # self.__lfh = prt

    def addDataName(self, name):
        self.__dataId = name

    def getDataName(self):
        return self.__dataId

    def __applyType(self, compareAs, sValue):
        if compareAs not in ["int", "integer"]:
            lData = int(sValue)
        elif compareAs in ["float", "double"]:
            lData = float(sValue)
        elif compareAs in ["string", "substring"]:
            lData = str(sValue)
        else:
            lData = int(sValue)
        return lData

    def addData(self, compareCode, data, mode="<", compareAs="integer"):
        self.__compareCode = compareCode
        self.__compareAs = compareAs
        if compareAs in ["int", "integer"]:
            lData = int(data)
        elif compareAs in ["float", "double"]:
            lData = float(data)
        elif compareAs in ["string", "substring"]:
            lData = str(data)
        else:
            lData = int(data)

        if compareCode == -1:
            self.min = lData
            self.lower = mode
        elif compareCode == 1:
            self.max = lData
            self.upper = mode
        elif compareCode == 0:
            self.min = lData
            self.max = lData
            self.lower = mode
            self.upper = mode
        elif compareCode == 88:
            if data.lower() == "true" or data.lower() == "ok":
                self.logical = False
            else:
                self.logical = True
        elif compareCode in [77, 78, 55, 56]:
            self.string = str(data)

    def check(self, value):
        if self.__compareCode in [-1, 1, 0]:
            ret = self.__checkValue(value)
        elif self.__compareCode in [88]:
            ret = self.__checkBoolean(value)
        elif self.__compareCode in [77]:
            ret = self.__checkString(value)
        elif self.__compareCode in [78]:
            ret = self.__checkSubString(value)  # XX Not implemented yet  pylint: disable=no-member
        elif self.__compareCode in [55]:
            ret = self.__checkStringInList(value)
        elif self.__compareCode in [56]:
            ret = self.__checkSubStringInList(value)
        else:
            ret = 0
        return ret

    def printMe(self, lfh):
        lfh.write("+taskFunction.printMe()  min %s max %s lower %s upper %s\n" % (self.min, self.max, self.lower, self.upper))
        lfh.write(
            "+taskFunction.printMe()  dataId %s compare code %r compareAs %s logical %r string %s\n"
            % (self.__dataId, self.__compareCode, self.__compareAs, self.logical, self.string)
        )

    def __checkBoolean(self, value):
        if value:
            if self.logical:
                return 1
            else:
                return 0
        else:
            if self.logical:
                return 0
            else:
                return 1

    def __checkString(self, value):

        if value is None:
            if self.string.lower() == "none":
                return 1
            else:
                return 0

        if str(value).lower() == self.string.lower():
            return 1
        else:
            return 0

    def __checkStringInList(self, valList):

        if valList is None:
            return 0
        if not isinstance(valList, list):
            return 0
        try:
            for val in valList:
                if str(self.string).lower() == str(val).lower():
                    return 1
            return 0
        except:  # noqa: E722 pylint: disable=bare-except
            return 0

    def __checkSubStringInList(self, valList):
        if valList is None:
            return 0
        if not isinstance(valList, list):
            return 0
        try:
            for val in valList:
                if str(self.string).lower() in str(val).lower():
                    return 1
            return 0
        except:  # noqa: E722 pylint: disable=bare-except
            return 0

    def __checkValue(self, sValue):

        value = self.__applyType(self.__compareAs, sValue)

        if self.lower == ">" and self.upper == "<":
            if value > self.min and value < self.max:
                return 1
            else:
                return 0
        elif self.lower == ">=" and self.upper == "<":
            if value >= self.min and value < self.max:
                return 1
            else:
                return 0
        elif self.lower == ">" and self.upper == "<=":
            if value > self.min and value <= self.max:
                return 1
            else:
                return 0
        elif self.lower == ">=" and self.upper == "<=":
            if value >= self.min and value <= self.max:
                return 1
            else:
                return 0
        elif self.lower == "==" and self.upper == "==":
            if value == self.min and value == self.max:
                return 1
            else:
                return 0
        elif self.lower == "!=" and self.upper == "!=":
            if value == self.min and value == self.max:
                return 0
            else:
                return 1

        else:
            return 0
