# coding=utf-8
# pylint: disable=inconsistent-return-statements
import os
import re
import sys
import importlib
import inspect
from utils import log


class TestBase(object):

    def __init__(self):
        self.working_path = os.getcwd()
        self.test_case_path = self.get_test_case_path()
        self.modules = []
        self.tests = []
        self.module_list = []

    def get_test_case_path(self):
        test_case_path = None
        dirs = os.listdir(self.working_path)
        for item in dirs:
            temp_path = os.path.join(self.working_path, item)
            if "TestScripts" in item or "testcase" == item.lower():
                test_case_path = temp_path
        return test_case_path

    def get_all_script_path(self, script):
        list_script = script.split(';')
        path_list = []
        if self.test_case_path is not None:
            for single_script in list_script:
                path = self._get_full_path_script(single_script.strip())
                if path is not None:
                    path_list.append(path)
        return path_list

    def _get_full_path_script(self, script):
        if script.find(':') != -1:
            file_name = script.split(':')
            if file_name[0].find('.py') == -1:
                file_path = self.get_file_path(self.test_case_path, file_name[0]+'.py')
            else:
                file_path = self.get_file_path(self.test_case_path, file_name[0])
            if file_path is not None:
                abs_path = file_path + ':' + file_name[1]
            else:
                abs_path = None
        else:
            abs_path = self.get_file_path(self.test_case_path, script)
        return abs_path

    def get_file_path(self, path, file_):
        _files = os.listdir(path)
        for item in _files:
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                ret = self.get_file_path(item_path, file_)
                if ret is not None:
                    return ret
            elif item == file_:
                return os.path.join(path, item)

    def get_all_modules(self, path):
        if path is None or os.path.exists(path) is False:
            return
        _files = os.listdir(path)
        for item in _files:
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                ret = self.get_all_modules(item_path)
                if ret is not None:
                    return ret
            elif ".py" in item and ("test" in item.lower() or "tc_" in item  or "mc_" in item)and "__init__" not in item and ".pyc" not in item:
                self.module_list.append(item_path)

    def list_tests(self):
        for item in self.module_list:
            self.list_test_in_one_file(item)

    def list_test_in_one_file(self, file_path):
        module_name = os.path.basename(file_path).split(".")[0]
        if str(module_name).startswith("tc_") is True or str(module_name).startswith("mc_") is True:
            self.tests.append(os.path.basename(file_path))   #oakgate test case
        else:
            file_ = open(file_path, encoding='UTF-8')
            class_name = None
            for line_ in file_.readlines():
                # get_class_name = self.get_class_name(line_)
                get_class_name, base_class_name = self.get_class_subclass_name(line_)
                self.add_base_class_tests(module_name, base_class_name, get_class_name)
                if get_class_name is not None:
                    class_name = get_class_name
                    test = "{}:{}".format(module_name, class_name)
                    self.tests.append(test)
                else:
                    get_function_name = self.get_function_name(line_)
                    if get_function_name:
                        test = "{}:{}.{}".format(module_name, class_name, get_function_name[0])
                        self.tests.append(test)
            file_.close()

    def add_base_class_tests(self, module_name, base_class_name, class_name):
        new_tests = list()
        if base_class_name not in ["", "object", None]:
            base_test = "{}:{}".format(module_name, base_class_name)
            for test in self.tests:
                test_fun = test.split(".")
                if len(test_fun) == 2:
                    if test_fun[0] == base_test:
                        if test_fun:
                            try:
                                new_test = "{}:{}.{}".format(module_name, class_name, test_fun[1])
                                new_tests.append(new_test)
                            except Exception as all_exception:
                                print(all_exception)
        self.tests.extend(new_tests)

    def get_class_name(self, line):
        rets = re.findall("^\s*class\s+(Test[a-zA-Z0-9\_]+)\(", line)
        return rets

    def get_class_subclass_name(self, line):
        class_name, base_class_name = None, None
        rets = re.findall("^\s*class\s+([a-zA-Z0-9\_]+)\((.*?)\)", line)
        if rets:
            class_name, base_class_name = rets[0][0], rets[0][1]
        return class_name, base_class_name

    def get_function_name(self, line):
        rets = re.findall("^\s+def\s+(test[a-zA-Z0-9\_]+)\(", line)
        return rets

    def test(self):
        return self.tests

    def get_log_path(self):
        log_path = os.path.join(self.working_path, "log")
        if os.path.exists(log_path) is False:
            os.mkdir(log_path)
        return log_path
