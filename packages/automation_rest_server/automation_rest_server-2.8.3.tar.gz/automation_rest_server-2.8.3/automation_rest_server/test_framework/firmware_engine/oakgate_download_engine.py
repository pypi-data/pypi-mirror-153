
import subprocess
import os
import time
from utils.system import decorate_exception_result
from test_framework.firmware_engine.models.firmware_path import FirmwareBinPath
from utils import log
from test_framework.state import State


class OakgateDownload(object):

    def __init__(self):
        super(OakgateDownload, self).__init__()
        self.root_path = os.getcwd()
        self.script_path = os.path.join(self.root_path, "Utility")
        self.logs_path = os.path.join(self.root_path, "Logs")
        self.orig_log_folders = list()
        self.latest_log_folders = list()
        self.fw_path_manage = FirmwareBinPath()

    def get_fw_path(self, parameters):
        if parameters["auto_build"] == "True":
            volume = parameters.get("volume", "ALL")
            nand = parameters.get("nand", "BICS4")
            win_fw_bin, _ = self.fw_path_manage.get_auto_build_fw_path(parameters["commit"], volume, nand)
        else:
            win_fw_bin = parameters["fw_path"]
        return win_fw_bin

    def gen_cmd_line(self, fw_path, ogt):
        cmd = "cd /d {} && python cnex_auto_dl_fw.py --oakgate={} --image2={}".format(self.script_path, ogt, fw_path)
        log.INFO("oakgate download: {}".format(cmd))
        return cmd

    def get_orig_logs(self):
        log_dirs = os.listdir(self.logs_path)
        for item in log_dirs:
            if os.path.isdir(os.path.join(self.logs_path, item)):
                self.orig_log_folders.append(os.path.join(self.logs_path, item))
        print("self.org logs", self.orig_log_folders)

    def get_new_log(self, oakgate):
        new_logs = list()
        self.latest_log_folders = os.listdir(self.logs_path)
        for item in self.latest_log_folders:
            log_item = os.path.join(self.logs_path, item)
            if os.path.isdir(log_item):
                if log_item not in self.orig_log_folders:
                    for new_log_item in os.listdir(log_item):
                        if os.path.isfile(os.path.join(log_item, new_log_item)):
                            if oakgate in new_log_item:    # check if this log belong to correct oagkate
                                new_logs.append(os.path.join(log_item, new_log_item))
        print("new_logs", new_logs)
        return new_logs

    @decorate_exception_result
    def run(self, parameters):
        fw_path = self.get_fw_path(parameters)
        oakgate = parameters["oakgate"]
        self.get_orig_logs()
        cmd = self.gen_cmd_line(fw_path, oakgate)
        ret = os.system(cmd)
        logs = self.get_new_log(oakgate)
        return ret, logs
