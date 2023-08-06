# coding=utf-8
import yaml
import os
from flask_restful import Resource
from flask_restful import marshal_with
from rest_server.resource.models.helper import resource_fields
from test_framework.state import State


class OakgateResource(Resource):

    def __init__(self):
        self.working_path = None

    @marshal_with(resource_fields, envelope='resource')
    def get(self):
        data = []
        self.working_path = os.environ["working_path"]
        oakgate_config = os.path.join(self.working_path, "Config", "BasicConfig", "oakgate.yaml")
        if os.path.exists(oakgate_config):
            with open(oakgate_config, "r", encoding='utf-8') as f_:
                cont = f_.read()
                configs = yaml.load(cont)
                for key in configs.keys():
                    data.append(key)
        result = {
            "data": data,
            "state": State.PASS
        }
        return result
