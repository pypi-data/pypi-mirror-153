##
# File:    CommandLineArgs.py
# Date:    15-Mar-2009
#
# Updates:
#  22-April-2010 : Incorporation into enterpise.
#
#  2-May-2015   jdw jdw remove -gui/interface arg.
#               jdw refacotor
##

"""
Interpret the run time parameters of the WFE
"""

__docformat__ = "restructuredtext en"
__author__ = "Tom Oldfield"
__email__ = "oldfield@ebi.ac.uk"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.24"

import sys
import getopt


class CommandLineArgs(object):

    """
    run time parameter class
    """

    def __init__(self, argv):
        self.workflow = "Workflow-initial-V2.xml"
        self.path = "./"
        self.sessionID = ""
        self.initTask = "entry-point"
        self.debug = 1
        self.processState = "PROC"
        self.instanceID = None
        self.accession = "1UIS"
        self.log = None
        self.wfDepth = 0  # which WF file name to get back from a nested name

        try:
            opts, _args = getopt.getopt(
                argv[1:],
                "hd:l:s:t:i:w:p:a:k:z:xr",
                ["help", "debug=", "log=", "session=", "task=", "instance=", "workflow=", "path=", "processState=", "accession=", "depth=", "xample", "recover"],
            )
        except getopt.GetoptError:
            # print help information and exit:
            self.usage()
            return None

        for opt, arg in opts:
            #      print  " opt " + opt + " : arg " + arg
            if opt in ("-h", "--help"):
                self.usage()
                return None
            elif opt in ("-d", "--debug"):
                self.debug = int(arg)
            elif opt in ("-l", "--log"):
                self.log = arg
            elif opt in ("-t", "--task"):
                self.initTask = arg
            elif opt in ("-i", "--instance"):
                self.instanceID = arg
            elif opt in ("-s", "--session"):
                self.sessionID = arg
            elif opt in ("-p", "--path"):
                self.path = arg
            elif opt in ("-w", "--workflow"):
                self.workflow = arg
            elif opt in ("-a", "--accession"):
                self.accession = arg
            elif opt in ("-k", "--processState"):
                self.processState = arg
            elif opt in ("-z", "--depth"):
                self.wfDepth = int(arg)
            elif opt in ("-r", "--recover"):
                self.processState = arg

    def getDebug(self):
        return self.debug

    def getSessionID(self):
        return self.sessionID

    def getProcessState(self):
        return self.processState

    def getPath(self):
        return self.path

    def getWFdepth(self):
        return self.wfDepth

    def getWorkFlowFileName(self):
        """
        -w annotation(sequenceModule)
        -w one(two(three(four)))
        """

        anyB = self.workflow.find("(")

        if anyB < 0 and self.wfDepth > 0:
            # systax error in wf request
            print("Request for workflow of depth " + str(self.wfDepth) + " that is invalid in " + self.workflow + " : zero level error")
            sys.exit(0)

        if anyB < 0:
            return self.workflow
        else:
            start = 0
            for i in range(0, self.wfDepth + 1):
                b1 = self.workflow.find("(", start)
                if b1 < 0:
                    print("Request for workflow of depth " + str(self.wfDepth) + " that is invalid in " + self.workflow + " : " + str(i) + " level error")
                    exit(0)
                if i == self.wfDepth:
                    return self.workflow[start:b1]
                start = b1 + 1

        return self.workflow

    def getInitTask(self):
        return self.initTask

    def usage(self):

        print("Usage of the engine")
        print("python mainEngine.py -s <session name> [-i <Task>] [-d 1]")
        print("-s  : Session name or deposition ID : required to run engine on domain data")
        print("-w  : workflow File name : no default")
        print("-p  : path for XML workflows : default = ./")
        print("-i  : instance ID")
        print("-g  : interface console (default - interface is external)")
        print("-t  : start workflow at this task")
        print("-d  : debug level 0/1/2/3 (default = 0)")
        print("-l  : log output file")
        print("-a  : accession code only for  -x")
        print("-x  : Insert dummy dep_id and class_id into DB")
        print("-r  : automatically recover instance from last working task")
        print("-k  : set domain data processState - only valid with -x")
        print("-z  : set the WFdepth (default = 0)")
