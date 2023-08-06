# coding=utf-8
import os
from test_framework.test_runner import Runner
from utils import log
from test_framework.test_base import TestBase


class TestCase(TestBase):

    def __init__(self, test_case_name=None):
        super(TestCase, self).__init__()
        self.test_name = test_case_name
        self.runner = Runner()
        self.get_all_modules(self.test_case_path)
        self.list_tests()

    def stop(self):
        return self.runner.stop()

    def get_test_cases(self):
        return self.tests

    def list_and_filter_tests(self, filters):
        filter_result = []
        if filters.lower() == "all":
            filter_result = self.tests
        else:
            for item in self.tests:
                if filters in item:
                    filter_result.append(item)
        return filter_result

    def run(self, test_name=None, parameters=None):
        log.INFO("test case run")
        if test_name is not None:
            self.test_name = test_name
        test_paths = self.get_all_script_path(self.test_name)
        test_path = test_paths[0] if test_paths else None
        self.runner.process_run(self.test_name, test_path, parameters, 1, 0)
        return self.runner.get_results()
