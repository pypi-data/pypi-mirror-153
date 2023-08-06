#!/usr/bin/env python
"""
FIO operation

@author: yyang
"""
import os
import stat
import platform
import subprocess
from collections import OrderedDict
from multiprocessing import cpu_count
from threading import Thread
from utils.system import execute


WORKING_PATH = os.getcwd()
STATE_755 = stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH
FIO_LINUX_PATH = os.path.join(os.path.dirname(__file__), "tool", "fio")
FIO_WINDOWS_PATH = r"C:\Program Files\fio\fio.exe"


class Fio(object):
    def __init__(self):
        system = platform.system()
        if system == "Linux":
            if not os.path.exists(FIO_LINUX_PATH):
                raise RuntimeError("FIO is non-existent: '{}'".format(FIO_LINUX_PATH))
            self.fio = FIO_LINUX_PATH
            if not os.access(self.fio, os.X_OK):
                os.chmod(self.fio, STATE_755)
            self.__fio_dos2_unit()
            self.__init_aio_max_nr()
            self.__init_scaling_governor()
        elif system == "Windows":
            if not os.path.exists(FIO_WINDOWS_PATH):
                raise RuntimeError("FIO is non-existent: '{}'".format(FIO_WINDOWS_PATH))
            self.fio = "fio"
        else:
            raise RuntimeError("Unknown OS: '{}'".format(system))
        self.thread = None
        self.args = list()
        self.parm = OrderedDict()

    @staticmethod
    def __init_scaling_governor():
        for i in range(cpu_count()):
            scaling_governor = "/sys/devices/system/cpu/cpu{}/cpufreq/scaling_governor".format(i)
            execute("echo performance > {}".format(scaling_governor),
                    cmdline=False, console=False, interrupt=False)

    @staticmethod
    def __init_aio_max_nr(default=1048576):
        cmd = "cat /proc/sys/fs/aio-max-nr"
        _, output = execute(cmd, cmdline=False, console=False, interrupt=True)
        if int(output) < default:
            cmd = "echo > /proc/sys/fs/aio-max-nr {}".format(default)
            execute(cmd, cmdline=False, console=False, interrupt=True)

    @staticmethod
    def __fio_dos2_unit():
        fio_path = os.path.join(os.path.dirname(__file__), "tool")
        cmd = "cd {} && dos2unix *".format(fio_path)
        execute(cmd, cmdline=False)

    def parse_cmd(self, jobfile=None, section=None, **kwargs):
        args = [self.fio]

        self.parm.update(kwargs)
        for key, val in self.parm.items():
            if val in [None, False]:
                pass
            elif val is True:
                args.append("--{}".format(key))
            else:
                args.append("--{}={}".format(key, val))
                if key == "runtime":
                    args.append("--time_based")

        args += self.args

        if jobfile:
            args.append(jobfile)
            if section:
                args.append("--section={}".format(section))

        return " ".join(args)

    def set_parm(self, key, value=None):
        """
        (key, True)         --> --key
        (key, None/False)   --> ignore
        (key, string)       --> --key=string
        """
        self.parm[key] = value

    def clear_parm(self):
        self.parm.clear()

    def import_dict(self, **kwargs):
        self.parm.update(kwargs)

    def import_list(self, *args):
        self.args += args

    def start(self, jobfile=None, section=None, cmdline=True, interrupt=True, outfile=None,
              **kwargs):
        if outfile:
            self.set_parm("output", outfile)

        cmd = self.parse_cmd(jobfile, section, **kwargs)

        if cmdline:
            print("# {}".format(cmd))

        status = subprocess.call(cmd, shell=True)
        print("")

        if status and interrupt:
            raise RuntimeError("Run FIO failed!")

        output = open(outfile).read() if outfile else ""

        return status, output

    def __start(self, jobfile=None, section=None, cmdline=True, outfile=None, args=None):
        if outfile:
            self.set_parm("output", outfile)

        args = args if args else {}
        cmd = self.parse_cmd(jobfile, section, **args)

        status, output = execute(cmd, cmdline, console=False, interrupt=False)

        return status, output

    def run(self, jobfile=None, section=None, cmdline=True, outfile=None, **kwargs):
        self.thread = Thread(target=self.__start,
                              args=(jobfile, section, cmdline, outfile, kwargs))
        self.thread.setDaemon(True)
        self.thread.start()

    def join(self):
        if self.thread:
            self.thread.join()
        else:
            raise RuntimeError("Fio thread is not set!")

    def get_result(self):
        if self.thread:
            status, output = self.thread.get_result()
            self.thread = None
        else:
            raise RuntimeError("FIO thread is not set!")

        return status, output
