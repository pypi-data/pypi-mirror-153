import os
from utils import log
import time
import subprocess
from test_framework.state import State
from test_framework.engine.perses_engine import PersesEngine
from utils import log


class PersesPowerEngine(PersesEngine):

    def __init__(self):
        super(PersesPowerEngine, self).__init__()

    def run_test(self, test_case, parameters):
        para_str = self.convert_para_2_string(parameters)
        if para_str == "":
            command_line = "python run.py powercycle -n {}".format(test_case)
        else:
            command_line = "python run.py powercycle -n {} -v {}".format(test_case, para_str)
        log.INFO("PersesPowerEngine run command: {}".format(command_line))
        child1 = subprocess.Popen(command_line, shell=True)
        return_code = child1.wait()
        return return_code
