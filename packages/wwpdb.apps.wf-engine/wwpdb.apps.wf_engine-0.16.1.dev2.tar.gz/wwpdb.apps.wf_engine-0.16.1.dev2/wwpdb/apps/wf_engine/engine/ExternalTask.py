##
# File:    ExternalTask.py
# Date:    15-Mar-2009
#
# Updates:
#  22-April-2010 : Incorporation into enterpise.
#  #
#  15-Feb-2015   jdw - Gutted -  strip out broken gui console
#   5-Apr-2015   jdw   Adjust logging output -
#  2-May-2015    jdw   refactor -
#  1-Jun-2016    jdw   review for restart/recovery issues -
#
##

"""
The external task processor.
"""


import time
import sys
import datetime
import logging

from wwpdb.apps.wf_engine.wf_engine_utils.time.TimeStamp import TimeStamp

logger = logging.getLogger(name="root")


class ExternalTask(object):

    """
    This task manager is for the control and access to the manual interfaces

    All communication is via the statusDB
      handleExternalTask : puts in "waiting"
      This method is aware of an interface "open" ; but takes no action (for now)
      The exit condition is "closed(<N>)" within the statusDB; N = return condition from interface
    Note :
      The WFM uses the instance data for testing, the WFE is based on task data.  Therefore this
        method uses both the instance and task data for communication.

    """

    def __init__(self, eUtil, depositionID, WorkflowClassID, WorkflowInstanceID, task, debug=0, recovery=0):

        self.task = task
        self.__debug = debug
        self.WorkflowInstanceID = WorkflowInstanceID
        self.WorkflowClassID = WorkflowClassID
        self.depositionID = depositionID
        self.recovery = recovery
        self.__timeStamp = TimeStamp()
        self.__eUtil = eUtil
        logger.info("\n+ExternalTask.__init__ : ------------------------------------------------------------------------------------")
        logger.info(
            "+ExternalTask.__init__ : depositionId %r workflowclassid %r workflowinstanceid %r task.name %r recovery %r\n",
            depositionID,
            WorkflowClassID,
            WorkflowInstanceID,
            task.name,
            recovery,
        )

    def __setDBTaskStatus(self, typein, mode):  # pylint: disable=unused-argument
        """
        Method to update the wf_task table - audit trail data for WFE

        type: argument not used --
        """

        taskID = {}
        taskID["WF_TASK_ID"] = self.task.name
        taskID["WF_INST_ID"] = self.WorkflowInstanceID
        taskID["WF_CLASS_ID"] = self.WorkflowClassID
        taskID["DEP_SET_ID"] = self.depositionID
        taskID["STATUS_TIMESTAMP"] = self.__timeStamp.getSecondsFromReference()

        self.__eUtil.updateStatus(taskID, mode)

    def __setDBInstStatus(self, typein, mode):  # pylint: disable=unused-argument
        """
        Method to update the wf_instance table - WFM communication

        type: argument not used -

        """

        now = self.__timeStamp.getSecondsFromReference()
        instDB = {}
        instDB["WF_INST_ID"] = self.WorkflowInstanceID
        instDB["WF_CLASS_ID"] = self.WorkflowClassID
        instDB["DEP_SET_ID"] = self.depositionID
        instDB["STATUS_TIMESTAMP"] = now
        self.__eUtil.updateStatus(instDB, mode)
        # Tom :  update the wf_instance_last table - note it is unique over dep_set_id

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
        ok = self.__eUtil.runUpdateSQL(sql)
        if ok < 1:
            logger.info("+ExternalTask.__setDBInstStatus - CRITICAL : failed to update wf_instance_last table\n")

    def __getDBInstStatus(self):
        """
        Method to get the status of the instance - for WFM communication
        """

        self.__eUtil.updateConnection()

        instID = self.__eUtil.getObject(self.depositionID, self.WorkflowClassID, self.WorkflowInstanceID)

        if instID is None:
            logger.info("+ExternalTask.__getDBInstStatus :  *** Database went away ***\n")
            logger.info("+ExternalTask.__getDBInstStatus : Exception : database went away\n")
            logger.info("+ExternalTask.__getDBInstStatus : Manual task : getDBInstStatus \n")
            logger.info("+ExternalTask.__getDBInstStatus : UTC time = %s\n", str(datetime.datetime.utcnow()))
            sys.exit(0)

        else:
            ret = self.__eUtil.getStatus(instID)

        return ret

    def handleTask(self):
        """
        The main wait function for the manual interface.  loop for wait
        for the statusDB to change.

        Note that the wait is on the instance state (to reduce contention for  WFM and interfaces)

        """
        logger.info(
            "\n+ExternalTask.handleExternalTask : starts with id %s  class %s instance %s task.name %r recovery %r",
            self.depositionID,
            self.WorkflowClassID,
            self.WorkflowInstanceID,
            self.task.name,
            self.recovery,
        )
        # set the instance and task  status to waiting
        if self.recovery == 0:
            logger.info("+ExternalTask.handleExternalTask : depositionID %r task.name %r set task status WAITING", self.depositionID, self.task.name)
            self.__setDBTaskStatus("manual", "waiting")

        # put in a passthrough for restarting interfaces - ie if the UI has put closed into
        # the status DB then we don't want to overwrite this - just pass stright through and capture this
        if self.recovery == 0:
            logger.info("+ExternalTask.handleExternalTask : depositionID %r task.name %r set instance status WAITING", self.depositionID, self.task.name)
            self.__setDBInstStatus("manual", "waiting")

        # A short sleep to make sure everyone is up and waiting.
        try:
            time.sleep(1.0)
        except Exception as _e:  # noqa: F841
            logger.info("+ExternalTask.handleExternalTask :  Exception during timer %s ", self.depositionID)
            return str(-1)

        startTime = datetime.datetime.now()

        opened = False
        while True:
            state = self.__getDBInstStatus()

            if self.__debug > 3:
                elapsedT = datetime.datetime.now() - startTime
                logger.debug(
                    "+ExternalTask.handleExternalTask :  id %s  class %s instance %s elapsed (secs) %d state %r ",
                    self.depositionID,
                    self.WorkflowClassID,
                    self.WorkflowInstanceID,
                    elapsedT.total_seconds(),
                    str(state),
                )

            if state[:6] == "closed":
                n1 = state.find("(")
                n2 = state.find(")")
                if n1 >= 0 and n2 > (n1 + 1):
                    ret = state[n1 + 1 : n2]
                else:
                    # we get the default return state from the interface
                    ret = "0"
                # reset the instance state for the WFM
                self.__setDBInstStatus("manual", "running")
                logger.info("+ExternalTask.handleExternalTask : depositionID %r detected CLOSED instance status - reset to running", self.depositionID)
                break
            elif state == "close(o)" or state == "close(0)" or state == "closed()":
                # cludge from wrong interface return - probably don't need this
                ret = "0"
                # reset the instance state for the WFM
                self.__setDBInstStatus("manual", "running")
                logger.info("+ExternalTask.handleExternalTask : depositionID %r detected CLOSED instance status - set to running", self.depositionID)
                break
            elif state == "open":
                # still waiting - but the interface is now open
                if not opened:
                    logger.info("+ExternalTask.handleExternalTask : depositionID %r detected OPEN instance status - update LAST instance", self.depositionID)
                    opened = True
                    # manage the UI not knowing about this new table
                    sql = (
                        "update wf_instance_last set status_timestamp="
                        + str(self.__timeStamp.getSecondsFromReference())
                        + ", inst_status='open', wf_class_id = '"
                        + self.WorkflowClassID
                        + "', wf_inst_id = '"
                        + self.WorkflowInstanceID
                        + "' where dep_set_id = '"
                        + self.depositionID
                        + "'"
                    )

                    _ok = self.__eUtil.runUpdateSQL(sql)  # noqa: F841
            elif state == "waiting":
                # still waiting - no one has opened the interface
                pass  # pylint: disable=unnecessary-pass
            elif state == "exception":
                # the interface threw and exception code
                logger.info("+ExternalTask.handleExternalTask : depositionID %r detected EXCEPTION instance status - reset to exception", self.depositionID)
                self.__setDBInstStatus("manual", "exception")
                ret = str(-1)
                break
            elif state == "aborted":
                # the interface threw and exception code
                logger.info("+ExternalTask.handleExternalTask : depositionID %r detected ABORTED instance status - reset to ABORTED", self.depositionID)
                self.__setDBInstStatus("manual", "aborted")
                ret = str(-1)
                break

            try:
                time.sleep(0.7)
            except Exception as _e:  # noqa: F841
                # someone killed the WFE wait : register an exception
                logger.info("+ExternalTask.handleExternalTask :  Exception during timer %s ", self.depositionID)
                self.__setDBInstStatus("manual", "exception")
                ret = str(-1)
                break

        logger.info(
            "\n+ExternalTask.handleExternalTask : ENDS for id %s  class %s instance %s task.name %r recovery %r return value %r",
            self.depositionID,
            self.WorkflowClassID,
            self.WorkflowInstanceID,
            self.task.name,
            self.recovery,
            ret,
        )
        #
        return int(ret)
