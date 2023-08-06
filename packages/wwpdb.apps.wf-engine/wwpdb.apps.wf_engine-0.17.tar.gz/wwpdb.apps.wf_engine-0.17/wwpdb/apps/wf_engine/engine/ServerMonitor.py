##
# File: ServerMonitor.py
# Date: ~ 2009
#
#  Updates:
#     10-Mar-2015   jdw refactored
#     25-Apr-2015   jdw purge unused code sections
#     8-May-2015    jdw reorganized sleep/wake processing - handle exit conditions
#     3-Jun-2016    jdw Overall watch method to resolve restart and session import issues
#
##

import time
import signal
import socket
import logging


from wwpdb.apps.wf_engine.engine.WorkflowManager import WorkflowManager

from wwpdb.apps.wf_engine.wf_engine_utils.run.MyLogger import MyLogger
from wwpdb.apps.wf_engine.wf_engine_utils.process.ProcessUtils import ProcessUtils
from wwpdb.apps.wf_engine.engine.EngineUtils import EngineUtils
from wwpdb.apps.wf_engine.wf_engine_utils.time.TimeStamp import TimeStamp

logger = logging.getLogger(name="root")


class ServerMonitor(object):

    """

     Original author T.J.Oldfield 2009


     Main server  demon
      manages processes by pinging statusDB

    Checks for processes that need to be run
    checks for kills/restarts for processes it owns
    checks on other server demons to see if they are broken
    checks and puts to sleep tired processes
    checks and wakes up processes

    puts its current state into the statusDB (load and onership)
    """

    def __init__(self, instID, classID, depID, debug=0):  # pylint: disable=unused-argument
        self.__baseEngineProcessName = "WFEngineRunnerExec"
        self.rowLim = 1
        self.wait = False
        self.locking = False
        #    self.inStatus = "init"
        #    self.outStatus = "init"
        self.inStatus = "runWF"
        self.outStatus = "runningWF"
        #  watch loop delay interval - seconds
        self.waitTime = 5
        # not used
        # self.sleepTime = 3600
        self.classID = classID
        self.depID = depID
        self.monitorDict = {}
        self.extremeLoad = 16
        self.normalLoad = 8
        # ~ idle timeout value - seconds
        # self.purgeTime = 60
        self.purgeTime = 600

        self.debug = debug
        self.__lfh = MyLogger(level=logging.INFO)

        self.hostname = socket.gethostname()

        ##
        # JDW  - creating new connection here -- Can this be passed along ??
        self.__eUtil = EngineUtils(verbose=self.debug)
        self.__timeStamp = TimeStamp()

        self.validSleep = ["waiting", "open"]

        self.__pu = ProcessUtils(verbose=True, log=self.__lfh)
        # Temporary setting to track process monitoring
        # self.__pu.setDebug(flag=True)
        logger.info("+ServerMonitor.__init__() Normal load %s and high load is %s ", self.normalLoad, self.extremeLoad)

    def watch(self):
        """
        Montitoring method that looks at the communication table in the database for new tasks.

        JDW - This is the ONLY public entry point in this class -
        """

        logger.info("+ServerMonitor.watch() Starting watch process")

        # first - what does this server own - get state of communication table
        # take this out as the status module does not respect concurrency and so the restart
        #  overwrites any mmCIF changes on recover
        #    self.__recoverState()

        # use this skip work
        newWork = 1
        numMonitored = 0
        while True:
            for loop in range(1, 10000000):
                #      do a reconnect after timeout - stop stale conenctions
                self.__eUtil.updateConnection()

                if loop == 1:
                    self.__monitorRestart(verbose=True)
                #
                dictList = []
                if (loop % newWork) == 0:
                    # Look for the next PENDING workflow, add to the monitored list, and invoke.
                    dictList = self.__getStatusData(self.inStatus, self.outStatus)
                    if dictList is not None and len(dictList) > 0:
                        # start new workflows
                        self.__addProcess(dictList)

                # manage monitored PENDING entries in communications table belonging to this server
                self.__manageProcess()

                time.sleep(self.waitTime)  # wait for x seconds

                # newWork will be adjusted to 1/2/3 depending on the number of managed processes --
                newWork = self.__getWorkStep()

                # check the process workflows looking for WF in a wait state
                if loop % 2 == 0:
                    self.__sleepWorkFlow()

                if (loop + 1) % 2 == 0:
                    self.__wakeUpWorkflow()

                if loop % 5 == 0:
                    self.__monitorRestart(verbose=True)

                if len(self.monitorDict) != numMonitored:
                    numMonitored = len(self.monitorDict)
                    self.__showMonitored()

    def __addProcess(self, dictList):
        """
        Starts a PENDING workflow based on the tasks described in the input dictionary list.

        Tasks are also copied to the global self.monitorDict for this serverMonitor() instance

         >> sets all previous wf_instance for depID to exception if not already exception (preserve time)?
        """
        numT = len(dictList)
        for ii, edict in enumerate(dictList):
            logger.info("+ServerMonitor.__addProcess begin iteration %d or %d", ii + 1, numT)
            logger.info("+ServerMonitor.__addProcess using dictionary =  %s", edict.items())
            depID = edict["DEP_SET_ID"]
            classID = edict["WF_CLASS_ID"]
            # instID = edict['WF_INST_ID']
            wfName = edict["WF_CLASS_FILE"]
            if wfName is None:
                logger.info("+ServerMonitor.__addProcess No workflow class name found - ignoring ")
            else:
                logger.info("+ServerMonitor.__addProcess for %s classID %s wfName %s ", depID, classID, wfName)
                n = wfName.find(":")
                # look up a workflow nesting of task
                if n > 0:
                    taskID = wfName[n + 1 :]
                    wfName = wfName[:n]
                    if (taskID == "Annotate") and (wfName == "Annotation.bf.xml"):
                        taskID = "entry-point"
                else:
                    taskID = "entry-point"
                logger.info("+ServerMonitor.__addProcess for %s wfName %s using taskID %s ", depID, wfName, taskID)
                #
                # set all the old instances to exception
                #
                replaceStatus = "aborted"
                logger.info("+ServerMonitor.__addProcess %s setting active workflow instances to %s", depID, replaceStatus)
                sql = (
                    "update wf_instance set inst_status = '" + replaceStatus + "' where dep_set_id = '" + str(depID) + "' and inst_status not in ('exception','aborted','finished')"
                )
                _ok = self.__eUtil.runUpdateSQL(sql)  # noqa: F841

                logger.info("+ServerMonitor.__addProcess starting workflow manager for %s classId %s wfName %s taskID %s", depID, classID, wfName, taskID)
                wf = WorkflowManager(wfName, depID, None, taskID)
                pid = wf.runWF(wait=False)
                m = {}
                m["depID"] = depID
                m["classID"] = classID
                m["pid"] = pid
                m["timeStamp"] = self.__timeStamp.getSecondsFromReference()
                m["status"] = "working"
                self.monitorDict[depID] = m
                #
                logger.info(
                    "+ServerMonitor.__addProcess end iteration %d of %d for %s classID %s wfName %s taskId %s  status %s", ii + 1, numT, depID, classID, wfName, taskID, m["status"]
                )

        logger.info("+ServerMonitor.__addProcess leaving after %d iterations", numT)

    def __deleteProcess(self, depid, value):  # pylint: disable=unused-argument
        """
        Removes a server engine dictionary entry  value is
        """
        del value["depID"]
        del value["pid"]
        del value["classID"]
        del value["timeStamp"]
        del value["status"]

    def __createNewBucket(self, depID, classID, file, now):
        """
        method to create a new instance entry as a place holder for a WF not previously run
        """
        ts = self.__timeStamp.getTimeStringLocal(now)
        logger.info("+ServerMonitor.__createNewBucket - begins for %s classID %s file %s timeStamp %s", depID, classID, file, ts)
        try:
            wfInstId = self.__eUtil.getNextInstanceId(depID)
            #
            sql = (
                "insert into wf_instance (wf_inst_id, wf_class_id, dep_set_id, owner, inst_status, status_timestamp) values ('"
                + wfInstId
                + "','"
                + classID
                + "','"
                + depID
                + "','"
                + file
                + "','init','"
                + str(now)
                + "')"
            )

            logger.info("+ServerMonitor.__createNewBucket - for %s classID %s owner/file %s with new wfInstID %s", depID, classID, file, wfInstId)
            logger.info("+ServerMonitor.__createNewBucket  - new bucket %s", str(sql))
            ok = self.__eUtil.runUpdateSQL(sql)
            if ok == 1:
                logger.info("+ServerMonitor.__createNewBucket wf_instance insert succeeded for %s", str(depID))
            else:
                logger.info("+ServerMonitor.__createNewBucket wf_instance insert failed for %s", str(depID))

            sql = "select dep_set_id from wf_instance_last where dep_set_id = '" + depID + "'"
            ok = self.__eUtil.runSelectSQL(sql)

            if ok is None or len(ok) < 1:
                sql = (
                    "insert into wf_instance_last (wf_inst_id, wf_class_id, dep_set_id, owner, inst_status, status_timestamp) values ('"
                    + wfInstId
                    + "','"
                    + classID
                    + "','"
                    + depID
                    + "','"
                    + file
                    + "','init','"
                    + str(now)
                    + "')"
                )
                ok = self.__eUtil.runUpdateSQL(sql)
            else:
                sql = (
                    "update wf_instance_last set wf_inst_id = '"
                    + wfInstId
                    + "', wf_class_id = '"
                    + classID
                    + "', owner = '"
                    + file
                    + "', inst_status = 'init', status_timestamp = '"
                    + str(now)
                    + "' where dep_set_id = '"
                    + depID
                    + "'"
                )
                ok = self.__eUtil.runUpdateSQL(sql)
        except Exception as e:
            logger.info("+ServerMonitor.__createNewBucket for %s function failed %s", depID, str(e))
            ok = 0

        if ok < 1:
            logger.info("+ServerMonitor.__createNewBucket failed insert in wf_instance_last for %s", str(depID))
            return False
        else:
            logger.info("+ServerMonitor.__createNewBucket wf_instance set %s classID %s owner/file %s wfInstID %s status init at %s", depID, classID, file, wfInstId, ts)
            logger.info("+ServerMonitor.__createNewBucket wf_instance_last insert succeeded for %s", str(depID))

            return True

    def __manageGetInstanceRow(self, timeNow, allRow):
        """
        Private method to get the last ordinal within the wf_instance table for a dep_id / class_id


        """

        lastOrdinal = -1

        # first - get the last wf_instance record for that ID
        #        sql = "select ordinal from wf_instance where dep_set_id = '" + str(allRow[1]) + "' and wf_class_id = '" + str(allRow[2]) + "' order by status_timestamp limit 1"
        # October-7th put in desc order :  DO NOT REMOVE CLASSID as it defines where the retart occured - which might not be the last.

        sql = (
            "select ordinal, wf_inst_id from wf_instance where dep_set_id = '"
            + str(allRow[1])
            + "' and wf_class_id = '"
            + str(allRow[2])
            + "' order by status_timestamp desc limit 1"
        )
        last = self.__eUtil.runSelectSQL(sql)
        # fail state 1 : we did not get a row - bum communication
        logger.info("+ServerMonitor.__manageGetInstanceRow - Last status from wf_instance depID %s and classId %s status %r", allRow[1], allRow[2], last)
        if last is None or len(last) < 1:
            logger.info("+ServerMonitor.__manageGetInstanceRow - %s no status returned - target row %r ", allRow[1], allRow)
            # create a bucket holder  - since WF always create a new one
            #
            if not self.__createNewBucket(allRow[1], allRow[2], allRow[6], timeNow):
                logger.info("+ServerMonitor.__manageGetInstanceRow  Failed communication depId %s %s", allRow[1], allRow[4])
                sql = "update communication set status = 'failed', actual_timestamp = " + str(timeNow) + " where ordinal = " + str(allRow[0])
                _ok = self.__eUtil.runUpdateSQL(sql)  # noqa: F841
                return -1, -1, -1
            else:
                sql = (
                    "select ordinal, wf_inst_id from wf_instance where dep_set_id = '"
                    + str(allRow[1])
                    + "' and wf_class_id = '"
                    + str(allRow[2])
                    + "' order by status_timestamp desc limit 1"
                )
                last = self.__eUtil.runSelectSQL(sql)

        for ll in last:
            lastOrdinal = ll[0]
            lastInst = ll[1]
            break

        if lastOrdinal < 0:
            logger.info("+ServerMonitor.__manageGetInstanceRow  :  Failed communication %s: %s", allRow[1], allRow[4])
            sql = "update communication set status = 'failed', actual_timestamp = " + str(timeNow) + " where ordinal = " + str(allRow[0])
            _ok = self.__eUtil.runUpdateSQL(sql)  # noqa: F841
            return -1, -1, -1

        logger.info("+ServerMonitor.__manageGetInstanceRow - classId %s lastInst %s lastOrdinal %s", allRow[2], lastInst, str(lastOrdinal))
        return lastOrdinal, lastInst, allRow[2]

    def __manageKillProcess(self, timeNow, lastOrdinal, allRow):  # pylint: disable=unused-argument
        """
        kill the process and all its children,
        This only works with processes owned by this server - and server is active (internal list)
        """
        logger.info("+ServerMonitor.__manageKillProcess starts for %s", allRow[1])
        if allRow[1] not in self.monitorDict:
            return

        value = self.monitorDict[allRow[1]]
        # check that the pid is valid - if the process is sleeping then it is NONE
        if value["pid"] is not None:
            value["status"] = "sleeping"
            # JDW -- add my process utils -
            # JDW 5-Apr-2015 add parent to child list - fix kill followed restart problem
            pidList = []
            pidList.append(value["pid"].pid)
            pidList.extend(self.__pu.getChildren(value["pid"].pid))
            logger.info("+ServerMonitor.__manageKillProcess for %s class %s pidList %r", value["depID"], value["classID"], pidList)
            self.__pu.killProcessList(pidList[::-1], mySignal=signal.SIGKILL)
        #
        logger.info("+ServerMonitor.__manageKillProcess leaving for %s", allRow[1])

    def __manageResetUpdate(self, timeNow, lastOrdinal, lastInst, lastClass, allRow):
        """
        update the reset code and change the running instance to reset
        """
        logger.info(
            "+ServerMonitor.__manageResetUpdate : starts for deposition %s lastClass %s lastInst %s lastOrdinal %r - allrow %r", allRow[1], lastClass, lastInst, lastOrdinal, allRow
        )

        sql = "update communication set status = 'INIT', activity = 'INIT',actual_timestamp = " + str(timeNow) + " where ordinal = " + str(allRow[0])
        nrow = self.__eUtil.runUpdateSQL(sql)

        depID = allRow[1]

        #  set all previous instances - take off 1 second so we don't get time overlap
        # removed 7th Nov - but back in temporarily
        # #
        sql = (
            "update wf_instance set inst_status = 'aborted', status_timestamp = "
            + str(timeNow - 1)
            + " where dep_set_id = '"
            + str(depID)
            + "' and inst_status not in ('exception','finished')"
        )
        _ok = self.__eUtil.runUpdateSQL(sql)  # noqa: F841

        # set the last instance to init
        sql = "update wf_instance set inst_status = 'init', status_timestamp = " + str(timeNow) + ", owner = '" + str(allRow[6]) + "' where ordinal = " + str(lastOrdinal)
        _ok = self.__eUtil.runUpdateSQL(sql)  # noqa: F841

        # Only need the one sql as we only have one reference for this depID
        sql = (
            "update wf_instance_last set wf_inst_id = '"
            + lastInst
            + "', inst_status = 'init', wf_class_id = '"
            + str(lastClass)
            + "', owner = 'Annotation.bf.xml', status_timestamp = "
            + str(timeNow)
            + ", owner = '"
            + str(allRow[6])
            + "' where dep_set_id = '"
            + str(depID)
            + "'"
        )
        _ok = self.__eUtil.runUpdateSQL(sql)  # noqa: F841

        logger.info("+ServerMonitor.__manageResetUpdate :  Set deposition %s  back to init (%s)\n", str(allRow[1]), str(nrow))

    def __manageWaitingUpdate(self, timeNow, lastOrdinal, allRow):
        """
        update the open code and change the running instance to waiting
        do not change the activity state
        """

        sql = "update communication set status = 'WORKING', actual_timestamp = " + str(timeNow) + " where ordinal = " + str(allRow[0])
        # OLD          sql = "update wf_instance set inst_status = 'waitingWF' where ordinal = " + str(allRow[0])
        nrow = self.__eUtil.runUpdateSQL(sql)
        # sql = "update wf_instance set inst_status = 'waiting', status_timestamp
        # = " + str(timeNow) + " where dep_set_id = '" + str(allRow[1]) + "' and
        # wf_class_id = '" + str(allRow[2]) + "' and wf_inst_id = '" +
        # str(allRow[3]) + "'"
        sql = "update wf_instance set inst_status = 'waiting', status_timestamp = " + str(timeNow) + " where ordinal = " + str(lastOrdinal)
        nrow = self.__eUtil.runUpdateSQL(sql)
        logger.info("+ServerMonitor.__manageWaitingUpdate :  Set %s open interface back to waiting (%s)\n", str(allRow[1]), str(nrow))

        sql = "update wf_instance_last set inst_status = 'waiting', status_timestamp = " + str(timeNow) + " where dep_set_id = '" + str(allRow[1]) + "'"
        nrow = self.__eUtil.runUpdateSQL(sql)

    def __manageProcess(self):
        """
        Look for PENDING status for workflows already ASSIGNED to this host (e.g. host in communication table) but not necessarily monitored by this
        server process.

        method to look for status codes in the communication that need an action
        to reset the workflow for an ID
        killWF : will kill all processes associated with that ID
                  waitWF : will unlock an open interface : setting "open" to "waiting"

        restartWF : will do a kill followed by a status code reset
        restartGoWF : will do a kill, status code reset, and reRun the WF


        WARNING :  contains work around for WFM not setting the wf_intance.
                   uses the ordinal of the last row "lastOrdinal"

        """
        #
        # JDW -- This scans for pending entries in communication table ASSIGNED to the current host -
        #
        # get all the depositions owned by this monitor from the the database
        sql = (
            "select ordinal,dep_set_id, parent_wf_class_id,parent_wf_inst_id, command, status, wf_class_file from communication where upper(status) = 'PENDING' and host = '"
            + str(self.hostname)
            + "'"
        )

        allList = self.__eUtil.runSelectSQL(sql)
        if (allList is None) or (len(allList) < 1):
            # logger.info("+ServerMonitor.__manageProcess() starting with NO pending entries")
            # jdw just return here as there is nothing to do
            return
        else:
            logger.info("+ServerMonitor.__manageProcess() starting for %d PENDING entries", len(allList))

        # Check for any missing entries in internal monitorDict

        if allList is not None:
            for row in allList:
                if row[1] in self.monitorDict.keys():
                    logger.info("+ServerMonitor.__manageProcess found monitored entry %s status %s command %s", str(row[1]), str(row[5]), str(row[4]))
                    # pass
                else:
                    #           create new dictionary item
                    m = {}
                    m["depID"] = row[1]
                    m["classID"] = row[2]
                    m["pid"] = None  # it cannot be running - this is the OBJECT not the pid value in the object !
                    m["timeStamp"] = self.__timeStamp.getSecondsFromReference()
                    m["status"] = "working"
                    self.monitorDict[row[1]] = m
                    logger.info("+ServerMonitor.__manageProcess  adding entry to the MONITORED list %s list length %s", str(row[1]), str(len(self.monitorDict)))

        timeNow = self.__timeStamp.getSecondsFromReference()
        if allList is not None:
            for allRow in allList:
                lastOrdinal, lastInst, lastClass = self.__manageGetInstanceRow(timeNow, allRow)
                logger.info("+ServerMonitor.__manageProcess - lastOrdinal %s lastInst %s lastClass %s current command %s", lastOrdinal, lastInst, lastClass, allRow[4])
                if lastOrdinal < 0:
                    return
                # just kills the process cascade
                if allRow[4] == "killWF":
                    logger.info("+ServerMonitor.__manageProcess :  killing process (killWF)\n")
                    # logger.flush()
                    self.__manageKillProcess(timeNow, lastOrdinal, allRow)
                    #          self.__manageKillUpdate(timeNow,lastOrdinal,lastInst,allRow)
                    self.__manageResetUpdate(timeNow, lastOrdinal, lastInst, lastClass, allRow)
                elif allRow[4] == "restartWF":
                    logger.info("+ServerMonitor.__manageProcess :  resetting process (restartWF)\n")
                    # This actually does not start the WF - just marks it ready to start
                    # logger.flush()
                    self.__manageKillProcess(timeNow, lastOrdinal, allRow)
                    self.__manageResetUpdate(timeNow, lastOrdinal, lastInst, lastClass, allRow)
                elif allRow[4] == "restartGoWF":
                    logger.info("+ServerMonitor.__manageProcess :  resetting process (restartGoWF)\n")
                    # This actually does the WF
                    # logger.flush()
                    self.__manageKillProcess(timeNow, lastOrdinal, allRow)
                    self.__manageResetUpdate(timeNow, lastOrdinal, lastInst, lastClass, allRow)
                    self.__markRunTest(allRow[1])

                elif allRow[4] == "waitWF":
                    logger.info("+ServerMonitor.__manageProcess :  resetting interface to waiting (waitWF)\n")
                    # logger.flush()
                    # this will set the code to waiting regardless : assumes WFM is correct
                    self.__manageWaitingUpdate(timeNow, lastOrdinal, allRow)

        logger.info("+ServerMonitor.__manageProcess() leaving after processing %d PENDING entries", len(allList))

        # logger.flush()

    def __markRunTest(self, depid):

        timeNow = self.__timeStamp.getSecondsFromReference()
        self.__markRun(timeNow, depid)

    def __markRun(self, timestamp, depid):

        sql = "update communication set command = 'runWF', actual_timestamp = " + str(timestamp) + ", receiver = 'WFE', status = 'PENDING' where dep_set_id = '" + str(depid) + "'"
        ret = self.__eUtil.runUpdateSQL(sql)

        logger.info(" ServerMonitor.__markRun update command %s ", sql)
        logger.info(" ServerMonitor.__markRun update returns %r ", ret)

        sql = "select dep_set_id, parent_wf_class_id, wf_class_id, wf_inst_id,status, activity, actual_timestamp from communication where  dep_set_id = '" + str(depid) + "'"
        myList = self.__eUtil.runSelectSQL(sql)
        logger.info("+ServerMonitor.__markRun : - myList  %r", myList)

    def __checkProcess(self):
        """
        Self monitor of the internal processs managed by this instance
        rewrite using the communication table : but instID and classID not filled
          select dep_set_id, wf_class_id, wf_inst_id,status, activity from communication
                  where dep_set_id in ('  ....... ')
        """

        ngather = 0
        nlost = 0
        nsleep = 0
        gather = ""
        ncomplete = 0
        load = 0
        delList = []

        bored = 100
        myList = None

        #
        if len(self.monitorDict) > 0:
            # JDW 5-Apr-2015 -- change to parent_wf_class_id local to this method -
            sql = "select dep_set_id, parent_wf_class_id, wf_inst_id,status, activity, actual_timestamp from communication where  dep_set_id in ("
            for depid, value in self.monitorDict.items():
                sql = sql + "'" + depid + "',"
            sql = sql[:-1] + ")"
            myList = self.__eUtil.runSelectSQL(sql)
            logger.info("+ServerMonitor.__checkProcess :  monitored status  - current monitored ID list is %r", myList)

        if myList is not None:
            for row in myList:
                depid = row[0]
                status = row[3]
                activity = row[4]
                myClass = row[1]

                if status is None or activity is None:
                    logger.debug("+ServerMonitor.__checkProcess :  Skipping %s parent class %s has status %s", str(depid), myClass, str(status))
                    continue

                if status.upper() == "WORKING" and activity.upper() == "WORKING":
                    if depid in self.monitorDict:
                        mon = self.monitorDict[depid]
                        if mon is not None and "pid" in mon:
                            if mon["pid"] is not None:
                                if mon["pid"].poll() is None:
                                    # the process has not return code - so is still running
                                    load = load + 1
                                    ngather = ngather + 1
                                    if len(gather) < 200:
                                        gather = gather + "[" + str(depid) + ",working,-]" + ";"
                                else:
                                    ncomplete = ncomplete + 1
                                    # pass
                    # return code of completed process
                    #        print " id = " , depid , "   " , instID

                elif status.upper() == "INIT":
                    # If this server owns this but nothing has happened for 1 hour - drop it
                    howlong = self.__timeStamp.getSecondsFromReference() - row[5]
                    if howlong > bored and howlong < 10000000:
                        # only delete the reference if we have been checking for 1 hour
                        # this will be picked up later from the WFM
                        logger.info("+ServerMonitor.__checkProcess %s with INIT status added to delete list", str(depid))
                        delList.append(depid)

                    nlost = nlost + 1
                elif status.upper() == "FINISHED":
                    # If this server owns this but nothing has happened for 1 hour - drop it
                    # Workflow finished correctly - no way of starting again - temporary fix
                    howlong = self.__timeStamp.getSecondsFromReference() - row[5]
                    if howlong > bored and howlong < 10000000:
                        # only delete the reference if we have been checking for 1000 seconds
                        logger.info("+ServerMonitor.__checkProcess %s with FINISHED status added to delete list", str(depid))
                        delList.append(depid)
                    nlost = nlost + 1
                elif status.upper() == "EXCEPTION" or status[-1].upper() == "X":
                    # logger.debug("+ServerMonitor.__checkProcess :  Workflow for " + str(depid) + " parent class " + myClass + " has status " + str(status))
                    # logger.flush()
                    nlost = nlost + 1
                elif status.upper() == "WORKING" and activity.upper() == "SLEEPING":
                    # actually not done as I filter for working processes
                    load = load + 0.001
                    nsleep = nsleep + 1
                    ngather = ngather + 1
                    if len(gather) < 200:
                        pass
                #               gather = gather + "[" + str(depid) + ",sleeping,-]" + ";"

        for depid in delList:
            # temporary fix - what the hell ?
            if depid in self.monitorDict:
                mon = self.monitorDict[depid]
                if self.__timeStamp.getSecondsFromReference() - mon["timeStamp"] > bored:
                    # the action in the internal monitor is old too (ie we have not just tried to do something)
                    logger.info("+ServerMonitor.__checkProcess  deleting %s from monitor dictionary - current length %s", str(depid), str(len(self.monitorDict)))
                    value = self.monitorDict[depid]
                    # jdw this does nothing
                    self.__deleteProcess(depid, value)
                    del self.monitorDict[depid]

        logger.debug("+ServerMonitor.__checkProcess  host %s load %d nsleep %d nlost %d ngather %d gather %r ", self.hostname, load, nsleep, nlost, ngather, gather)
        self.__updateResourceStatus(gather)

        return load

    def __updateResourceStatus(self, gather):
        """
        Process to monitor the server load - writes a status entry

        # JDW -- not sure how this is used.  Fixed all of the backend calls --

        """
        logger.debug("+ServerMonitor.__updateResourceStatus() - starting host %s engine_monitoring update ", self.hostname)
        if len(gather) > 3:
            if gather.endswith(";"):
                gather = gather[:-1]
        #
        MemInfo = self.__pu.getMemoryInfo()
        CpuInfo = self.__pu.getCpuInfo()

        sql = "select hostname from engine_monitoring where hostname = '" + self.hostname + "'"
        myList = self.__eUtil.runSelectSQL(sql)

        timeNow = self.__timeStamp.getSecondsFromReference()
        #
        if len(myList) > 0:
            sql = (
                "update engine_monitoring set  total_physical_mem = "
                + str(MemInfo["MemTotal"])
                + ", total_virtual_mem = "
                + str(MemInfo["TotalTotal"])
                + ", physical_mem_usage = "
                + str(MemInfo["MemUsed"])
                + ", virtual_mem_usage = "
                + str(MemInfo["SwapUsed"])
                + ", swap_total = "
                + str(MemInfo["SwapTotal"])
                + ", swap_used = "
                + str(MemInfo["SwapUsed"])
                + ", swap_free = "
                + str(MemInfo["SwapFree"])
                + ", cached = "
                + str(MemInfo["Cached"])
                + ", buffers = "
                + str(MemInfo["Buffers"])
                + ",cpu_number = "
                + str(CpuInfo["Ncpu"])
                + " , cpu_usage = "
                + str(CpuInfo["Usage"])
                + ", ids_set = '"
                + gather
                + "' , status_timestamp = "
                + str(timeNow)
                + " where hostname = '"
                + str(self.hostname)
                + "'"
            )
        else:
            sql = (
                "insert engine_monitoring (hostname,total_physical_mem,total_virtual_mem,physical_mem_usage,virtual_mem_usage,swap_total,swap_used,swap_free,cached,buffers,cpu_number,cpu_usage,ids_set,status_timestamp) values ('"  # noqa: E501
                + str(self.hostname)
                + "', "
                + str(MemInfo["MemTotal"])
                + ","
                + str(MemInfo["TotalTotal"])
                + " , "
                + str(MemInfo["MemUsed"])
                + ", "
                + str(MemInfo["SwapUsed"])
                + ", "
                + str(MemInfo["SwapTotal"])
                + ","
                + str(MemInfo["SwapUsed"])
                + ", "
                + str(MemInfo["SwapFree"])
                + ","
                + str(MemInfo["Cached"])
                + ","
                + str(MemInfo["Buffers"])
                + ","
                + str(CpuInfo["Ncpu"])
                + ", "
                + str(CpuInfo["Usage"])
                + " , '"
                + gather
                + "' , "
                + str(timeNow)
                + ")"
            )

        ret = self.__eUtil.runUpdateSQL(sql)
        if ret is None or ret < 1:
            logger.info("+ServerMonitor.__updateResourceStatus() - host %s engine_monitoring update failed  sql = %s", self.hostname, sql)

    def __isRunningProcess(self, depID, myName="mainEngine"):
        """
        Method to return a list of process ids for current server monitor and child 'workmanager' processes.
        First list is the ones owned the current parent process and the second list is owned by a different process group.

        JDW -- remove exit condition for this method
        """

        myList = self.__pu.findProcesses(key="cmdline", value=myName, op="str_in")
        myPidList = [t[0] for t in myList]

        oList = self.__pu.findProcesses(key="cmdline", value=depID, op="str_in")

        retMe = []
        retOther = []

        if myList is None or len(myList) < 1:
            logger.info("ServerMonitor.__isRunningProcess : WARNING - Could not find processes ids for entry %r process %r", depID, myName)
            return retMe, retOther

        for oTup in oList:
            if oTup[1] in myPidList:
                retMe.append(oTup[0])
            else:
                retOther.append(oTup[0])
        return retMe, retOther

    def __wakeUpWorkflow(self):
        """
        For all sleeping WF we need review whether the wf_instance state has changed
        This could be slow and so I need to review this as we may have many 1000 of
        sleeping WF.  Probably OK for UI - how do we manage 'review' can we get this
          to poke something directly to the communication table.

        (thinking - In WFE - if communication = "sleeping" for a "closed(?) UI we could
                    could update communication to "wakeup"

        Note : I have put in a cludge for now : I wait 60 seconds for the WF to start running before
               checking to wake it up

        """

        timeNow = self.__timeStamp.getSecondsFromReference()

        sql = (
            "select communication.ordinal,wf_instance_last.dep_set_id,wf_class_file,communication.host from wf_instance_last,communication where wf_instance_last.dep_set_id = communication.dep_set_id and communication.host = '"  # noqa: E501
            + self.hostname
            + "' and communication.activity = 'SLEEPING' and wf_instance_last.inst_status not in ("
        )
        for valid in self.validSleep:
            sql = sql + "'" + str(valid) + "',"
        # Problem - when is a wakeup call stale ?
        #  We have an issue that if the server is off line we lose the wakeup.
        #  If we make this longer, then sleep/wake bounces
        #
        sql = sql[:-1] + ") and (" + str(timeNow) + " - wf_instance_last.status_timestamp) < 60"

        myList = self.__eUtil.runSelectSQL(sql)

        if myList is None or len(myList) == 0:
            return
        else:
            for row in myList:
                logger.info("+ServerMonitor.__wakeUpWorkflow : detected sleeping entry %r with new task %r\n", row[1], row[2])
                # wait 1 minute to get the process started
                if row[1] in self.monitorDict:
                    m = self.monitorDict[row[1]]
                    if m["status"] == "sleeping":
                        logger.info("+ServerMonitor.__wakeUpWorkflow : checking monitored sleeping entry %r with new task %r\n", row[1], row[2])
                        pid, _subPid = self.__isRunningProcess(row[1], myName=self.__baseEngineProcessName)
                        if pid is None or len(pid) == 0:
                            m["status"] = "working"
                            command = "update communication set activity = 'WORKING', actual_timestamp = " + str(timeNow) + " where ordinal in (" + str(row[0]) + ")"
                            _nrow = self.__eUtil.runUpdateSQL(command)  # noqa: F841
                            # need to recover the annotation flow - so run the annotation-WF at the correct module-WF at the correct task
                            # there is no process so run it
                            # look up a workflow nesting of task
                            # if there is a workflow nesting, then force a ,looup from annotate root, otherwise just recover
                            n = row[2].find(":")
                            if n > 0:
                                row[2] = row[2][:n]
                                wf = WorkflowManager(row[2], row[1], "recoverannotate", "recover")
                            else:
                                wf = WorkflowManager(row[2], row[1], "recover", "recover")

                            logger.info("+ServerMonitor.__wakeUpWorkflow : recovered %s at %s", str(row[1]), str(row[2]))

                            pid = wf.runWF(wait=False)
                            # set the ID to the new ownership
                            m["pid"] = pid
                        else:
                            m["status"] = "working"
                            logger.info("+ServerMonitor.__wakeUpWorkflow : Error : workflow for %s is running - impossible ", str(row[1]))
                    else:
                        logger.info("+ServerMonitor.__wakeUpWorkflow Process is already working %s", str(row[1]))
                else:
                    # JDW --
                    logger.info("+ServerMonitor.__wakeUpWorkflow : ignoring sleeping entry %r with new task %r on host %s\n", row[1], row[2], row[3])

    def __showMonitored(self):
        """Log the current list of monitored entries"""
        logger.info("+ServerMonitor.__showMonitored  total monitored entries %d", len(self.monitorDict))
        for ky in self.monitorDict.keys():
            m = self.monitorDict[ky]
            logger.info("+++++      %-10s %-10s", m["depID"], m["status"])

    def __monitorRestart(self, verbose=False):
        """
        Method to recover the run time state of the monitoring server from data in the communication table

        1) Get all entries ASSIGNED to this host/server in WORKING or SLEEPING state
        2) If a workflow is working - restart with recovery, add the entry

        """
        if verbose:
            logger.info("+ServerMonitor.__monitorRestart STARTING ----------------------------------------------------  ")
            logger.info("+ServerMonitor.__monitorRestart INITIAL MONITOR LIST  ---------------------------------------")
            self.__showMonitored()

        sql = "select ordinal,dep_set_id,activity,wf_class_file from communication where host = '" + self.hostname + "' and activity in ('SLEEPING', 'WORKING' )"
        allList = self.__eUtil.runSelectSQL(sql)

        if verbose:
            logger.info("+ServerMonitor.__monitorRestart found candidate entries ASSIGNED to host %s = %s", str(self.hostname), str(len(allList)))

        for row in allList:
            #  - skip any monitored entries -
            if row[1] in self.monitorDict:
                continue
            _pidMe, pidOther = self.__isRunningProcess(row[1], myName=self.__baseEngineProcessName)
            if pidOther is not None:
                self.__pu.killProcessList(pidOther)
            #
            if row[2] == "WORKING":
                #
                n = row[3].find(":")
                if n > 0:
                    row[3] = row[3][:n]
                    wf = WorkflowManager(row[3], row[1], "recoverannotate", "recover")
                else:
                    wf = WorkflowManager(row[3], row[1], "recover", "recover")

                logger.info("+ServerMonitor.__monitorRestart : recovering WORKING entry %s with activity %s", str(row[1]), str(row[2]))
                pid = wf.runWF(wait=False)
                m = {}
                m["depID"] = row[1]
                m["classID"] = row[3]
                m["pid"] = pid
                m["timeStamp"] = self.__timeStamp.getSecondsFromReference()
                m["status"] = "working"
                self.monitorDict[row[1]] = m
            elif row[2] == "SLEEPING":
                #
                m = {}
                logger.info("+ServerMonitor.__monitorRestart:  monitoring SLEEPING entry %s", str(row[1]))
                m["depID"] = row[1]
                m["classID"] = row[3]
                m["pid"] = None
                m["timeStamp"] = self.__timeStamp.getSecondsFromReference()
                m["status"] = "sleeping"
                self.monitorDict[row[1]] = m
        #
        if verbose:
            logger.info("+ServerMonitor.__monitorRestart REVISED MONITOR LIST  ---------------------------------------")
            self.__showMonitored()
            logger.info("+ServerMonitor.__monitorRestart COMPLETED  ---------------------------------------")
        #

    def __sleepWorkFlow(self):
        """
          Looks for idle ACTIVE (WORKING) entries with  instance status (waiting/open)


        method to review the current running annotations and look for WF that
        are not doing anything
        a) open or waiting UI   (wf_instance.status = 'waiting' or 'open')
        b) waiting for decision update from journal/depositor/annotator
                      (wf_instance = 'review') ????
        1) Open/waiting UI can be put to sleep
        2) Must be very careful what we put to sleep - processes and workflows cannot be slept - they are active.

        We just kill all processes associated with this WF if they have done
          nothing for at least 1 hour

        """

        timeNow = self.__timeStamp.getSecondsFromReference()

        # get all WF that are owned by this server that have 'working' status but have not changed state for "purgetime"

        sql = (
            "select communication.ordinal,wf_instance.dep_set_id from wf_instance,communication where wf_instance.dep_set_id = communication.dep_set_id and communication.host = '"
            + self.hostname
            + "' and communication.activity = 'WORKING' and wf_instance.inst_status in ("
        )
        for valid in self.validSleep:
            sql = sql + "'" + str(valid) + "',"

        sql = sql[:-1] + ") and (" + str(timeNow) + " - wf_instance.status_timestamp) > " + str(self.purgeTime)

        allList = self.__eUtil.runSelectSQL(sql)

        if allList is None or len(allList) < 1:
            return

        command = "update communication set activity = 'SLEEPING', actual_timestamp = " + str(timeNow) + " where ordinal in ("

        n = 0
        if allList is not None:
            for allRow in allList:
                if allRow[1] in self.monitorDict:
                    m = self.monitorDict[allRow[1]]
                    if m["status"] == "working":
                        logger.info("+ServerMonitor.__sleepWorkFlow : checking process list workflow for %s ", allRow[1])
                        pid, _other = self.__isRunningProcess(allRow[1], myName=self.__baseEngineProcessName)
                        if pid is not None:
                            m["status"] = "sleeping"
                            logger.info("+ServerMonitor.__sleepWorkFlow : killing processes for %s ", allRow[1])
                            self.__manageKillProcess(timeNow, 0, allRow)
                            command = command + str(allRow[0]) + ","
                            n = n + 1
                        else:
                            logger.info("+ServerMonitor.__sleepWorkFlow : no process associated with %r", allRow[1])
                            m["status"] = "sleeping"
                    else:
                        logger.info("+ServerMonitor.__sleepWorkFlow found unexpected workflow in sleeping  state for %r", allRow[1])
                        m["status"] = "sleeping"

        command = command[:-1] + ")"

        if n > 0:
            nrow = self.__eUtil.runUpdateSQL(command)
            logger.info("+ServerMonitor.__sleepWorkFlow  workflow sleeper - number of ID's put to sleep = %s", str(nrow))
        else:
            # JDW this update code is never applied so there are no DEAD workflows !
            command = "update communication set activity = 'DEAD', actual_timestamp = " + str(timeNow) + " where ordinal in ("
            p = ""
            for allRow in allList:
                #    logger.info("+ServerMonitor.sleepWorkFlow  ID = " + str(allRow[1]))
                command = command + str(allRow[0]) + ","
                p = p + str(allRow[0]) + ","
            command = command[:-1] + ")"
            # logger.info("+ServerMonitor.sleepWorkFlow  Warning : Stale working deposition : No process found to kill for now " + str(p))
            #      nrow = self.__eUtil.runUpdateSQL(command)

    def __getStatusData(self, inStatus, outStatus):  # pylint: disable=unused-argument
        """
        Returns a list (1) of dictionaries describing PENDING workflows TO BE monitored by this system.

        This method ASSIGNS hostname in the communication table.

        inStatus: is the target command in the communication table (e.g runWF)

        outStatus:  NOT USED

        Returns:  data ONLY from the communications table for the selected PENDING entry -

        """

        # Take the rowLimit=1 list of pending tasks in communication table with command = inStatus
        #
        command = (
            "select communication.ordinal, communication.dep_set_id, communication.wf_class_ID, communication.wf_inst_id,communication.wf_class_file, communication.sender, communication.actual_timestamp, parent_wf_class_id from communication where communication.receiver = 'WFE' and communication.command = '"  # noqa: E501
            + inStatus
            + "' and communication.status = 'PENDING' limit "
            + str(self.rowLim)
        )

        myList = self.__eUtil.runSelectSQL(command)

        if len(myList) < 1:
            return {}

        # just to make sure we capture multiple pending for one ID

        timeNow = self.__timeStamp.getSecondsFromReference()
        tS = self.__timeStamp.getTimeStringLocal(timeNow)
        me = self.hostname
        #
        # This will always return something -  command = "update communication set
        # activity = 'WORKING', status = 'WORKING', host = '" + me + "',
        # actual_timestamp = " + str(timeNow) + " where ordinal in ("

        # this will only update a row if the status was pending - and this server obtained the work - all server make the same generic request
        command = "update communication set activity = 'WORKING', status = 'WORKING'  where ordinal in ("
        for row in myList:
            command = command + str(row[0]) + ","
        command = command[:-1] + ")"

        nrow = self.__eUtil.runUpdateSQL(command)
        logger.info("+SeverMonitor.getStatusData updated %d rows with WORKING status ordinals %r at %s", nrow, myList, tS)

        # Logic only works for limit = 1 for now, if we updated no rows, then we did not get ownership of rows.
        if nrow == 0:
            return []
        else:
            ret = []
            # now we own job - mark the host and time stamp
            command = "update communication set host = '" + me + "', actual_timestamp = " + str(timeNow) + " where ordinal in ("
            for row in myList:
                command = command + str(row[0]) + ","
            command = command[:-1] + ")"
            nrow = self.__eUtil.runUpdateSQL(command)
            if nrow > 0:
                for row in myList:
                    rdict = {}
                    rdict["DEP_SET_ID"] = row[1]
                    rdict["WF_INST_ID"] = row[3]
                    rdict["WF_CLASS_FILE"] = row[4]
                    # class_id or parent_class_id
                    if row[2]:
                        rdict["WF_CLASS_ID"] = row[2]
                    else:
                        rdict["WF_CLASS_ID"] = row[7]
                    ret.append(rdict)
                    logger.info("+SeverMonitor.getStatusData returns dict %r ", rdict.items())
                    break
            else:
                logger.info("+ServerMonitor.getStatusData : Failed to get the job %s", str(command))
                ret = []
            return ret

    def __getWorkStep(self):

        load = self.__checkProcess()

        if load > self.normalLoad:
            if load > self.extremeLoad:
                return 3
            else:
                return 2
        else:
            return 1

    # --------------------------------------------------------------------------------------------------------------
    def XwatchList(self, serverList):
        """
        Get the list of wf-instances that should be active
        running - check the serverList to see if anyone owns this - it should be active
        closed(?) - this is waiting to be picked up by a server - does a server own this ?
        waiting/open are valid states for states that are not managed by a server
        """

        # get the list of ID which are running or closed
        sql = "select distinct(dep_set_id) from wf_instance where substr(inst_status,1,4) in ('runn','clos') and substr(dep_set_id,1,2) = 'D_'"

        myList = self.__eUtil.runSelectSQL(sql)

        if len(myList) == 0:
            # there are no ID running or closed
            return
        else:
            for row in myList:
                # check the server list to see if someone owns this entry
                found = False
                for serverID in serverList:
                    if serverID[2].find(row[0]) >= 0:
                        found = True
                        break
                if not found:
                    # No server owns this deposition
                    #          print " No server owns dep_set_id = " + str(row[0])
                    sql = (
                        "select wf_class_id,wf_inst_id,inst_status,status_timestamp,owner from wf_instance where dep_set_id = '"
                        + row[0]
                        + "' and wf_class_id <> 'popDB' order by status_timestamp desc limit 1"
                    )
                    watch = self.__eUtil.runSelectSQL(sql)
                    if watch is not None:
                        for row2 in watch:
                            mode = 0
                            if row2[2].find("clos") >= 0:
                                # we have found a closed dep_set_id
                                logger.info("Found a closed UI %s, %s, %s", str(row[0]), str(row2[0]), str(row2[1]))
                                mode = 1
                            elif row2[2].find("runn") >= 0:
                                logger.info("Found a running dep %s, %s, %s", str(row[0]), str(row2[0]), str(row2[1]))
                                mode = 2
                            # get the current task for this instance
                            if mode > 0:
                                sql = "select wf_task_id from wf_task where dep_set_id = '" + row[0] + "' and wf_inst_id = '" + row2[1] + "' order by status_timestamp desc limit 1"
                                tasks = self.__eUtil.runSelectSQL(sql)
                                taskID = None
                                if tasks is not None:
                                    for task in tasks:
                                        taskID = task[0]
                                        logger.info("        current task = %s", taskID)
                                if taskID is not None:
                                    m = {}
                                    # At this stage we can see that no server has access to this process.
                                    # we need to see if the process is actually running already
                                    logger.info("running workflow to capture orphen job")
                                    pids, _subPid = self.__isRunningProcess(row[0], myName=self.__baseEngineProcessName)
                                    if pids is None or len(pids) < 1:
                                        # there is no process so run it
                                        wf = WorkflowManager(row2[4], row[0], None, taskID)
                                        pid = wf.runWF(wait=False)
                                        m["pid"] = pid
                                    else:
                                        if len(pids) == 1:
                                            m["pid"] = pids[0]
                                        else:
                                            #  we need to find the parent
                                            m["pid"] = pids[0]
                                            logger.info(" Oh crap - I got multiple ID ")
                                    m = {}
                                    m["depID"] = row[0]
                                    m["classID"] = row2[4]
                                    m["timeStamp"] = self.__timeStamp.getSecondsFromReference()
                                    m["status"] = "working"
                                    self.monitorDict[row[0]] = m
