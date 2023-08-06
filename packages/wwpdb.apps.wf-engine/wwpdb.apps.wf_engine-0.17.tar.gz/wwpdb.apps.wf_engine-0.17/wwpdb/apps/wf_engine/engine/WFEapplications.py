##
# File: WFEapplications.py
# Date:
#
# jdw    WARNING loads of domain specific functions here called from all over wfm and depui.
# jdw -- grab bag of functions -- change date 'unknown' date today
# jdw -- replace missing workflow with placeholder workflow in initilliseInstance(DBstatusAPI, id)
#
# 4-Aug-2015 jdw -- add def runOutOfBandWorkflow(DBstatusAPI, depSetId, classId, classFileName)
# Aug-2015 lm -- add def getWfStatus
#
#  14-Jul-2016 jdw add validation_server flag to functions runWorkflowOnUpload() & runValidationUpload()
#  26-Sep-2017 ep  initilliseDepositDict() parameterize strings to ensure proper quoting
#  26-Oct-2018 ep  remove dead code, switch to logging
#
# #
import time
import sys
import os
import pickle
import datetime
import logging

from wwpdb.utils.wf.process.ProcessRunner import ProcessRunner
from wwpdb.utils.wf.WfDataObject import WfDataObject
from wwpdb.utils.wf.dbapi.WfDbApi import WfDbApi
from wwpdb.utils.wf.dbapi.dbAPI import dbAPI
from wwpdb.utils.config.ConfigInfo import ConfigInfo, getSiteId
from wwpdb.utils.wf.dbapi.WFEtime import getTimeNow
from email.mime.text import MIMEText

logger = logging.getLogger()


def getPicklePath(depSetId=None):
    """Return path to deposition pkl files - to break circular dependency
    if depSetId set, return deposition specific path
    """

    # logger.debug("Getting PicklePath for %s" % depSetId)

    cI = ConfigInfo()
    WWPDB_APP_VERSION_STRING = "v-200"

    depstrpath = cI.get("SITE_ARCHIVE_STORAGE_PATH")
    if not depstrpath:
        logger.error("SITE_ARCHIVE_STORAGE_PATH not set")
        return None

    file_upload_temp_dir = os.path.join(depstrpath, "deposit", "temp_files")
    storage_pickled_depositions = os.path.join(file_upload_temp_dir, "deposition" + "-" + WWPDB_APP_VERSION_STRING)

    if depSetId:
        fPath = os.path.join(storage_pickled_depositions, str(depSetId))
    else:
        fPath = storage_pickled_depositions

    return fPath


def getNotesEmailAddr():
    """Returns the email address for archiving messages"""
    email = "wwpdb-da-system@rcsb.rutgers.edu"

    siteid = getSiteId()
    # Debugging at PDBe
    if siteid == "PDBE_DEV":
        cI = ConfigInfo()
        email = cI.get("ANNOTATION_EMAIL")

    return email


def runOutOfBandWorkflow(DBstatusAPI, depSetId, classId, classFileName):
    """UPDATE status.communication SET  sender=%s, receiver=%s, wf_class_id=%s, wf_class_file=%s,
                                  command=%s, status=%s, actual_timestamp=%s, data_version=%s
                                  WHERE ( dep_set_id=%s);

    ['WFUTILS', 'WFE', 'PDBX2PDBX_DEP', 'wf_op_pdbx2pdbx_fs_deposit.xml',
     'runWF', 'PENDING', Decimal('492013055.527617'), 'latest',
     'D_1000208939']
    """
    t = getTimeNow()
    sqlTemplate = "UPDATE status.communication SET  sender='%s', receiver='%s', wf_class_id='%s', wf_class_file='%s', command='%s', status='%s', actual_timestamp='%s', data_version='%s' WHERE ( dep_set_id='%s')"  # noqa: E501
    tdata = ("WFUTILS", "WFE", classId, classFileName, "RunWF", "PENDING", str(t), "latest", depSetId)
    sql = sqlTemplate % (tdata)
    ok = DBstatusAPI.runUpdateSQL(sql)
    return ok


def reRunWorkflow(depID):
    """
    method to reRun the validation WF just by setting the communication status to pending
    """

    status = "OK"
    try:
        timestamp = getTimeNow()
        wfApi = WfDbApi(verbose=True)
        sql = "select wf_class_file,command from communication where dep_set_id = '" + str(depID) + "'"
        rows = wfApi.runSelectSQL(sql)
        for row in rows:
            if row[0] in ["ValidDeposit.xml", "depRunOnUpload.xml", "wf_op_validdeposit_fs_deposit.xml", "wf_op_uploaddep_fs_deposit.xml"] and row[1] in ["runWF", "restartGoWF"]:
                sql = "update communication set status = 'PENDING',actual_timestamp = '" + str(timestamp) + "' where dep_set_id = '" + str(depID) + "'"
                ok = wfApi.runUpdateSQL(sql)
                if ok < 1:
                    status = "Failed to mark this for restart "
            else:
                status = "WF was not in deposition "
            break
    except Exception as e:
        status = "Kill WF error " + str(e)

    logger.info("Restart WF request:  %s : %s", str(depID), str(status))

    return status


