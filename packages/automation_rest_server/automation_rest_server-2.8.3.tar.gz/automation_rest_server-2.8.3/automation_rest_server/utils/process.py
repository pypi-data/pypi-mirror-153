# coding=utf-8
# pylint: disable=dangerous-default-value
import re
import time
import platform
import subprocess
from multiprocessing import Process
from utils import log


class MyProcess(Process):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        super(MyProcess, self).__init__(group, target, name, args, kwargs)
        log.INFO("MyProcess init")

    def stop(self):
        print("MyProcess . stop")
        if "windows" in platform.system().lower():
            log.INFO("system is windows")
            ret = self._kill_process_windows()
        else:
            log.INFO("system is linux")
            self._kill_process_linux()
            ret = 0
        return ret

    def get_subproecess(self, parent_pid, pid_information):
        sub_pids = re.findall("\s+([0-9]+)\s+{}".format(parent_pid), pid_information.decode('utf-8'))
        if sub_pids:
            for pid_ in sub_pids:
                pids_ = self.get_subproecess(pid_, pid_information)
                for item in pids_:
                    if item not in sub_pids:
                        sub_pids.append(item)
        return sub_pids

    def _kill_process_linux(self):
        cmd = "ps -ef"
        child2 = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        out = child2.communicate()
        sub_process_ids = self.get_subproecess(self.pid, out[0])
        sub_process_ids.append(self.pid)
        log.INFO(sub_process_ids)
        for id_ in sub_process_ids:
            subprocess.call("kill {}".format(id_), shell=True)
            time.sleep(1)

    def _kill_process_windows(self):
        cmd = "taskkill  /F /T /PID {}".format(self.pid)
        ret = subprocess.call(cmd, shell=True)
        return ret
