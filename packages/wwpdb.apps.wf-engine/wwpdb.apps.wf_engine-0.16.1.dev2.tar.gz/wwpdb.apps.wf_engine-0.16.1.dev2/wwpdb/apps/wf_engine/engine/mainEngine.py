##
# File:    mainEngine.py
# Date:    15-Mar-2009
#
# Updates:
#  22-April-2010 : Incorporation into enterpise.
#  09-August-2010 : Include logging
#  13-Feb-2015 jdw : major overhaul -
#  25-Apr-2015 jdw : another refactoring & continued revision of task processing -
#  2-May-2015  jdw : rewrote switch/branching task
#  2-Sep-2015  jdw : replace incomplete list of hardcoded storage types with api call --
#  7-Spe-2015  jdw : handle constant values assigned by api
#
##

"""

Workflow engine - reads the workflow and starts at
a point in the workflow given by the state of the
depositionID.

Entry point = "run" though this is not a threaded process

The WFE uses the first task/ instance ID and depID to start
  at the right point
"recovery" mode will also start at the last valid point in the WF

The rest is just a infinite loop of task follow task.

"""

__docformat__ = "restructuredtext en"
__author__ = "Tom Oldfield"
__email__ = "oldfield@ebi.ac.uk"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.24"

import sys
import time
import os
import logging
from xml.dom import minidom

# from threading import *

from wwpdb.apps.wf_engine.engine.SwitchTask import SwitchTask
from wwpdb.apps.wf_engine.engine.ExternalTask import ExternalTask
from wwpdb.apps.wf_engine.engine.WorkflowSession import WorkflowSession
from wwpdb.apps.wf_engine.engine.CommandLineArgs import CommandLineArgs
from wwpdb.apps.wf_engine.engine.ProcessManager import ProcessManager
from wwpdb.apps.wf_engine.engine.WorkflowManager import WorkflowManager

from wwpdb.apps.wf_engine.engine.InterpretDataObject import fillAPIinputObject
from wwpdb.apps.wf_engine.engine.InterpretDataObject import fillAPIoutputObject
from wwpdb.apps.wf_engine.engine.InterpretDataObject import getObjectValue
from wwpdb.apps.wf_engine.engine.InterpretDataObject import getTaskParameterDict


from wwpdb.apps.wf_engine.engine.EngineUtils import EngineUtils

#
from wwpdb.apps.wf_engine.reader.parseXML import parseXML

#
from wwpdb.apps.wf_engine.wf_engine_utils.time.TimeStamp import TimeStamp

from wwpdb.apps.wf_engine.wf_engine_utils.run.MyLogger import MyLogger
from wwpdb.apps.wf_engine.wf_engine_utils.process.ProcessUtils import ProcessUtils
from wwpdb.io.locator.DataReference import DataFileReference

logger = logging.getLogger(name="root")