def getValidationStatus(depID, wfApi=None):
    """
    method to see if there is a valid row in the database for communication and that it is WORKING for deposition uploads
    """

    if not wfApi:
        wfApi = WfDbApi(verbose=True)

    sql = (
        "select status from communication where dep_set_id = '"
        + str(depID)
        + "' and wf_class_file in ('ValidDeposit.xml','depRunOnUpload.xml','wf_op_validdeposit_fs_deposit.xml','wf_op_uploaddep_fs_deposit.xml')"
    )
    rows = wfApi.runSelectSQL(sql)
    logger.debug(sql)
    logger.debug(str(rows))

    if rows is not None and len(rows) > 0:
        for row in rows:
            return row[0].lower()
    else:
        return "unknown"

    return "unknown"


def getWfStatus(depID, wfApi=None):
    """
    method to check the status of a current workflow; and to see if there is a valid row in the database for communication and that it is WORKING for deposition uploads
    """

    if not wfApi:
        wfApi = WfDbApi(verbose=True)

    # sql = "select status from communication where dep_set_id = '" + str(depID) + "' and wf_class_file = '" + classFile +"'"
    sql = "select status, wf_class_file from communication where dep_set_id = '" + str(depID) + "'"
    rows = wfApi.runSelectSQL(sql)
    if rows is not None and len(rows) > 0:
        # if rows[0][0] != 'WORKING':
        if rows[0][0] == "FINISHED":
            logger.info("wf_engine.engine.WFEapplications.getWfStatus: %s", sql)
            logger.info("wf_engine.engine.WFEapplications.getWfStatus: %s", str(rows))
        for row in rows:
            return row
            # return row[0].lower()
    else:
        return "unknown"

    return "unknown"


def killAllWF(depID, who):

    status = "OK"
    try:
        timestamp = getTimeNow()
        wfApi = WfDbApi(verbose=True)

        sql = (
            "update communication set command = 'killWF', actual_timestamp = '" + str(timestamp) + "', receiver = 'WFE', status = 'PENDING' where dep_set_id = '" + str(depID) + "'"
        )
        ok = wfApi.runUpdateSQL(sql)
        if ok < 1:
            status = "Failed to mark this for process kill"
    except Exception as e:
        status = "Kill WF error " + str(e)

    logger.info("Kill WF request:  %s from %s", str(depID), str(who))

    return status


def waitTime(sec):

    time.sleep(sec)


# Updated jdw
#


def wfClassDir():
    # JDW -- deprecated -- directory containing the directory containing ---
    siteId = getSiteId(defaultSiteId="WWPDB_DEPLOY_TEST")
    cI = ConfigInfo(siteId)
    ret = cI.get("SITE_WF_PYTHON_PATH")
    # ret = os.path.abspath(os.path.join(os.path.abspath(__file__), '../../')) + '/'
    return ret


def getNextInstanceId(DBstatusAPI, depID, prt=sys.stderr):
    """
    Create new workflow instance from the statusDB
    Returns the ID
    The status API returns an ID as a number, result is padded with zeros on a field width of 3
    """
    sql = "select max(cast(substr(wf_inst_id,3) as decimal(5,0)))+1 from wf_instance where dep_set_id = '" + str(depID) + "'"

    ll = DBstatusAPI.runSelectSQL(sql)

    if ll is None:
        instID = 1
    else:
        for el in ll:
            if el is None:
                instID = 1
            else:
                if el[0] is None:
                    instID = 1
                else:
                    instID = el[0]

    ret = "W_" + str(instID).zfill(3)

    prt.write("+getNextInstanceId: Created new workflow instance ID = %s" % str(ret))

    return ret


def insertInitialStateDB(DBstatusAPI, depID, debug=0, prt=sys.stderr):
    """Method to insert or update the instance of the annotation workflow within the wf_instance/wf_instance_last table -"""
    # Check if this workflow already exists in the wf_instance table -
    #
    sql = "select ordinal from wf_instance where (wf_class_id = 'Annotate')  and (dep_set_id = '" + str(depID) + "')  order by status_timestamp desc limit 1"
    allList = DBstatusAPI.runSelectSQL(sql)

    if allList is not None and len(allList) > 0:
        return updateInitialStateDB(DBstatusAPI, depID, debug=debug, prt=prt)

    now = getTimeNow()
    instId = getNextInstanceId(DBstatusAPI, depID, prt=prt)

    sql = (
        "insert into wf_instance (wf_inst_id, wf_class_id, dep_set_id, owner, inst_status, status_timestamp) values ('"
        + instId
        + "','Annotate','"
        + depID
        + "','Annotation.bf.xml','init','"
        + str(now)
        + "')"
    )
    ok = DBstatusAPI.runInsertSQL(sql)
    if int(ok) == 1:
        prt.write("+insertInitialStateDB - insert returns %r row into wf_instance for %r\n" % (ok, depID))
    #
    # Try update then insert -
    sql = (
        "update wf_instance_last set owner = 'Annotation.bf.xml', wf_class_id = 'Annotate' , inst_status = 'init', "
        + " wf_inst_id = '"
        + instId
        + "', status_timestamp = '"
        + str(now)
        + "'  where dep_set_id = '"
        + str(depID)
        + "'"
    )
    prt.write("+insertInitialStateDB - SQL =  %s \n" % sql)
    ok = DBstatusAPI.runUpdateSQL(sql)
    prt.write("+insertInitialStateDB - return ok  =  %r \n" % ok)
    if int(ok) == 1:
        prt.write("+updateInitialStateDB - Updating Annotate class in wf_instance suceeded for %s\n" % depID)
    else:
        sql = (
            "insert into wf_instance_last (wf_inst_id, wf_class_id, dep_set_id, owner, inst_status, status_timestamp) values ('"
            + instId
            + "','Annotate','"
            + depID
            + "','Annotation.bf.xml','init','"
            + str(now)
            + "')"
        )
        ok = DBstatusAPI.runInsertSQL(sql)
        if int(ok) == 1:
            prt.write("+insertInitialStateDB - Inserted 1 row into wf_instance_last for %s\n " % depID)
        else:
            prt.write("+insertInitialStateDB - Updating Annotate class in wf_instance failed for %s\n" % depID)


