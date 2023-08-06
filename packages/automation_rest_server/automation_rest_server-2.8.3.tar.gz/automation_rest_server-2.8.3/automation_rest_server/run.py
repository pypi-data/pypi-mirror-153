#!/usr/bin/env python
# coding=utf-8
import os
import sys
import re
import yaml
import argparse
sys.path.append(os.path.join(os.path.dirname(__file__)))
from test_framework.test_pool import TestPool
from test_framework.test_suite import TestSuite
from test_framework.test_case import TestCase
from rest_server.reset_server import *
from rest_server.resource.models.ftp_server import thread_start_ftp_server
from test_framework.database import update_abnormal_end_tests
from utils.env import get_env_identify_info
from utils.pip_operation import PIPOperation
from utils import log


def add_sub_argument_group(subparsers, name, handler_function):
    regression_parser = subparsers.add_parser(name, help='%s tests executor' % name)
    regression_required_arguments = regression_parser.add_argument_group('required arguments')
    regression_required_arguments.add_argument('--name', '-n', type=str, required=False,
                                               help='test suite ,test case name or operation name', default="fio")
    regression_required_arguments.add_argument('--variables', '-v', type=str,  default=None,
                                               help='user variables, format: var1:value1,var2:value3', required=False)
    regression_required_arguments.add_argument('--list', '-l', type=str, default=None,
                                               help='list and filter test case', required=False)
    regression_required_arguments.add_argument('--fw', '-f', type=str, default=None,
                                               help='fw path for upgrade', required=False)
    regression_required_arguments.add_argument('--port', '-p', type=str, default="5000",
                                               help='start server port id', required=False)
    regression_required_arguments.add_argument('--reboot', '-r', action='store_true',
                                               help='start after reboot', default=False, required=False)
    regression_required_arguments.add_argument('--work_path', '-w', type=str, default="",
                                               help='automation platform path, test-platform or perses', required=False)
    regression_parser.set_defaults(executor_function=handler_function)


def create_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    add_sub_argument_group(subparsers, 'testsuite', test_suite_handle)
    add_sub_argument_group(subparsers, 'testcase', test_case_handle)
    add_sub_argument_group(subparsers, 'start', start_rest_server)
    return parser


def start_rest_server(args):
    if PIPOperation.have_new_version() is False:
        get_env_identify_info()
        _ = TestPool(args.reboot)
        if args.reboot is False:
            update_abnormal_end_tests()
        thread_start_ftp_server()
        APP.run(host="0.0.0.0", port=args.port)


def test_suite_handle(args):
    test_suite = TestSuite()
    if args.list is not None:
        rets = test_suite.list_and_filter_tests(args.list)
        for item in rets:
            print(item)
    else:
        test_suite.run(args.name)


def test_case_handle(args):
    test_case = TestCase(args.name)
    if args.list is not None:
        rets = test_case.list_and_filter_tests(args.list)
        for item in rets:
            print(item)
    else:
        test_case.run()


def load_global_config():
    config_file = os.path.join(os.getcwd(), 'config.yml')
    if os.path.exists(config_file):
        conf = yaml.load(open(config_file).read(), Loader=yaml.FullLoader)
        for key, val in conf.items():
            os.environ[key] = val


def get_work_path(args):
    work_path = os.getcwd()
    if args.work_path != "":
        if os.path.exists(args.work_path):
            work_path = args.work_path
    print("working path", work_path)
    return work_path


def add_globals(args):
    load_global_config()
    os.environ["root_path"] = os.path.join(os.path.dirname(__file__))
    os.environ["working_path"] = get_work_path(args)
    os.environ["PYTHONPATH"] = get_work_path(args)
    os.environ['PYTHONUNBUFFERED'] = "TRUE"
    os.environ["prun_port"] = args.port
    if args.variables is not None:
        str_variable = args.variables
        rets = re.findall("(\w+)\:([^\,]+)", str_variable)
        for item in rets:
            os.environ[str(item[0])] = str(item[1])


def run():
    parser = create_parser()
    args = parser.parse_args()
    try:
        add_globals(args)
        args.executor_function(args)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    run()
