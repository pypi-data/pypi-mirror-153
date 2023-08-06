import os
from utils import log
import time
import subprocess
from test_framework.state import State
from test_framework.engine.special_parameter import Parameters


class PersesEngine(object):

    def __init__(self):
        self.working_path = os.environ["working_path"]
        self.log_path = self.get_log_path()
        self.orig_log_folders = list()
        self.latest_log_folders = list()
        self.parm = Parameters()

    def get_log_path(self):
        log_path = os.path.join(self.working_path, "log")
        if os.path.exists(log_path) is False:
            os.mkdir(log_path)
        return log_path

    def get_new_log(self, test_case):
        test_name = test_case.split('.')[-1]
        self.latest_log_folders = os.listdir(self.log_path)
        new_logs = list()
        for item in self.latest_log_folders:
            if item not in self.orig_log_folders:
                if os.path.isfile(os.path.join(self.log_path, item)):
                    if test_name in item:
                        new_logs.append(os.path.join(self.log_path, item))
        return new_logs

    def get_orig_logs(self):
        self.orig_log_folders = os.listdir(self.log_path)

    @staticmethod
    def convert_para_2_string(parameters):
        para_str = ""
        for key, value in parameters.items():
            temp = "{}:{}".format(key, value)
            if para_str == "":
                para_str = temp
            else:
                para_str = "{},{}".format(para_str, temp)
        return para_str

    def update_fw_path(self, parameters):
        parameters = self.parm.generate_perses_linux_fw_path(parameters)
        return parameters

    def run_test(self, test_case, parameters):
        parameters = self.update_fw_path(parameters)
        para_str = self.convert_para_2_string(parameters)
        if para_str == "":
            command_line = "python run.py testcase -n {}".format(test_case)
        else:
            command_line = "python run.py testcase -n {} -v {}".format(test_case, para_str)
        log.INFO("PersesEngine run command: {}".format(command_line))
        child1 = subprocess.Popen(command_line, shell=True)
        return_code = child1.wait()
        return return_code

    def run(self, test_case, test_path, parameters, queue):
        self.get_orig_logs()
        ret_code = self.run_test(test_case, parameters)
        logs = self.get_new_log(test_case)
        if ret_code == 0:
            test_result = State.PASS
        elif ret_code == 1:
            test_result = State.FAIL
        elif ret_code == 2:
            test_result = State.BLOCK
        elif ret_code == 3:
            test_result = State.ERROR_NOT_FOUND
        elif ret_code == 10:
            test_result = State.ERROR_UNHEALTHY
        elif ret_code == 99:
            test_result = State.ERROR_BASE_EXCEPTION
        else:
            test_result = State.BLOCK
        result = {"name": test_case, "result": test_result, "log": logs}
        print("testcase: {}".format(test_case), result)
        queue.put(result)
        return ret_code
