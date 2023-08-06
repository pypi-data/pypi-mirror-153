# coding=utf-8
# pylint: disable=eval-used
from flask_restful import reqparse
from flask_restful import Resource
from flask_restful import marshal_with
from rest_server.resource.models.helper import resource_fields
from test_framework.test_pool import TestPool
from test_framework.state import State
from tool.iometer.iometer import IoMeter


PARSER = reqparse.RequestParser()
PARSER.add_argument('parameters')
PARSER.add_argument('mode')
PARSER.add_argument('key')


class IometerBenchmarkResource(Resource):

    def __init__(self):
        self.test_pool = TestPool()
        self.tool = IoMeter()


    @marshal_with(resource_fields, envelope='resource')
    def get(self):
        script_list = self.tool.get_script_list()
        result = {"msg": "", "state": State.PASS, "data": script_list}
        return result
