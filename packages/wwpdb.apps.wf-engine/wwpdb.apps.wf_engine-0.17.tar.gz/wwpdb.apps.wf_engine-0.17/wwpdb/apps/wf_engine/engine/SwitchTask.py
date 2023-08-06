##
# File:     SwitchTask.py
#
# Original:    autoDecideTask.py
# Date:    15-Mar-2009
#
# Updates:
#  22-April-2010 : Incorporation into enterpise.
#
#   3-May-2015  jdw rewritten
#
##
"""

"""

import logging
from wwpdb.apps.wf_engine.engine.InterpretDataObject import getObjectValue
from wwpdb.apps.wf_engine.wf_engine_utils.run.MyLogger import MyLogger

logger = logging.getLogger(name="root")


class SwitchTask(object):

    """
    Handle switch/case comparison and branching workflow task
    """

    def __init__(self, task, debug=0):

        self.task = task
        self.debug = debug
        self.__lfh = MyLogger(level=logging.INFO)

    def handleTask(self, valueD):
        if self.task is None:
            return -1
        logger.info("+SwitchTask.getFunctionReturn : starting for task %s valueD %r\n", self.task.name, valueD)
        funcList = self.task.getFunc()
        count = 0
        sValue = None
        for f in funcList:
            if f is None or f.getDataName() not in valueD:
                return -1
            data = valueD[f.getDataName()]
            sValue = getObjectValue(data, self.debug, self.__lfh)

            if sValue is None:
                return -1

            if self.debug > 0:
                logger.info("+SwitchTask.getFunctionReturn :  test value  %r", sValue)
                f.printMe(self.__lfh)

            if f.check(sValue) == 1:
                return count
            count = count + 1
        #
        logger.info("+SwitchTask.getFunctionReturn :  comparison failed with sValue %r\n ", sValue)
        return -1
