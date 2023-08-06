#! /usr/bin/python
## -*- coding: utf-8 -*-
import os
import time
import re
import subprocess
import csv
from utils import log
from tool.diskpart.diskpart import format_raw, format_x


class IoMeter(object):

    def __init__(self):

        self.name = "iometer"
        self.working_path = os.environ["working_path"]
        self.iometer_path = os.path.join(self.working_path, "Tools", "IOMeter_for_Client_PC", "IOmeter.exe")
        if os.path.exists(self.iometer_path):
            self.icf_path = os.path.join(os.path.dirname(self.iometer_path), "script")
            self.result_path = os.path.join(os.path.dirname(self.iometer_path), "results")
            if os.path.exists(self.result_path) is False:
                os.mkdir(self.result_path)
        else:
            self.iometer_path = None
            self.icf_path = None
            self.result_path = None


    def kill(self):
        command = 'taskkill /F /T /IM Iometer.exe'
        os.system(command)
        command = 'taskkill /F /T /IM Dynamo.exe'
        os.system(command)

    def get_script_list(self):
        script_list = list()
        if self.icf_path is not None:
            file_lists = os.listdir(self.icf_path)
            for file_ in file_lists:
                if ".icf" in file_:
                    script_list.append(file_)
        return script_list

    def get_version(self):
        version_file = os.path.join(os.path.dirname(self.iometer_path), "version.txt")
        file_ = open(version_file)
        content = file_.readline()
        version_ = re.findall("v(.+)", content)[0]
        return version_


    def _get_log_name_with_time_tag(self, string_):
        return "{}_{}.csv".format(string_, time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))

    def update_target_to_icf(self, icf_file, target_id):
        target_name = "{}:PHYSICALDRIVE".format(target_id)
        icf_path = os.path.join(self.icf_path, icf_file)
        if os.path.exists(icf_path) is False:
            log.ERR("icf not exist: %s", icf_file)
        else:
            self._update_file(icf_path, target_name)

    def update_target_name_to_icf(self, icf_file, target_name):
        icf_path = os.path.join(self.icf_path, icf_file)
        if os.path.exists(icf_path) is False:
            log.ERR("icf not exist: %s", icf_file)
        else:
            self._update_file(icf_path, target_name)

    def run_benchmark(self, test_parameters):
        config_file = test_parameters["config_file"]
        target_id = test_parameters["target_id"]
        self.disk_part(test_parameters["diskpart"])
        if target_id != "":
            self.update_target_name_to_icf(config_file, target_id)
        status, out_put = self.run_tests(config_file)
        logs = self.get_logs(out_put)
        result = self.get_bechmark_result(logs[0])
        log_ = "log file: {}".format(out_put)
        # logs = self.get_list_to_string(logs)
        return status, log_, result

    def get_list_to_string(self, logs):
        log_str = str()
        for item in logs:
            log_str = log_str + "new_file:\n" + item
        return log_str

    def disk_part(self, type_):
        if type_ == "raw":
            format_raw()
        elif type_ == "X":
            format_x()

    def get_logs(self, log_path):
        logs = list()
        for file_ in os.listdir(self.result_path):
            if log_path in file_:
                result_path = os.path.join(self.result_path, file_)
                with open(result_path, 'r') as file_r:
                    log_content = file_r.read()
                    logs.append(log_content)
        return logs

    def run_tests(self, icf_file, target_id=None):
        if target_id is not None:
            self.update_target_to_icf(icf_file, target_id)
        result_name = self._get_log_name_with_time_tag(icf_file.split(".")[0])
        test_case_path = os.path.join(self.icf_path, icf_file)
        result_path = os.path.join(self.result_path, result_name)
        cmd = "{} /c {} /r {}".format(self.iometer_path, test_case_path, result_path)
        ret = subprocess.call(cmd, shell=True)
        return ret, result_name

    def run_tests_popen(self, icf_file, target_id=None):
        if target_id is not None:
            self.update_target_to_icf(icf_file, target_id)
        result_name = self._get_log_name_with_time_tag(icf_file.split(".")[0])
        test_case_path = os.path.join(self.icf_path, icf_file)
        result_path = os.path.join(self.result_path, result_name)
        cmd = "{} {} {}".format(self.iometer_path, test_case_path, result_path)
        process_ = subprocess.Popen(cmd, shell=True)
        return process_, result_name

    def _update_file(self, path, new_target):
        content = ""
        next_is_targe = False
        with open(path, "r") as file_r:
            for line in file_r:
                if next_is_targe is False:
                    if "'Target\n" in line:
                        next_is_targe = True
                else:
                    line = "    {}\n".format(new_target)
                    next_is_targe = False
                content += line
        with open(path, "w") as file_w:
            file_w.write(content)

    def get_bechmark_result(self, logs):
        result = dict()
        if logs != "":
            lines = logs.split("\n")
            for line in lines:
                summary = line.split(',')
                if summary[0] == "ALL":
                    result = {
                        "iops": float(summary[6]),
                        "read_iops": float(summary[7]),
                        "write_iops": float(summary[8]),
                        "mibps": float(summary[9]),
                        "read_mibps": float(summary[10]),
                        "write_mibps": float(summary[11])
                    }
                    break
        return result

    def get_iops_bandwidth(self, result):
        """
        :param result:
        :return:  iops: k, bandwidth: MB/s
        """
        iops, bandwidth = 0, 0
        logs = self.get_logs(result)
        if logs != "":
            lines = logs[0].split("\n")
            for line in lines:
                summary = line.split(',')
                if summary[0] == "ALL":
                    iops = float('%.2f' % (float(summary[6]) / 1000))
                    bandwidth = float('%.2f' % (float(summary[9])))
                    break
        else:
            log.ERR("Result is not find, %s", result)
        return iops, bandwidth

    def check_perf_result(self):
        ret = True
        check_item = [
            {"name": "4K_Ran_70R-30W_QD32", "benchmark": 50, "type": "iops"},
            {"name": "4K_Ran_Reads_QD4", "benchmark": 40, "type": "iops"},
            {"name": "4K_Ran_Reads_QD128", "benchmark": 150, "type": "iops"},
            {"name": "4K_Ran_Writes_QD128", "benchmark": 30, "type": "iops"},
            {"name": "128K_Seq_Reads_QD128", "benchmark": 1600, "type": "bandwidth"},
            {"name": "128K_Seq_Writes_QD128", "benchmark": 800, "type": "bandwidth"}
        ]
        for item in check_item:
            iops, bandw = self.get_iops_bandwidth("{}.csv".format(item["name"]))
            value = iops if item["type"] == "iops" else bandw
            if value < item["benchmark"]:
                log.ERR("Failed: Test: %s %s, actual is %s k, benchmark is %s k",
                        item["name"], item["type"], value, item["benchmark"])
                ret = ret & False
            else:
                log.INFO("Passed Test: %s %s, actual is %s k, benchmark is %s k",
                         item["name"], item["type"], value, item["benchmark"])
        return ret

    def _get_error_count(self, errors):
        count = 0
        for error in errors:
            sub_count = len(list(filter(lambda x: x > 0, error)))
            count += sub_count
        if count > 0:
            print(errors)
        return count

    def check_errors(self, test_log):
        log_path = os.path.join(self.result_path, test_log)
        if os.path.exists(log_path) is False:
            return None
        error_index, read_err_index, write_err_index = -1, -1, -1
        error_line_count = 0
        get_errors = []
        file_ = open(log_path)
        csv_reader = csv.reader(file_)
        for line_ in csv_reader:
            if "Errors" in line_:
                error_index = line_.index("Errors")
                read_err_index = line_.index("Read Errors")
                write_err_index = line_.index("Write Errors")
                error_line_count = len(line_)
                print("errors index:", error_index, read_err_index, write_err_index)
                continue
            if error_index != -1 and len(line_) == error_line_count:
                errors = [int(line_[error_index]), int(line_[read_err_index]), int(line_[write_err_index])]
                get_errors.append(errors)
        count = self._get_error_count(get_errors)
        return count
