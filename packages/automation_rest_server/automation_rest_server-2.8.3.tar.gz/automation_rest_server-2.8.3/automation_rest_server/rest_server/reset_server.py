# coding=utf-8
from flask import Flask
from flask_restful import Api
from .resource.test_resource import TestResource
from .resource.operation_resource import OperationResource
from .resource.state_resource import StateResource
from .resource.benchmark_resource import BenchmarkResource
from .resource.iometer_benchmark_resource import IometerBenchmarkResource
from .resource.oakgate_resource import OakgateResource
from .resource.models.ftp_server import thread_start_ftp_server
from .resource.stop_flag_resource import StopFlagResource
from .resource.git_resource import GitResource
from .resource.upgrade_resource import UpgradeResource
from .resource.build_firmware_resource import BuildFirmwareResource
from test_framework.database import update_abnormal_end_tests


APP = Flask(__name__)
API = Api(APP)


API.add_resource(OperationResource, "/operation")
API.add_resource(StateResource, "/state/<type_>", "/state")
API.add_resource(TestResource, '/test/<filter_>', '/test', '/test/<type_>/<filter_>', '/test/results/<key_>',
                 '/test/testsuite/<test_name_>')
API.add_resource(BenchmarkResource, "/benchmark", "/benchmark/results/<key_>")
API.add_resource(IometerBenchmarkResource, "/benchmark/iometer/testlist")
API.add_resource(OakgateResource, "/oakgate/device_list")
API.add_resource(StopFlagResource, "/stopflag")
API.add_resource(GitResource, "/git")
API.add_resource(UpgradeResource, "/upgrade")
API.add_resource(BuildFirmwareResource, "/firmware_build", "/firmware_build/<key_>")


if __name__ == '__main__':
    update_abnormal_end_tests()
    thread_start_ftp_server()
    APP.run(host="0.0.0.0", debug=False)
