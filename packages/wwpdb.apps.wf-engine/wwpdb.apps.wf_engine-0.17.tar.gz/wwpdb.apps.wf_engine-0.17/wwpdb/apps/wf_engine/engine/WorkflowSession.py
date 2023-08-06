##
# File:    WorkflowSession.py
# Date:    15-Mar-2009
#
# Updates:
#  10-May-2010 : convert to use the status DB
#
#  2-May-2015  jdw -- Refactor -- sql and db connections
##

"""
  class to manage recovery from old workflow states
"""

import sys
import logging
from wwpdb.apps.wf_engine.wf_engine_utils.time.TimeStamp import TimeStamp

logger = logging.getLogger(name="root")


class WorkflowSession(object):
    def __init__(self, eUtil, depID, classID, debug=True, prt=sys.stderr):  # pylint: disable=unused-argument
        self.depID = depID
        self.classID = classID
        self.__eUtil = eUtil
        self.__timeStamp = TimeStamp()
        self.debug = debug
        self.taskID = None
        # self.__lfh = prt

    def autoRecover(self):

        instID = self.__getLastInstanceID()

        if instID is None:
            return None, None

        taskID = self.autoRecoverInstance(instID)

        return instID, taskID

    def autoRecoverInstance(self, instID):
        """
        Reads the status DB to to find the last task for an instance
        to see where it died
        Finds the last task that did NOT finish
        """

        sql = (
            "select wf_task_id,task_name,task_type,task_status,status_timestamp from wf_task where dep_set_id = '"
            + self.depID
            + "' and wf_class_id = '"
            + self.classID
            + "' and wf_inst_id = '"
            + instID
            + "' and not task_status = 'finished' order by status_timestamp limit 1 "
        )

        ret = self.__eUtil.runSelectSQL(sql)

        # we now should have 1 row of task =
        # the last one that finished

        if ret is not None:
            for row in ret:
                logger.info("+WorkflowSession.autoRecover :  Last not finished = %s, of task type = %s completed at %s", str(row[1]), str(row[2]), str(row[4]))
                self.taskID = str(row[0])
                return row[0]
        else:
            logger.info("+WorkflowSession.getLastInstanceID : WF error - cannot recover this WF - no task ever finished ")
            self.taskID = "entry-point"
            return None

    def recoverFromAnnotate(self):

        sql = "select wf_class_id from wf_instance_last where dep_set_id = '" + str(self.depID) + "'"
        ss = self.__eUtil.runSelectSQL(sql)
        for s in ss:
            taskID = s[0]

        return taskID

    def autoRecoverInstanceGetLastFinished(self, instID):
        """
        Reads the status DB to to find the last task for an instance
        to see where it died
        Finds the last task that finished, and recovers the
          reference data for that task, and restarts at the
          next task
        """

        sql = (
            "select wf_task_id,task_name,task_type,task_status,status_timestamp from wf_task where dep_set_id = '"
            + self.depID
            + "' and wf_class_id = '"
            + self.classID
            + "' and wf_inst_id = '"
            + instID
            + "' and task_status = 'finished' order by status_timestamp desc limit 1"
        )

        ret = self.__eUtil.runSelectSQL(sql)

        # we now should have 1 row of task =
        # the last one that finished

        if ret is not None:
            for row in ret:
                logger.info("+WorkflowSession.autoRecover :  Last finished = %s, of task type = %s completed at %s", str(row[1]), str(row[2]), str(row[4]))
                self.taskID = str(row[0])
                return row[0]
        else:
            logger.info("+WorkflowSession.getLastInstanceID : WF error - cannot recover this WF - no task ever finished ")
            self.taskID = "entry-point"
            return None

    def __getLastInstanceID(self):
        """
        Find that last occurance of the instanceID
        """

        sql = (
            "select wf_inst_id,status_timestamp from wf_instance where dep_set_id = '" + self.depID + "' and wf_class_id = '" + self.classID + "' order by wf_inst_id desc limit 1"
        )

        if self.debug:
            logger.info("+WorkflowSession.__getLastInstanceID :  looking for last instance for depID= %s, classID= %s", str(self.depID), str(self.classID))

        ret = self.__eUtil.runSelectSQL(sql)

        if ret is not None and len(ret) > 0:
            for row in ret:
                instID = row[0]
                delta = float(row[1] - self.__timeStamp.getSecondsFromReference()) / 60.0
                logger.info("+WorkflowSession.__getLastInstanceID : Found instID = %s  age = %.3f minutes", instID, delta)
            return instID
        else:
            logger.info("+WorkflowSession.__getLastInstanceID : Catastrophic WF error - cannot recover instance ID ")
            return None

    # def __recoverAt(self, instID, taskID):
    #     """  NOT USED
    #       Reads the status DB to to find the last inst_ID
    #       to see where it died
    #       Recover from the prescribed taskID
    #     """

    #     sql = "select wf_task_id,task_name,task_type,task_status,status_timestamp from wf_task where dep_set_id = '" + self.depID + "' and wf_class_id = '" + \
    #         self.classID + "' and wf_inst_id = '" + instID + "' and wf_inst_id = '" + taskID + "'  order by status_timestamp desc limit 1"

    #     ret = self.__eUtil.runSelectSQL(sql)

    #     # we now should have 1 row of task =
    #     # the last one that finished

    #     if ret is not None:
    #         for row in ret:
    #             logger.info("+WorkflowSession.autoRecover :  Last finished = %s, of task type %s completed at %s", str(row[1]), str(row[2]), str(row[4]))
    #             return row[0]
    #     else:
    #         logger.info("+WorkflowSession.getLastInstanceID : WF error - cannot recover this WF - no task ever finished ")
    #         return "entry-point"
