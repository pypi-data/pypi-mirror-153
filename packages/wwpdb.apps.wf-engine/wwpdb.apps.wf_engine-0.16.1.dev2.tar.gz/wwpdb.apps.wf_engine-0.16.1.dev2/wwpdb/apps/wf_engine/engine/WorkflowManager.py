##
# File:    WorkflowManager.py
# Date:    15-Mar-2015
#
# Updates:
#   20-Mar-2015   jdw cleanup all of the hardcoded and inconsistent pathing
#                     move logfiles out data directories --
#
#
##
import time
import os
import threading
import subprocess
import logging
from wwpdb.utils.config.ConfigInfo import ConfigInfo, getSiteId

logger = logging.getLogger(name="root")


class WorkflowManager(threading.Thread):
    def __init__(self, file, depID, instID, taskID="entry-point"):
        threading.Thread.__init__(self)
        self.status = 0
        self.file = file

        self.depID = depID
        self.instID = instID
        self.taskID = taskID
        self.__siteId = getSiteId(defaultSiteId="WWPDB_DEPLOY_TEST")
        self.__cI = ConfigInfo(self.__siteId)
        self.__wfXmlPath = self.__cI.get("SITE_WF_XML_PATH")

    # def setCommand(self, command):
    #     self.command = command

    def abort(self):
        self.status = 8

    def runWF(self, wait):

        self.status = 1

        logDir = self.__getLogDirectoryPath(self.depID)
        logFile = os.path.join(logDir, str(self.depID) + "_WF_" + str(self.file[:-4]) + ".log")
        logger.info("+WorkflowManager.runWF() -------------------------------------------------------")
        logger.info("+workflowManager.runWF() :    siteID       = %s", str(self.__siteId))
        logger.info("+workflowManager.runWF() :     depID       = %s", str(self.depID))
        logger.info("+workflowManager.runWF() :  WF class file  = %s", str(self.file))
        logger.info("+workflowManager.runWF() :   taskID        = %s", str(self.taskID))
        logger.info("+workflowManager.runWF() :  XML path       = %s", self.__wfXmlPath)
        logger.info("+workflowManager.runWF() :   logfile       = %s", str(logFile))
        logger.info("+workflowManager.runWF() : wait flag       = %s", str(wait))

        if self.instID is None:
            args = [
                "python",
                "-m",
                "wwpdb.apps.wf_engine.engine.mainEngine",
                "-0",
                "-s",
                self.depID,
                "-t",
                self.taskID,
                "-d",
                "2",
                "-l",
                logFile,
                "-w",
                self.file,
                "-p",
                self.__wfXmlPath,
            ]
        else:
            args = [
                "python",
                "-m",
                "wwpdb.apps.wf_engine.engine.mainEngine",
                "-0",
                "-s",
                self.depID,
                "-i",
                self.instID,
                "-t",
                self.taskID,
                "-d",
                "2",
                "-l",
                logFile,
                "-w",
                self.file,
                "-p",
                self.__wfXmlPath,
            ]

        istat = subprocess.Popen(args)
        if wait:
            istat.wait()

        self.status = 2
        time.sleep(1)
        logger.info("+WorkflowManager.runWF() workflow subprocess for %s task %r with pid %r", self.depID, self.taskID, str(istat))
        logger.info("+WorkflowManager.runWF() -------------------------------------------------------")
        return istat

    def run(self):

        self.status = 1
        logDir = self.__getLogDirectoryPath(self.depID)
        logFile = os.path.join(logDir, str(self.depID) + "_WF_" + str(self.file[:-4]) + ".log")
        logger.info("+workflowManager.run() :   siteID      = %s", str(self.__siteId))
        logger.info("+WorkFlowManager.run() :   depID       = %s", str(self.depID))
        logger.info("+WorkFlowManager.run() : WF class file = %s", str(self.file))
        logger.info("+WorkFlowManager.run() :  taskID       = %s", str(self.taskID))
        logger.info("+WorkFlowManager.run() : XML path      = %s", self.__wfXmlPath)
        logger.info("+WorkFLowManager.run() : logfile       = %s", str(logFile))

        if self.instID is None:
            args = [
                "python",
                "-m",
                "wwpdb.apps.wf_engine.engine.mainEngine",
                "-0",
                "-s",
                self.depID,
                "-t",
                self.taskID,
                "-d",
                "2",
                "-l",
                logFile,
                "-w",
                self.file,
                "-p",
                self.__wfXmlPath,
            ]

        else:
            args = [
                "python",
                "-m",
                "wwpdb.apps.wf_engine.engine.mainEngine",
                "-0",
                "-s",
                self.depID,
                "-i",
                self.instID,
                "-t",
                self.taskID,
                "-d",
                "2",
                "-l",
                logFile,
                "-w",
                self.file,
                "-p",
                self.__wfXmlPath,
            ]

        istat = subprocess.call(args)
        if istat == 0:
            self.status = 2
        else:
            self.status = 3
        time.sleep(1)
        #
        logger.info("+WorkflowManager.run() workflow subprocess for %s task %r returns value %r ", self.depID, str(self.taskID), str(istat))
        logger.info("+WorkflowManager.run() -------------------------------------------------------")
        return

    def workflowStatus(self):
        return self.status

    def __getLogDirectoryPath(self, depID):

        topSessionPath = self.__cI.get("SITE_WEB_APPS_TOP_SESSIONS_PATH")
        logDir = os.path.join(topSessionPath, "wf-logs", depID)

        if not os.path.exists(logDir):
            os.makedirs(logDir)

        return logDir