def resetInitialStateDB(DBstatusAPI, depID, debug=0, prt=sys.stderr):
    """
    Method to reset (insert/update) a annotation workflow back to init state by setting the owner, status and class
    """
    #
    sql = "select ordinal from wf_instance where (wf_class_id = 'Annotate')  and (dep_set_id = '" + str(depID) + "')  order by status_timestamp desc limit 1"
    allList = DBstatusAPI.runSelectSQL(sql)

    if (allList is not None) and (len(allList) > 0):
        return updateInitialStateDB(DBstatusAPI, depID, debug=debug, prt=prt)
    else:
        return insertInitialStateDB(DBstatusAPI, depID, debug=debug, prt=prt)


def updateInitialStateDB(DBstatusAPI, depID, debug=0, prt=sys.stderr):  # pylint: disable=unused-argument
    """
    Method to reset the annoation workflow back to init state by setting the owner, status and class
    """
    #
    sql = "select ordinal from wf_instance where (wf_class_id = 'Annotate')  and (dep_set_id = '" + str(depID) + "')  order by status_timestamp desc limit 1"
    allList = DBstatusAPI.runSelectSQL(sql)

    if allList is not None:
        for allRow in allList:
            now = getTimeNow()
            ordinal = allRow[0]
            prt.write("+updateInitialStateDB - Ordinal  %s found for depID %s \n" % (depID, ordinal))
            sql = (
                "update wf_instance set owner = 'Annotation.bf.xml', wf_class_id = 'Annotate' , inst_status = 'init', status_timestamp = '"
                + str(now)
                + "' where ordinal = "
                + str(ordinal)
            )
            ok = DBstatusAPI.runUpdateSQL(sql)
            # update the wf_instance_last table
            sql = (
                "update wf_instance_last set owner = 'Annotation.bf.xml', wf_class_id = 'Annotate' , inst_status = 'init', status_timestamp = '"
                + str(now)
                + "' where dep_set_id = '"
                + str(depID)
                + "'"
            )
            ok = DBstatusAPI.runUpdateSQL(sql)
            if int(ok) == 1:
                prt.write("+updateInitialStateDB - %s status=%r for updating Annotate class in wf_instance \n" % (depID, ok))
            else:
                prt.write("+updateInitialStateDB - %s status=%r for updating Annotate class in wf_instance \n" % (depID, ok))


def DepUIgetDepositorEmail(depID):
    """
    go get the depositor email
    """

    logger.info("Getting email address for '%s'", depID)
    # This code is here to break a dependence on DepUI code from WFE
    fPath = getPicklePath(depID)

    if not fPath:
        logger.error(" The storage location of the pickle file is not known")
        return None

    fName = os.path.join(fPath, "formdata.pkl")

    if os.path.isfile(fName):
        try:
            f = open(fName, "rb")
            dat = pickle.load(f)
            f.close()
            if "email" in dat:
                return dat["email"]
            else:
                return None
        except Exception as e:
            logger.exception("Tried to get the formdata and return email %s", str(e))
            return None
    else:
        ss = dbAPI(depID)
        ret = ss.runSelectNQ(table="user_data", select=["email", "role"], where={"dep_set_id": depID, "role": "valid"})
        for r in ret:
            return r[0]
        return None


def WFEsendEmail(email, frm, subject, message, bcc=None):
    # Used when enabling FTP from WFM
    import smtplib

    if email is None:
        logger.error(" Invalid email %s", str(email))
        return

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = frm
    msg["To"] = email
    sendTo = [email]
    if bcc:
        sendTo = [email] + [bcc]
        logger.debug("send email (bcc) to %s", str(bcc))

    cI = ConfigInfo()
    noreplyaddr = cI.get("SITE_NOREPLY_EMAIL", "noreply@mail.wwpdb.org")

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    logger.debug("send email from %s", str(frm))
    logger.debug("send email to %s", str(email))
    try:
        s = smtplib.SMTP("localhost")
        s.sendmail(noreplyaddr, sendTo, msg.as_string())
        s.quit()
    except Exception as e:
        logger.error(" Exception in WFE.WFEsendEmail %s", str(e))


def resetComms(DBstatusAPI, id):  # pylint: disable=redefined-builtin

    t = getTimeNow()
    sql = (
        "update communication set sender='INSERT',receiver='LOAD',command='INIT',status='INIT',actual_timestamp='"
        + str(t)
        + "',parent_dep_set_id='"
        + str(id)
        + "',parent_wf_class_id='Annotate',wf_class_file = 'Annotation.bf.xml',parent_wf_inst_id='W_001' where dep_set_id = '"
        + id
        + "'"
    )
    logger.info(sql)
    DBstatusAPI.runUpdateSQL(sql)


