##
# File:    ProcessManager.py
# Date:    15-Mar-2009
#
# Updates:
#  22-April-2010 : Incorporation into enterpise.
#  14-Feb-2015   jdw  -- initial refactoring -    gutted
#   9-Mar-2015   jdw remove WFEapplication dependency --
#  2-May-2015    jdw gutted -
#
##

"""
manages the application processes via the API
This is the class that manages processes - they
can be within the WFE (there are a small number)
or they can be within the API
"""

__docformat__ = "restructuredtext en"
__author__ = "Tom Oldfield"
__email__ = "oldfield@ebi.ac.uk"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.24"

import sys
import os
import time
from threading import Thread
import logging
import traceback


from wwpdb.apps.wf_engine.engine.ServerMonitor import ServerMonitor

from wwpdb.utils.wf.process.ProcessRunner import ProcessRunner
from wwpdb.apps.wf_engine.engine.EngineUtils import EngineUtils

# from wwpdb.apps.wf_engine.wf_engine_utils.run.MyLogger import MyLogger
from wwpdb.apps.wf_engine.wf_engine_utils.time.TimeStamp import TimeStamp

logger = logging.getLogger(name="root")


class ProcessManager(Thread):

    """
    The process manager runs a process and sits and waits

    """

    def __init__(self, task, debug=0):
        """Input task is the current task object"""
        Thread.__init__(self)
        self.debug = debug
        self.__verbose = debug
        self.status = "unknown"
        self.elapsedTime = None
        self.task = task
        self.result = -1
        self._thetime = 0
        # self.__myLog = MyLogger()
        self.depositionID = None
        self.WorkflowClassID = None
        self.WorkflowInstanceID = None
        #
        self.__timeStamp = TimeStamp()
        #
        # input data for process : these are key / value pairs - of the input data
        self.input = {}
        #
        self.__taskParameterD = {}
        #
        # output data for process : these are key / value pairs
        self.output = {}

        self.instanceExitState = "finished"

    def getExitState(self):
        return self.instanceExitState

    def setInput(self, valueD, taskParamD):
        if self.debug > 0:
            if valueD is not None:
                logger.info("+ProcessManager.setInput() value dictionary %r\n", valueD.items())
            if taskParamD is not None:
                logger.info("+ProcessManager.setInput() task parameter dictionary %r\n", taskParamD.items())
        self.__taskParameterD = taskParamD
        self.input = valueD

    def setOutput(self, valueD):
        if self.debug > 0:
            if valueD is not None:
                logger.info("+ProcessManager.setOutput() value dictionary %r\n", valueD.items())

        self.output = valueD

    def setStatsInfo(self, depositionID, WorkflowClassID, WorkflowInstanceID):

        self.depositionID = depositionID
        self.WorkflowClassID = WorkflowClassID
        self.WorkflowInstanceID = WorkflowInstanceID

    def abort(self):
        logger.error(" call to abort")
        self.status = "abort"

    def __setDBInstStatus(self, mode, eUtilObj):

        now = self.__timeStamp.getSecondsFromReference()
        instDB = {}
        instDB["WF_INST_ID"] = self.WorkflowInstanceID
        instDB["WF_CLASS_ID"] = self.WorkflowClassID
        instDB["DEP_SET_ID"] = self.depositionID
        instDB["STATUS_TIMESTAMP"] = now
        eUtilObj.updateStatus(instDB, mode)

        sql = (
            "update wf_instance_last set status_timestamp="
            + str(now)
            + ", inst_status='"
            + mode
            + "', wf_class_id = '"
            + self.WorkflowClassID
            + "', wf_inst_id = '"
            + self.WorkflowInstanceID
            + "' where dep_set_id = '"
            + self.depositionID
            + "'"
        )
        ok = eUtilObj.runUpdateSQL(sql)
        if ok < 1:
            logger.error("+ProcessManager.__setDBInstStatus() CRITICAL : failed to update wf_instance_last table")

    def __setDBTaskStatus(self, mode, eUtilObj):

        taskID = {}
        taskID["WF_TASK_ID"] = self.task.name
        taskID["WF_INST_ID"] = self.WorkflowInstanceID
        taskID["WF_CLASS_ID"] = self.WorkflowClassID
        taskID["DEP_SET_ID"] = self.depositionID
        taskID["STATUS_TIMESTAMP"] = self.__timeStamp.getSecondsFromReference()
        eUtilObj.updateStatus(taskID, mode)

    def run(self):
        """
        This is the entry point of the process manager which is
        legacy run as a Thread

        It then justs calls runProcess
        """
        eUtilObj = EngineUtils(verbose=self.__verbose)
        self.status = "starting"
        self.__setDBTaskStatus("running", eUtilObj)

        if self.debug > 1:
            logger.info("+ProcessManager.run : %s : %s", str(self.status), str(self.__getElapsedTime()))

        self.__runProcess(eUtilObj)

        if self.debug > 1:
            logger.info("+ProcessManager.run :  %s %s", str(self.status), str(self.__getElapsedTime()))

        self.elapsedTime = None
        return self.status

    def __waitTime(self, sec):
        time.sleep(sec)

    def getState(self):
        return self.status

    def getResult(self):
        return self.result

    def __updateElapsedTime(self):
        """Update the elapsed time."""
        self.elapsedTime = self.elapsedTime + (self.__timeStamp.getSecondsFromReference() - self._thetime)

    def __getElapsedTime(self):
        """Show the elapsed time of the thread."""
        if self.elapsedTime is None:
            self.elapsedTime = 0
            self._thetime = self.__timeStamp.getSecondsFromReference()
        else:
            self.__updateElapsedTime()
        return "%5.2fs" % self.elapsedTime

    def __runProcess(self, eUtilObj):
        """
        This is the action method called by "run" It does all the work.

        if the uniqueWhere name = wfe : then do the task here . mostly very simple
          about the only useful wfe function is "wait"

        if the uniqueWhere name = "api" : then do the task in the API using  ProcessRunner()
        """

        self.status = "running"
        #  All output is directed to this task logfile -

        processLogName = (
            str(self.depositionID)
            + "_"
            + str(self.WorkflowClassID)
            + "_"
            + str(self.task.name)
            + "_"
            + str(self.WorkflowInstanceID)
            + "_"
            + str(self.task.name)
            + "_"
            + str(self.task.uniqueName)
            + ".log"
        )
        processLog = os.path.join(eUtilObj.getLogDirectoryPath(self.depositionID), processLogName)
        logfh = open(processLog, "w")

        if self.debug > 0:
            logfh.write("+ProcessManager.__runProcess :  task name     = " + str(self.task.name) + "\n")
            logfh.write("+ProcessManager.__runProcess :  name (simple) = " + str(self.task.nameHumanReadable) + "\n")
            logfh.write("+ProcessManager.__runProcess :  uniqueAction  = " + str(self.task.uniqueAction) + "\n")
            logfh.write("+ProcessManager.__runProcess :  uniqueWhere   = " + str(self.task.uniqueWhere) + "\n")

        if self.task.uniqueWhere == "wfe":
            ##
            #  The following tasks link out to functions that should deprecated ---
            if self.task.uniqueAction == "initDB":
                self.instanceExitState = "init"
                eUtilObj.initDepositContext(self.depositionID, self.WorkflowClassID, self.WorkflowInstanceID, self.input)
            elif self.task.uniqueAction == "releaseHPUB":
                eUtilObj.setReleaseStatus(self.depositionID, "HPUB")
            elif self.task.uniqueAction == "sendDepEmail":
                eUtilObj.sendDepositorEmail(self.depositionID, self.task.description)
            elif self.task.uniqueAction == "randomAnnotator":
                eUtilObj.setRandomAnnotator(self.depositionID)
            #
            ##
            elif self.task.uniqueAction == "die" or self.task.uniqueAction == "throw":
                self.status = self.task.uniqueName
                return
            elif self.task.uniqueAction == "finished":
                eUtilObj.setFinished(self.depositionID)
            elif self.task.uniqueAction == "resetStatus":
                eUtilObj.resetInitialStateDB(self.depositionID)
            elif self.task.uniqueAction == "fileExist":
                eUtilObj.testFilesExist(self.input, self.output)
            elif self.task.uniqueAction == "wait":
                self.__waitTime(self.task.runTime)
            elif self.task.uniqueAction == "monitorDB":
                monitor = ServerMonitor(self.WorkflowInstanceID, self.WorkflowClassID, self.depositionID, self.debug)
                monitor.watch()
            else:
                logfh.write("+ProcessManager.__runProcess :   ***** Unknown WFE application ****\n")
                self.__setDBTaskStatus("badNameX", eUtilObj)
                self.__setDBInstStatus("exception", eUtilObj)
                sys.exit(1)
        elif self.task.uniqueWhere == "api":

            if self.debug > 0:
                process = ProcessRunner(True, logfh)
            else:
                process = ProcessRunner(False, logfh)
            process.setAction(self.task.uniqueAction)

            if self.__taskParameterD is not None:
                process.setParameterDict(self.__taskParameterD)

            if self.input is not None:
                for key, value in self.input.items():
                    if self.debug > 1:
                        try:
                            cN = value.__class__.__name__
                            logfh.write("+ProcessManager.__runProcess :  setting input %s using object type %s\n" % (key, cN))
                            value.printMe()
                        except Exception as _e:  # noqa: F841
                            logfh.write("+ProcessManager.__runProcess :  setting input %s with value %r\n" % (key, value))
                    process.setInput(key, value)
            if self.output is not None:
                for key, value in self.output.items():
                    if self.debug > 1:
                        try:
                            cN = value.__class__.__name__
                            logfh.write("+ProcessManager.__runProcess :  setting output %s using object type %s\n" % (key, cN))
                            value.printMe()
                        except Exception as _e:  # noqa: F841
                            logfh.write("+ProcessManager.__runProcess :  setting output %s with value %r\n" % (key, value))

                    process.setOutput(key, value)

            if not process.preCheck():
                logfh.write("+ProcessManager.__runProcess : data pre-check fails for task %s action %s" % (self.task.name, self.task.uniqueAction))
                self.status = "exception"
                self.__setDBTaskStatus("exception", eUtilObj)
                self.__setDBInstStatus("exception", eUtilObj)
                sys.exit(1)

            ok = process.run()
            if not ok:
                pass

        if self.debug > 0:
            for key, value in self.output.items():
                try:
                    cN = value.__class__.__name__
                    logfh.write("+ProcessManager.__runProcess :  returned output %s has object type %s\n" % (key, cN))
                    value.printMe(logfh)
                except Exception as _e:  # noqa: F841
                    traceback.print_exc(file=logfh)
                    logfh.write("+ProcessManager.__runProcess :  returned output %s has value %r\n" % (key, value))

        self.status = "complete"
        self.__setDBTaskStatus("complete", eUtilObj)

        if self.debug > 0:
            logfh.write("+ProcessManager.__runProcess :  finished task name  %s\n" % self.task.name)

        # close the log file
        logfh.close()
