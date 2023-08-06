# coding=utf-8
import os
import json
from flask_restful import reqparse
from flask_restful import Resource
from flask_restful import marshal_with
from rest_server.resource.models.helper import resource_fields
from test_framework.test_pool import TestPool
from test_framework.state import TestType
from test_framework.state import State


PARSER = reqparse.RequestParser()
PARSER.add_argument('parameters')
PARSER.add_argument('execute_name')


class UpgradeResource(Resource):

    def __init__(self):
        self.test_pool = TestPool()

    @marshal_with(resource_fields, envelope='resource')
    def post(self):
        args = PARSER.parse_args()
        parameters = eval(args["parameters"])
        execute_name = args['execute_name']
        result = self._async_download(execute_name, parameters)
        return result

    def _async_download(self, test_name, parameters):
        data = list()
        key = self.test_pool.add_test(test_name, TestType.DownloadSerial, parameters)
        data.append(key)
        state_ = State.PASS if key is not None else State.ERROR_NOT_FOUND
        result = {"data": data, "state": state_, "msg": "Test {} key {}".format(test_name, key)}
        return result
