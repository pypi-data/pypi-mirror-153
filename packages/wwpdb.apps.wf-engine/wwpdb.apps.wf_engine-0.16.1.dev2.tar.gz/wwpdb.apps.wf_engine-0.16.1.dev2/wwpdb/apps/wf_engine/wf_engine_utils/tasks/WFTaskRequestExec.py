#!/usr/bin/env python
##
# File: WFTaskRequestExec.py
# Date: 13-Apr-2014  jdw
#
# Updates:
#    2-Mar-2015  jdw add tabular reports
#   18-Mar-2015  jdw add report content customization.
#   13-Apr-2015  jdw add application tables deposition and user_data -
#   15-Apr-2015  jdw add load/reload of deposition status tables -
#   27-Jul-2015  jdw add loadWfDefFile()
#    4-Aug-2015  jdw add --delete_user_data and remove static wf_inst_id's from the
#                         task descriptions.
#    2-Oct-2015  jdw add task 'MASKMPFX_DEP'
#   10-Nov-2015  jdw add additional truncate table targets for the v2 system.
#   18-Apr-2016  jdw Moving 'codes_db' from save to truncate -
#   18-Apr-2016  jdw Add truncate-accession option
#   18-Apr-2016  jdw Fill missing accession loader options - -
#   18-Apr-2016  jdw restore wf_class_dict to truncate list -
#    5-May-2016  jdw pdb_entry table removed from the truncate list
#   31-Jul-2016  jdw adjust option ordering for documentation
#                    update truncation lists
##
"""
Set up execution envirnoment for running workflow tasks --

"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.001"

import sys
import os
import time
from tabulate import tabulate
from optparse import OptionParser  # pylint: disable=deprecated-module

from wwpdb.io.locator.PathInfo import PathInfo
from wwpdb.utils.config.ConfigInfo import getSiteId
from wwpdb.apps.wf_engine.wf_engine_utils.tasks.WFTaskRequest import WFTaskRequest
from mmcif_utils.pdbx.PdbxIo import PdbxEntryInfoIo


class WFTaskRequestWorker(object):

    """Wrapper for WFTaskRequest() class.   Provides entry points for command line interaction
    with the workflow system.
    """

    def __init__(self, databaseName=None, verbose=False, log=sys.stderr):
        self.__verbose = verbose
        self.__lfh = log
        self.__debug = False
        self.__siteId = getSiteId(defaultSiteId="WWPDB_DEPLOY_MACOSX")
        #
        self.__wftr = WFTaskRequest(siteId=self.__siteId, verbose=self.__verbose, log=self.__lfh)
        if databaseName is not None:
            self.__wftr.setDataStore(dataStoreName=databaseName)
        #
        #
        self.__taskD = {
            "ANNOTATE_MODULE": {"wfClassId": "AnnMod", "wfClassFile": "AnnotateModule.xml"},
            "REPORTS_MODULE": {"wfClassId": "ReportMod", "wfClassFile": "ReportsModule.xml"},
            "ANNOTATION_WF": {"wfClassId": "Annotate", "wfClassFile": "Annotation.bf.xml"},
            "SUBMIT": {"wfClassId": "depRunOnSubmit", "wfClassFile": "depRunOnSubmit.xml"},
            "UPLOAD": {"wfClassId": "depRunOnUpload", "wfClassFile": "depRunOnUpload.xml"},
            "SEQUENCE_MODULE": {"wfClassId": "SeqMod", "wfClassFile": "SequenceModule.xml"},
            "PDBX2PDBX_DEP": {"wfClassId": "PDBX2PDBX_DEP", "wfClassFile": "wf_op_pdbx2pdbx_fs_deposit.xml"},
            "MTZSF2PDBX_DEP": {"wfClassId": "MTZSF2PDBX_DEP", "wfClassFile": "wf_op_mtzsf2pdbx_fs_deposit.xml"},
            "MASKMPFX_DEP": {"wfClassId": "MASKMPFX_DEP", "wfClassFile": "wf_op_maskmpfx_fs_deposit.xml"},
            "TEST_MODULE_ACCESSOR_DECISION": {"wfClassId": "AccDecTest_1", "wfClassFile": "Accessor-decision-tests.xml"},
            "TEST_MODULE_ITERATORS": {"wfClassId": "IterTests_1", "wfClassFile": "Iterator-tests.xml"},
        }
        #
        self.__defaultD = {"sender": "WFUTILS", "receiver": "WFE", "command": "runWF", "status": "PENDING"}
        #
        #

    def setDebug(self, flag=False):
        self.__wftr.setDebug(flag=flag)
        self.__debug = flag

    def loadWfDefFile(self, wfFileName):
        """Load the descriptive details of the input workflow definition in the wf_class_dict table."""
        return self.__wftr.loadWfDefinition(wfFileName)

    def loadWfDefByKey(self, wfDefKey):
        """Load the descriptive details of the input workflow definition in the wf_class_dict table."""
        if wfDefKey in self.__taskD:
            return self.__wftr.loadWfDefinition(self.__taskD[wfDefKey])
        else:
            return False

    def loadAccessions(self, accessionType, accessionPath=None):
        if accessionType == "PDB":
            self.__wftr.loadAccessions(tableId="PDB_ACCESSION", accessionType=accessionType, filePath=accessionPath)
        elif accessionType == "EMDB":
            self.__wftr.loadAccessions(tableId="EMDB_ACCESSION", accessionType=accessionType, filePath=accessionPath)
        elif accessionType == "BMRB":
            self.__wftr.loadAccessions(tableId="BMRB_ACCESSION", accessionType=accessionType, filePath=accessionPath)
        else:
            return False
        return True

    def add(self, depSetId):
        options = {}
        options.update(self.__defaultD)
        options["status"] = "INIT"
        options["command"] = "INIT"
        #
        return self.__wftr.addDataSet(depSetId=depSetId, **options)

    def deleteSet(self, depSetId, tableIdList):
        #
        try:
            for tableId in tableIdList:
                self.__wftr.deleteDataSet(depSetId=depSetId, tableId=tableId)
            return True
        except:  # noqa: E722 pylint: disable=bare-except
            return False

    def writeTruncateScript(self, dbName, tableNameList, suffix=None):
        #
        try:
            if suffix is not None and len(suffix) > 0:
                fn = "truncate-%s-%s-script.sql" % (dbName, suffix)
            else:
                fn = "truncate-%s-%s-script.sql" % (dbName, "selected")
            fp = open(fn, "w")
            fp.write("use %s ;\n" % dbName)
            for tableName in tableNameList:
                fp.write("truncate table %s ;\n" % tableName)
            fp.close()
        except:  # noqa: E722 pylint: disable=bare-except
            return False

    def clearAll(self, tableIdList):
        """For tables defined in the schema map  --"""
        #
        try:
            for tableId in tableIdList:
                self.__wftr.clearTable(tableId=tableId)
            return True
        except:  # noqa: E722 pylint: disable=bare-except
            return False

    def assignTask(self, depSetId, taskOp=None):
        if taskOp is None:
            return False
        #
        options = {}
        options.update(self.__defaultD)
        if taskOp in self.__taskD.keys():
            options.update(self.__taskD[taskOp])
            return self.__wftr.assignTask(depSetId=depSetId, **options)
        elif taskOp.lower() in ["stop", "kill"]:
            options["command"] = "killWF"
            return self.__wftr.assignTask(depSetId=depSetId, **options)
        elif taskOp.lower() in ["restart"]:
            options["command"] = "restartWF"
            return self.__wftr.assignTask(depSetId=depSetId, **options)
        elif taskOp.lower() in ["restartgo"]:
            options["command"] = "restartGoWF"
            return self.__wftr.assignTask(depSetId=depSetId, **options)
        elif taskOp.lower() in ["wait"]:
            options["command"] = "waitWF"
            return self.__wftr.assignTask(depSetId=depSetId, **options)
        elif taskOp.lower() in ["delete", "remove"]:
            return self.__wftr.deleteDataSet(depSetId=depSetId)  # THIS IS MISSING AN ARGUMENT  pylint: disable=no-value-for-parameter
        else:
            return False

    def reportVertical(self, ofh=sys.stdout, reportType="COMMUNICATION", depSetId=None):
        """Terminal display of rdbms tables defined via SchemaDefBase() and related
        classes -
        """
        rdL = self.__wftr.getReport(reportType=reportType, depSetId=depSetId)
        for rd in rdL:
            if depSetId is not None:
                ofh.write("\n ++ DATA SET:  %s\n" % depSetId)
            else:
                ofh.write("\n ++ FULL REPORT:\n")

            for k, v in rd.items():
                depSetId = "UNASSIGNED"
                if "DEP_SET_ID" in rd:
                    depSetId = rd["DEP_SET_ID"]
                ofh.write(" ++ (%12s) ++    %-40s :  %s\n" % (depSetId, k, v))

    def report(self, ofh=sys.stdout, reportType="COMMUNICATION", depSetId=None, attributeIdList=None):
        """Formatted tabular reports of rdbms tables defined via SchemaDefBase() and related
        classes -
        """
        if attributeIdList is None:
            attributeIdList = []
        if depSetId is not None:
            ofh.write("\nTable identifer: %s for data set %s\n" % (reportType, depSetId))
        else:
            ofh.write("\nTable identifer: %s\n" % reportType)
        #
        rdL = self.__wftr.getReport(reportType=reportType, depSetId=depSetId)
        if rdL is not None and len(rdL) > 0:
            if (attributeIdList is not None) and (len(attributeIdList) > 0):
                tdL = []
                hL = rdL[0].keys()
                thL = []
                for h in attributeIdList:
                    if h in hL:
                        thL.append(h)

                tdL.append(thL)
                for rd in rdL:
                    tL = []
                    for attributeId in attributeIdList:
                        if attributeId in hL:
                            tL.append(rd[attributeId])
                    tdL.append(tL)

                ofh.write("%s\n" % tabulate(tdL, headers="firstrow", tablefmt="grid"))
            else:
                hL = rdL[0].keys()
                hD = {}
                for h in hL:
                    hD[h] = h
                ofh.write("%s\n" % tabulate(rdL, hD, tablefmt="grid"))
        else:
            ofh.write("No data\n")

    def __mapDepositItems(self, mD):
        """Map items for data model file to schema attributes -
           "DEP_SET_ID": "dep_set_id",
           "PDB_ID": "pdb_id",
           "INITIAL_DEPOSITION_DATE": "initial_deposition_date",
           "ANNOTATOR_INITIALS": "annotator_initials",
           "DEPOSIT_SITE": "deposit_site",
           "PROCESS_SITE": "process_site",
           "STATUS_CODE": "status_code",
           "AUTHOR_RELEASE_STATUS_CODE": "author_release_status_code",
           "TITLE": "title",
           "AUTHOR_LIST": "author_list",
           "EXP_METHOD": "exp_method",
           "STATUS_CODE_EXP": "status_code_exp",
           "SG_CENTER": "SG_center",
           "DEPPW": "depPW",
           "NOTIFY": "notify",
          # "DATE_BEGIN_PROCESSING": "date_begin_processing",
          # "DATE_END_PROCESSING": "date_end_processing",
           "EMAIL": "email",
           "LOCKING": "locking",
           "COUNTRY": "country",
           "NMOLECULE": "nmolecule",
           "EMDB_ID": "emdb_id",
           "BMRB_ID": "bmrb_id",
           "STATUS_CODE_EMDB": "status_code_emdb",
           "STATUS_CODE_BMRB": "status_code_bmrb",
           "STATUS_CODE_OTHER": "status_code_other"

        mapL = [
          ('pdb_id', 'pdbId'),
          ('experimental_methods','expMethod'),
          ('struct_title','title'),
          ('status_code','statusCode'),
          ('auth_release_code','authorReleaseStatusCode'),
          ('deposit_date','initialDepositionDate'),
          ('annotator_initials','annotatorInitials'),
          ('begin_processing_date','dateBeginProcessing'),
           ]
        """
        uD = {}
        mapL = [
            ("pdb_id", "pdbId"),
            ("experimental_methods", "expMethod"),
            ("struct_title", "title"),
            ("status_code", "statusCode"),
            ("auth_release_code", "authorReleaseStatusCode"),
            ("deposit_date", "initialDepositionDate"),
            ("annotator_initials", "annotatorInitials"),
            ("begin_processing_date", "dateBeginProcessing"),
        ]
        for mt in mapL:
            if (mt[0] in mD) and (len(mD[mt[0]]) > 0):
                uD[mt[1]] = mD[mt[0]]
        return uD

    def reloadDepositionStatus(self, depSetId, fileSource="archive", contentType="model", mileStone=None, versionId="latest"):  # pylint: disable=unused-argument
        """Load/reload deposition status database with domain details extracted from the input
        model file.

        """
        pI = PathInfo(siteId=self.__siteId, sessionPath=".", verbose=self.__verbose, log=self.__lfh)
        fp = pI.getModelPdbxFilePath(depSetId, fileSource=fileSource, mileStone=mileStone, versionId=versionId)
        self.__lfh.write("+WFTaskRequestWorker.reloadDepositionStatus() target model file path (PDBx):   %s\n" % fp)
        if os.access(fp, os.R_OK):
            ei = PdbxEntryInfoIo(verbose=self.__verbose, log=self.__lfh)
            ei.setFilePath(filePath=fp)
            mD = ei.getInfoD(contextType="general")
            mD.update(ei.getInfoD(contextType="history"))
            #
            if self.__debug:
                self.__lfh.write("+WFTaskRequestWorker.reloadDepositionStatus() model data dictionary %r\n" % mD.items())
        else:
            self.__lfh.write("+WFTaskRequestWorker.reloadDepositionStatus() unable to open model file at: %s\n" % fp)
            return 0
        #
        uD = self.__mapDepositItems(mD)
        dL = self.__wftr.selectDeposition(tableId="DEPOSITION", depSetId=depSetId)
        if len(dL) > 0:
            if self.__debug:
                self.__lfh.write("+WFTaskRequestWorker.reloadDepositionStatus() updating  - overwriting existing deposition status data: %r\n" % dL)
            nR = self.__wftr.updateDeposition(depSetId=depSetId, **uD)
        else:
            if self.__debug:
                self.__lfh.write("+WFTaskRequestWorker.reloadDepositionStatus() inserting  - new deposition status data: %r\n" % uD)
            nR = self.__wftr.insertDeposition(depSetId=depSetId, **uD)

        return nR


def main():
    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    reportD = {
        "communication_1": (
            "COMMUNICATION",
            ["DEP_SET_ID", "ORDINAL_ID", "PARENT_WF_INST_ID", "WF_INST_ID", "PARENT_WF_CLASS_ID", "WF_CLASS_FILE", "WF_CLASS_ID", "COMMAND", "DATA_VERSION"],
        ),
        "communication_2": (
            "COMMUNICATION",
            ["DEP_SET_ID", "ORDINAL_ID", "PARENT_WF_INST_ID", "WF_INST_ID", "SENDER", "RECEIVER", "HOST", "STATUS", "ACTIVITY", "ACTUAL_TIMESTAMP"],
        ),
        "communication": ("COMMUNICATION", []),
        "task": ("WF_TASK", []),
        "instance": ("WF_INSTANCE", []),
        "last_instance": ("WF_INSTANCE_LAST", []),
        "monitor_1": ("ENGINE_MONITORING", ["HOSTNAME", "STATUS_TIMESTAMP", "TOTAL_PHYSICAL_MEM", "TOTAL_VIRTUAL_MEM", "PHYSICAL_MEM_USAGE", "VIRTUAL_MEM_USAGE"]),
        "monitor_2": ("ENGINE_MONITORING", ["HOSTNAME", "CPU_USAGE", "CPU_NUMBER", "IDS_SET", "SWAP_TOTAL", "SWAP_USED", "SWAP_FREE"]),
        "deposition_1": (
            "DEPOSITION",
            ["ORDINAL", "DEP_SET_ID", "PDB_ID", "INITIAL_DEPOSITION_DATE", "ANNOTATOR_INITIALS", "DEPOSIT_SITE", "PROCESS_SITE", "STATUS_CODE", "AUTHOR_RELEASE_STATUS_CODE"],
        ),
        "deposition_2": ("DEPOSITION", ["ORDINAL", "DEP_SET_ID", "TITLE", "AUTHOR_LIST"]),
        "deposition_3": ("DEPOSITION", ["ORDINAL", "DEP_SET_ID", "EXP_METHOD", "STATUS_CODE_EXP", "SG_CENTER", "DEPPW", "NOTIFY", "DATE_BEGIN_PROCESSING", "DATE_END_PROCESSING"]),
        "deposition_4": (
            "DEPOSITION",
            ["ORDINAL", "DEP_SET_ID", "EMAIL", "LOCKING", "COUNTRY", "NMOLECULE", "EMDB_ID", "BMRB_ID", "STATUS_CODE_EMDB", "STATUS_CODE_BMRB", "STATUS_CODE_OTHER"],
        ),
        "user_data": ("USER_DATA", ["ORDINAL", "DEP_SET_ID", "EMAIL", "LAST_NAME", "ROLE", "COUNTRY"]),
        "wf_defs": ("WF_CLASS_DICT", ["ORDINAL_ID", "WF_CLASS_ID", "WF_CLASS_NAME", "TITLE", "AUTHOR", "VERSION", "CLASS_FILE"]),
    }
    #
    # Full list of managed tables --
    #
    # tableIdList = ["COMMUNICATION", "WF_TASK", "WF_INSTANCE", "WF_INSTANCE_LAST", "ENGINE_MONITORING", "DEPOSITION", "USER_DATA"]
    #
    # Table subsets for workflow and depositon
    #
    workflowTableIdList = ["COMMUNICATION", "WF_TASK", "WF_INSTANCE", "WF_INSTANCE_LAST", "WF_REFERENCE", "ENGINE_MONITORING"]
    depositionTableIdList = ["DEPOSITION"]
    userDataTableIdList = ["USER_DATA"]
    tablesPersistD = {
        "depui_django": {
            "save": ["auth_permission", "django_content_type"],
            "truncate": [
                "auth_group",
                "auth_group_permissions",
                "auth_message",
                "auth_user",
                "auth_user_groups",
                "auth_user_user_permissions",
                "depui_depositionstatus",
                "depui_depositionuiuser",
                "depui_wwpdbupload",
                "django_session",
                "django_site",
                "depui_deposition",
                "depui_relatedentries",
                "depui_experiments",
                "depui_requestedcodes",
                "depui_mapvoxel",
                "depui_processaction",
                "depui_processactionfile",
            ],
        },
        # status contains the following constructed views - 'dep_instance','dep_last_instance',
        #   18-Apr-2016 Moving 'codes_db' from save to truncate
        "status": {
            "save": ["bmrbID", "citation", "da_group", "da_users", "emdbID", "pdbID", "taxonomy", "sgcenters", "site", "status"],
            "truncate": [
                "anno_selection",
                "author_corrections",
                "communication",
                "contact_author",
                "database_PDB_obs_spr",
                "database_ref",
                "database_related",
                "dep_with_problems",
                "deposition",
                "django_session",
                "engine_monitoring",
                "experiments_db",
                "manager_site",
                "other_data",
                "process_information",
                "related_db",
                "release_request",
                "timestamp",
                "user_data",
                "wf_instance",
                "wf_instance_last",
                "wf_reference",
                "wf_task",
                "wf_class_dict",
                "com",
                "remind_message_track",
                "status_change",
                "codes_db",
                "batch_user_data",
                "group_deposition_information",
            ],
            "truncate-accession": ["bmrbID", "emdbID", "pdbID", "codes_db"],
        },
        #
        #
        "da_internal": {
            "truncate": [
                "PDB_status_information",
                "audit_author",
                "chem_comp",
                "citation",
                "citation_author",
                "database_2",
                "diffrn_source",
                "em_admin",
                "entity",
                "entity_poly",
                "exptl",
                "ndb_struct_conf_na",
                "pdbx_audit_revision_category",
                "pdbx_audit_revision_details",
                "pdbx_audit_revision_group",
                "pdbx_audit_revision_history",
                "pdbx_audit_revision_item",
                "pdbx_contact_author",
                "pdbx_database_PDB_obs_spr",
                "pdbx_database_related",
                "pdbx_database_status_history",
                "pdbx_deposit_group",
                "pdbx_depui_entry_details",
                "pdbx_entity_nonpoly",
                "pdbx_molecule",
                "pdbx_molecule_features",
                "pdbx_prerelease_seq",
                "processing_status",
                "rcsb_status",
                "struct",
                "struct_keywords",
                "struct_site_keywords",
            ],
            "save": [],
        },
    }

    #
    parser.add_option("--dataset", dest="depSetId", default=None, help="Target deposition data set")
    parser.add_option("--add", dest="addOp", default=False, help="Add deposition data set to workflow system", action="store_true")
    parser.add_option("--task", dest="taskOp", default=None, help="Workflow task name to be invoked")

    parser.add_option("--file_source", dest="fileSource", default=None, help="Input file source for data set archive|deposit")
    parser.add_option("--milestone", dest="milestone", default=None, help="Input dataset milestone")
    parser.add_option("--file_version", dest="fileVersion", default="latest", help="Input data set file version")

    parser.add_option("--report", dest="reportOp", default=None, help="Create report: communication, monitor, task, instance, last_instance, deposition, user_data or summary")
    parser.add_option("--database", dest="databaseName", default=None, help="Set alternative workflow status database (default database = status)")

    parser.add_option("--delete_workflow", dest="deleteWorkflowOp", default=False, help="Delete data set from the workflow table subset", action="store_true")
    parser.add_option("--delete_deposition", dest="deleteDepositionOp", default=False, help="Delete data set from the deposition table subset", action="store_true")
    parser.add_option("--delete_user_data", dest="deleteUserDataOp", default=False, help="Delete data set from the user data table subset", action="store_true")
    parser.add_option("--truncate_script", dest="truncateOp", default=False, help="Create scripts to clear all workflow and deposition user data", action="store_true")
    parser.add_option("--truncate_accessions", dest="truncateAccessionsOp", default=False, help="Create scripts to clear all accession tables", action="store_true")
    #
    parser.add_option("--reload_status", dest="reloadStatus", default=False, help="(Re)Load workflow status database for input data set", action="store_true")

    parser.add_option("--accession_file", dest="accessionPath", default=None, help="Accession file path")
    parser.add_option("--load_accessions_pdb", dest="loadAccessionsPdb", default=False, help="Load PDB accession codes", action="store_true")
    parser.add_option("--load_accessions_bmrb", dest="loadAccessionsBmrb", default=False, help="Load BMRB accession codes", action="store_true")
    parser.add_option("--load_accessions_emdb", dest="loadAccessionsEmdb", default=False, help="Load EMDB accession codes", action="store_true")
    #
    parser.add_option("--load_wf_def_file", dest="wfDefFileName", default=None, help="Load workflow definition file name (in project path) to class table")
    #
    parser.add_option("-v", "--verbose", default=False, action="store_true", dest="verbose", help="Enable verbose output")
    parser.add_option("-d", "--debug", default=False, action="store_true", dest="debug", help="Enable debug output")

    (options, _args) = parser.parse_args()

    trw = WFTaskRequestWorker(databaseName=options.databaseName, verbose=options.verbose, log=sys.stderr)
    lt = time.strftime("%Y %m %d %H:%M:%S", time.localtime())
    #
    if options.debug:
        trw.setDebug(flag=options.debug)

    if options.reloadStatus and options.fileSource in ["deposit", "archive"] and options.depSetId is not None:
        sys.stdout.write("+WFTaskRequestExec(main) starting status reload at  %s\n" % lt)
        trw.reloadDepositionStatus(depSetId=options.depSetId, fileSource=options.fileSource, mileStone=options.milestone, versionId=options.fileVersion)
    elif options.reportOp in ["summary"]:
        sys.stdout.write("+WFTaskRequestExec(main) starting report op at  %s\n" % lt)
        for op in ["communication_1", "communication_2", "last_instance", "instance", "task"]:
            trw.report(reportType=reportD[op][0], depSetId=options.depSetId, attributeIdList=reportD[op][1])
    elif options.reportOp in ["monitor"]:
        sys.stdout.write("+WFTaskRequestExec(main) starting report op at  %s\n" % lt)
        for op in ["monitor_1", "monitor_2"]:
            trw.report(reportType=reportD[op][0], depSetId=options.depSetId, attributeIdList=reportD[op][1])
    elif options.reportOp in ["deposition"]:
        sys.stdout.write("+WFTaskRequestExec(main) starting report op at  %s\n" % lt)
        for op in ["deposition_1", "deposition_2", "deposition_3", "deposition_4"]:
            trw.report(reportType=reportD[op][0], depSetId=options.depSetId, attributeIdList=reportD[op][1])
    elif options.reportOp in reportD:
        sys.stdout.write("+WFTaskRequestExec(main) starting report op at  %s\n" % lt)
        trw.report(reportType=reportD[options.reportOp][0], depSetId=options.depSetId, attributeIdList=reportD[options.reportOp][1])

    elif options.deleteWorkflowOp and options.depSetId is not None:
        sys.stdout.write("+WFTaskRequestExec(main) starting workflow delete op %s at  %s\n" % (options.depSetId, lt))
        trw.deleteSet(depSetId=options.depSetId, tableIdList=workflowTableIdList[:-1])

    elif options.deleteDepositionOp and options.depSetId is not None:
        sys.stdout.write("+WFTaskRequestExec(main) starting deposition delete op for %s at  %s\n" % (options.depSetId, lt))
        trw.deleteSet(depSetId=options.depSetId, tableIdList=depositionTableIdList)

    elif options.deleteUserDataOp and options.depSetId is not None:
        sys.stdout.write("+WFTaskRequestExec(main) starting deposition delete op for %s at  %s\n" % (options.depSetId, lt))
        trw.deleteSet(depSetId=options.depSetId, tableIdList=userDataTableIdList)

    elif options.truncateOp:
        sys.stdout.write("+WFTaskRequestExec(main) creating truncation scripts at  %s\n" % lt)
        for db, tD in tablesPersistD.items():
            for kS, tL in tD.items():
                if kS == "truncate":
                    trw.writeTruncateScript(dbName=db, tableNameList=tL, suffix="")

    elif options.addOp and options.depSetId is not None:
        sys.stdout.write("+WFTaskRequestExec(main) starting add   op on %s at  %s\n" % (options.depSetId, lt))
        trw.add(depSetId=options.depSetId)

    elif options.taskOp is not None and options.depSetId is not None:
        sys.stdout.write("+WFTaskRequestExec(main) assigning task op %s for %s at %s\n" % (options.taskOp, options.depSetId, lt))
        trw.assignTask(depSetId=options.depSetId, taskOp=options.taskOp)
    elif options.loadAccessionsPdb and options.accessionPath is not None:
        sys.stdout.write("+WFTaskRequestExec(main) loading PDB accessions from %s at %s\n" % (options.accessionPath, lt))
        trw.loadAccessions(accessionType="PDB", accessionPath=options.accessionPath)
    elif options.loadAccessionsBmrb and options.accessionPath is not None:
        sys.stdout.write("+WFTaskRequestExec(main) loading BMRB accessions from %s at %s\n" % (options.accessionPath, lt))
        trw.loadAccessions(accessionType="BMRB", accessionPath=options.accessionPath)
    elif options.loadAccessionsEmdb and options.accessionPath is not None:
        sys.stdout.write("+WFTaskRequestExec(main) loading EMDB accessions from %s at %s\n" % (options.accessionPath, lt))
        trw.loadAccessions(accessionType="EMDB", accessionPath=options.accessionPath)
    elif options.truncateAccessionsOp:
        sys.stdout.write("+WFTaskRequestExec(main) creating accesion tables truncation script at  %s\n" % lt)
        trw.writeTruncateScript(dbName="status", tableNameList=tablesPersistD["status"]["truncate-accession"], suffix="accession")
    elif options.wfDefFileName is not None:
        trw.loadWfDefFile(wfFileName=options.wfDefFileName)
    else:
        pass


if __name__ == "__main__":
    main()
#