def initialiseComms(DBstatusAPI, id):  # pylint: disable=redefined-builtin

    sql = "select dep_set_id from communication where dep_set_id = '" + str(id) + "'"

    allList = DBstatusAPI.runSelectSQL(sql)

    logger.info("****************%s", str(allList))

    if allList is None or len(allList) < 1:
        # The normal case - insert a new value
        t = getTimeNow()
        sql = (
            "insert communication (sender,receiver,dep_set_id,command,status,actual_timestamp,parent_dep_set_id,parent_wf_class_id,parent_wf_inst_id,wf_class_file) values ('INSERT','LOAD','"  # noqa: E501
            + str(id)
            + "','INIT','INIT',"
            + str(t)
            + ", '"
            + str(id)
            + "','Annotate','W_001','Annotation.bf.xml')"
        )
        logger.info(sql)
        DBstatusAPI.runInsertSQL(sql)
    else:
        # we already have that dep_setID - so just reset the communication
        resetComms(DBstatusAPI, id)


def initilliseInstance(DBstatusAPI, id):  # pylint: disable=redefined-builtin
    """If there is no existing wf_instance for the input id then add a placeholder instance -"""
    sql = "select dep_set_id from wf_instance where dep_set_id = '" + str(id) + "'"

    allList = DBstatusAPI.runSelectSQL(sql)

    t = getTimeNow()
    if allList is None or len(allList) < 1:
        # The normal case - insert a new value
        sql = (
            "insert wf_instance (wf_inst_id,wf_class_id,dep_set_id,owner,inst_status,status_timestamp) values ('W_001','PLACEHOLDER','"
            + str(id)
            + "','wf_op_placeholder.xml','dep','"
            + str(t)
            + "')"
        )
        DBstatusAPI.runInsertSQL(sql)
        sql = (
            "insert wf_instance_last (wf_inst_id,wf_class_id,dep_set_id,owner,inst_status,status_timestamp) values ('W_001','PLACEHOLDER','"
            + str(id)
            + "','wf_op_placeholder.xml','dep','"
            + str(t)
            + "')"
        )
        DBstatusAPI.runInsertSQL(sql)
    else:
        # we already have that dep_setID - so just reset the communication
        pass


def initilliseDepositDict(DBstatusAPI, id, pdb="?", data=None):  # pylint: disable=unused-argument,redefined-builtin
    """
    raw deposition table inialisation
    """

    depDB = {}
    depDB["DEP_SET_ID"] = id

    if DBstatusAPI.exist(depDB):
        logger.info("ID exists ")
        sql = "update deposition set "
        args = ()
        first = False
        for key, value in data.items():
            if not first:
                first = True
            else:
                sql = sql + ","
            sql = sql + str(key) + " = %s"
            # comma important with single value tuples
            args += (str(value),)
        sql = sql + " where dep_set_id = %s"
        args += (str(id),)

        logger.info("%s %s", sql, args)
        DBstatusAPI.runUpdateSQL(sql, args)
    else:
        # I do not think this code path is used - missing
        # commas between keys and values - EP 2017-09-26
        logger.info("ID is new")
        sql = "insert deposition (dep_set_id,"
        for key, value in data.items():
            sql = sql + str(key)
        sql = sql + ') values ("' + str(id) + '",'
        for key, value in data.items():
            sql = sql + '"' + str(value) + '"'

        sql = sql + ")"
        logger.info(sql)
        DBstatusAPI.runInsertSQL(sql)


def getdepUIPassword(DBstatusAPI, id):  # pylint: disable=redefined-builtin

    depDB = {}
    depDB["DEP_SET_ID"] = id

    try:
        if DBstatusAPI.exist(depDB):
            logger.info("ID exists ")
            sql = "select depPW from  deposition where dep_set_id = '" + str(id) + "'"
            logger.info(sql)
            allList = DBstatusAPI.runSelectSQL(sql)

            if allList is not None:
                for allRow in allList:
                    pw = allRow[0]
                    return pw
    except Exception as _e:  # noqa: F841
        logger.exception("Failed to get depUI PW in status DB")

    return None


def setdepUIPassword(DBstatusAPI, id, pw):  # pylint: disable=redefined-builtin
    """
    keep this separate so we never overwrite the PW
    """

    depDB = {}
    depDB["DEP_SET_ID"] = id

    try:
        if DBstatusAPI.exist(depDB):
            sql = "update deposition set depPW = '" + str(pw) + "' where dep_set_id = '" + str(id) + "'"
            DBstatusAPI.runUpdateSQL(sql)
        else:
            logger.info(" Cannot set depUI password - depID does not exist")
    except Exception as e:
        logger.exception("Failed to set depUI PW in status DB %s", str(e))


