# coding=utf-8
# pylint: disable=unused-variable
import os
import yaml
import time
import random
import string
from multiprocessing import Queue
from tool.fio.fio import Fio
from utils.process import MyProcess
from test_framework.state import State


class TestBenchmarkGroup(object):

    def __init__(self):
        self.process_run_ = None
        self.working_path = os.environ.get('working_path', '')
        self.config_path = os.path.join(self.working_path, "configuration", "benchmark")
        self.results = list()

    @staticmethod
    def generate_group_key():
        time_string = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        code = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
        key = "{}_{}".format(time_string, code)
        return key

    def load_benchmark_config(self, config_file):
        config = os.path.join(self.config_path, config_file)
        configs = None
        if os.path.exists(config):
            configs = yaml.load(open(config).read(), Loader=yaml.FullLoader)
        return configs

    @staticmethod
    def _get_unique_code():
        letter_len = 10
        code = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(letter_len))
        return code

    def update_benchmark_parameters(self, benchmark_pars,  parameters, group_name, group_key):
        benchmark_pars["group_key"] = group_key
        benchmark_pars["group_name"] = group_name
        benchmark_pars["key"] = self._get_unique_code()
        benchmark_pars["project_name"] = parameters["project"]
        benchmark_pars["tester"] = parameters["tester"]
        return benchmark_pars

    def _run(self, test_name, parameters, queue):
        try:
            benchmarks = self.load_benchmark_config(parameters["script"])
            if benchmarks is not None:
                ret, out_put = State.PASS, ""
                group_key = self.generate_group_key()
                for item in benchmarks:
                    fio = Fio()
                    benchmark_parm = self.update_benchmark_parameters(item, parameters, test_name, group_key)
                    print("Benchmark parms:", benchmark_parm)
                    status, out_put, result = fio.run_benchmark(benchmark_parm)
                    ret = State.PASS if status == 0 else State.FAIL
            else:
                ret, out_put = State.ERROR_NOT_FOUND, "Config: {} did not found".format(parameters["script"])
            result = {"name": test_name, "result": ret, "msg": out_put, "benchmark_result": ""}
            queue.put(result)
        except Exception as e:
            print(e)
            result = None
        return result

    def run(self, test_name, test_parameters):
        queue = Queue()
        self.process_run_ = MyProcess(target=self._run, args=(test_name, test_parameters, queue, ))
        self.process_run_.start()
        self.process_run_.join()
        value = queue.get(True)
        self.results.append(value)
        return self.results

    def stop(self):
        print("TestBenchmark runner . stop")
        if self.process_run_ is not None:
            ret = self.process_run_.stop()
        else:
            ret = -1
        return ret
