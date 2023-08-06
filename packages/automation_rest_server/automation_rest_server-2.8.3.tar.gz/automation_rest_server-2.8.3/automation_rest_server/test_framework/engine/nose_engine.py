import os
from utils import log
import time
import subprocess
from test_framework.state import State


class NoseEngine(object):

    def __init__(self):
        self.working_path = os.environ["working_path"]
        self.log_path = self.get_log_path()

    def get_log_path(self):
        log_path = os.path.join(self.working_path, "log")
        if os.path.exists(log_path) is False:
            os.mkdir(log_path)
        return log_path

    @staticmethod
    def get_msg(out, err):
        msg = str()
        if err is not None:
            msg += err.decode('utf-8')
        if out is not None:
            msg += out.decode('utf-8')
        return msg

    def save_msg(self, msg, test_case):
        test_function = test_case.split(".")
        log_file = "{}_{}.log".format(test_function[-1],time.time())
        log_path = os.path.join(self.log_path, log_file)
        with open(log_path, "w") as file_:
            file_.write(msg)
        return log_path

    def command_run_test(self, test_case, test_path):
        test_function = test_case.split(".")
        xml_name = "nosetests_%s_%s.xml" % (test_function[-1], time.time())
        xml_path = os.path.join(self.log_path, xml_name)
        command_line = "nosetests --exe --nocapture --with-printlog --with-xunit --xunit-file={} -x {}"\
            .format(xml_path, test_path)
        child1 = subprocess.Popen(command_line, shell=True)
        return_code = child1.wait()
        ret = True if return_code == 0 else False
        return ret, xml_path

    def run(self, test_case, test_path, parameters, queue):
        ret,  xml_path = self.command_run_test(test_case, test_path)
        if ret is True:
            log.INFO("TestCase run succeed.%s", test_case)
            result = State.PASS
        else:
            log.ERR("TestCase run failed. %s", test_case)
            result = State.FAIL
        result = {"name":test_case, "result": result, "log":xml_path, "xml_path": xml_path}
        queue.put(result)
        return ret