# API in use - references id by name...
def initilliseDepositV2(
    DBstatusAPI,
    id,  # pylint: disable=redefined-builtin,unused-argument
    pdb="?",
    date=None,  # pylint: disable=unused-argument
    initials="unknown",  # pylint: disable=unused-argument
    deposit_site="?",
    process_site="?",
    status_code="DEP",
    author_code="?",
    title="?",
    author_list="?",
    expt="?",
    status_code_exp="?",
    SG_center="?",
    ann="dep",
    email="",
    requested_codes=None,
):
    """
    raw deposition table inialisation
    """

    if requested_codes is None:
        requested_codes = []

    depDB = {}
    depDB["DEP_SET_ID"] = id

    if DBstatusAPI.exist(depDB):
        logger.info("ID exists ")
        sql = "update deposition set process_site = '" + str(process_site) + "', exp_method = '" + str(expt) + "' where dep_set_id = '" + str(id) + "'"
        logger.info(sql)
        DBstatusAPI.runUpdateSQL(sql)
    else:
        sql = (
            "insert deposition (dep_set_id, pdb_id, emdb_id, bmrb_id, deposit_site, process_site, status_code, author_release_status_code, title, author_list, exp_method, status_code_exp, SG_center, annotator_initials,email) values ('"  # noqa: E501
            + str(id)
            + "','"
            + str(pdb)
            + "','"
            + str(pdb)
            + "','"
            + str(pdb)
            + "','"
            + str(deposit_site)
            + "','"
            + str(process_site)
            + "','"
            + str(status_code)
            + "','"
            + str(author_code)
            + "','"
            + str(title)
            + "','"
            + str(author_list)
            + "','"
            + str(expt)
            + "','"
            + str(status_code_exp)
            + "','"
            + str(SG_center)
            + "','"
            + str(ann)
            + "','"
            + str(email)
            + "')"
        )

        DBstatusAPI.runInsertSQL(sql)
        if "EMDB" in requested_codes:
            sql = "update deposition set status_code_emdb = %r where dep_set_id = %r" % (status_code, id)
            DBstatusAPI.runInsertSQL(sql)


def runValidationUpload(DBstatusAPI, id, validation_server=False):  # pylint: disable=redefined-builtin
    """
    (old: Add request to run WF  : DepValModule.xml)
    Add request to run WF  : wf_op_validdeposit_fs_deposit.xml

    Jul/2016 function is called by deposit/depui/upload.py
    """

    status = getValidationStatus(id, wfApi=DBstatusAPI)
    now = getTimeNow()

    logger.info(" Engine.WFEapplications.runValidationUpload %s", str(now))
    logger.info(" Engine.WFEapplications.runValidationUpload %s", str(id))
    logger.info(" Engine.WFEapplications.runValidationUpload %s", str(status))

    if validation_server:
        wfName = "wf_op_validserver_fs_deposit.xml"
    else:
        wfName = "wf_op_validdeposit_fs_deposit.xml"

    if status == "working":
        sql = (
            "update communication set command = 'restartGoWF',  wf_class_file = '"
            + wfName
            + "', wf_class_id = 'DepVal', status = 'PENDING', actual_timestamp = '"
            + str(now)
            + "' where dep_set_id = '"
            + id
            + "'"
        )
    else:
        sql = (
            "update communication set sender = 'DEP', receiver = 'WFE', wf_class_file = '"
            + wfName
            + "', wf_class_id = 'DepVal', command = 'runWF', status = 'PENDING', actual_timestamp = '"
            + str(now)
            + "', parent_dep_set_id = '"
            + str(id)
            + "', parent_wf_class_id = 'DepUpload', parent_wf_inst_id = 'W_001' where dep_set_id = '"
            + id
            + "'"
        )

    logger.info(" Engine.WFEapplications.runValidationUpload - %s", str(sql))

    nrow = DBstatusAPI.runUpdateSQL(sql)
    logger.info(" WFE.runValidationUpload :  Rows affected: %i", nrow)


def runWorkflowOnUpload(DBstatusAPI, id, validation_server=False):  # pylint: disable=redefined-builtin
    """
    (old: Add request to run WF  : depRunOnUpload.xml)
    Add request to run WF  : wf_op_uploaddep_fs_deposit.xml

    Jul/2016 function is called by deposit/depui/upload.py
    """

    try:
        status = getValidationStatus(id, wfApi=DBstatusAPI)
        now = getTimeNow()
        logger.info(" Engine.WFEapplications.runWorkflowOnUpload %s", str(now))
        logger.info(" Engine.WFEapplications.runWorkflowOnUpload %s", str(id))
        logger.info(" Engine.WFEapplications.runWorkflowOnUpload %s", str(status))
        if validation_server:
            wfName = "wf_op_uploadvalsrv_fs_deposit.xml"
        else:
            wfName = "wf_op_uploaddep_fs_deposit.xml"
        if status == "working":
            # sql = "update communication set command = 'restartGoWF',  wf_class_file = 'depRunOnUpload.xml', status = 'PENDING', actual_timestamp = '" + \
            #    str(now) + "' where dep_set_id = '" + id + "'"
            sql = (
                "update communication set command = 'restartGoWF',  wf_class_file = '"
                + wfName
                + "', wf_class_id = 'uploadMod', status = 'PENDING', actual_timestamp = '"
                + str(now)
                + "' where dep_set_id = '"
                + id
                + "'"
            )

        else:

            # sql = "update communication set sender = 'DEP', receiver = 'WFE', wf_class_file = 'depRunOnUpload.xml', command = 'runWF', status = 'PENDING', actual_timestamp = '" + \
            #    str(now) + "', parent_dep_set_id = '" + str(id) + "', parent_wf_class_id = 'DepUpload', parent_wf_inst_id = 'W_001' where dep_set_id = '" + id + "'"
            sql = (
                "update communication set sender = 'DEP', receiver = 'WFE', wf_class_file = '"
                + wfName
                + "', wf_class_id = 'uploadMod', command = 'runWF', status = 'PENDING', actual_timestamp = '"
                + str(now)
                + "', parent_dep_set_id = '"
                + str(id)
                + "', parent_wf_class_id = 'DepUpload', parent_wf_inst_id = 'W_001' where dep_set_id = '"
                + id
                + "'"
            )

        logger.info(" Engine.WFEapplications.runWorkflowOnUpload - %s", str(sql))

        nrow = DBstatusAPI.runUpdateSQL(sql)
        logger.info(" WFE.runWorkflowOnUpload :  Rows affected: %i", nrow)
    except Exception as e:
        logger.exception("Exception Engine.WFEapplications.runWorkflowOnUpload %s", str(e))


