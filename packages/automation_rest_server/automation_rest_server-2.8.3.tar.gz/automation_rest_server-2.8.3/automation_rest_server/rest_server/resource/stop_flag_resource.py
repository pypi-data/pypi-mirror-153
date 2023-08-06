# coding=utf-8
from flask_restful import reqparse
from flask_restful import Resource
from flask_restful import marshal_with
from rest_server.resource.models.helper import resource_fields
from test_framework.test_pool import TestPool
from test_framework.state import State

PARSER = reqparse.RequestParser()
PARSER.add_argument('stop_flag')


class StopFlagResource(Resource):

    def __init__(self):
        self.test_pool = TestPool()

    @marshal_with(resource_fields, envelope='resource')
    def get(self):
        data = list()
        stop_flag = self.test_pool.stop_flag
        data.append(stop_flag)
        result = {
            "data": data,
            "state": State.PASS
        }
        return result

    @marshal_with(resource_fields, envelope='resource')
    def post(self):
        args = PARSER.parse_args()
        stop_flag = args["stop_flag"]
        self.test_pool.stop_flag = True if stop_flag == "True" else False
        result = {"msg": "set stop_flag to {}".format(stop_flag), "state":State.PASS}
        return result