class mainEngine(object):
    def __init__(self, debug=4, prt=None):  # pylint: disable=unused-argument
        logger.info("+mainEngine.__init__ Starts log level at %d", logger.getEffectiveLevel())
        # Global variables
        # path - this is a list that contains the tasks visited in order
        self.path = []
        # debug level
        self.debug = debug
        #        self.__lfh = MyLogger(level=logging.DEBUG)
        self.__lfh = MyLogger(level=logging.INFO)

        self.__verbose = debug > 0

        self.__depositionId = ""
        self.__wfClassId = ""
        self.__wfInstId = ""
        self.__wfClassFileName = ""

        # this should be available everywhere
        self.runTimeParameters = None

        # ---  Database connection and methods encapsulated in the EngineUtils() class
        self.__eUtil = EngineUtils(verbose=self.__verbose)
        self.__timeStamp = TimeStamp()
        #
        # Something went wrong - exception task
        self.exception = None
        self.instanceExitState = "finished"

    def __createDBclass(self, wfMetaDataObj):
        """
        Internal method create a workflow-class reference if not present.
        The statusDB class-dict contains one reference to each workflow class - so we only update when we find
        a new one.
        """

        classDB = {}
        classDB["WF_CLASS_ID"] = wfMetaDataObj.getID()
        classDB["WF_CLASS_FILE"] = wfMetaDataObj.getName()
        classDB["WF_CLASS_NAME"] = wfMetaDataObj.getName()
        classDB["TITLE"] = wfMetaDataObj.getDescription()
        classDB["AUTHOR"] = wfMetaDataObj.getAuthor()
        classDB["VERSION"] = wfMetaDataObj.getVersionMajor() + wfMetaDataObj.getVersionMinor()

        db = self.__eUtil
        if db.exist(classDB):
            if self.debug > 0:
                logger.info("+mainEngine.__createDBclass : found existing instance for workflow class %s file %s", wfMetaDataObj.getID(), wfMetaDataObj.getName())
        else:
            if self.debug > 0:
                logger.info("+mainEngine.__createDBclass : inserting new workflow class object for %s file %s", wfMetaDataObj.getID(), wfMetaDataObj.getName())
            db.saveObject(classDB, "insert")

        if self.debug > 1:
            logger.info("+mainEngine.__createDBclass :  done with classDB")

    def __setDBInstStatus(self, typein, mode, task):  # pylint: disable=unused-argument
        """
        Method to update the instance data in the status DB
        The WFM uses this instance data to reduce contention.

        The method always does an update since the instance
        data must exist on entry to the workflow - and a new
        workflow instance is always created with each run
        """

        now = self.__timeStamp.getSecondsFromReference()
        instDB = {}
        instDB["WF_INST_ID"] = self.__wfInstId
        instDB["WF_CLASS_ID"] = self.__wfClassId
        instDB["DEP_SET_ID"] = self.__depositionId
        #    instDB['STATUS_TIMESTAMP'] = datetime.datetime.utcnow()
        instDB["STATUS_TIMESTAMP"] = now

        self.__eUtil.updateConnection()
        db = self.__eUtil
        db.updateStatus(instDB, mode)

        # Tom :  update the wf_instance_last table - note it is unique over dep_set_id

        sql = (
            "update wf_instance_last set status_timestamp="
            + str(now)
            + ", inst_status='"
            + mode
            + "', wf_class_id = '"
            + self.__wfClassId
            + "', wf_inst_id = '"
            + self.__wfInstId
            + "' where dep_set_id = '"
            + self.__depositionId
            + "'"
        )
        ok = self.__eUtil.runUpdateSQL(sql)
        if ok < 1:
            logger.error("+mainEngine.__setDBInstStatus - failed to update wf_instance_last table for %s", self.__depositionId)

    def __setDBTaskStatus(self, typein, mode, task):
        """
        Method to update the task data in the status DB
        Current :
          The exist status of the task must be done since
          a loop in the workflow might mean we revisit a task
        To be done and supported by sytem :
          A status should always insert with a new task
          since we need to record all loop structure in WF
        """

        taskID = {}
        taskID["WF_TASK_ID"] = task.name
        taskID["WF_INST_ID"] = self.__wfInstId
        taskID["WF_CLASS_ID"] = self.__wfClassId
        taskID["DEP_SET_ID"] = self.__depositionId
        taskID["TASK_NAME"] = task.name
        taskID["TASK_TYPE"] = typein
        taskID["TASK_STATUS"] = mode
        #    taskID['STATUS_TIMESTAMP'] = datetime.datetime.utcnow()
        taskID["STATUS_TIMESTAMP"] = self.__timeStamp.getSecondsFromReference()

        # This version only creates unique taskID
        if self.__eUtil.exist(taskID):
            self.__eUtil.updateStatus(taskID, mode)
        else:
            self.__eUtil.saveObject(taskID, "insert")

    # def __getNewInstanceIDDB(self, depositionId):
    #     """
    #       Create new workflow instance from the statusDB
    #       Returns the ID
    #       The status API returns an ID as a number, this method
    #       prefixes the numeric with a W_
    #     """

    #     # This returns unique instID on depID AND the classID ; want the next one on depID only
    #     #    instID = self.__eUtil.getNextWfInstId(self.__depositionId,self.__wfClassId)

    #     sql = "select max(cast(substr(wf_inst_id,3) as decimal(5,0)))+1 from wf_instance where dep_set_id = '" + str(depositionId) + "'"

    #     ll = self.__eUtil.runSelectSQL(sql)

    #     if ll is None:
    #         instID = 1
    #     else:
    #         for l in ll:
    #             if l is None:
    #                 instID = 1
    #             else:
    #                 if l[0] is None:
    #                     instID = 1
    #                 else:
    #                     instID = l[0]

    #     ret = "W_" + str(instID).zfill(3)

    #     if self.debug > 0:
    #         logger.info("+mainEngine.__getNewInstanceIDDB : for data set ID = %s next workflow instance ID = %s", depositionId, ret)

    #     return ret

    def __createNewDBwfInstance(self):
        """
        Creates a new instance record within the status DB.
        A duplicate should NEVER be created and is a problem
        of the API-instance ID generator
        """

        instDB = {}

        #        self.__wfInstId = self.__getNewInstanceIDDB(self.__depositionId)
        self.__wfInstId = self.__eUtil.getNextInstanceId(self.__depositionId)

        now = self.__timeStamp.getSecondsFromReference()
        instDB["WF_INST_ID"] = self.__wfInstId
        instDB["WF_CLASS_ID"] = self.__wfClassId
        instDB["DEP_SET_ID"] = self.__depositionId
        instDB["OWNER"] = self.__wfClassFileName
        instDB["INST_STATUS"] = "running"
        instDB["STATUS_TIMESTAMP"] = now
        if not self.__eUtil.exist(instDB):
            self.__eUtil.saveObject(instDB, "insert")
        else:
            logger.info("+mainEngine.__createNewDBWfInstance  *** Error : duplicate instance %s", str(self.__wfInstId))
            constDict = {}
            constDict["WF_INST_ID"] = self.__wfInstId
            self.__eUtil.saveObject(instDB, "update", constDict)

        # Tom New code for the wf_instance_last table

        sql = "select ordinal from wf_instance_last where dep_set_id = '" + self.__depositionId + "'"
        elist = self.__eUtil.runSelectSQL(sql)

        if elist is None or len(elist) == 0:
            ind = -1
        else:
            for el in elist:
                if el is None:
                    ind = -1
                else:
                    ind = el[0]

        if ind < 0:
            # Create new row
            sql = (
                "insert wf_instance_last(wf_inst_id,wf_class_id,dep_set_id,owner,inst_status,status_timestamp) values ('"
                + self.__wfInstId
                + "','"
                + self.__wfClassId
                + "','"
                + self.__depositionId
                + "','"
                + self.__wfClassFileName
                + "','running',"
                + str(now)
                + ")"
            )
            ok = self.__eUtil.runInsertSQL(sql)
        else:
            # sql = "update wf_instance_last set wf_inst_id='" +
            # self.__wfInstId + "', wf_class_id='" + self.__wfClassId +
            # "', dep_set_id='" +  self.__depositionId + "',  inst_status='running',
            # status_timestamp=" + str(now) + " where ordinal = " + str(ind)
            sql = (
                "update wf_instance_last set wf_inst_id='"
                + self.__wfInstId
                + "', wf_class_id='"
                + self.__wfClassId
                + "', dep_set_id='"
                + self.__depositionId
                + "', owner='"
                + self.__wfClassFileName
                + "', inst_status='running', status_timestamp="
                + str(now)
                + " where ordinal = "
                + str(ind)
            )
            ok = self.__eUtil.runUpdateSQL(sql)

        if ok < 1:
            logger.error("+mainEngine.__createNewDBWfInstance failed to update wf_instance_last table")
        else:
            logger.info("+mainEngine.__createNewDBWfInstance wf_instance[_last] tables updated with %s", str(instDB))

    # def __doExceptionTask(self):
    #     """
    #       Global exception handler - this is the unhandled
    #         exception only
    #       Need to review this.
    #     """
    #     # for now just exit(1) - but we need to find the next task

    #     logger.error("+mainEngine.__doExceptionTask.  : called exit ")
    #     sys.exit(1)

    def __findEntryPoint(self, taskObjList):
        """
         find the starting point in the workflow
        - this is the default starting point
        """

        startingPoint = self.__findTaskByType("Entry-point", taskObjList)

        return startingPoint

    def __findTaskByType(self, typein, taskObjList):
        """
        Returns a task found by the task type, only of use
        for start/stop/exception - since the return will be
        ambigious for other types
        returns the task object
        """

        for task in taskObjList:

            if task.type.lower() == typein.lower():
                if self.debug > 1:
                    logger.info("+mainEngine.findTaskByType : Found task with type = %s", str(task.type))

                return task

        logger.error("+mainEngine.findTaskByType : Failed to find a task-by-type %s", str(typein))

        sys.exit(0)

    def __findTaskNameFromHumanName(self, humanName, taskObjList):
        """
        Returns a task found by the task name(ie unique ID) returns the task object
        """

        for task in taskObjList:
            if task.nameHumanReadable == humanName:
                if self.debug > 1:
                    logger.info("+mainEngine.__findTaskNameFromNumanName :   Found task with name = %s", str(task.name))
                return task

        # this method should not die
        return None

    def __findTaskByName(self, name, taskObjList):
        """
        Returns a task found by the task name(ie unique ID)
        returns the task object
        """

        for task in taskObjList:
            if task.name == name:
                if self.debug > 1:
                    logger.info("+mainEngine.__findTaskByName :   Found named task %s", str(task.name))
                return task

        logger.error("+mainEngine.__findTaskByName - Failed to find a task-by-name %s", str(name))
        return None

    def __loopTest(self, task, iterator, value):
        """
        method to manage a loop task
        It is really a test against an iterator.  Notice that the loop
        test only returns 2 states, the normal next task, or the exit
        loop next-task.  The usable return state is that the loop
        variable data object is made equal to the i'th iterator value.
        1) if the loop variable is not set - set it to the first iterator
        2) if the loop variable is set, then test it against the iterator
           list and set the loop variable = next item : return 0 :
           the first "nextTask"
        3) If we are at the end of the loop then return 1 : the second "nextTask"
        """

        for _key, data in value.items():
            # valueKey = key
            valueData = getObjectValue(data, self.debug, self.__lfh)
        for _key, data in iterator.items():
            # iteratorKey = key
            iteratorData = getObjectValue(data, self.debug, self.__lfh)

        if not isinstance(iteratorData, list):
            logger.info("+mainEngine.__loopTest : *** Error in WF - can only use a list for loop %s", str(type(iteratorData)))
            logger.info("+mainEngine.__loopTest : *** Error in WF - This is the data %s", str(iteratorData))
            return -1

        if self.debug > 1:
            logger.info("+mainEngine.__loopTest :   Loop output variable %s", str(valueData))
            logger.info("+mainEngine.__loopTest :   Loop input iterator %s", str(iteratorData))
            logger.info("+mainEngine.__loopTest :   Loop input length %s", str(len(iteratorData)))

        if self.debug > 0:
            logger.info(" +mainEngine.__loopTest : loop at %s / %s", str(valueData), str(len(iteratorData)))

        if valueData is None:
            # we are starting the loop
            if self.debug > 1:
                logger.info("+mainEngine.__loopTest : ValueData  =  %s", str(valueData))
                logger.info("+mainEngine.__loopTest : task.param =  %s", str(task.param))
            for _key, data in value.items():
                if len(iteratorData) < 1:
                    if self.debug > 1:
                        logger.info("+mainEngine.__loopTest :   Loop list of zero length \n")
                    return 1
                if task.param is not None and task.param == "index":
                    data.data = str("1")
                else:
                    data.data = iteratorData[0]
                if self.debug > 1:
                    logger.info("+mainEngine.__loopTest :  starting loop %s", str(data.data))
                return 0
        else:
            if task.param is not None and task.param == "index":
                index = int(valueData)
                if index >= len(iteratorData) - 1:
                    if self.debug > 1:
                        logger.info("+mainEngine.__loopTest : (index return) found end of loop ")
                    return 1
                else:
                    for _key, data in value.items():
                        data.data = str(index + 1)
                        if self.debug > 1:
                            logger.info("+mainEngine.__loopTest (index return) - Data value : %s", str(data.data))
                        return 0
            else:
                for index, item in enumerate(iteratorData):
                    if item == valueData:
                        if index >= len(iteratorData) - 1:
                            if self.debug > 1:
                                logger.info("+mainEngine.__loopTest : (value return) found end of loop ")
                            return 1
                        else:
                            for _key, data in value.items():
                                data.data = iteratorData[index + 1]
                                if self.debug > 1:
                                    logger.info("+mainEngine.__loopTest :  (value return) data value %s", str(data.data))
                                return 0

        return -1

    def __runProcess(self, task, dataValues, dataObjList):  # pylint: disable=unused-argument
        """
        JDW  Revised method to run single process task in a thread -

        """
        logger.info("+mainEngine.__runProcess :  Starting process %s", task.name)
        self.__setDBTaskStatus("process", "init", task)

        # setup the process
        self.__setDBTaskStatus("process", "start", task)
        process = ProcessManager(task, self.debug)
        process.setStatsInfo(self.__depositionId, self.__wfClassId, self.__wfInstId)
        dataForTask = task.getDataReference(dataObjList)
        if dataForTask:
            dataInput = self.__handleIOData("input", task, dataForTask, dataObjList)
            taskParamD = getTaskParameterDict(dataObjList, task.parameter, self.debug, self.__lfh)
            process.setInput(dataInput, taskParamD)
            dataOutput = self.__handleIOData("output", task, dataForTask, dataObjList)
            process.setOutput(dataOutput)

        # start the process
        process.start()
        processThread = process

        status = "running"
        #   find the longest failtime of all processes
        failTime = 0
        if task.failTime == 0:
            failTime = 2147483640  # about 68 years
        if task.failTime > failTime:
            failTime = task.failTime

        loop = 0
        while loop < failTime:
            loop = loop + 1
            time.sleep(1)

            # check if any crashed
            status = processThread.getState()
            if self.debug > 2:
                logger.debug("+mainEngine.__runProcess :  current status = %s", str(status))
            if self.__isException(status):
                logger.info("+mainEngine.__runProcess :  Task %s crashed", task.name)
                self.__setDBTaskStatus("process", "crashedX", task)
                self.__setDBInstStatus("process", "exception", task)
                self.exception = status
                return "exception"

            #   have they all completed ?
            status = processThread.getState()
            if status == "complete":
                logger.info("+mainEngine.__runProcess : task complete : %s", task.name)
                self.__setDBTaskStatus("process", "complete", task)
                self.instanceExitState = processThread.getExitState()
                return "complete"

        # The fail time is reached : abort any running tasks
        self.__setDBTaskStatus("process", "timeoutX", task)
        processThread.abort()
        logger.error("+mainEngine.__runProcess :  Trying to kill process")

        pid = os.getpid()
        logger.info("+mainEngine.__runProcess Stopping children %s id %s", str(processThread.getName()), str(pid))
        pu = ProcessUtils(verbose=True, log=self.__lfh)
        cPidList = pu.getChildren(pid)
        myStatus = pu.killProcessList(cPidList)
        logger.info("+mainEngine.__runProcess : Child kill status is %r", myStatus)
        time.sleep(1)
        #  record the task in exception and continue to dump the rest
        self.exception = "timeoutX"
        self.__setDBInstStatus("process", "exception", task)
        return "exception"

    def __runWorkflow(self, task, recoveryFlag):
        """
        Internal method to manage a workflow in a separate thread -
        """
        logger.info("+mainEngine.__runWorkflow() : %s  worflow %s instance %s recoveryFlag %r", self.__depositionId, task.name, self.__wfInstId, recoveryFlag)

        if recoveryFlag == 0:
            workflowThread = WorkflowManager(task.file, self.__depositionId, self.__wfInstId, "entry-point")
        elif recoveryFlag == 1:
            workflowThread = WorkflowManager(task.file, self.__depositionId, self.__wfInstId, "recover")
        elif recoveryFlag == 2:
            workflowThread = WorkflowManager(task.file, self.__depositionId, "recover", "recover")
        elif recoveryFlag == 3:
            # not used
            workflowThread = WorkflowManager(task.file, self.__depositionId, "Annotate", str(task.name))

        self.__setDBTaskStatus("workflow", "start", task)
        workflowThread.start()
        self.__setDBTaskStatus("workflow", "running", task)

        status = -1
        #
        failTime = 0
        if task.failTime == 0:
            failTime = 2147483640
        if task.failTime > failTime:
            failTime = task.failTime

        logger.info("+mainEngine.__runWorkflow() : %s  worflow %s timeout %d", self.__depositionId, task.name, failTime)
        loop = 0
        while loop < failTime:
            loop = loop + 1
            time.sleep(1)

            # check if any crashed
            status = workflowThread.workflowStatus()
            if status == 3:
                logger.info("+mainEngine.__runWorkflow() : %s  workflow %s crashed", self.__depositionId, task.name)
                self.__setDBTaskStatus("workflow", "crashedX", task)
                self.__setDBInstStatus("workflow", "exception", task)
                self.exception = "workflowX"
                return "exception"

            #   have they all completed ?
            # if status is 2 then all workflows have completed
            status = workflowThread.workflowStatus()
            if status == 2:
                logger.info("+mainEngine.__runWorkflow() : %s  workflow %s completed", self.__depositionId, task.name)
                self.__setDBTaskStatus("workflow", "complete", task)
                return "complete"

            # check that all started
            status = workflowThread.workflowStatus()
            if status == 0:
                logger.info("+mainEngine.__runWorkflow() : %s  workflow %s not started (exception)", self.__depositionId, task.name)
                self.__setDBTaskStatus("workflow", "startX", task)
                self.__setDBInstStatus("workflow", "exception", task)
                return "exception"

        # The fail time is reached : abort any running tasks
        self.__setDBTaskStatus("workflow", "timeoutX", task)
        workflowThread.abort()
        time.sleep(1)
        logger.info("+mainEngine.__runWorkflow() : %s  workflow %s timed out (exception)", self.__depositionId, task.name)
        self.__setDBInstStatus("workflow", "exception", task)
        return "exception"

    def __handleTask(self, task, dataObjList, recoveryFlag):
        """
        Input: - task is list of tasks objects (LENGTH=1 always)

        Takes control of a task and runs the task
        1) checks whether there a valid parallel tasks
        2) parallel processes and workflows are run elsewhere
        3) get the data for the single workflow path
        4) run the relevant task exception manager + task
        """
        logger.info(
            "+mainEngine.__handleTask : -------------------------------------------   STARTS for class %s TASK %s   -------------------------------------- ",
            self.__wfClassId,
            task.name,
        )
        logger.info(
            "+mainEngine.__handleTask : starting for %s class %s task %s  type %s recoveryFlag %r", self.__depositionId, self.__wfClassId, task.name, task.type, recoveryFlag
        )

        if task.type != "Manual":
            self.__setDBTaskStatus(task.type, "init", task)

        ret = 0
        status = "init"
        # real data dictionary of data values used for input and output
        dataValues = {}

        if task.type == "Workflow":
            logger.info("+mainEngine.__handleTask : %s calling runWorkflow for class %s task %s recoveryFlag %r", self.__depositionId, self.__wfClassId, task.name, recoveryFlag)
            status = self.__runWorkflow(task, recoveryFlag)
            ret = 0

        elif task.type == "Process":
            logger.info("+mainEngine.__handleTask : %s calling runProcess for class %s task %s", self.__depositionId, self.__wfClassId, task.name)
            status = self.__runProcess(task, dataValues, dataObjList)
            ret = 0

        else:
            logger.info("+mainEngine.__handleTask : %s starting inline handler for class %s task %s", self.__depositionId, self.__wfClassId, task.name)
            task.dump(self.__lfh)
            dataForTask = task.getDataReference(dataObjList)

            inputValues = None
            outputValues = None
            if dataForTask:
                inputValues = self.__handleIOData("input", task, dataForTask, dataObjList)
                outputValues = self.__handleIOData("output", task, dataForTask, dataObjList)

            if self.debug > 1:
                if dataForTask:
                    logger.info("+mainEngine.__handleTask :  Data objects for in-line task %s type %s", task.name, task.type)
                    for dat in dataForTask:
                        dat.printMe(self.__lfh)

            if task.type == "Manual":
                logger.info(
                    "+mainEngine.__handleTask :  %s EXTERNAL MANUAL task for class %s task %s with recoveryFlag %r", self.__depositionId, self.__wfClassId, task.name, recoveryFlag
                )
                if recoveryFlag == 0:
                    self.__setDBTaskStatus(task.type, "start", task)
                manual = ExternalTask(self.__eUtil, self.__depositionId, self.__wfClassId, self.__wfInstId, task, self.debug, recoveryFlag)
                # need to get the correct name of the data object
                ret = manual.handleTask()
                if ret < 0:
                    self.__setDBTaskStatus(task.type, "exception", task)
                    self.__setDBInstStatus(task.type, "exception", task)
                    logger.info("+mainEngine.__handleTask set TASK/INSTANCE status for EXTERNAL MANUAL task %r to exception", task.name)
                    self.exception = "manualX"
                    status = "exception"

                else:
                    self.__eUtil.addReferenceOverwrite(self.__depositionId, self.__wfClassId, None, None, task.name, str(ret))
                    logger.info("+mainEngine.__handleTask set TASK status for EXTERNAL MANUAL task %r to complete", task.name)
                    self.__setDBTaskStatus(task.type, "complete", task)
                    status = "complete"

            elif task.type == "Loop":
                logger.info("+mainEngine.__handleTask :  loop class %s task %s ", self.__wfClassId, task.name)
                self.__setDBTaskStatus(task.type, "start", task)
                ret = self.__loopTest(task, inputValues, outputValues)
                if ret < 0:
                    # then the function return resulted in exception
                    self.__setDBTaskStatus(task.type, "exception", task)
                    self.__setDBInstStatus(task.type, "exception", task)
                    self.exception = "loopX"
                    status = "exception"
                else:
                    status = "complete"
            elif task.type == "Decision":
                logger.info("+mainEngine.__handleTask :  %s switch class %s task %s type %s ", self.__depositionId, self.__wfClassId, task.name, task.type)
                self.__setDBTaskStatus(task.type, "start", task)
                switch = SwitchTask(task, debug=self.debug)
                # need to get the correct name of the data object
                self.__setDBTaskStatus(task.type, "running", task)
                ret = switch.handleTask(inputValues)
                # put the return value into the status database
                if ret < 0:
                    # then the function return resulted in exception
                    self.__setDBTaskStatus(task.type, "exception", task)
                    self.__setDBInstStatus(task.type, "exception", task)
                    self.exception = "decisionX"
                    status = "exception"
                else:
                    self.__eUtil.addReferenceOverwrite(self.__depositionId, self.__wfClassId, None, None, task.name, str(ret))
                    self.__setDBTaskStatus(task.type, "complete", task)
                    status == "complete"  # pylint: disable=pointless-statement
            elif task.type == "Entry-point":
                status == "complete"  # pylint: disable=pointless-statement
            elif task.type == "Exit-point":
                status == "complete"  # pylint: disable=pointless-statement
            elif task.type == "Exception":
                logger.info("+mainEngine.__handleTask :  Exception handler thown in workflow class %s - aborting", self.__wfClassId)
                self.__setDBTaskStatus(task.type, "abort", task)
                self.__setDBInstStatus(task.type, "abort", task)
                logger.info("+mainEngine.__handleTask : exiting for %s with status %r ret %r", self.__depositionId, status, ret)
                sys.exit(1)
            else:
                logger.info("+mainEngine.__handleTask : failure : class %s undefined task type %r ", self.__wfClassId, task.type)
                logger.info("+mainEngine.__handleTask : exiting for %s with status %r ret %r", self.__depositionId, status, ret)
                sys.exit(0)

        if not status == "exception":
            self.__setDBTaskStatus(task.type, "finished", task)

        logger.info("+mainEngine.__handleTask : returning for %s with status %r ret %r", self.__depositionId, status, ret)
        return ret

    def __handleIOData(self, mode, task, dataForTask, dataObjList):
        """
        Method to return data object dictionaries
        The data objects for the task as searched and cross referenced
          with the data in the data list

        if a processName has been defined then we have an API process
          which requires that we call objects by pre-defined names
        if a processName is undefined then we are using a switch task
          task or other non-API process.  Just pass data back as required
        The names of the API-process data objects are looked up and
          cross-referenced with the WF data objects.
        Where there is multiple input/output, then the object number
          is matched
        """

        # Need to handle the name of the data object properly
        # Warning - there is no sorted order to the data input names
        # how to we handle which item is which ????

        logger.info(
            "+mainEngine.__handleIOData : Starts for task %s mode %s action %s where %s data object length %d",
            task.name,
            mode,
            task.uniqueAction,
            task.uniqueWhere,
            len(dataForTask),
        )
        dfr = DataFileReference()
        storageTypeList = dfr.getStorageTypeList()
        #
        ret = {}
        nWFData = 0
        for data in dataForTask:
            if data.localMode.startswith(mode) or data.localMode.startswith("both"):
                if self.debug > 0:
                    logger.info("+mainEngine.__handleIOData :  Found %s reference %s", str(mode), str(data.name))
                    logger.info("+mainEngine.__handleIOData :  Storage type = %s", str(data.where))
                if (data.where in storageTypeList) or (data.where in ["constant", "inline"]) or (data.where[0:4] == "path"):
                    nWFData = nWFData + 1
                else:
                    pass
        #
        # Only if the processName is defined then we have a process
        # Other tasks will have no uniqueAction defined - so we
        # just get the data and call it by the uniqueID of the data object

        if task.uniqueAction is None:
            if self.debug > 0:
                logger.info("+mainEngine.__handleIOData :  Using task data from wfe")
        elif task.uniqueWhere == "wfe":
            if self.debug > 0:
                logger.info("+mainEngine.__handleIOData :  Using task data from wfe")
        elif task.uniqueWhere == "api":
            if self.debug > 0:
                logger.info("+mainEngine.__handleIOData :  Using task data from api")

            nProcessData = 0
            if mode == "input":
                nProcessData = task.ActionRegistry.getInputObjectCount(task.uniqueAction)
                ioNames = task.ActionRegistry.getInputObjectNames(task.uniqueAction)
                if self.debug > 1:
                    logger.info("+mainEngine.__handleIOData :  Number of input data = %s for fask name %s", str(nProcessData), str(task.uniqueAction))
                    logger.info("+mainEngine.__handleIOData :  registry input data names = %s", str(ioNames))
            elif mode == "output":
                nProcessData = task.ActionRegistry.getOutputObjectCount(task.uniqueAction)
                ioNames = task.ActionRegistry.getOutputObjectNames(task.uniqueAction)
                if self.debug > 1:
                    logger.info("+mainEngine.__handleIOData :  Number of output data = %s task name %s", str(nProcessData), str(task.uniqueAction))
                    logger.info("+mainEngine.__handleIOData :  registry output data names = %s", str(ioNames))
            else:
                logger.info("+mainEngine.__handleIOData :   Error : undefined IO mode in handleIOData %s", str(mode))

            if nProcessData == 0 and nWFData > 0:
                logger.info("+mainEngine.__handleIOData :  WARNING : input defined in WF - none required for process : %s IO = %s ", str(task.uniqueAction), str(mode))
                return None
            if nProcessData > 0 and nWFData == 0:
                logger.info("+mainEngine.__handleIOData :  WARNING : no input defined in WF - input required for process : %s IO = %s", str(task.uniqueAction), str(mode))
                return None
            if nProcessData < nWFData:
                logger.info("+mainEngine.__handleIOData :  WARNING : not enough data define in WF for process %s IO = %s", str(task.uniqueAction), str(mode))
                return None
            if nProcessData > nWFData:
                logger.info("+mainEngine.__handleIOData :  WARNING : too many data tems define in WF for process %s IO = %s", str(task.uniqueAction), str(mode))
                return None
        else:
            logger.info("+mainEngine.__handleIOData :   **** Unknown function <where> %s", str(task.uniqueWhere))

        nWFData = 0
        for data in dataForTask:
            logger.info(
                "+mainEngine.__handleIOData : name %r data.localMode %r data.where %r task.uniqueName %r task.uniqueWhere %r",
                data.name,
                data.localMode,
                data.where,
                task.uniqueName,
                task.uniqueWhere,
            )
            if data.localMode.startswith(mode) or data.localMode.startswith("both"):
                #
                #   change for to include 'constants' returned from api -
                if (data.where in storageTypeList) or (data.where[0:4] == "path") or ((data.where in ["constant"]) and (task.uniqueWhere == "api")):
                    #
                    if data.localMode.startswith("input") or data.localMode.startswith("both"):
                        fillAPIinputObject(dataObjList, data, self.__depositionId, self.debug, self.__lfh)
                    if data.localMode.startswith("output") or data.localMode.startswith("both"):
                        fillAPIoutputObject(dataObjList, data, self.__depositionId, self.debug, self.__lfh)

                    # if there is no task.uniqueAction - then call the object by the WF name
                    #
                    if task.uniqueName is None:
                        ret[data.name] = data.ApiData
                    elif task.uniqueWhere == "api":
                        logger.info("+mainEngine.__handleIOData : match ioNames using %r ", data.localMode)
                        if data.localMode[-1] in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                            for ioName in ioNames:
                                if ioName[-1] == data.localMode[-1]:
                                    ret[ioName] = data.ApiData
                                    logger.info("+mainEngine.__handleIOData :   found new indexed data name %s, %s %s", str(ioName), str(data.localMode), str(data.name))
                        else:
                            ret[ioNames[nWFData]] = data.ApiData
                    else:
                        ret[data.name] = data.ApiData
                    nWFData = nWFData + 1
                elif data.where == "workflow" or data.where == "WF":
                    # This is a workflow state model instance, probably in memory too.
                    # THIS IS A REAL DATA VALUE
                    #         ret[data.name] = data.data
                    ret[data.name] = data
                elif data.where in ["constant"]:
                    # this is a variable or a constant in the data declaration
                    ret[data.name] = data
                else:
                    logger.info("+mainEngine.__handleIOData :   *** Catastrophic Workflow failure : Unknown data origin %s", str(data.where))
                    sys.exit(0)

        return ret

    def __getNextTask(self, lastTask, opt, taskObjList):
        """
        Return the next task from the lasttask, for a decision task it will return the option number task
        """

        nextTask = None

        name = lastTask.getNextTaskName(opt)

        if name:
            nextTask = self.__findTaskByName(name, taskObjList)
            if self.debug > 1:
                logger.info("+mainEngine.__getNextTask :   Found next task: %s", str(nextTask.name))

        else:
            logger.info("+mainEngine.__getNextTask :  *** Catastrophic workflow error : failed to find next task")
            logger.info("+mainEngine.__getNextTask :  in %s number %s", str(lastTask), str(opt))

        return nextTask

    def __readWorkFlow(self, wfFilePath, debugLevel=0):
        """
        Get dom object for workflow class file -
        """
        xmldoc = minidom.parse(wfFilePath)
        parse = parseXML(debugLevel, self.__lfh)
        return parse, xmldoc

    def __readWorkFlowHeader(self, parse, xmldoc):
        """
        Get workflow metadata object --
        """
        wfMetaDataObj = parse.getMetaData(xmldoc)
        return wfMetaDataObj

    def __readWorkFlowBody(self, parse, xmldoc, depositionID, instanceID):
        """
        Return the task object and data object lists from the workflow definition
        """
        taskObjList = parse.getTaskObjects(xmldoc)
        dataObjList = parse.getDataObjects(depositionID, instanceID, xmldoc)
        return taskObjList, dataObjList

    def __outputPath(self):
        """Outputs to the terminal the pathway taken by the workflow"""

        logger.info("+mainEngine.outputPath :  Path taken\n")

        for p in self.path:
            logger.info(" -> %s", str(self.__prettyPrintTask(p)))
        logger.info("\n")

    def __prettyPrintTask(self, t):
        """
        Simple output method to print out the task name for humans
        """

        if t.name.lower() == t.nameHumanReadable.lower():
            return t.name
        else:
            return "(" + t.name + ":" + t.nameHumanReadable + ")"

    def __manageException(self, workingTask, opt, taskObjList):
        """
        General exception manager:
        if opt < 0 : Ouch - bad return state from task - basically
          no return task could be found = really a workflow class error
          instance is marked as exception

        if self.exception == exception : generic exception
           do not reset the exception state - instance will be marked as "exception"
        if self.exception == some other valid exception type (see below)

        if the exception task has a nextTask - this is used
        if the exception task has handles - then the self.exception is matched and used
        if the exception task has nothing - then it just exits(1)


        Exceptions
           exception   : generic
           crashedX    : process crashed
           manualX     : manual UI error
           decisionX   : automated decision errro
           workflowX   : workflow error
           badNameX   : unknown WFE process reference
           timeoutX   : process ran out of time
           startX : process never started
           all    : anything else
           rest   : anything else
        """

        logger.info("+mainEngine.__manageException:  starting")

        if self.exception is None:
            logger.info("+mainEngine.__manageException : No exception - should not be in manageException\n")
            return 0, workingTask

        if workingTask is None:
            logger.info("+mainEngine.__manageException :  Unknown current task \n")
            return -1, None

        if opt < 0:
            logger.info("+mainEngine.__manageException :  Unknown parallel number in task %d \n", opt)
            # an old way of handling exceptions - reset and continue
            opt = 0

        if workingTask.exception is None:
            logger.info("+mainEngine.__manageException  :  In task = %s", str(workingTask.name))
            logger.info("+mainEngine.__manageException :  No exception handler declared ")

        if self.debug > 0:
            logger.info("+mainEngine.__manageException  :  Exception managed = %s", str(self.exception))
            logger.info("+mainEngine.__manageException  :  In task = %s", str(workingTask.name))
            logger.info("+mainEngine.__manageException  :  Exception handler = %s", str(workingTask.exception))

        #  get the handled exception task and continue
        taskException = self.__findTaskByName(workingTask.exception, taskObjList)

        # add to the task path : need to add to the status DB
        self.path.append(taskException)

        if taskException.data is None or taskException.data == []:
            # no handlers defined
            logger.info("+mainEngine.__manageException  :  No handlers defined %s", str(self.exception))
            logger.info(str(taskException.outputName))
            if taskException.outputName is None or taskException.outputName == [] or taskException.outputName[0] == "":
                logger.info("+mainEngine.__manageException  :  No exception nexttask - will die\n")
                self.exception = "exception"
                return -1, None
            else:
                logger.info("+mainEngine.__manageException  :  Global exception next task %s \n", taskException.outputName[0])
                self.exception = None
                return 0, taskException
        else:
            # handler data is block of 5 data : print string, exception , nexttask , ,
            if self.debug > 1:
                logger.info("+mainEngine.__manageException  :  List of declared handles for this exception manager\n")
                for datum in taskException.data:
                    if datum[0] is not None:
                        logger.info(" Exception handler %s warning : %s, %s", str(taskException.name), str(datum[0]), str(datum[1]))
            # look for specific handles
            for datum in taskException.data:
                if datum[1].lower() == self.exception.lower():
                    if self.debug > 0:
                        logger.info("+mainEngine.__manageException  : Exception manager - found handler name = %s\n", str(datum[1]))
                    if datum[2].lower() == "die":
                        logger.info("+mainEngine.__manageException  :  handle to DIE called\n")
                        self.exception = "exception"
                        return -1, None
                    else:
                        taskException.outputName = []
                        taskException.outputName.append(datum[2])
                        self.exception = None
                        return 0, taskException
                # now handle any remaining options
                if datum[1].lower() == "all" or datum[1].lower() == "rest":
                    if self.debug > 0:
                        logger.info("+mainEngine.__manageException  : Exception manager - handler name = %s", str(datum[1]))
                    if datum[2].lower() == "die":
                        logger.info("+mainEngine.__manageException  :  handle to DIE called\n")
                        self.exception = "exception"
                        return -1, None
                    else:
                        taskException.outputName = []
                        taskException.outputName.append(datum[2])
                        self.exception = None
                        return 0, taskException

        return -1, None

    def runNoThrow(self, argv, runTime=None):

        self.run(argv, runTime, throwExit=False)

    def run(self, argv, runTime=None, throwExit=True):
        """
        The main workflow engine method
        1) get runtime parameters, set the main engine parameteres
        2) read the workflow class  WF
        3) Set the state for class and instance in DB
        4) Determine the task recovery point if required : fetch state
        5) run workflow until exception/end point
           Exception : run handler - and continue in WF at handle
        """

        if runTime is None:
            self.runTimeParameters = CommandLineArgs(argv)
        else:
            self.runTimeParameters = runTime

        if not self.runTimeParameters:
            return

        self.__depositionId = self.runTimeParameters.getSessionID()

        if self.runTimeParameters.debug >= 0:
            self.debug = self.runTimeParameters.debug

        self.__wfClassFileName = self.runTimeParameters.workflow
        self.__wfInstId = self.runTimeParameters.instanceID
        recoveryFlag = 0

        logger.info(
            "+mainEngine.run  ------------------------- Starting for depositionID = %s  WFInstID %s workflow file %s ",
            str(self.__depositionId),
            str(self.__wfInstId),
            str(self.__wfClassFileName),
        )

        if not self.__depositionId:
            logger.info("+mainEngine.run :  Workflow cannot proceed without a depositionID\n")
            return
        wfFilePath = os.path.join(self.runTimeParameters.getPath(), self.runTimeParameters.getWorkFlowFileName())
        parse, xmldoc = self.__readWorkFlow(wfFilePath)

        # get the meta data from the workflow class file -  sets global workflow details (e.g. classID )
        wfMetaDataObj = self.__readWorkFlowHeader(parse, xmldoc)
        self.__wfClassId = wfMetaDataObj.getID()

        # create DB entry for the class
        self.__createDBclass(wfMetaDataObj)

        # is there a parameter that will override the current workflow state
        startTask = None
        taskName = self.runTimeParameters.getInitTask()
        #
        logger.info("+mainEngine.run : command-line args class %s starting task name %s instance %s", self.__wfClassId, taskName, self.__wfInstId)

        if not taskName:
            logger.info("+mainEngine.run  : Error : cannot find task name for start point in command-line arguments\n")
            logger.info("+mainEngine.run  ------------------------------------------  returning for %s ", self.__depositionId)
            sys.exit(0)
        else:
            if taskName.lower() == "start" or taskName.lower() == "entry-point":
                # this is the normal case :
                # start from scratch with new instance ID : so create a new DB entry for this
                self.__createNewDBwfInstance()
                logger.info("+mainEngine.run  : starting workflow %s at task %s\n", self.__wfClassFileName, taskName)
            elif taskName.lower() == "recover":
                if self.__wfInstId is None:
                    logger.info("+mainEngine.run  : *** Error : Recover requires a valid WorkflowInstanceID")
                    logger.info("+mainEngine.run  ------------------------------------------  returning for %s ", self.__depositionId)
                    sys.exit(0)
                if self.__wfInstId == "recover":
                    recoveryFlag = 2
                    # find the last instanceID and the last finished task
                    #  WE NEED A TASK THAT WE CAN RECOVER FROM - get state of workflow variable
                    ws = WorkflowSession(self.__eUtil, self.__depositionId, self.__wfClassId, debug=self.debug)
                    self.__wfInstId, taskName = ws.autoRecover()
                    logger.info("+mainEngine.run %s autorecover() returns instance %s  task name %s recoveryFlag %s ", self.__depositionId, self.__wfInstId, taskName, recoveryFlag)
                elif self.__wfInstId.startswith("recoverannotate"):
                    ws = WorkflowSession(self.__eUtil, self.__depositionId, self.__wfClassId, debug=self.debug)
                    taskName = ws.recoverFromAnnotate()
                    self.__wfInstId = "Annotate"
                    recoveryFlag = 2
                    # task name is correct
                    logger.info(
                        "+mainEngine.run %s recoverFromAnnotate() returns instance %s  task name %s recoveryFlag %s ", self.__depositionId, self.__wfInstId, taskName, recoveryFlag
                    )
                else:
                    # find the last finished task
                    ws = WorkflowSession(self.__eUtil, self.__depositionId, self.__wfClassId, debug=self.debug)
                    taskName = ws.autoRecoverInstance(self.__wfInstId)
                    recoveryFlag = 1
                    logger.info(
                        "+mainEngine.run %s autoRecoverInstance() returns instance %s  task name %s recoveryFlag %s ", self.__depositionId, self.__wfInstId, taskName, recoveryFlag
                    )
            else:
                # Just get the last instance as we have a taskName
                # we passed the classID - so we have to find the actual ID
                # #
                logger.info("+mainEngine.run - searching for last instance of class %s taskName %r", self.__wfClassId, taskName)
                ws = WorkflowSession(self.__eUtil, self.__depositionId, self.__wfClassId, debug=self.debug)
                self.__wfInstId, _junk = ws.autoRecover()
                logger.info("+mainEngine.run - autorecover() class %s taskName %r returns instance %r ", self.__wfClassId, taskName, self.__wfInstId)

        #
        # - read the workflow body
        curTaskObjList, curDataObjList = self.__readWorkFlowBody(parse, xmldoc, self.__depositionId, self.__wfInstId)

        # Find the task to start the workflow from
        if taskName is None:
            logger.error("+mainEngine.run  classID %r instanceID %r  missing taskName", self.__wfClassId, self.__wfInstId)
            logger.error("+mainEngine.run  ------------------------------------------  exiting for %s ", self.__depositionId)
            sys.exit(0)
        elif taskName.lower() == "start" or taskName.lower() == "entry-point":
            startTask = self.__findEntryPoint(curTaskObjList)
        else:
            #  try the HumanReadable first
            startTask = self.__findTaskNameFromHumanName(taskName, curTaskObjList)
            if startTask is None:
                startTask = self.__findTaskByName(taskName, curTaskObjList)

        # no start task bail
        if not startTask:
            logger.info("+mainEngine.run  - returning for depositionId %s with NO startpoint in workflow %s task name %r ", self.__depositionId, self.__wfClassFileName, taskName)
            return

        logger.info(
            "+mainEngine.run - assigning start task for class %s  instance %r taskName %r startTask %r recoveryFlag %s",
            self.__wfClassId,
            self.__wfInstId,
            taskName,
            startTask,
            recoveryFlag,
        )
        self.path.append(startTask)

        workingTask = startTask
        logger.info("+mainEngine.run - Workflow starts with class %s task %s", self.__wfClassId, workingTask.name)

        if workingTask.name == "End":
            logger.info("+mainEngine.run  : depositionID %s workingtask is at END", str(self.__depositionId))
            logger.info("+mainEngine.run  ------------------------------------------  returning for %s ", self.__depositionId)
            return

        if recoveryFlag == 0:
            self.__setDBInstStatus("workflow", "running", workingTask)

        while True:
            logger.info("+mainEngine.run - begin task loop class %s instance %s workingtask %s type %s\n\n", self.__wfClassId, self.__wfInstId, workingTask.name, workingTask.type)

            opt = self.__handleTask(workingTask, curDataObjList, recoveryFlag)

            logger.info("+mainEngine.run - workingtask %s handleTask return code %r exception %r", workingTask.name, opt, self.exception)
            recoveryFlag = 0

            if self.exception is not None:
                # This will return the exception task - and where to go next if handled
                opt, workingTask = self.__manageException(workingTask, opt, curTaskObjList)

            if workingTask is None:
                break

            if workingTask.type == "Exit-point":
                break

            # get the next task from the current task
            workingTask = self.__getNextTask(workingTask, opt, curTaskObjList)

            if not workingTask:
                break

            # ie you cannot run "end" in parallel with any other task

            self.path.append(workingTask)

        if self.exception is None:
            self.__setDBInstStatus("all", self.instanceExitState, None)
        else:
            self.__eUtil.setException(self.__depositionId)
            logger.info(
                "+mainEngine.run - exception for workflow %s for %s with exception %r status %r",
                str(self.__wfClassFileName),
                self.__depositionId,
                self.exception,
                self.instanceExitState,
            )
            logger.info("+mainEngine.run  ------------------------------------------  returning for %s ", self.__depositionId)

            if throwExit:
                # set the communication table to exception
                return 1
            else:
                return

        if self.debug >= 0:
            self.__outputPath()

        logger.info("+mainEngine.run  : Completed workflow from %s for %s", str(self.__wfClassFileName), self.__depositionId)
        logger.info("+mainEngine.run  ------------------------------------------  returning for %s\n", self.__depositionId)
        if throwExit:
            return 0
        else:
            return

    def __isException(self, name):
        values = ["exception", "crashedX", "manualX", "decisionX", "workflowX", "badNameX", "timeoutX", "startX", "stopX", "loopX"]
        if name in values:
            return True
        else:
            return False


def main(argv):
    runTimeParameters = CommandLineArgs(argv)
    debugN = runTimeParameters.debug
    logPath = runTimeParameters.log

    # Set logging details --
    # logger = logging.getLogger(name='root')
    if debugN > 2:
        logger.setLevel(logging.DEBUG)
    elif debugN > 0:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.ERROR)

    logging.captureWarnings(True)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s")
    handler = logging.FileHandler(logPath)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    ##
    #   Log is overwritten by the logging facility  so don't open here -- jdw
    #    if (log is not None):
    #        output = open(log, "w")
    #
    engine = mainEngine(debug=debugN, prt=None)

    stat = engine.run(argv, runTimeParameters)

    exit(stat)


if __name__ == "__main__":
    main(sys.argv[1:])
