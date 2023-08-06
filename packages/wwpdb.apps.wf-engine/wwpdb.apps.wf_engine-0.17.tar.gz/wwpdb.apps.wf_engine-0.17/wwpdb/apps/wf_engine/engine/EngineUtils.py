##
# File: EngineUtils.py
# Date: Mar 8, 2015
#
# Updates:
#    26-Apr-2015  jdw remove dependence on workflow metadata object
#                     remove unnecessary update of wf_class_dir table --
#     4-Aug-2015  jdw add getNextInstanceId(dataSetId)
#     9-Dec-2015  jdw add version specific path v-152 dependency formdata.pkl.  Not a future issue.
# #
import time
import sys
import os
import pickle
import datetime
import random
import smtplib

from wwpdb.utils.wf.process.ProcessRunner import ProcessRunner
from wwpdb.utils.wf.WfDataObject import WfDataObject
from wwpdb.utils.wf.dbapi.WfDbApi import WfDbApi
from wwpdb.utils.wf.dbapi.dbAPI import dbAPI

from email.mime.text import MIMEText
from wwpdb.utils.config.ConfigInfo import ConfigInfo, getSiteId
from wwpdb.apps.wf_engine.wf_engine_utils.time.TimeStamp import TimeStamp

import logging
from wwpdb.apps.wf_engine.wf_engine_utils.run.MyLogger import MyLogger

logger = logging.getLogger(name="root")

##
# JDW  -- This class will replace the DBStatusApi structure -
# #


