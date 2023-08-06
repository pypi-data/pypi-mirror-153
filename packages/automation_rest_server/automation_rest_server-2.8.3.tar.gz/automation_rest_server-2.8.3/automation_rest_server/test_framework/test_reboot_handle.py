
import os
from test_framework.reboot_engine import SSERebootEngine
from test_framework.state import State
from utils import log


class RebootHandle(object):

    def __init__(self):
        self.results = list()
        self.working_path = os.environ["working_path"]
        self.engine = self.get_engine()

    def get_engine(self):
        if "neuron" in self.working_path:
            log.INFO("Get reboot engine: neuron")
            engine = SSERebootEngine()
        else:
            engine = None
        return engine

    def run(self, test_case, test_parameters):
        if self.engine is not None:
            result = self.engine.run(test_case)
        else:
            result = {"name": test_case, "result": State.ERROR_ABNORMAL_END, "log": "RebootHandle: ERROR_ABNORMAL_END"}
        self.results.append(result)
        return self.results


