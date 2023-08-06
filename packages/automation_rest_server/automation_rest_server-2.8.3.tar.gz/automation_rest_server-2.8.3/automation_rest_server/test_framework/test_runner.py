# coding=utf-8
import time
import os
from multiprocessing import Queue
from utils import log
from utils.process import MyProcess
from test_framework.engine import PersesEngine, OakgateEngine, PersesPowerEngine, NoseEngine, SSEEngine
from utils.system import decorate_exception


class Runner(object):

    def __init__(self):
        self.results = list()
        self.process_run_ = None
        self.working_path = os.environ["working_path"]
        self.engine = self.get_engine()
        # self.log_path = self.get_log_path()

    def get_engine(self):
        if "test-platform" in self.working_path:
            engine = OakgateEngine()
        elif self.is_perses_power_cycle() is True:
            engine = PersesPowerEngine()
        elif "perses" in self.working_path:
            engine = PersesEngine()
        elif "neuron" in self.working_path:
            engine = SSEEngine()
        else:
            engine = NoseEngine()
        print("get engine", engine)
        return engine

    def get_results(self):
        return self.results

    def is_perses_power_cycle(self):
        result = False
        if ("perses_power_cycle" in os.environ.keys()) and ("perses" in self.working_path.lower()):
            result = True
        return result

    def stop(self):
        print("test runner . stop")
        if self.process_run_ is not None:
            ret = self.process_run_.stop()
        else:
            ret = -1
        return ret

    @decorate_exception
    def process_run(self, test_case, test_case_path=None, parameters=None, loop=1, timeout=0):
        log.INFO("process_run")
        value = None
        for item in range(loop):
            log.INFO("Run test in loop: %s", item)
            start_time = time.time()
            current_time = start_time
            queue = Queue()
            self.process_run_ = MyProcess(target=self.engine.run, args=(test_case, test_case_path, parameters, queue,))
            self.process_run_.daemon = True
            self.process_run_.start()
            if timeout > 0:
                while current_time - start_time < timeout:
                    current_time = time.time()
                    time.sleep(5)
                self.process_run_.stop()
            else:
                self.process_run_.join()
            value = queue.get(True)
            self.results.append(value)
        return value
