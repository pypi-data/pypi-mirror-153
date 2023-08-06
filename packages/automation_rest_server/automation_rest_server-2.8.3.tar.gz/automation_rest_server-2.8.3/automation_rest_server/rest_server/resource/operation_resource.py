# coding=utf-8
import os
from flask_restful import reqparse
from flask_restful import Resource
from flask_restful import marshal_with
from rest_server.resource.models.helper import resource_fields
from test_framework.state import State
from tool.device import NVME


PARSER = reqparse.RequestParser()
PARSER.add_argument('operate_name')
PARSER.add_argument('fw')
PARSER.add_argument('slot')
PARSER.add_argument('device_index')


class OperationResource(Resource):

    def __init__(self):
        pass

    def get_fw_path(self, fw_name):
        working_path = os.environ["working_path"]
        fw_home_path = os.path.join(working_path, "fw_bin")
        fw_path = os.path.join(fw_home_path, fw_name)
        if os.path.exists(fw_path):
            return fw_path
        return None

    @marshal_with(resource_fields, envelope='resource')
    def post(self):
        args = PARSER.parse_args()
        operate_name = args["operate_name"]
        fw_name = args["fw"]
        slot = args["slot"]
        device_index = args['device_index']
        fw_path = self.get_fw_path(fw_name)
        device = NVME(device_index)
        if operate_name == "upgrade" and fw_path is not None:
            result, str_out = device.upgrade_fw(fw_path, device_index=device_index, slot=slot)
            if result is True:
                result = {"msg":"FW upgrade succeed, logs:\n {}".format(str_out), "state":State.PASS}
            else:
                result = {"msg": "FW upgrade failed, logs:\n {}".format(str_out), "state":State.FAIL}
        else:
            result = {"msg": "Operation: {} is not support".format(operate_name), "state":State.ERROR_NOT_FOUND}
        return result
