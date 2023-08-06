
import re
import os
import time
from test_framework.state import State
from utils import log


class SSERebootEngine(object):

    def __init__(self):
        self.working_path = os.environ["working_path"]
        self.logs_path = os.path.join(self.working_path, "logs")

    def run(self, test_case):
        log.INFO("SSERebootEngine begin to run")
        result = dict()
        while True:
            ret = self.check_result(test_case)
            if ret == State.RUNNING:
                time.sleep(10)
                continue
            else:
                test_logs = self.get_test_log(test_case)
                result = {"name": test_case, "result": ret, "log": test_logs}
                break
        log.INFO("SSERebootEngine End")
        print(result)
        return result

    def get_test_log(self, test):
        log.INFO("get_test_log:{}".format(test))
        rets = re.findall("([^/]+).py", test)
        log_list = list()
        if rets:
            logs_list = self.get_logs_list()
            test_name = rets[0]
            log.INFO("test name:{}".format(test_name))
            for item in logs_list:
                log.INFO("check log:{}".format(item))
                log_file = os.path.join(self.logs_path, item)
                if test_name in item and os.path.isfile(log_file):
                    log_list.append(log_file)
                    log.INFO("Find test log: {}".format(item))
                    break
        return log_list

    def get_logs_list(self):
        dir_list = os.listdir(self.logs_path)
        if dir_list:
            dir_list = sorted(dir_list, key=lambda x: os.path.getmtime(os.path.join(self.logs_path, x)), reverse=True)
        log.INFO(dir_list)
        return dir_list

    def check_result(self, test):
        ret = State.RUNNING
        state_file = os.path.join(self.working_path, "neuron_status.txt")
        with open(state_file, 'r',  encoding='utf-8') as f:
            for line in f.readlines():
                if test in line:
                    rets = line.split(",")
                    status = rets[2].strip()
                    log.INFO("SSE REBOOT: TEST: {}, RESULT:{}".format(test, status))
                    if "Pass" in status:
                        ret = State.PASS
                    elif "Fail" in status:
                        ret = State.FAIL
        return ret
