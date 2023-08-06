# coding=utf-8
import os
from flask_restful import reqparse
from flask_restful import Resource
from flask_restful import marshal_with
from test_framework.test_suite import TestSuite
from test_framework.test_case import TestCase
from rest_server.resource.models.helper import resource_fields
from test_framework.test_pool import TestPool
from test_framework.state import State
from test_framework.test_result import TestResult
from test_framework.state import TestType


PARSER = reqparse.RequestParser()
PARSER.add_argument('test')
PARSER.add_argument('mode')
PARSER.add_argument('key')
PARSER.add_argument('parameters')


class TestResource(Resource):

    def __init__(self):
        self.test_result = TestResult()
        self.test_suite = None
        self.test_case = None
        self.test_pool = TestPool()

    def _sync_run(self, test_name, test_parameter=None):
        self.test_suite = TestSuite()
        self.test_case = TestCase()
        test_handler = None
        self.set_test_parameters(test_parameter)
        if self.is_test_case(test_name):
            test_handler = self.test_case
        elif self.is_test_suite(test_name):
            test_handler = self.test_suite
        if test_handler is not None:
            ret = test_handler.run(test_name, test_parameter)
            get_result = self._summary_test_result(list(ret))
            state_ = State.PASS if get_result is True else State.FAIL
            msg = "Test: {}, state: {}".format(list(ret), state_)
        else:
            state_ = State.ERROR_NOT_FOUND
            msg = "Test:{} did not found".format(test_name)
        result = {"msg": msg, "state": state_}
        return result

    def is_test_case(self, test_name):
        test_case_list = self.test_pool.get_all_test_case()
        ret = True if test_name in test_case_list else False
        return ret

    def is_test_suite(self, test_name):
        test_suite_list = self.test_pool.get_all_test_suite()
        ret = True if test_name in test_suite_list else False
        return ret

    def _async_run(self, test_name, parameters):
        data = list()
        if self.is_test_case(test_name):
            key = self.test_pool.add_test(test_name, TestType.TestCase, parameters)
            data.append(key)
        elif self.is_test_suite(test_name):
            key = self.test_pool.add_test(test_name, TestType.TestSuite, parameters)
            data.append(key)
        else:
            key = self.test_pool.add_test(test_name, TestType.TestCase, parameters)
            data.append(key)
        state_ = State.PASS if key is not None else State.ERROR_NOT_FOUND
        result = {"data": data, "state": state_, "msg": "Test {} key {}".format(test_name, key)}
        return result

    def _filter_test(self, test_type, filter_):
        test_handler = TestCase() if test_type == "test_case" else TestSuite()
        test_lists = test_handler.list_and_filter_tests(filter_)
        state_ = State.PASS if test_lists else State.ERROR_NOT_FOUND
        msg = "List succeed" if test_lists else "List failed"
        result = {"data": test_lists, "state": state_, "msg": msg}
        return result

    def _get_async_result(self, key_):
        results, state = self.test_pool.get_state_by_key(key_)
        if state in [State.PASS, State.FAIL, State.BLOCK, State.ERROR_UNHEALTHY]:
            msg = self.test_result.get_test_suite_test_msg(results)
        else:
            msg = "Key: {}, state is {}".format(key_, State.verdicts_map[state])
        result = {"msg": "{}".format(msg), "state": state}
        return result

    def _get_test_suite_case_list(self, test_suite_name):
        try:
            test_suite = TestSuite()
            test_suites = test_suite.load_test_suite(test_suite_name)
            data = list()
            data.append(str(test_suites))
            result = {"data": data, "state": State.PASS}
        except BaseException as message:
            result = {"msg": "ts:{} not found. {}".format(test_suite_name, message), "state": State.ERROR_NOT_FOUND}
        return result

    def _summary_test_result(self, results):
        if results:
            failed_list = list(filter(lambda X: X["result"] is False, results))
            result = False if failed_list else True
        else:
            result = None
        return result

    @staticmethod
    def set_test_parameters(parameters):
        if type(parameters) is dict:
            for key in parameters.keys():
                os.environ[key] = parameters[key]

    def test_set_parameters(self, parameters):
        print("Custom global parameters: ")
        if type(parameters) is dict:
            for key in parameters.keys():
                print("parametesr: ", key, os.environ[key])

    @marshal_with(resource_fields, envelope='resource')
    def post(self):
        args = PARSER.parse_args()
        test_name = args["test"]
        mode = args["mode"]
        parameters = eval(args["parameters"])
        print("test_name", test_name)
        print("parameters", parameters)
        if mode == "sync":
            result = self._sync_run(test_name, parameters)
        else:
            result = self._async_run(test_name, parameters)
        return result

    @marshal_with(resource_fields, envelope='resource')
    def get(self, filter_=None, key_=None, test_name_=None, type_=None):
        if filter_ is not None:
            result = self._filter_test(type_, filter_)
        elif key_ is not None:
            result = self._get_async_result(key_)
        elif test_name_ is not None:
            result = self._get_test_suite_case_list(test_name_)
        else:
            result = {"msg": "command did not support", "state": State.ERROR_NOT_FOUND}
        return result

    @marshal_with(resource_fields, envelope='resource')
    def delete(self, filter_=None):
        ret = self.test_pool.stop_test(filter_)
        state = State.PASS if ret is True else State.FAIL
        msg = "Stop tests succeed" if ret is True else "Stop tests failed"
        result = {"state": state, "msg": msg}
        return result
