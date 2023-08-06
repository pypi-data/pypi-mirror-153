##
# File:  WFEngineRunner.py
# Date:  13-Feb-2015  J.Westbrook
# Updates:
#
###
##
"""
Launch and restart workflow engine process.

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
import logging

from wwpdb.apps.wf_engine.engine.mainEngine import mainEngine
from wwpdb.utils.detach.DetachedProcessBase import DetachedProcessBase


logger = logging.getLogger(name="root")


class WFEngineRunner(DetachedProcessBase):
    """Launch and restart workflow engine process."""

    def __init__(self, pidFile="WFEngineRunner.pid", debugLevel=1, wfXmlPath=".", stdin=os.devnull, stdout=os.devnull, stderr=os.devnull, wrkDir="."):

        super(WFEngineRunner, self).__init__(pidFile=pidFile, stdin=stdin, stdout=stdout, stderr=stderr, wrkDir=wrkDir)

        self.__debugLevel = debugLevel
        self.__pidFile = pidFile
        self.__wfXmlPath = wfXmlPath

    def run(self):
        """Start a new workflow engine process  -"""
        logger.info("+WFEngingeRunner.run() Start workflow engine  with %s\n", self.__pidFile)

        engine = mainEngine(self.__debugLevel, sys.stderr)
        normal = ["WFRunner", "-x", "-k", "WF", "-t", "entry-point", "-s", "monitor", "-w", "MonitorDB.xml", "-p", self.__wfXmlPath]
        engine.runNoThrow(normal)

        logger.info("+WFEngineRunner.run() Leaving with %s\n", self.__pidFile)
        return True

    def setDebugLevel(self, level=0):
        self.__debugLevel = level


if __name__ == "__main__":
    wfr = WFEngineRunner()
    wfr.run()