def WFEsetAnnotator(DBstatusAPI, depID, annotator):

    sql = "update deposition set annotator_initials = '" + annotator + "' where dep_set_id = '" + depID + "'"
    _ok = DBstatusAPI.runUpdateSQL(sql)  # noqa: F841


def WFEexception(DBstatusAPI, depID):

    WFEsetCommunication(DBstatusAPI, "EXCEPTION", "EXCEPTION", depID)


def WFEfinished(DBstatusAPI, depID):

    WFEsetCommunication(DBstatusAPI, "FINISHED", "FINISHED", depID)


def WFEsetCommunication(DBstatusAPI, status, activity, depID):

    timeNow = getTimeNow()
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

    ok = DBstatusAPI.runUpdateSQL(sql)

    if ok == 1:
        logger.info("Set the communication to %s doe dep_set_id = %s", str(status), str(depID))
    else:
        logger.info("Failed to set the communication table to %s for dep_set_id = %s", str(status), str(depID))


def getInitialDate(depid):

    ret = "error"
    if depid is not None:
        wfApi = WfDbApi(verbose=True)
        sql = "select initial_deposition_date from deposition where dep_set_id = '" + depid + "'"
        dat = wfApi.runSelectSQL(sql)
        if dat is not None and len(dat) > 0:
            for r in dat:
                ret = r[0]

    return ret


def getAnnotatorInitials(depid):

    ret = "error"
    if depid is not None:
        wfApi = WfDbApi(verbose=True)
        sql = "select annotator_initials from deposition where dep_set_id = '" + depid + "'"
        dat = wfApi.runSelectSQL(sql)
        if dat is not None and len(dat) > 0:
            for r in dat:
                ret = r[0]

    return ret


def getStatusCode(depid):

    ret = "error"
    if depid is not None:
        wfApi = WfDbApi(verbose=True)
        sql = "select status_code from deposition where dep_set_id = '" + depid + "'"
        dat = wfApi.runSelectSQL(sql)
        if dat is not None and len(dat) > 0:
            for r in dat:
                ret = r[0]

    return ret


def getStatusCodeEMDB(depid):

    ret = "error"
    if depid is not None:
        wfApi = WfDbApi(verbose=True)
        sql = "select status_code_emdb from deposition where dep_set_id = '" + depid + "'"
        dat = wfApi.runSelectSQL(sql)
        if dat is not None and len(dat) > 0:
            for r in dat:
                ret = r[0]

    return ret


def setStatusCode(depID, code):

    valid = ["PROC", "AUTH", "DEP", "VAL", "HPUB", "REL", "REPL", "HOLD", "OBS", "WAIT", "WDRN", "REFI"]

    if code not in valid:
        return False, "Invalid status code"

    try:
        wfApi = WfDbApi(verbose=True)
        sql = "update deposition set status_code = '" + str(code) + "' where dep_set_id = '" + depID + "'"
        n = wfApi.runUpdateSQL(sql)
        if n == 0:
            return False, "Update did not occur - possible invalid dep_set_id or no change to code "
        else:
            return True, "Status updated"
    except Exception as e:
        return False, "Exception : " + str(e)


# ############################################
#  Believed not in use - except for examples
# ############################################