class EngineUtils(WfDbApi):
    def __init__(self, verbose=True):
        #  This will create a database connection in the base class --
        #
        super(EngineUtils, self).__init__(log=MyLogger(level=logging.INFO), verbose=False)
        #
        self.__verbose = verbose
        self.__number = 0
        self.__timeStamp = TimeStamp()
        self.__when = self.__timeStamp.getSecondsFromReference()
        self.__lfh = MyLogger(level=logging.INFO)
        self.__SKIP_EMAIL = False
        self.__siteId = getSiteId(defaultSiteId="WWPDB_DEPLOY_PRODUCTION_RU")
        self.__cI = ConfigInfo(self.__siteId)
        if self.__siteId == "WWPDB_DEPLOY_MACOSX":
            # Always skip e-mail notifications on the development platform -
            self.__SKIP_EMAIL = True
        else:
            self.__SKIP_EMAIL = False
        logger.info("+EngineUtils.__init__ Starting ----------------------- (%s) ---------------------------------", self.__siteId)

    def updateConnection(self, timeOutSeconds=3600):
        """Update database connection if down or expired (older than timeOutSeconds)."""

        if (not self.isConnected()) or ((self.__timeStamp.getSecondsFromReference() - self.__when) > timeOutSeconds):
            ok = self.reConnect()
            if not ok:
                logger.info("+EngineUtils.checkConnection : database connection failed at connenction number = %d\n", self.__number)
                return False
            self.__when = self.__timeStamp.getSecondsFromReference()
            self.__number += 1
            logger.info("+EngineUtils.checkConnection : creating new database connection number = %d", self.__number)
        return True

    def resetInitialStateDB(self, depID):
        """
        Method to reset a deposition back to init state by setting the owner, status and class
        """

        # select ordinal from wf_instance where dep_set_id = 'D_057171'  order by status_timestamp desc limit 1;
        # get the last row in the instance table for this ID
        #
        sql = "select ordinal from wf_instance where dep_set_id = '" + str(depID) + "'  order by status_timestamp desc limit 1"
        allList = self.runSelectSQL(sql)

        if allList is not None:
            for allRow in allList:
                ordinal = allRow[0]
                logger.info("Ordinal found for ID %s , ordinal = %s", str(depID), str(ordinal))
                sql = "update wf_instance set owner = 'Annotation.bf.xml', wf_class_id = 'Annotate' , inst_status = 'init' where ordinal = " + str(ordinal)
                ok = self.runUpdateSQL(sql)
                # update the wf_instance_last table
                sql = "update wf_instance_last set owner = 'Annotation.bf.xml', wf_class_id = 'Annotate' , inst_status = 'init' where dep_set_id = '" + str(depID) + "'"
                ok = self.runUpdateSQL(sql)
                if int(ok) == 1:
                    logger.info("Updated 1 row to initialise status DB")
                else:
                    logger.info("DID NOT UPDATE status")

    def waitTime(self, sec):
        time.sleep(sec)

    def getLogDirectoryPath(self, depID):

        topSessionPath = self.__cI.get("SITE_WEB_APPS_TOP_SESSIONS_PATH")
        logDir = os.path.join(topSessionPath, "wf-logs", depID)

        if not os.path.exists(logDir):
            os.makedirs(logDir)

        return logDir

    def setException(self, depID):

        self.setCommunication("EXCEPTION", "EXCEPTION", depID)

    def setFinished(self, depID):

        self.setCommunication("FINISHED", "FINISHED", depID)

    def setCommunication(self, status, activity, depID):

        timeNow = self.__timeStamp.getSecondsFromReference()
        sql = (
            "update communication set status = '"
            + str(status)
            + "', activity = '"
            + str(activity)
            + "', actual_timestamp = "
            + str(timeNow)
            + " where dep_set_id  = '"
            + str(depID)
            + "'"
        )

        ok = self.runUpdateSQL(sql)

        if ok == 1:
            logger.info("Set the communication to %s for dep_set_id = %s", str(status), str(depID))
        else:
            logger.info("Failed to set the communication table to %s for dep_set_id = %s", str(status), str(depID))

    def testFilesExist(self, inputs, outputs):

        dinput = None
        output = None
        if inputs is not None:
            for key, value in inputs.items():
                if self.__verbose:
                    logger.info("+EngineUtils.testFilesExist :  testing input named %s content type %s", str(key), str(type(value)))
                dinput = value
        if outputs is not None:
            for key, value in outputs.items():
                if self.__verbose:
                    logger.info("+EngineUtils.testFilesExist :   setting output named %s content type %s", str(key), str(type(value)))
                output = value

        if dinput is None:
            logger.info("+EngineUtils.testFilesExist :   missing input data object")
        if output is None:
            logger.info("+EngineUtils.testFilesExist :  missing output data object ")

        fp = dinput.getFilePathReference()
        if dinput.getFilePathExists(fp):
            output.setValue("true")
        else:
            output.setValue("false")

        logger.info("+EngineUtils.testFilesExist : returns " + output.getValue() + " for " + fp)

    ##
    #  These methods are maintained for backward compatibility but should be deprecated !!!
    def setReleaseStatus(self, depID, status):

        sql = "update deposition set author_release_status_code = '" + status + "' where dep_set_id = '" + depID + "'"
        _ok = self.runUpdateSQL(sql)  # noqa: F841

    def WFEsetAnnotator(self, depID, annotator):

        sql = "update deposition set annotator_initials = '" + annotator + "' where dep_set_id = '" + depID + "'"
        _ok = self.runUpdateSQL(sql)  # noqa: F841

    def setRandomAnnotator(self, depID):

        sql = "select initials from da_users where length(user_name) = 2"
        allList = self.runSelectSQL(sql)

        n = random.randrange(1, len(allList))

        annotator = allList[n][0]

        sql = "update deposition set annotator_initials = '" + annotator + "' where dep_set_id = '" + depID + "'"
        _ok = self.runUpdateSQL(sql)  # noqa: F841

    def __sendEmail(self, email, frm, subject, message):

        if email is None:
            logger.error("+EngineUtils.__sendEmail Invalid email %s", str(email))
            return

        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = frm
        msg["To"] = email
        noreplyaddr = self.__cI.get("SITE_NOREPLY_EMAIL", "noreply@mail.wwpdb.org")

        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        logger.info("+EngineUtils.__sendEmail send email from %s", str(frm))
        logger.info("+EngineUtils.__sendEmail send email to %s", str(email))
        try:
            s = smtplib.SMTP("localhost")
            s.sendmail(noreplyaddr, [email], msg.as_string())
            s.quit()
        except Exception as e:
            logger.error("+EngineUtils.__sendEmail failing with %s", str(e))

    def sendDepositorEmail(self, depID, data):
        #  JDW - for compatibility WFE running under a host based site id needs to determine the e-mail path for each case -
        if os.access(os.path.join(self.__cI.get("SITE_ARCHIVE_STORAGE_PATH"), "deposit", "temp_files", "deposition-v-200", str(depID), "citation.pkl"), os.R_OK):
            url = self.__cI.get("SITE_CURRENT_DEP_EMAIL_URL")
            logger.info("+EngineUtils.sendDepositorEmail - %s  site %s return v200 url %s", depID, self.__siteId, url)
        # elif os.access(os.path.join(self.__cI.get('SITE_ARCHIVE_STORAGE_PATH'), 'deposit', 'temp_files', 'deposition-v-152', str(depID), "formdata.pkl"), os.R_OK):
        #     url = self.__cI.get('SITE_LEGACY_DEP_EMAIL_URL')
        #     logger.info("+EngineUtils.sendDepositorEmail - %s  site %s return v152 url %s", depID, self.__siteId, url)
        elif os.access(os.path.join(self.__cI.get("SITE_ARCHIVE_STORAGE_PATH"), "deposit", "temp_files", "deposition", str(depID), "formdata.pkl"), os.R_OK):
            url = self.__cI.get("SITE_DEP_EMAIL_URL")
            logger.info("+EngineUtils.sendDepositorEmail - %s  site %s return legacy url %s", depID, self.__siteId, url)
        else:
            url = self.__cI.get("SITE_DEP_EMAIL_URL")
            logger.info("+EngineUtils.sendDepositorEmail path tests failing - %s  site %s using default url %s", depID, self.__siteId, url)
        #

        data = data.replace("$DEPID", depID)
        data = data.replace("$DEPURL", url)
        data = data.replace("$LINEFEED", "\n")

        words = data.split("|")
        email = self.__getDepositorEmail(depID)
        logger.info("+EngineUtils.sendDepositorEmail - %s sending to email %s ", depID, email)
        if self.__SKIP_EMAIL:
            logger.info("+EngineUtils.sendDepositorEmail - Skipped sending email to %s ", email)
        else:
            self.__sendEmail(email, words[0], words[1], words[2])

    def __getDepositorEmail(self, depID):
        """
        go get the depositor email

        ## JDW modified to work in V152/V200 compatibility mode -
        """
        fName = os.path.join(self.__cI.get("SITE_ARCHIVE_STORAGE_PATH"), "deposit", "temp_files", "deposition", str(depID), "formdata.pkl")
        if not os.access(fName, os.R_OK):
            fName = os.path.join(self.__cI.get("SITE_ARCHIVE_STORAGE_PATH"), "deposit", "temp_files", "deposition-v-152", str(depID), "formdata.pkl")
        #
        logger.info("+EngineUtils.__getDepositorEmail - %s at %s searching for email in file %s ", depID, self.__siteId, fName)
        if os.path.isfile(fName):
            try:
                logger.info("+EngineUtils.__getDepositorEmail - %s s opening serialized file %s ", depID, fName)
                f = open(fName, "rb")
                dat = pickle.load(f)
                f.close()
                if "email" in dat:
                    return dat["email"]
                else:
                    return None
            except Exception as e:
                logger.exception("+EngineUtils.__getDepositorEmail failed to recover formdata and return email  %s", str(e))
                return None
        else:
            logger.info("+EngineUtils.__getDepositorEmail - %s searching for email in database", depID)
            ss = dbAPI(depID)
            ret = ss.runSelectNQ(table="user_data", select=["email", "role"], where={"dep_set_id": depID, "role": "valid"})
            for r in ret:
                return r[0]
            return None

    def initDepositContext(self, depositionID, WorkflowClassID, WorkflowInstanceID, dinput):
        """
        method to extract information from the current model file and load this into the status database.
        """

        logger.info("+EngineUtils.initDepositContext : ============================================")
        logger.info("+EngineUtils.initDepositContext : depID = %s", str(depositionID))
        logger.info("+EngineUtils.initDepositContext : ============================================")

        if self.__verbose:
            process = ProcessRunner(True, self.__lfh)
        else:
            process = ProcessRunner(False, self.__lfh)

        process.setAction("status")

        if dinput is None:
            logger.info("+EngineUtils.initDepositContext :  Requires input object \n")
            sys.exit(0)

        for key, value in dinput.items():
            if self.__verbose:
                logger.info("+EngineUtils.initDepositContext :  setting input %s %s", str(key), str(value.getReferenceType()))
                logger.info("+EngineUtils.initDepositContext :  setting input %s %s", str(key), str(value))
            process.setInput("src", value)

        wfoOut = WfDataObject()
        wfoOut.setContainerTypeName("dict")
        wfoOut.setValueTypeName("string")
        process.setOutput("dst", wfoOut)

        if not process.preCheck():
            logger.info("+EngineUtils.initDepositContext  : failed to setup process\n")

        if not process.run():
            logger.info("+EngineUtils.initDepositContext : failed to run process\n")

        dataDict = wfoOut.getValue()
        if dataDict is None:
            logger.info(" There is no dataDictionary - exiting")
            exit(0)

        depDB = {}
        depDB["DEP_SET_ID"] = depositionID
        depDB["PDB_ID"] = "????"
        if "accessions" in dataDict:
            acc = dataDict["accessions"]
            depDB["PDB_ID"] = "????"
            if acc is not None:
                accPDB = acc["PDB"]
                if accPDB is not None:
                    if len(accPDB) > 0:
                        depDB["PDB_ID"] = accPDB[0]

        if "recvd_initial_deposition_date" in dataDict:
            depDB["INITIAL_DEPOSITION_DATE"] = dataDict["recvd_initial_deposition_date"]
        else:
            # JDW JDW
            today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
            # depDB['INITIAL_DEPOSITION_DATE'] = 'unknown'
            depDB["INITIAL_DEPOSITION_DATE"] = today
        if "deposit_site" in dataDict:
            depDB["DEPOSIT_SITE"] = dataDict["deposit_site"]
        else:
            depDB["DEPOSIT_SITE"] = "unknown"
        if "process_site" in dataDict:
            depDB["PROCESS_SITE"] = dataDict["process_site"]
        else:
            depDB["PROCESS_SITE"] = "unknown"
        if "status_code" in dataDict:
            depDB["STATUS_CODE"] = dataDict["status_code"]
        else:
            depDB["STATUS_CODE"] = "PROC"

        logger.info("******* OVERWRITE OF STATUS CODE to PROC ***************")
        depDB["STATUS_CODE"] = "PROC"
        if "annotator_initials" not in dataDict or dataDict["annotator_initials"] == "UNASSIGNED":
            depDB["ANNOTATOR_INITIALS"] = "unknown"
        else:
            depDB["ANNOTATOR_INITIALS"] = dataDict["annotator_initials"]
            logger.info("******* OVERWRITE OF ANNOTATOR INITIALS TO AN *******")
            depDB["ANNOTATOR_INITIALS"] = "unknown"
        if "author_release_status_code" not in dataDict:
            depDB["AUTHOR_RELEASE_STATUS_CODE"] = "HPUB"
        else:
            depDB["AUTHOR_RELEASE_STATUS_CODE"] = dataDict["author_release_status_code"]
        depDB["TITLE"] = dataDict["title"].replace("'", " ")

        if "audit_author" in dataDict:
            auth = dataDict["audit_author"]
        else:
            auth = "unknown"

        if auth is not None:
            if isinstance(auth, list):
                depDB["AUTHOR_LIST"] = ""
                depDB["AUTHOR_LIST"] = " ".join(["%s," % a for a in auth])
            elif isinstance(auth, str):
                depDB["AUTHOR_LIST"] = auth
            else:
                logger.info(" Unknown type of author list %s", str(type(auth)))
            depDB["AUTHOR_LIST"] = depDB["AUTHOR_LIST"].replace("'", " ")
        else:
            depDB["AUTHOR_LIST"] = "unknown"
        #
        depDB["EXP_METHOD"] = dataDict["exp_method"]
        if depDB["EXP_METHOD"].find("NMR") >= 0:
            if "status_code_nmr" in dataDict:
                depDB["STATUS_CODE_EXP"] = dataDict["status_code_nmr"]
            else:
                depDB["STATUS_CODE_EXP"] = "Unknown"
        elif depDB["EXP_METHOD"].find("EM") >= 0:
            if "status_code_em" in dataDict:
                depDB["STATUS_CODE_EXP"] = dataDict["status_code_em"]
            else:
                depDB["STATUS_CODE_EXP"] = "Unknown"
        else:
            if "status_code_sf" in dataDict:
                depDB["STATUS_CODE_EXP"] = dataDict["status_code_sf"]
            else:
                depDB["STATUS_CODE_EXP"] = "Unknown"
        if "full_name_of_center" in dataDict:
            depDB["SG_CENTER"] = dataDict["full_name_of_center"]
        else:
            depDB["SG_CENTER"] = "Unknown"

        if self.exist(depDB):
            # then we do nothing - since this workflow does not modify the depostion
            constDict = {}
            constDict["DEP_SET_ID"] = depositionID
            self.saveObject(depDB, "update", constDict)
        else:
            self.saveObject(depDB, "insert")
            if self.__verbose:
                logger.info("+EngineUtils.initDepositContext : done insert data object in DB\n")

        instDB = {}
        instDB["WF_INST_ID"] = WorkflowInstanceID
        instDB["WF_CLASS_ID"] = WorkflowClassID
        instDB["DEP_SET_ID"] = depositionID
        instDB["STATUS_TIMESTAMP"] = datetime.datetime.utcnow()
        self.updateStatus(instDB, "init")

        # and also initialise the wf_instance_last table
        sql = "update wf_instance_last set status_timestamp=" + str(self.__timeStamp.getSecondsFromReference()) + ", inst_status='init' where dep_set_id = '" + depositionID + "'"
        ok = self.runUpdateSQL(sql)
        if ok < 1:
            logger.error("+EngineUtils.initDepositContext() failed to update wf_instance_last table")

    def getNextInstanceId(self, dataSetId):
        """
        Create new/next workflow instance for the input data set Id using wf_instance table data.

        """

        sql = "select max(cast(substr(wf_inst_id,3) as decimal(5,0)))+1 from wf_instance where dep_set_id = '" + str(dataSetId) + "'"

        ll = self.runSelectSQL(sql)

        if ll is None:
            instID = 1
        else:
            for l in ll:  # noqa: E741
                if l is None:
                    instID = 1
                else:
                    if l[0] is None:
                        instID = 1
                    else:
                        instID = l[0]

        ret = "W_" + str(instID).zfill(3)

        if self.__verbose > 0:
            logger.info("+mainEngine.__getNewInstanceIDDB : for data set ID = %s next workflow instance ID = %s", dataSetId, ret)

        return ret


##
#  END JDW
