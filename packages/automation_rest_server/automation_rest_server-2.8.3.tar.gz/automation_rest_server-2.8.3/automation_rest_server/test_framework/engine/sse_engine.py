import os
import re
import platform
from utils import log
import time
import subprocess
from test_framework.state import State
from test_framework.engine.special_parameter import Parameters


class SSEEngine(object):

    def __init__(self):
        self.working_path = os.environ["working_path"]
        self.logs_path = os.path.join(self.working_path, "logs")
        self.orig_log_folders = list()
        self.latest_log_folders = list()

    def get_orig_logs(self):
        self.orig_log_folders.clear()
        for item in os.listdir(self.logs_path):
            if os.path.isfile(os.path.join(self.logs_path, item)):
                self.orig_log_folders.append(item)

    @staticmethod
    def get_test_name(test_case):
        names = re.findall("([^/]*?).py", test_case)
        test_name = names[0] if names else ""
        return test_name

    def get_new_log(self, test_case):
        test_name = self.get_test_name(test_case)
        new_logs = list()
        for item in os.listdir(self.logs_path):
            if os.path.isfile(os.path.join(self.logs_path, item)):
                if (item not in self.orig_log_folders) and (test_name in item):
                    new_logs.append(os.path.join(self.logs_path, item))
        return new_logs

    @staticmethod
    def _get_python_interpreter():
        if 'Windows' == platform.system():
            interpreter = "py -3"
        else:
            interpreter = "python3"
        return interpreter

    @staticmethod
    def _convert_dict_2_str(parameters):
        str_para = ""
        for key, value in parameters.items():
            if str_para == "":
                str_para = "{}:{}".format(key, value)
            else:
                str_para = "{},{}:{}".format(str_para, key, value)
        return str_para

    def execute_test(self, test, parameters):
        cmd_line = "cd {}; {} neuron_cli.py --test {}".format(self.working_path, self._get_python_interpreter(), test)
        if bool(parameters):
            cmd_line = "{} --para {}".format(cmd_line, self._convert_dict_2_str(parameters))
        log.INFO("Test case command:{}".format(cmd_line))

        popen = subprocess.Popen(cmd_line, shell=True)   # stdout=subprocess.PIPE, stderr=subprocess.PIPE
        popen.communicate()
        ret_code = popen.returncode

        log.INFO("cmd return code: {}".format(ret_code))
        return ret_code

    @staticmethod
    def del_parameter(parameters):
        if "script" in parameters.keys():
            parameters.pop("script")
        if "key" in parameters.keys():
            parameters.pop("key")

    def check_result(self, test):
        ret = State.FAIL
        state_file = os.path.join(self.working_path, "neuron_status.txt")
        with open(state_file, 'r',  encoding='utf-8') as f:
            for line in f.readlines():
                if test in line:
                    rets = line.split(",")
                    status = rets[2].strip()
                    if "Pass" in status:
                        ret = State.PASS
        return ret

    def run(self, test_case, test_path, parameters, queue):
        log.INFO("see engine running")
        self.get_orig_logs()
        self.del_parameter(parameters)
        ret_code = self.execute_test(test_case, parameters)
        test_logs = self.get_new_log(test_case)
        test_result = self.check_result(test_case)
        result = {"name": test_case, "result": test_result, "log": test_logs}
        print(result)
        queue.put(result)
        return ret_code