# Only used by examples - not in production
def populateDeposit(DBstatusAPI, depositionID):
    """
    Entry point added to the workflow system to create an object within
    the state system
    """

    debug = 3
    log = sys.stderr

    # Get the data out of the mmCIF
    if debug > 0:
        process = ProcessRunner(True, log)
    else:
        process = ProcessRunner(False, log)

    process.setAction("status")

    wfoInp = WfDataObject()
    wfoInp.setDepositionDataSetId(depositionID)
    wfoInp.setStorageType("archive")
    wfoInp.setContentTypeAndFormat("model", "pdbx")
    wfoInp.setVersionId("latest")
    # dP = wfoInp.getDirPathReference()
    # fP = wfoInp.getFilePathReference()
    # oVn = wfoInp.getFileVersionNumber()
    process.setInput("src", wfoInp)

    wfoOut = WfDataObject()
    wfoOut.setContainerTypeName("dict")
    wfoOut.setValueTypeName("string")
    process.setOutput("dst", wfoOut)

    if not process.preCheck():
        logger.error("WFE.WFEapplications.initialliseDeposit  : failed to setup process")

    if not process.run():
        logger.error("WFE.WFEapplications.initialliseDeposit : failed to run process")

    dataDict = wfoOut.getValue()

    if dataDict is not None:
        if "title" in dataDict:
            title = dataDict["title"].replace("'", " ")
        else:
            title = "Unknown"

        if "audit_author" in dataDict:
            auth = dataDict["audit_author"]
            if isinstance(auth, list):
                author_list = ""
                author_list = " ".join(["%s," % a for a in auth])
            elif isinstance(auth, str):
                author_list = auth
            else:
                logger.info(" Unknown type of author list %s", str(type(auth)))
            author_list = author_list.replace("'", " ")
        else:
            author_list = "unknown"

        if "exp_method" in dataDict:
            ex = dataDict["exp_method"]
            expt = ""
            if "status_code_nmr" in dataDict or ex.find("NMR") >= 0:
                expt += "NMR"
            if "status_code_em" in dataDict or ex.find("EM") >= 0:
                if len(expt) > 0:
                    expt += ","
                expt += "EM"
            if "status_code_sf" in dataDict or ex.find("XRAY") >= 0:
                if len(expt) > 0:
                    expt += ","
                expt += "xray"
        else:
            expt = "Unknown"

        if "full_name_of_center" in dataDict:
            sg_center = dataDict["full_name_of_center"]
        else:
            sg_center = "Unknown"

        now = datetime.datetime.utcnow().strftime("%Y-%m-%d")

        sql = (
            "update deposition set initial_deposition_date = '"
            + str(now)
            + "',title = '"
            + str(title)
            + "', author_list = '"
            + str(author_list)
            + "', exp_method = '"
            + str(expt)
            + "',sg_center = '"
            + str(sg_center)
            + "' where dep_set_id = '"
            + str(depositionID)
            + "' and status_code = 'DEP'"
        )
        logger.info(sql)
        nrow = DBstatusAPI.runUpdateSQL(sql)
        logger.info("rows change %s", str(nrow))


# NOT IN USE EXCEPT IN A SAMPLE SCRIPT in WFE XXXXX
def initilliseDB(metaData, depositionID, WorkflowClassID, WorkflowInstanceID, DBstatusAPI, dinput, debug=0, prt=sys.stderr):
    """
    method to extract information from the domain data
    using a depositionDB and put this into the statusDB
    """

    prt.write("WFE.WFEapplications.initialliseDB : ============================================\n")
    prt.write("WFE.WFEapplications.initialliseDB :  Intiallising DB for depID = " + str(depositionID) + "\n")
    prt.write("WFE.WFEapplications.initialliseDB : ============================================\n")

    if prt == sys.stderr:
        log = sys.stderr
    else:
        processLog = "log/status_" + str(depositionID) + "_" + WorkflowClassID + "_" + WorkflowInstanceID + ".log"
        log = open(processLog, "w")

    if debug > 0:
        process = ProcessRunner(True, log)
    else:
        process = ProcessRunner(False, log)

    process.setAction("status")

    if dinput is None:
        prt.write("WFE.WFEapplications.initialliseDB :  Requires input object \n")
        sys.exit(0)

    for key, value in dinput.items():
        if debug > 0:
            prt.write("WFE.WFEapplications.initialliseDB :  setting input " + str(key) + str(value.getReferenceType()) + "\n")
            prt.write("WFE.WFEapplications.initialliseDB :  setting input " + str(key) + str(value) + "\n")
        process.setInput("src", value)

    wfoOut = WfDataObject()
    wfoOut.setContainerTypeName("dict")
    wfoOut.setValueTypeName("string")
    process.setOutput("dst", wfoOut)

    if not process.preCheck():
        prt.write("WFE.WFEapplications.initialliseDB  : failed to setup process\n")

    if not process.run():
        prt.write("WFE.WFEapplications.initialliseDB : failed to run process\n")

    dataDict = wfoOut.getValue()
    if dataDict is None:
        logger.error(" There is no dataDictionary ")
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
        logger.info(depDB["AUTHOR_LIST"])
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

    if DBstatusAPI.exist(depDB):
        # then we do nothing - since this workflow does not modify the depostion
        constDict = {}
        constDict["DEP_SET_ID"] = depositionID
        DBstatusAPI.saveObject(depDB, "update", constDict)
    else:
        DBstatusAPI.saveObject(depDB, "insert")
        if debug > 0:
            prt.write("WFE.WFEapplications.initialliseDB : done insert data object in DB\n")
    #
    classDB = {}
    classDB["WF_CLASS_ID"] = WorkflowClassID
    classDB["WF_CLASS_FILE"] = metaData.getName()
    classDB["WF_CLASS_NAME"] = metaData.getName()
    classDB["TITLE"] = metaData.getDescription()
    classDB["AUTHOR"] = metaData.getAuthor()
    classDB["VERSION"] = metaData.getVersionMajor() + metaData.getVersionMinor()

    if DBstatusAPI.exist(classDB):
        if debug > 0:
            prt.write("WFE.WFEapplications.initialliseDB : updating the workflow class\n")
        # do nothing as we have run this workflow
        # We need to review the version to see if it is the same - how do we
        #   handle a new version of the workflow-class ?
        constDict = {}
        constDict["WF_CLASS_ID"] = WorkflowClassID
        DBstatusAPI.saveObject(classDB, "update", constDict)
    else:
        if debug > 0:
            prt.write("WFE.WFEapplications.initialliseDB : creating the workflow class object\n")
        DBstatusAPI.saveObject(classDB, "insert")

    instDB = {}
    instDB["WF_INST_ID"] = WorkflowInstanceID
    instDB["WF_CLASS_ID"] = WorkflowClassID
    instDB["DEP_SET_ID"] = depositionID
    instDB["STATUS_TIMESTAMP"] = datetime.datetime.utcnow()
    DBstatusAPI.updateStatus(instDB, "init")

    # and also initialise the wf_instance_last table
    sql = "update wf_instance_last set status_timestamp=" + str(getTimeNow()) + ", inst_status='init' where dep_set_id = '" + depositionID + "'"
    logger.info(sql)
    ok = DBstatusAPI.runUpdateSQL(sql)
    if ok < 1:
        logger.info(" CRITICAL : failed to update wf_instance_last table")

    if log != sys.stderr:
        log.close()


