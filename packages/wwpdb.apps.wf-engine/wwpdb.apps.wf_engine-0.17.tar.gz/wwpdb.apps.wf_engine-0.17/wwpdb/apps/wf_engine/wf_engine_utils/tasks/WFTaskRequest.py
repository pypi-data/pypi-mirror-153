##
# File:  WFTaskRequest.py
# Date:  10-April-2014  J. Westbrook
#
# Updates:
#
# 27-Jul-2015  add loadWfDefinition()
###
##
""" Manage workflow task requests and status queries --

This software was developed as part of the World Wide Protein Data Bank
Common Deposition and Annotation System Project

Copyright (c) 2010-2015 wwPDB

This software is provided under a Creative Commons Attribution 3.0 Unported
License described at http://creativecommons.org/licenses/by/3.0/.

"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.07"

import os
import sys
import traceback
import platform
from wwpdb.utils.config.ConfigInfo import ConfigInfo
from wwpdb.utils.db.WorkflowSchemaDef import WorkflowSchemaDef
from wwpdb.utils.db.MyDbAdapter import MyDbAdapter
from wwpdb.apps.wf_engine.wf_engine_utils.time.TimeStamp import TimeStamp

#
from xml.dom import minidom
from wwpdb.apps.wf_engine.reader.parseXML import parseXML


class WFTaskRequest(MyDbAdapter):

    """Manage workflow task requests and status queries --"""

    def __init__(self, siteId, verbose=False, log=sys.stderr):
        super(WFTaskRequest, self).__init__(schemaDefObj=WorkflowSchemaDef(verbose=verbose, log=log), verbose=verbose, log=log)
        # self.__verbose = verbose
        self.__lfh = log
        self.__siteId = siteId
        self.__cI = ConfigInfo(self.__siteId)
        #
        self.__myFullHostName = platform.uname()[1]
        #
        self.__timeStamp = TimeStamp()
        self.__setup()

    def setDebug(self, flag=True):
        self._setDebug(flag=flag)

    def __setup(self):
        self.__commTableId = "COMMUNICATION"
        self.__commContextId = "COMMUNICATION"

        defValD = {
            "depSetId": "D_0000000000",
            "sender": "WFUTILS",
            "receiver": "WFE",
            "command": "runWF",
            "status": "PENDING",
            "wfInstId": None,
            "wfClassId": None,
            "wfClassFile": None,
            "actualTimestamp": None,
            "host": None,
            "activity": None,
            "dataVersion": "latest",
        }
        defValD["hostName"] = self.__myFullHostName
        self._setParameterDefaultValues(contextId=self.__commContextId, valueD=defValD)
        self.__wfTableIdList = ["COMMUNICATION", "WF_TASK", "WF_INSTANCE", "WF_INSTANCE_LAST", "DEPOSITION", "USER_DATA", "ENGINE_MONITORING", "WF_CLASS_DICT"]
        for tableId in self.__wfTableIdList:
            mapL = self._getDefaultAttributeParameterMap(tableId)
            self._setAttributeParameterMap(tableId=tableId, mapL=mapL)

        #
        # mapL = [('DEP_SET_ID', 'depId'),
        #        ('PARENT_WF_INST_ID', 'wfInstId'),
        #        ('PARENT_WF_CLASS_ID', 'wfClassId'),
        #        ('PARENT_DEP_SET_ID', 'parentDepId'),
        #        ('ACTUAL_TIMESTAMP', 'timeStamp'),
        #        ('SENDER', 'sender'),
        #        ('RECEIVER', 'receiver'),
        #        ('STATUS', 'status'),
        #        ('COMMAND', 'command'),
        #        ('WF_CLASS_ID', 'wfClassId'),
        #        ('WF_INST_ID', 'wfInstId'),
        #        ('WF_CLASS_FILE', 'wfClassFile'),
        #        ('DATA_VERSION', 'dataVersion'),
        #        ('HOST', 'hostName'),
        #        ('ACTIVITY', 'activity')
        #        ]

        cMapL = [("DEP_SET_ID", "depSetId")]
        for tableId in self.__wfTableIdList[:-1]:
            self._setConstraintParameterMap(tableId=tableId, mapL=cMapL)
        #
        #
        self.__reportFiltersD = {
            "ACTUAL_TIMESTAMP": (self.__timeStamp, "getTimeStringLocal"),
            "STATUS_TIMESTAMP": (self.__timeStamp, "getTimeStringLocal"),
            "ORDINAL_ID": (self, "_formatIntVal"),
        }
        #

    def loadWfDefinition(self, wfFileName):
        """
        Load the workflow description in the input workflow definition in wf_class_dict table
        overwriting any existing definition.

        """
        wfFilePath = os.path.join(self.__cI.get("SITE_WF_XML_PATH"), wfFileName)
        if os.access(wfFilePath, os.R_OK):
            debugLevel = 0
            xmldoc = minidom.parse(wfFilePath)
            parse = parseXML(debugLevel, self.__lfh)
            wfMetaData = parse.getMetaData(xmldoc)
            wfOpts = {}
            wfOpts["wfClassId"] = wfMetaData.getID()
            wfOpts["classFile"] = wfFileName
            wfOpts["wfClassName"] = wfMetaData.getName()
            wfOpts["title"] = wfMetaData.getDescription()
            wfOpts["author"] = wfMetaData.getAuthor()
            wfOpts["version"] = wfMetaData.getVersionMajor() + wfMetaData.getVersionMinor()
            #
            _ok = self._deleteRequest(tableId="WF_CLASS_DICT", wfClassId=wfMetaData.getID())  # noqa: F841
            return self._insertRequest(tableId="WF_CLASS_DICT", contextId=None, **wfOpts)
        else:
            return False

    def setDataStore(self, dataStoreName):
        self._setDataStore(dataStoreName=dataStoreName)

    def createDataStore(self):
        """Create/recreate tables defined in the class workflow definition."""
        self._createSchema()

    def __filterReportData(self, dList, fD):
        """apply filters on the input list of dictionaries -"""
        for d in dList:
            for k, v in fD.items():
                if k in d:
                    d[k] = getattr(v[0], v[1])(d[k])

    def _formatIntVal(self, iVal):
        return "%10d" % iVal

    def selectDeposition(self, depSetId, tableId):
        return self._select(tableId, depSetId=depSetId)

    def updateDeposition(self, depSetId, **kw):
        if "depSetId" not in kw:
            kw["depSetId"] = depSetId
        return self._updateRequest(tableId="DEPOSITION", contextId=None, **kw)

    def insertDeposition(self, depSetId, **kw):
        if "depSetId" not in kw:
            kw["depSetId"] = depSetId
        return self._insertRequest(tableId="DEPOSITION", contextId=None, **kw)

    def getReport(self, reportType=None, depSetId=None):
        """Internal method to fetch report data of the report input type  and
        optional data set identifier.
        """
        tableId = reportType
        if tableId in self.__wfTableIdList:
            if depSetId is None:
                dList = self._select(tableId=tableId)
                self.__filterReportData(dList, self.__reportFiltersD)
                return dList
            else:
                dList = self._select(tableId=tableId, depSetId=depSetId)
                self.__filterReportData(dList, self.__reportFiltersD)
                return dList
        else:
            return []

    def deleteDataSet(self, depSetId, tableId):
        """Delete the input deposition data set from the input table."""
        return self._deleteRequest(tableId=tableId, depSetId=depSetId)

    def clearTable(self, tableId):
        """Clear the input table."""
        return self._deleteRequest(tableId=tableId)

    def addDataSet(self, depSetId, **kwargs):
        """
        Add and entry for the dataset for the input deposition data set.

        optional qualifiers:

                      sender="WFUTILS"
                      receiver="WFE"
                      command="runWF"
                      status="PENDING"
                      wfInstId=None
                      wfClassId=None
                      wfClassFile=None
                      actualTimestamp=None
                      host=None
                      activity=None
                      dataVersion=None

        """
        options = self._getParameterDefaultValues(contextId=self.__commContextId)
        options.update(kwargs)
        options["depSetId"] = depSetId
        options["actualTimestamp"] = self.__timeStamp.getSecondsFromReference()
        return self._insertRequest(tableId=self.__commTableId, contextId=self.__commContextId, **options)

    def assignTask(self, depSetId, **kwargs):
        """
        Request the next task for the input deposition data set.

        depId               << required

        optional qualifiers:

                      sender="WFUTILS"
                      receiver="WFE"
                      command="runWF"
                      status="PENDING"
                      wfInstId=None
                      wfClassId=None
                      wfClassFile=None
                      actualTimeStamp=None
                      host=None
                      activity=None
                      dataVersion=None

        """
        options = self._getParameterDefaultValues(contextId=self.__commContextId)
        options.update(kwargs)
        options["depSetId"] = depSetId
        options["actualTimestamp"] = self.__timeStamp.getSecondsFromReference()
        return self._updateRequest(tableId=self.__commTableId, contextId=self.__commContextId, **options)

    def loadAccessions(self, tableId, accessionType=None, filePath=None):
        try:
            mapL = self._getDefaultAttributeParameterMap(tableId)
            self._setAttributeParameterMap(tableId=tableId, mapL=mapL)
            #
            if accessionType == "PDB":
                cMapL = [("PDB_ID", "pdbId")]
                idName = "pdbId"
            elif accessionType == "BMRB":
                cMapL = [("BMRB_ID", "bmrbId")]
                idName = "bmrbId"
            elif accessionType == "EMDB":
                cMapL = [("EMDB_ID", "emdbId")]
                idName = "emdbId"
            self._setConstraintParameterMap(tableId=tableId, mapL=cMapL)
            #
            iCount = 0
            ifh = open(filePath, "r")
            accList = ifh.readlines()
            ifh.close()
            for acc in accList:
                if acc.startswith("#") or len(acc) < 3:
                    continue
                options = {}
                options[idName] = acc[:-1]
                nL = self._select(tableId=tableId, **options)
                if len(nL) > 0:
                    self.__lfh.write("WFTaskRequest.loadAccessions() skipping existing code %s\n" % acc[:-1])
                else:
                    options = {}
                    options[idName] = acc[:-1]
                    options["used"] = "n"
                    self._insertRequest(tableId=tableId, contextId=None, **options)
                    iCount += 1
            self.__lfh.write("WFTaskRequest.loadAccessions() loaded %d codes\n" % iCount)
        except:  # noqa: E722 pylint: disable=bare-except
            self.__lfh.write("WFTaskRequest.loadAccessions() failed \n")
            traceback.print_exc(file=self.__lfh)
            return False


if __name__ == "__main__":
    wfr = WFTaskRequest(None, verbose=True, log=sys.stderr)
