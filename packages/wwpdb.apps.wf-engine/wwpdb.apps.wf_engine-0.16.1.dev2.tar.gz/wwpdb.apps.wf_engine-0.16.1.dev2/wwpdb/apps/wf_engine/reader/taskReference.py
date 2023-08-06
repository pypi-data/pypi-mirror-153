##
# File:    taskReference.py
# Date:    15-Mar-2009
#
# Updates:
#  22-April-2010 : Incorporation into enterpise.
#
##

"""
task object
"""

__docformat__ = "restructuredtext en"
__author__ = "Tom Oldfield"
__email__ = "oldfield@ebi.ac.uk"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.24"

import sys
from wwpdb.apps.wf_engine.reader.TaskComparitor import TaskComparitor
from wwpdb.apps.wf_engine.reader.TaskParameter import TaskParameter
from wwpdb.apps.wf_engine.reader.parseTimeDelta import parseTimeDelta

from wwpdb.utils.wf.process.ActionRegistry import ActionRegistry


class taskModule:

    """
    Holds the task object, the task information is passed
      out of the XML dom object
    """

    def __init__(self, debug=0, prt=sys.stderr):

        # string, double, complex, etc
        self.type = "unknown"
        # name of task for crossReference
        self.name = "unknown"
        # name of task for crossReference - human readable form
        self.nameHumanReadable = "unknown"
        # can we stop here for data
        self.breakPoint = "false"
        # exception hander : the task to handle expection
        self.exception = None
        # Used to store application name and file for workflows etc
        self.file = "unknown"
        # desciption - information for humans
        self.description = "unknown"
        # Not used   JDW
        # inputName - where the task flow was passed from
        # self.inputName = []
        #
        # outputName - where the task flow goes to.
        self.outputName = []
        # dataObject - list of data references
        self.data = []
        # expected run time
        self.runTime = 1
        # failsafe die
        self.failTime = 4
        # debug level
        self.debug = debug
        self.__lfh = prt
        # functions : list of functions
        self.func = []
        # parameters : 1 parameter
        self.param = None

        self.ActionRegistry = ActionRegistry()

        self.uniqueName = None
        self.uniqueType = None
        self.uniqueWhere = None
        self.uniqueAction = None
        self.uniqueActionName = None
        self.parameter = None
        #    self.uniqueContainer = None : put into data object
        #    self.uniqueType = None : put in data object

    def parseXML(self, taskNode):
        """parse the XML dom object to extract a task object"""

        self.name = taskNode.getAttribute("taskID")
        self.nameHumanReadable = taskNode.getAttribute("name")
        self.breakPoint = taskNode.getAttribute("breakpoint")
        self.exception = taskNode.getAttribute("exceptionID")
        self.uniqueActionName = taskNode.getAttribute("reference")
        if taskNode.nodeName == "wf:exception":
            self.outputName.append(taskNode.getAttribute("nextTask"))
            self.type = "exception"

        for taskType in taskNode.childNodes:
            if taskType.nodeName == "wf:description":
                self.description = taskType.firstChild.data
            elif taskType.nodeName == "wf:process":
                self.outputName.append(taskNode.getAttribute("nextTask"))
                self.parseProcessTask(taskType)
            elif taskType.nodeName == "wf:decision":
                self.parseAutoDecisionTask(taskType)
            elif taskType.nodeName == "wf:loop":
                self.outputName.append(taskNode.getAttribute("nextTask"))
                self.parseLoopTask(taskType)
            elif taskType.nodeName == "wf:workflow":
                self.type = "Workflow"
                self.file = taskType.getAttribute("file")
                self.outputName.append(taskNode.getAttribute("nextTask"))
                temp = taskType.getAttribute("runTime")
                self.runTime = int(parseTimeDelta(temp).total_seconds())
                temp = taskType.getAttribute("failTime")
                self.failTime = int(parseTimeDelta(temp).total_seconds())
            elif taskType.nodeName == "wf:handler":
                self.parseException(taskType)
            elif taskType.nodeName == "wf:manual":
                self.parseManualTask(taskType)
            elif taskType.nodeName == "wf:join":
                # this is not done at the moment - implied OR
                pass

    def parseException(self, exception):

        if self.debug > 0:
            pass
        datum = []
        # insert the default nextTask as the default handle
        self.outputName.append(exception.getAttribute("nextTask"))
        datum.append(exception.getAttribute("warning"))
        datum.append(exception.getAttribute("select"))
        datum.append(exception.getAttribute("nextTask"))
        datum.append("dummy1")
        datum.append("dummy2")
        self.data.append(datum)

        #    self.__lfh.write("+taskReference.parseException : data object (warning=<%40s> , select=<%15s>, nextTask = <%5s>\n" % (datum[0],datum[1],datum[2]));

    def parseLoopTask(self, loop):

        # for "value" in "iterator"
        self.type = "Loop"
        # no paramter - return value of list item,index : return index order of parameter ! ahhhh
        self.param = loop.getAttribute("parameter")
        # set the interator as the input to the loop
        datum = []
        datum.append(loop.getAttribute("iterator"))
        datum.append("input")
        self.data.append(datum)
        # set the value as the output to the loop
        datum = []
        datum.append(loop.getAttribute("value"))
        datum.append("output")
        self.data.append(datum)
        # there are 2 output tasks - the first is the loop next task
        # the second is the loop exit task
        self.outputName.append(loop.getAttribute("exitTask"))

    def parseAutoDecisionTask(self, decision):

        #   lookup = {"gte":">=","gt":">","lte":"<=","lt":"<","eq":"==","neq":"!=", "less":"<"}

        self.type = "Decision"
        self.file = decision.getAttribute("application")
        for info in decision.childNodes:
            if info.nodeName == "wf:dataObjectsLocation":
                for location in info.childNodes:
                    datum = []
                    if location.nodeName == "wf:location":
                        datum.append(str(location.getAttribute("dataID")))
                        datum.append(str(location.getAttribute("type")))
                        self.data.append(datum)
            elif info.nodeName == "wf:nextTasks":
                for output in info.childNodes:
                    if output.nodeName == "wf:nextTask":
                        self.outputName.append(output.getAttribute("taskID"))
                        for method in output.childNodes:
                            if method.nodeName == "wf:function":
                                #
                                compareAs = str(method.getAttribute("compareAs")).lower()
                                if compareAs not in ["int", "integer", "float", "double", "bool", "boolean", "string", "substring"]:
                                    # if omitted then apply a reasonable default  -
                                    if (method.getAttribute("string") != "") or (method.getAttribute("inList") != ""):
                                        compareAs = "string"
                                    else:
                                        compareAs = "integer"
                                f = TaskComparitor(self.debug, self.__lfh)
                                f.addDataName(method.getAttribute("dataID"))
                                if method.getAttribute("gte") != "":
                                    f.addData(-1, method.getAttribute("gte"), ">=", compareAs)
                                if method.getAttribute("gt") != "":
                                    f.addData(-1, method.getAttribute("gt"), ">", compareAs)
                                if method.getAttribute("lte") != "":
                                    f.addData(1, method.getAttribute("lte"), "<=", compareAs)
                                if method.getAttribute("less") != "":
                                    f.addData(1, method.getAttribute("less"), "<", compareAs)
                                if method.getAttribute("lt") != "":
                                    f.addData(1, method.getAttribute("lt"), "<", compareAs)
                                if method.getAttribute("eq") != "":
                                    f.addData(1, method.getAttribute("eq"), "==", compareAs)
                                if method.getAttribute("neq") != "":
                                    f.addData(1, method.getAttribute("neq"), "!=", compareAs)

                                if method.getAttribute("boolean") != "":
                                    f.addData(88, method.getAttribute("boolean"), compareAs="boolean")

                                if method.getAttribute("string") != "" and compareAs in ["string"]:
                                    f.addData(77, method.getAttribute("string"), compareAs=compareAs)
                                elif method.getAttribute("string") != "" and compareAs in ["substring"]:
                                    f.addData(78, method.getAttribute("string"), compareAs=compareAs)

                                elif method.getAttribute("inList") != "" and compareAs in ["string"]:
                                    f.addData(55, method.getAttribute("inList"), compareAs=compareAs)
                                elif method.getAttribute("inList") != "" and compareAs in ["substring"]:
                                    f.addData(56, method.getAttribute("inList"), compareAs=compareAs)
                        self.func.append(f)

    def parseProcessTask(self, process):

        self.type = "Process"
        temp = process.getAttribute("runTime")
        self.runTime = int(parseTimeDelta(temp).total_seconds())
        temp = process.getAttribute("failTime")
        self.failTime = int(parseTimeDelta(temp).total_seconds())

        for info in process.childNodes:
            if info.nodeName == "wf:detail":
                self.uniqueName = info.getAttribute("name")
                self.uniqueAction = info.getAttribute("action")
                if self.uniqueActionName is None or len(self.uniqueActionName) < 1:
                    self.uniqueActionName = self.uniqueAction
                self.parameter = info.getAttribute("parameter")
                self.uniqueWhere = info.getAttribute("where")
                if self.uniqueAction is not None:
                    if self.uniqueWhere == "api":
                        if not self.ActionRegistry.isDefinedAction(self.uniqueAction):
                            self.__lfh.write("+taskReference.parseException : **** Catastrophic WF error\n")
                            self.__lfh.write(
                                "+taskReference.parseProcessTask : Task refers to a APIprocess that does not exist : "
                                + str(self.uniqueAction)
                                + ", "
                                + str(self.uniqueWhere)
                                + "\n"
                            )
                            exit(0)
            #        self.uniqueContainer = info.getAttribute("returnContainer")
            #        self.uniqueType = info.getAttribute("returnType")
            elif info.nodeName == "wf:dataObjectsLocation":
                for data in info.childNodes:
                    datum = []
                    if data.nodeName == "wf:location":
                        datum.append(data.getAttribute("dataID"))
                        datum.append(data.getAttribute("type"))
                        self.data.append(datum)

    def parseManualTask(self, manual):

        self.type = "Manual"
        self.file = manual.getAttribute("application")
        for info in manual.childNodes:
            if info.nodeName == "wf:parameter":
                #        self.paramName = detail.getAttribute("name")
                n = 0
                self.param = TaskParameter()
                for write in info.childNodes:
                    if write.nodeName == "wf:write":
                        self.param.addTitle(write.getAttribute("title"))
                        self.param.addQuestion(write.getAttribute("question"))
                        for detail in write.childNodes:
                            if detail.nodeName == "wf:comment":
                                self.param.addComment(detail.firstChild.data)
                            elif detail.nodeName == "wf:objects":
                                for ob in detail.childNodes:
                                    if ob.nodeName == "wf:object":
                                        self.param.addObject(ob.getAttribute("ID"))
                                        self.param.addFormat(ob.getAttribute("format"))
            elif info.nodeName == "wf:nextTasks":
                for data in info.childNodes:
                    if data.nodeName == "wf:nextTask":
                        self.outputName.append(data.getAttribute("taskID"))
                        self.param.addOption(n, data.getAttribute("label"))
                        n = n + 1
            elif info.nodeName == "wf:dataObjectsLocation":
                for data in info.childNodes:
                    datum = []
                    if data.nodeName == "wf:location":
                        datum.append(data.getAttribute("dataID"))
                        datum.append(data.getAttribute("type"))
                        self.data.append(datum)

    def failTime(self):  # pylint: disable=method-hidden
        return self.failTime

    def runTime(self):  # pylint: disable=method-hidden
        return self.runTime

    def printName(self):
        """Convienence method to print the name of a task"""

        self.__lfh.write("+taskReference.printName : " + str(self.name) + "\n")
        return

    def printMe(self):
        """Convienence method to print things"""
        self.dump(self.__lfh)

    def dump(self, lfh):
        lfh.write("+taskReference.dump : Task type               %s\n" % self.type)
        lfh.write("+taskReference.dump : Task ID                 %s\n" % self.name)
        lfh.write("+taskReference.dump : Task name               %s\n" % self.nameHumanReadable)
        lfh.write("+taskReference.dump : Task breakpoint         %r\n" % self.breakPoint)
        lfh.write("+taskReference.dump : Task exception          %r\n" % self.exception)
        lfh.write("+taskReference.dump : Task file               %r\n" % self.file)
        lfh.write("+taskReference.dump : Task description        %s\n" % self.description)
        lfh.write("+taskReference.dump : Task unique name        %s\n" % self.uniqueName)
        lfh.write("+taskReference.dump : Task unique type        %s\n" % self.uniqueType)
        lfh.write("+taskReference.dump : Task unique where       %s\n" % self.uniqueWhere)
        lfh.write("+taskReference.dump : Task unique action      %s\n" % self.uniqueAction)
        lfh.write("+taskReference.dump : Task unique action name %s\n" % self.uniqueActionName)
        lfh.write("+taskReference.dump : Task output task names  %r\n" % self.outputName)

    def getDataReference(self, dataObjects):
        """Return the list of data objects from the input list related to the current task."""

        dat = []

        if self.data:
            for taskData in self.data:
                for dataRef in dataObjects:
                    if dataRef.isThisName(taskData[0]):
                        dataRef.localMode = taskData[1]
                        dat.append(dataRef)

        return dat

    def getName(self):
        return self.name

    def getFunc(self):
        return self.func

    def getNextTaskName(self, option=0):
        """Get the next task in the list"""

        whichOutput = 0
        for nextTask in self.outputName:
            if whichOutput == option:
                if self.debug > 0:
                    self.__lfh.write("+taskReference.getNextTaskName : next task " + str(nextTask) + " option " + str(option))
                return nextTask

            whichOutput = whichOutput + 1

        self.__lfh.write("+taskReference.getNextTaskName : Error : failed to find the next task by name\n")
        return None
