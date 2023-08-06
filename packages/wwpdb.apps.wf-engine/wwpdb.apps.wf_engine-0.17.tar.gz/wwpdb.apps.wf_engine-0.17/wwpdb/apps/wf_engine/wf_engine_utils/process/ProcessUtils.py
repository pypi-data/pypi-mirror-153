##
# File: ProcessUtils.py
# Date: 14-Feb-2015  J. Westbrook --
#
# Update:
# 12-Mar-2015 jdw add process search method ()
# 12-Mar-2015 jdw return parent process id in search method
#
##

__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Creative Commons Attribution 3.0 Unported"
__version__ = "V0.01"

import os
import psutil
import signal
import traceback


class ProcessUtils(object):
    """
    A collection of utilities for managing processes and extracting
    process and system status details.

    """

    def __init__(self, verbose, log):  # pylint: disable=unused-argument
        # self.__verbose = verbose
        self.__lfh = log
        self.__debug = False

    def setDebug(self, flag=True):
        self.__debug = flag

    def __compare(self, value, target, op="str_in"):
        """
        Compare value with target according to input operation.

        This is tailored to data types returned from process status queries.

        Return True if the comparison is satisfied
        """
        opList = ["str_in", "str_eq", "numb_eq", "numb_gt", "numb_lt"]
        if op not in opList:
            return False
        if target is None:
            return False
        if op in ["str_in"]:
            if isinstance(target, list):
                ok = value in " ".join(target)
            elif isinstance(target, str):
                ok = value in target
        elif op in ["str_eq"]:
            if isinstance(target, list):
                ok = value in target
            elif isinstance(target, str):
                ok = value == target
        elif op in ["numb_gt"]:
            ok = value < target
        elif op in ["numb_lt"]:
            ok = value > target
        elif op in ["numb_eq"]:
            ok = value == target
        else:
            ok = False
        return ok

    def findProcesses(self, key, value, op="str_in"):
        """Return the list of process & parent ids in which input value is found with the process target key -
        Queries are performed on the current process list.  Comparisons/selections performed with
        self.__compare() according the operation selection.
        """
        # valid list of process status  - keys -
        keyList = [
            "username",
            "num_ctx_switches",
            "pid",
            "connections",
            "cmdline",
            "create_time",
            "memory_info_ex",
            "num_fds",
            "memory_maps",
            "cpu_percent",
            "terminal",
            "ppid",
            "cwd",
            "nice",
            "status",
            "cpu_times",
            "memory_info",
            "threads",
            "open_files",
            "name",
            "num_threads",
            "exe",
            "uids",
            "gids",
            "memory_percent",
        ]
        pidList = []
        if key not in keyList:
            return pidList
        for p in psutil.process_iter():
            try:
                # jdw  - It is observed that processes may processes may not be available to
                #        to this call so trap this exception so that the iterator can continue.
                try:
                    pD = p.as_dict()
                except:  # noqa: E722 pylint: disable=bare-except
                    pass
                if key in pD:
                    # if self.__debug:
                    #    self.__lfh.write("+ProcessUtils.findProcess() testing for key %r  search target %r process return value %r\n" % (key, value, pD[key]))
                    if pD[key] is None:
                        continue
                    ok = self.__compare(value, pD[key], op=op)
                    if ok:
                        pidList.append((pD["pid"], pD["ppid"]))
                        if self.__debug:
                            self.__lfh.write("+ProcessUtils.findProcess() matched key %r value %r\n" % (key, pD[key]))
            except:  # noqa: E722 pylint: disable=bare-except
                if self.__debug:
                    self.__lfh.write("+ProcessUtils.findProcess() exception for key %r target %r\n" % (key, value))
                    traceback.print_exc(file=self.__lfh)
        if self.__debug:
            self.__lfh.write("+ProcessUtils.findProcess() key %r target %r search returns length %d\n" % (key, value, len(pidList)))
        return pidList

    def killProcessList(self, pidList, mySignal=signal.SIGKILL):
        try:
            for pid in pidList:
                os.kill(pid, mySignal)

                try:
                    os.waitpid(pid, 0)
                    self.__lfh.write("+ProcessUtils.killProcessList() process %s cleaned from process table\n" % (str(pid)))
                except OSError as e:
                    self.__lfh.write("+ProcessUtils.killProcessList() error waiting for pid (%s), error %s\n" % (str(pid), e))
            return True
        except Exception as e:
            self.__lfh.write("+ProcessUtils.killProcessList() failing with (%s)\n" % (str(e)))
        return False

    def getChildren(self, pid):
        """Return the list of process id's for the children of the input process id."""
        cL = []
        try:
            p = psutil.Process(pid)
            cPidList = p.children(recursive=True)
            for cPid in cPidList:
                iPid = int(str(cPid.pid))
                if iPid != pid:
                    cL.append(iPid)
        except Exception as e:
            self.__lfh.write("+ProcessUtils.getPidChildren() failing with (%s)\n" % (str(e)))

        return cL

    def getMemoryInfo(self):
        """
        From the  psutil class documentation -

        virtual_memory() returns statistics about system memory usage as a namedtuple including the following fields, expressed in bytes:

        total: total physical memory available.
        available: the actual amount of available memory that can be given instantly to processes that request more memory in bytes; this
        is calculated by summing different memory values depending on the platform (e.g. free + buffers + cached on Linux) and it is supposed
         to be used to monitor actual memory usage in a cross platform fashion.
        percent: the percentage usage calculated as (total - available) / total * 100.
        used: memory used, calculated differently depending on the platform and designed for informational purposes only.
        free: memory not being used at all (zeroed) that is readily available; note that this does not reflect the actual memory
                   available (use available instead).
        Platform-specific fields:

        active: (UNIX): memory currently in use or very recently used, and so it is in RAM.
        inactive: (UNIX): memory that is marked as not used.
        buffers: (Linux, BSD): cache for things like file system metadata.
        cached: (Linux, BSD): cache for various things.
        wired: (BSD, OSX): memory that is marked to always stay in RAM. It is never moved to disk.
        shared: (BSD): memory that may be simultaneously accessed by multiple processes.

        swap_memory() returns system swap memory statistics as a namedtuple including  the following fields:

            total: total swap memory in bytes
            used: used swap memory in bytes
            free: free swap memory in bytes
            percent: the percentage usage
            sin: the number of bytes the system has swapped in from disk (cumulative)
            sout: the number of bytes the system has swapped out from disk (cumulative)
        """
        d = {}
        d = {"MemTotal": 0, "SwapTotal": 0, "TotalFree": 0, "SwapFree": 0, "TotalUsed": 0, "Cached": 0, "MemFree": 0, "Buffers": 0, "TotalTotal": 0, "MemUsed": 0, "SwapUsed": 0}
        try:
            vM = psutil.virtual_memory()._asdict()
            sM = psutil.swap_memory()._asdict()
            #
            d["MemTotal"] = int(vM["total"] / 1000)
            d["MemUsed"] = int(vM["used"] / 1000)
            d["MemFree"] = int(vM["available"] / 1000)
            if "buffers" in vM:
                d["Buffers"] = int(vM["buffers"])
            #
            if "cached" in vM:
                d["Cached"] = int(vM["cached"])
            #
            d["SwapTotal"] = int(sM["total"] / 1000)
            d["SwapUsed"] = int(sM["used"] / 1000)
            d["SwapFree"] = int(sM["free"] / 1000)
            #
            d["TotalUsed"] = d["MemUsed"] + d["SwapUsed"]
            d["TotalFree"] = d["MemFree"] + d["SwapFree"]
            d["TotalTotal"] = d["MemTotal"] + d["SwapTotal"]

        except Exception as e:
            self.__lfh.write("+ProcessUtils.getMemoryInfo() failing with (%s)\n" % (str(e)))
            traceback.print_exc(file=self.__lfh)
        return d

    def getCpuInfo(self, waitSeconds=1.0):
        """Return the number of cores and aggregate fractional usage during the input
        interval (waitSeconds).

        """
        d = {}
        d["Ncpu"] = 1
        d["Usage"] = 0.001
        try:
            # total number of cores --
            d["Ncpu"] = psutil.cpu_count(logical=True)
            # aggregate fractional usage -
            d["Usage"] = float(psutil.cpu_percent(interval=waitSeconds)) / 100.0
        except Exception as e:
            self.__lfh.write("+ProcessUtils.getCpuInfo failing with (%s)\n" % (str(e)))
            traceback.print_exc(file=self.__lfh)

        return d
