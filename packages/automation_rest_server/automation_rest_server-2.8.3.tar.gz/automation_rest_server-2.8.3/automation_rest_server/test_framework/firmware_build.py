from test_framework.state import State, DownloadType
from test_framework.firmware_engine.build_firmware_engine import FirmwareBuildEngine
from utils.process import MyProcess
from multiprocessing import Queue


class FirmwareBuild(object):

    def __init__(self, execute_name):
        self.process_run_ = None
        self.results = list()
        self.execute_name = execute_name
        self.runner = FirmwareBuildEngine()

    def run(self, test_parameters):
        print("FirmwareBuild", test_parameters)
        queue = Queue()
        self.process_run_ = MyProcess(target=self._run, args=(test_parameters, queue, ))
        self.process_run_.start()
        self.process_run_.join()
        value = queue.get(True)
        print("FirmwareBuild result", value)
        self.results.append(value)
        return self.results

    def _run(self, test_parameters, queue):
        try:
            status, fw_path, log, commit = self.runner.run(test_parameters)
            ret = State.PASS if status == 0 else State.FAIL
            result = {"name": self.execute_name, "result": ret, "log": log, "fw_path": fw_path, "commit": commit}
            queue.put(result)
        except Exception as e:
            print(e)
            result = None
        return result

    def stop(self):
        print("FirmwareBuild runner . stop")
        if self.process_run_ is not None:
            ret = self.process_run_.stop()
        else:
            ret = -1
        return ret