# XXXXX Believe internal to this file only - privatize scope?
def updateDeposit(DBstatusAPI, depositionID, site="pdbe", title="?", auth="?", method="?"):
    """
    update deposition communications table
    """

    depDB = {}
    depDB["DEP_SET_ID"] = depositionID
    timeNow = getTimeNow()

    if DBstatusAPI.exist(depDB):

        logger.info(" -> Running SQL 1 : update deposition")
        if title is None:
            sql = "update deposition set annotator_initials = 'unknown',status_code = 'PROC'   where dep_set_id = '%s' and status_code = 'DEP'" % (depositionID)
        else:
            sql = (
                "update deposition set annotator_initials = 'unknown',status_code = 'PROC', deposit_site = '%s', title = '%s', author_list = '%s', exp_method = '%s' where dep_set_id = '%s' and status_code = 'DEP'"  # noqa: E501
                % (site, title, auth, method, depositionID)
            )
        logger.info(sql)
        nrow = DBstatusAPI.runUpdateSQL(sql)
        logger.info("Rows affected: %i", nrow)

        logger.info(" -> Running SQL 2 : insert wf_instance")
        # make sure we only get the last in case processing was done with new instance data
        sql = "select ordinal from wf_instance where dep_set_id = '" + str(depositionID) + "'  order by status_timestamp desc limit 1"
        allList = DBstatusAPI.runSelectSQL(sql)

        if allList is not None:
            for allRow in allList:
                ordinal = allRow[0]
                sql = (
                    "update wf_instance set wf_inst_id = 'W_001', wf_class_id = 'Annotate', owner = 'Annotation.bf.xml', inst_status = 'init', status_timestamp = '%s' where ordinal = '%s'"
                    % (timeNow, str(ordinal))
                )
                logger.info(sql)
                nrow = DBstatusAPI.runInsertSQL(sql)
                logger.info("Rows affected: %i", nrow)
                break

        logger.info(" -> Running SQL 3 : insert wf_instance_last")
        sql = (
            "update wf_instance_last set wf_inst_id = 'W_001', wf_class_id = 'Annotate', owner = 'Annotation.bf.xml', inst_status = 'init', status_timestamp = '%s' where dep_set_id = '%s'"
            % (timeNow, str(depositionID))
        )
        logger.info(sql)
        nrow = DBstatusAPI.runInsertSQL(sql)
        logger.info("Rows affected: %i", nrow)

        return nrow

    return 0


# Deprecated - but need to cleanup WF examples
def initilliseDeposit(
    DBstatusAPI,
    depositionID,
    pdb="?",
    date=None,  # pylint: disable=unused-argument
    initials="unknown",  # pylint: disable=unused-argument
    deposit_site="?",
    process_site="?",
    status_code="DEP",  # pylint: disable=unused-argument
    author_code="?",
    title="?",
    author_list="?",
    expt="?",
    status_code_exp="?",
    SG_center="?",
    ann="dep",
    email="",
):
    """
    raw deposition table inialisation
    """

    depDB = {}
    depDB["DEP_SET_ID"] = depositionID

    if DBstatusAPI.exist(depDB):
        logger.info("ID exists ")
        sql = "update deposition set process_site = '" + str(process_site) + "', exp_method = '" + str(expt) + "' where dep_set_id = '" + str(depositionID) + "'"
        logger.info(sql)
        DBstatusAPI.runUpdateSQL(sql)
    else:
        sql = (
            "insert deposition (dep_set_id, pdb_id, deposit_site, process_site, status_code, author_release_status_code, title, author_list, exp_method, status_code_exp, SG_center, annotator_initials,email) values ('"  # noqa: E501
            + str(depositionID)
            + "','"
            + str(pdb)
            + "','"
            + str(deposit_site)
            + "','"
            + str(process_site)
            + "','"
            + str(status_code)
            + "','"
            + str(author_code)
            + "','"
            + str(title)
            + "','"
            + str(author_list)
            + "','"
            + str(expt)
            + "','"
            + str(status_code_exp)
            + "','"
            + str(SG_center)
            + "','"
            + str(ann)
            + "','"
            + str(email)
            + "')"
        )
        logger.info(sql)
        DBstatusAPI.runInsertSQL(sql)


# Only used by examples XXX
def wfLogDirectory(depID):
    siteId = getSiteId(defaultSiteId="WWPDB_DEPLOY_TEST")
    cI = ConfigInfo(siteId)

    topSessionPath = cI.get("SITE_WEB_APPS_TOP_SESSIONS_PATH")
    logDir = os.path.join(topSessionPath, "wf-logs", depID)

    if not os.path.exists(logDir):
        os.makedirs(logDir)

    return logDir
