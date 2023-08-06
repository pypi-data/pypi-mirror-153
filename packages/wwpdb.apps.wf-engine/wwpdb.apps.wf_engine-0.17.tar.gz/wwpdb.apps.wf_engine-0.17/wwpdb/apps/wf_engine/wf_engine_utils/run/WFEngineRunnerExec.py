#!/usr/bin/env python
##
# File: WFEngineRunnerExec.py
# Date: 12-Feb-2015
#
# Updates:
#   5-Feb-2016 jdw provide host specific stdout/stderr logs --
#   4-Mar-2016 jdw add a more restrictive file permissions mask
##
"""
Set up execution envirnoment for workflow engine -

"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.001"

import sys
import os
import time
import logging

from optparse import OptionParser  # pylint: disable=deprecated-module
from wwpdb.apps.wf_engine.wf_engine_utils.run.WFEngineRunner import WFEngineRunner

import platform

from wwpdb.utils.config.ConfigInfo import ConfigInfo, getSiteId


def main():
    # adding a conservative permission mask for this
    os.umask(0o022)
    #
    siteId = getSiteId(defaultSiteId="WWPDB_DEPLOY_TEST")
    cI = ConfigInfo(siteId)

    #    topPath = cI.get('SITE_WEB_APPS_TOP_PATH')
    topSessionPath = cI.get("SITE_WEB_APPS_TOP_SESSIONS_PATH")
    wfXmlPath = cI.get("SITE_WF_XML_PATH")
    #
    myFullHostName = platform.uname()[1]
    myHostName = str(myFullHostName.split(".")[0]).lower()
    #

    wfLogDirPath = os.path.join(topSessionPath, "wf-logs")
    if not os.path.exists(wfLogDirPath):
        os.makedirs(wfLogDirPath)
    pidFilePath = os.path.join(wfLogDirPath, myHostName + ".pid")
    #
    stdoutFilepath = os.path.join(wfLogDirPath, myHostName + "-stdout.log")
    stderrFilepath = os.path.join(wfLogDirPath, myHostName + "-stderr.log")
    #
    #  Setup logging  --
    now = time.strftime("-%Y-%m-%d", time.localtime())
    wfLogFilePath = os.path.join(wfLogDirPath, myHostName + now + ".log")
    logger = logging.getLogger(name="root")
    logging.captureWarnings(True)
    #
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s - %(message)s")
    handler = logging.FileHandler(wfLogFilePath)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    #

    usage = "usage: %prog [options]"
    parser = OptionParser(usage)
    parser.add_option("--start", default=False, action="store_true", dest="startOp", help="Start workflow engine process")
    parser.add_option("--stop", default=False, action="store_true", dest="stopOp", help="Stop workflow process")
    parser.add_option("--restart", default=False, action="store_true", dest="restartOp", help="Restart workflow engine process")
    parser.add_option("--status", default=False, action="store_true", dest="statusOp", help="Report workflow enging process status")

    parser.add_option("-v", "--verbose", default=False, action="store_true", dest="verbose", help="Enable verbose output")
    parser.add_option("--debug", default=1, type="int", dest="debugLevel", help="Debug level [0-4]")
    parser.add_option("--xmlpath", default=None, dest="wfXmlPath", help="Workflow XML definition file path")

    (options, _args) = parser.parse_args()
    lt = time.strftime("%Y %m %d %H:%M:%S", time.localtime())
    #
    if options.debugLevel > 2:
        logger.setLevel(logging.DEBUG)
    elif options.debugLevel > 0:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.ERROR)
    if options.wfXmlPath is not None:
        wfXmlPath = os.path.abspath(options.wfXmlPath)

    wfr = WFEngineRunner(pidFile=pidFilePath, wfXmlPath=wfXmlPath, debugLevel=options.debugLevel, stdout=stdoutFilepath, stderr=stderrFilepath, wrkDir=wfLogDirPath)

    if options.startOp:
        sys.stdout.write("+WFEngineRunnerExec(main) starting workflow engine at %s\n" % lt)
        logger.info("+WFEngineRunnerExec(main) starting workflow engine at %s\n", lt)
        wfr.setDebugLevel(level=options.debugLevel)
        wfr.start()
    elif options.stopOp:
        sys.stdout.write("+WFEngineRunnerExec(main) stopping workflow engine at %s\n" % lt)
        logger.info("+WFEngineRunnerExec(main) starting workflow engine at %s\n", lt)
        wfr.stop()
    elif options.restartOp:
        sys.stdout.write("+WFEngineRunnerExec(main) restarting workflow engine at %s\n" % lt)
        wfr.setDebugLevel(level=options.debugLevel)
        wfr.restart()
    elif options.statusOp:
        sys.stdout.write("+WFEngineRunnerExec(main) reporting workflow engine status at %s\n" % lt)
        sys.stdout.write(wfr.status())
    else:
        pass


if __name__ == "__main__":
    main()
