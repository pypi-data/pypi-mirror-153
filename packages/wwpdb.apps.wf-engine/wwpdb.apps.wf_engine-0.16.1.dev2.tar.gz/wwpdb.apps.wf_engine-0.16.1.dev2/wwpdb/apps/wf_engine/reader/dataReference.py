##
# File:    dataReference.py
# Date:    15-Mar-2009
#
# Updates:
#  22-April-2010 : Incorporation into enterpise.
#
##

#
# data object definition
#

__docformat__ = "restructuredtext en"
__author__ = "Tom Oldfield"
__email__ = "oldfield@ebi.ac.uk"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.24"

import sys

from wwpdb.utils.wf.WfDataObject import WfDataObject


class dataModule(object):

    """Hold a data reference, passed variable is the XML dom
    object to be parsed"""

    def __init__(self, instanceID, depositionID, debug=0, prt=sys.stderr):

        self.debug = debug
        self.__lfh = prt

        # string, double, complex etc...
        self.type = "unknown"
        # reference name for lookup from task
        self.name = "unknown"
        # reference name for lookup from task - humanReadableForm
        self.nameHumanReadable = "unknown"
        # description is just a string for humans
        self.description = "unknown"
        # could be File, DataModel, WorkflowData
        self.where = "unknown"
        # localMode is the task mode for that data instance
        self.localMode = "unknown"
        # mutability of data - is it write-locked
        self.mutable = "true"
        # and the data for the WFE data only
        self.data = None
        # depositionID
        # create a apiDataobject
        self.ApiData = WfDataObject()
        self.ApiData.setDepositionDataSetId(depositionID)
        if debug > 1:
            self.__lfh.write("+dataModule.__init__ : depositionID " + str(depositionID) + "\n")

        self.ApiData.setWorkflowInstanceId(instanceID)
        if debug > 1:
            self.__lfh.write("+dataModule.__init__ :  instanceID  " + str(instanceID) + "\n")
        # status code for the data reading
        self.status = "OK"

        # containers for all API attributes
        self.valueContainer = None
        self.valueType = None
        self.version = None
        self.value = None
        self.format = None
        self.content = None
        self.selectCategory = None
        self.selectAttribute = None
        self.selectConditionAttribute = None
        self.partitionNumber = None
        self.referenceType = None

    def getValue(self):
        return self.data

    def setValue(self, value):
        self.data = value

    def setInstanceID(self, instanceID):

        self.ApiData.setWorkflowInstanceId(instanceID)
        if self.debug > 1:
            self.__lfh.write("+dataModule.setInstanceId:  setWorkflowInstanceId  " + str(instanceID) + "\n")

    def parseXML(self, data):
        #   class = dataModule : fill class variable from dom

        self.type = data.getAttribute("type")
        self.name = data.getAttribute("dataID")
        self.nameHumanReadable = data.getAttribute("name")

        self.valueContainer = data.getAttribute("container")
        self.valueType = data.getAttribute("type")
        self.mutable = data.getAttribute("mutable")

        for detail in data.childNodes:
            if detail.nodeName == "wf:description":
                self.description = detail.firstChild.data
            elif detail.nodeName == "wf:location":
                self.where = str(detail.getAttribute("where"))
                # if self.where == "archive" or self.where == "wf-instance" or self.where[:4] == "path" or self.where == 'deposit':
                if (len(self.where) > 0) and (self.where not in ["constant", "inline"]):
                    self.version = detail.getAttribute("version")
                    self.content = detail.getAttribute("content")
                    self.format = detail.getAttribute("format")
                    self.selectCategory = str(detail.getAttribute("selectCategory"))
                    self.selectAttribute = str(detail.getAttribute("selectAttribute"))
                    self.partitionNumber = str(detail.getAttribute("partitionNumber"))
                    self.selectConditionAttribute = str(detail.getAttribute("selectConditionAttribute"))
                    self.referenceType = str(detail.getAttribute("referenceType"))

                # WF data objects that are initialized values within workflow definitions.
                elif self.where == "constant":
                    if self.debug > 1:
                        self.__lfh.write("+dataModule.parseXML : found constant data object\n")
                        self.__lfh.write("+dataModule.parseXML : found container " + str(self.valueContainer) + "\n")
                        self.__lfh.write("+dataModule.parseXML : found type " + str(self.valueType) + "\n")
                        self.__lfh.write("+dataModule.parseXML : found value " + str(detail.getAttribute("value")) + "\n")
                    if self.valueContainer == "list":
                        s = detail.getAttribute("value")
                        self.data = []
                        self.data = s.split(",")
                    elif self.valueContainer == "string":
                        self.data = detail.getAttribute("value")
                    if self.debug > 1:
                        self.__lfh.write("+dataModule.parseXML : value = " + str(self.data))
                elif self.where == "inline":
                    if self.debug > 1:
                        self.__lfh.write("+dataModule.parseXML : found inline data object\n")
                        self.__lfh.write("+dataModule.parseXML : found container " + str(self.valueContainer) + "\n")
                        self.__lfh.write("+dataModule.parseXML : found type " + str(self.valueType) + "\n")
                        self.__lfh.write("+dataModule.parseXML : found value " + str(detail.getAttribute("value")) + "\n")
                    if self.valueContainer == "list":
                        self.data = []
                    elif self.valueContainer == "string":
                        self.data = ""
                    if self.debug > 1:
                        self.__lfh.write("+dataModule.parseXML : inline variable initialized with = " + str(self.data))

        if self.debug > 1:
            self.printMe(self.__lfh)

    def setLocalMode(self, local):
        # set the value of the local mode for Class = dataModule

        self.localMode = local

    def isThisName(self, compareName):

        if self.name == compareName:
            return "yes"
        else:
            return ""

    def printMe(self, lfh):
        lfh.write("+dataModule.printMe : Data ID               %s\n" % self.name)
        lfh.write("+dataModule.printMe : Data name             %s\n" % self.nameHumanReadable)
        lfh.write("+dataModule.printMe : Data description      %s\n" % self.description)
        lfh.write("+dataModule.printMe : Data Type             %s\n" % self.type)
        lfh.write("+dataModule.printMe : Data location(where)  %s\n" % self.where)
        lfh.write("+dataModule.printMe : Data Container        %s\n" % self.valueContainer)
        lfh.write("+dataModule.printMe : Data type             %s\n" % self.valueType)
        if self.data is not None:
            lfh.write("+dataModule.printMe : Data object value     %r\n" % self.data)
        if self.localMode:
            lfh.write("+dataModule.printMe : Data Mode             %s\n" % self.localMode)
        #
