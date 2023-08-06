##
# File:    parseXML.py
# Date:    15-Mar-2009
#
# Updates:
#  22-April-2010 : Incorporation into enterpise.
#
##

"""
entry point for the workflow class XML parser
"""

__docformat__ = "restructuredtext en"
__author__ = "Tom Oldfield"
__email__ = "oldfield@ebi.ac.uk"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.24"

import sys
from wwpdb.apps.wf_engine.reader.taskReference import taskModule
from wwpdb.apps.wf_engine.reader.dataReference import dataModule
from wwpdb.apps.wf_engine.reader.metaDataObject import metaDataObject


class parseXML(object):
    """Hold a data reference, passed variable is the XML dom
    object to be parsed"""

    def __init__(self, debug=0, prt=sys.stderr):

        self.debug = debug
        self.__lfh = prt

    def getMetaData(self, xmldoc):

        mData = None

        for outer in xmldoc.childNodes:
            if outer.nodeName == "wf:wwPDBworkflow":
                for thing in outer.childNodes:
                    if thing.nodeName == "wf:metadata":
                        mData = metaDataObject()
                        for metaData in thing.childNodes:
                            if metaData.nodeName == "wf:version":
                                self.__lfh.write(
                                    "WFE.parseXML.getMetaData : XML style = PRODUCTION : major release = "
                                    + str(metaData.getAttribute("major"))
                                    + " : Date = "
                                    + str(metaData.getAttribute("date"))
                                    + "\n"
                                )
                                mData.setVersionMajor(metaData.getAttribute("major"))
                                mData.setVersionMinor(metaData.getAttribute("minor"))
                                mData.setAuthor(metaData.getAttribute("author"))
                                mData.setDate(metaData.getAttribute("date"))
                                mData.setID(metaData.getAttribute("id"))
                                mData.setName(metaData.getAttribute("name"))
                            if metaData.nodeName == "wf:description":
                                for title in metaData.childNodes:
                                    if title.nodeName == "wf:short":
                                        mData.setDescription(title.firstChild.data)
                                    if title.nodeName == "wf:subtext":
                                        self.__lfh.write("WFE.parseXML.getMetaData :   --> " + str(title.firstChild.data) + "\n")

        return mData

    def getTaskObjects(self, xmldoc):

        taskObjects = []

        for outer in xmldoc.childNodes:
            for typeNode in outer.childNodes:
                if typeNode.nodeName == "wf:workflow":
                    for flowNodes in typeNode.childNodes:
                        if flowNodes.nodeName == "wf:flow":
                            for tasksNode in flowNodes.childNodes:
                                if tasksNode.nodeName == "wf:entryPoint":
                                    taskRef = taskModule(self.debug, self.__lfh)
                                    taskRef.type = "Entry-point"
                                    taskRef.name = tasksNode.getAttribute("taskID")
                                    taskRef.nameHumanReadable = tasksNode.getAttribute("name")
                                    taskRef.outputName.append(tasksNode.getAttribute("nextTask"))
                                    taskRef.exception = tasksNode.getAttribute("exceptionID")
                                    taskObjects.append(taskRef)
                                elif tasksNode.nodeName == "wf:exitPoint":
                                    taskRef = taskModule(self.debug, self.__lfh)
                                    taskRef.type = "Exit-point"
                                    taskRef.name = tasksNode.getAttribute("taskID")
                                    taskRef.nameHumanReadable = tasksNode.getAttribute("name")
                                    taskObjects.append(taskRef)
                                elif tasksNode.nodeName == "wf:exception":
                                    taskRef = taskModule(self.debug, self.__lfh)
                                    taskRef.type = "Exception"
                                    taskRef.parseXML(tasksNode)
                                    taskObjects.append(taskRef)
                                elif tasksNode.nodeName == "wf:tasks":
                                    for taskNode in tasksNode.childNodes:
                                        if taskNode.nodeName == "wf:task":
                                            taskRef = taskModule(self.debug, self.__lfh)
                                            taskRef.parseXML(taskNode)
                                            taskObjects.append(taskRef)
                                elif tasksNode.nodeName == "#text" or tasksNode.nodeName == "#comment":
                                    pass
                                else:
                                    self.__lfh.write("WFE.parseXML.getMetaData :  Critical workflow XMl error : Unknown FLOW tag " + str(tasksNode.nodeName) + "\n")
                                    sys.exit(0)

        return taskObjects

    def getDataObjects(self, depositionID, instanceID, xmldoc):

        dataObjects = []

        for outer in xmldoc.childNodes:
            for typeNode in outer.childNodes:
                if typeNode.nodeName == "wf:workflow":
                    for dataNodes in typeNode.childNodes:
                        if dataNodes.nodeName == "wf:dataObjects":
                            for dataNode in dataNodes.childNodes:
                                if dataNode.nodeName == "wf:dataObject":
                                    dat = dataModule(instanceID, depositionID, self.debug, self.__lfh)
                                    dat.parseXML(dataNode)
                                    dataObjects.append(dat)

        return dataObjects
