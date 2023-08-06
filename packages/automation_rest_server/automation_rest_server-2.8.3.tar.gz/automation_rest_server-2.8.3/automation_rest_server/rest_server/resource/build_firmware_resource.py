# coding=utf-8
import json
from flask_restful import reqparse
from flask_restful import Resource
from flask_restful import marshal_with
from test_framework.test_pool import TestPool
from rest_server.resource.models.helper import resource_fields
from test_framework.state import TestType, State


PARSER = reqparse.RequestParser()
PARSER.add_argument('rep_url')
PARSER.add_argument('rep_branch')
PARSER.add_argument('rep_user')
PARSER.add_argument('rep_password')
PARSER.add_argument('project')


class BuildFirmwareResource(Resource):

    def __init__(self):
        self.test_pool = TestPool()

    @marshal_with(resource_fields, envelope='resource')
    def post(self):
        args = PARSER.parse_args()
        rep_dict = {
            "rep_url": args["rep_url"],
            "rep_branch": args["rep_branch"],
            "rep_user": args["rep_user"],
            "rep_password": args["rep_password"],
            "project": args["project"]
        }
        results_data = list()
        build_name = "Build_{}".format(args["rep_branch"])
        key = self.test_pool.add_test(build_name, TestType.BuildFirmware, rep_dict)
        results_data.append(key)
        state_ = State.PASS if key is not None else State.ERROR_NOT_FOUND
        result = {"data": results_data, "state": state_, "msg": "Test {} key {}".format(build_name, key)}
        return result

    def _get_async_result(self, key_):
        results, state = self.test_pool.get_state_by_key(key_)
        data = list()
        data.append(json.dumps(results))
        result = {"msg": "", "state": state, "data": data}
        return result

    @marshal_with(resource_fields, envelope='resource')
    def get(self, key_=None):
        if key_ is not None:
            result = self._get_async_result(key_)
        else:
            result = {"msg": "command did not support", "state": State.ERROR_NOT_FOUND}
        return result
