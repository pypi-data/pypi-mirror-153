#! /usr/bin/python
## -*- coding: utf-8 -*-
import os
import re
import json
import subprocess
import sys
import platform
from datetime import datetime, timezone, timedelta
from collections import OrderedDict
from test_framework.test_base import TestBase
from utils.system import get_linux_nvme_devs, get_time_stamp
from tool.fio.fio_linux import Fio as LinuxFio
from test_framework.performance_database import decorate_collect_real_time_bw_iops
from test_framework.performance_database import decorate_collect_summary_result
from test_framework.performance_database import decorate_run_benchmark
from test_framework.performance_database import decorate_collect_lifetime_bw
from utils import log


class Fio(LinuxFio):

    def __init__(self):
        super(Fio, self).__init__()
        self.working_path = os.environ.get('working_path', r'D:\Automation\perses')
        self.base = TestBase()
        system_str = platform.system()
        self.parm = OrderedDict()
        if "windows" in system_str.lower():
            self.name = "windows_fio"
            self.fio_path = os.path.join(r"C:\Program Files\fio\fio.exe")
            self.fio_file_path = os.path.join(self.working_path, "testcase", "function", "fio", "config", "windows")
            self.fio_cmd = "fio"
        else:
            self.name = "linux_fio"
            self.fio_path = os.path.join(self.working_path, "tools", "fio")
            self.fio_file_path = os.path.join(self.working_path, "testcase", "function", "fio", "config", "linux")
            self.fio_cmd = "./fio"

    def get_version(self):
        cmd = "cd {} && fio -version".format(os.path.dirname(self.fio_path))
        test_p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (std_output, _) = test_p.communicate()
        finds = re.findall("fio\-([0-9\.]*)", std_output.decode("utf-8"))
        version = finds[0] if finds else 0
        return version

    def check_fio_path(self):
        if os.path.exists(self.fio_path) is False:
            raise Exception("fio did not exists, please install fio, fio install package at: Tools\\fio")

    def run_fio_file(self, fio_case):
        fio_path = self.get_fio_path(fio_case)
        cmd = "fio {}".format(fio_path)
        ret = subprocess.call(cmd, shell=True)
        return ret

    def run_fio_file_auto_detection_dev(self, fio_case):
        ret = -1
        fio_path = self.get_fio_path(fio_case)
        dev = get_linux_nvme_devs()
        if dev:
            dev_name = dev[0]["name"]
            cmd = "cd {} && {} -filename=/dev/{} {}".format(self.fio_path, self.fio_cmd, dev_name, fio_path)
            ret = subprocess.call(cmd, shell=True)
        return ret

    def get_fio_path(self, file_):
        path = self.base.get_file_path(self.fio_file_path, file_)
        if path is None:
            raise Exception("can't find fio config file", file_)
        return path

    def update_fio_arg(self, fio_file, **kwarg):
        fio_path = self.get_fio_path(fio_file)
        content = open(fio_path)
        new_content = ""
        for line in content:
            key = line.split("=")[0].strip()
            if key in kwarg.keys():
                new_line = "{}={} \n".format(key, kwarg[key])
            else:
                new_line = line
            new_content += new_line
        with open(fio_path, "w") as write_file:
            write_file.write(new_content)

    def popen_start_fio(self):
        cmd = self.parse_cmd()
        log.INFO(cmd)
        popen = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        return popen

    def to_byte(self, in_put):
        value_in_byte = -1
        rets = re.findall("([\d\.]+)([A-Za-z]*)", in_put)
        if rets:
            data = float(rets[0][0])
            unit = rets[0][1]
            if "ti" in unit.lower():
                value_in_byte = data*(1024**4)
            elif "gi" in unit.lower():
                value_in_byte = data*(1024**3)
            elif "mi" in unit.lower():
                value_in_byte = data*(1024**2)
            elif "ki" in unit.lower():
                value_in_byte = data*(1024**1)
            elif "ti" not in unit.lower() and "t" in unit.lower():
                value_in_byte = data*(1000**4)
            elif "gi" not in unit.lower() and "g" in unit.lower():
                value_in_byte = data*(1000**3)
            elif "mi" not in unit.lower() and "m" in unit.lower():
                value_in_byte = data*(1000**2)
            elif "ki" not in unit.lower() and "k" in unit.lower():
                value_in_byte = data*(1000**1)
            else:
                value_in_byte = data
        return value_in_byte

    @decorate_collect_real_time_bw_iops
    def analysis_fio_real_time_prints(self, prints):
        read_bw, write_bw, read_iops, write_iops = None, None, None, None
        if self.name == "windows_fio":
            re_patten = "\[([\w\.]+)\/([\w\.]+)\/.+?\]\s+\[([\w\.]+?)\/([\w\.]+?)\/[\w\s]+?iops"
        else:
            re_patten = "r\=([\w\.]+).*?w\=([\w\.]+).*?r\=([\w\.]+).*?w\=([\w\.]+)"
        finds = re.findall(re_patten, prints)[0]
        if finds:
            read_bw, write_bw, read_iops, write_iops = finds[0], finds[1], finds[2], finds[3]
        return self.to_byte(read_bw), self.to_byte(write_bw), self.to_byte(read_iops), self.to_byte(write_iops)

    def collect_prints_util_finished(self, popen, real_time):
        log.INFO("collect_prints_util_finished")
        prints = popen.stdout.readline
        for line in iter(prints, b''):
            try:
                log.INFO(line)
                if popen.poll() is not None:
                    break
                if "eta" in line and real_time == "enable":
                    read_bw, write_bw, read_iops, write_iops = self.analysis_fio_real_time_prints(line)
                    print(line, '\n', read_bw, write_bw, read_iops, write_iops)
            except Exception as all_exception:
                log.ERR(all_exception)
        popen.wait()
        return popen.returncode

    def get_new_fio_out_put_file(self, log_type="fio"):
        result_path = os.path.join(self.working_path, "result")
        if os.path.exists(result_path) is False:
            os.mkdir(result_path)
        fio_result_folder = os.path.join(result_path, "fio")
        if os.path.exists(fio_result_folder) is False:
            os.mkdir(fio_result_folder)
        file_name = "{}_{}.txt".format(log_type, get_time_stamp())
        new_file_path = os.path.join(fio_result_folder, file_name)
        new_bw_log = os.path.join(fio_result_folder, get_time_stamp())
        return new_file_path, new_bw_log

    def optimization_result(self, input_dict):
        if "clat_ns" in input_dict.keys():
            clat_key = "clat_ns"
            clat_base_unit = 1000
        elif "clat_ms" in input_dict.keys():
            clat_key = "clat_ms"
            clat_base_unit = 0.001
        else:
            clat_key = "clat"
            clat_base_unit = 1
        percentile = input_dict[clat_key]["percentile"]
        percentile_list = [percentile["99.000000"]/clat_base_unit,
                           percentile["99.900000"]/clat_base_unit, percentile["99.990000"]/clat_base_unit,
                           percentile["99.999000"]/clat_base_unit, percentile["99.999900"]/clat_base_unit,
                           percentile["99.999990"]/clat_base_unit, percentile["99.999999"]/clat_base_unit]
        result = {"io": input_dict["io_bytes"], "bw": input_dict["bw"], "iops": input_dict["iops"],
                  "avg_latency": input_dict[clat_key]["mean"]/clat_base_unit, "percentiles": percentile_list,
                  "max_latency": input_dict[clat_key]["max"] / clat_base_unit,
                  "min_latency": input_dict[clat_key]["min"] / clat_base_unit}
        return result

    def read_background_read_bw(self):
        file_path = os.path.join(self.working_path, "log", "background_read_bw.txt")
        log_file = open(file_path, mode="r")
        value = log_file.read()
        log_file.close()
        return value

    def write_background_read_bw(self, value):
        file_path = os.path.join(self.working_path, "log", "background_read_bw.txt")
        log_file = open(file_path, mode="w")
        log_file.write(value)
        log_file.close()

    @decorate_collect_summary_result
    def analysis_json_result(self, json_string):
        results = list()
        ret = re.findall(".*(\{[\w\W]*\}).*", json_string)
        if ret:
            output = json.loads(ret[0])
            jobs = output["jobs"]
            if jobs:
                job = jobs[0]
                read_result = {"read": self.optimization_result(job["read"])}
                write_result = {"write": self.optimization_result(job["write"])}
                results.append(read_result)
                results.append(write_result)
                # if str(read_result["read"]["bw"]) != "0.0" and str(read_result["read"]["bw"]) != "0":
                #     self.write_background_read_bw(str(read_result["read"]["bw"]))
        return results

    def nvme_format(self, parameters):
        if "lbaf" in parameters.keys():
            lbaf = parameters["lbaf"]
            if lbaf != "":
                cmd_line = "nvme format {} -l {}".format(parameters["fio"]["filename"], lbaf)
                ret = os.system(cmd_line)
                if ret != 0:
                    print("Format failed, cmd: {}".format(cmd_line))
                else:
                    print("Format succeed, cmd: {}".format(cmd_line))

    @decorate_run_benchmark
    def run_benchmark(self, parameters):
        background_process = None
        parameters = self.add_benchmark_fio_parameter(parameters)
        self.nvme_format(parameters)
        if parameters["background"] != "":
            background_process = self.run_background_traffic(parameters)
        status, output, result = self.run_main_fio_benchmark(parameters)
        if background_process is not None:
            self.kill_fio_process(background_process)
            background_process.kill()
        if parameters["background"] == "" and status == 0:
            self.save_read_bw(result)
        return status, output, result

    @staticmethod
    def add_benchmark_fio_parameter(parameters):
        parameters["fio"]["numa_cpu_nodes"] = 1
        return parameters

    def save_read_bw(self, result):
        log.INFO("save_read_bw , %s", str(result[0]["read"]["bw"]))
        if result:
            if str(result[0]["read"]["bw"]) != "0.0" and str(result[0]["read"]["bw"]) != "0":
                self.write_background_read_bw(str(result[0]["read"]["bw"]))

    def kill_fio_process(self, background_process):
        if "win" in sys.platform:
            command_line = "taskkill  /F /T /PID {}".format(background_process.pid)
        else:
            command_line = "killall -9 fio"
        log.INFO(command_line)
        subprocess.call(command_line, shell=True)

    def process_run_background_traffic(self, parameters):
        self.set_fio_parameters(parameters)
        print("background parameter")
        print(parameters)
        background_process = self.popen_start_fio()
        return background_process

    def random_write_background(self, parameters):
        background_process = None
        rate = self.get_bg_rate(parameters, 0.05)
        if rate != 0:
            random_write_parameters = {
                "rw": "randwrite",
                "ioengine": parameters["fio"]["ioengine"],
                "filename": parameters["fio"]["filename"],
                "continue_on_error": "all",
                "name": "random_write_background",
                "blocksize": "256k",
                "iodepth": "32",
                "numjobs": "1",
                "rwmixread": "0",
                "size": parameters["fio"]["size"],
                "runtime": str(int(parameters["fio"]["runtime"])+10),
                "rate":rate
            }
            background_process = self.process_run_background_traffic(random_write_parameters)
        return background_process

    def get_bg_rate(self, parameters, default=0.1):
        background_read_bw = 0
        if parameters["bg_rate"] == "":
            background_read_bw = self.read_background_read_bw()
            rate = str(float(background_read_bw)*1024*default)
        else:
            bg_rate = float(parameters["bg_rate"])
            if bg_rate > 1:
                rate = bg_rate
            else:
                background_read_bw = self.read_background_read_bw()
                rate = str(float(background_read_bw)*1024*bg_rate)
        log.INFO("FIO background: user input bg_rate: {}, read_bw:{}, rate:{} ".format(parameters["bg_rate"], background_read_bw, rate))
        return rate

    def seq_write_background(self, parameters):
        background_process = None
        rate = self.get_bg_rate(parameters, 0.1)
        if rate != 0:
            seq_write_parameters = {
                "rw": "write",
                "ioengine": parameters["fio"]["ioengine"],
                "filename": parameters["fio"]["filename"],
                "continue_on_error": "all",
                "name": "seq_write_background",
                "blocksize": "256k",
                "iodepth": "32",
                "numjobs": "1",
                "rwmixread": "0",
                "size": parameters["fio"]["size"],
                "runtime": str(int(parameters["fio"]["runtime"])+10),
                "rate": rate
            }
            background_process = self.process_run_background_traffic(seq_write_parameters)
        return background_process

    def run_background_traffic(self, parameters):
        if parameters["background"] == "seq_write":
            background_process = self.seq_write_background(parameters)
        else:
            background_process = self.random_write_background(parameters)
        return background_process

    def set_fio_parameters(self, fio_parameters):
        out_put, bw_log = self.get_new_fio_out_put_file()
        self.clear_parm()
        for key, value in fio_parameters.items():
            if value not in [None, ""]:
                self.set_parm(key, value)
        self.set_parm('direct', "1")
        self.set_parm('percentile_list', "99:99.9:99.99:99.999:99.9999:99.99999:99.999999:99.999999")
        self.set_parm('group_reporting', True)
        self.set_parm('thread', True)
        self.set_parm('eta', "always")
        if "runtime" in fio_parameters.keys():        # when full fill, set size %10, set ramp_time, fio will run cancelled
            if fio_parameters["runtime"] not in ["", "0"]:
                self.set_parm('ramp_time', "60")
        self.set_parm('norandommap ', True)
        self.set_parm('randrepeat', "0")
        self.set_parm('log_avg_msec', "1000")
        self.set_parm('output', out_put)
        self.set_parm("output-format", "json")
        self.set_parm("write_bw_log", bw_log)
        numjobs = fio_parameters["numjobs"]
        bw_logs = list()
        for index in range(int(numjobs)):
            name = "{}_bw.{}.log".format(bw_log, index+1)
            bw_logs.append(name)
        return out_put, bw_logs

    def analysis_fio_report(self, out_put):
        result = list()
        if os.path.exists(out_put):
            output = open(out_put).read()
            try:
                result = self.analysis_json_result(output)
            except Exception as all_exception:
                output = "Fio analysis_json_result failed: {}".format(out_put)
                log.ERR(all_exception)
                log.ERR(output)
        else:
            output = "Log file: {} not exist".format(out_put)
        return output, result

    @decorate_collect_lifetime_bw
    def analysis_bw_logs(self, bw_logs, start_time):
        write_bws = list()
        read_bws = list()
        for bw_log in bw_logs:
            write_logs, read_logs = self.analysis_bw_log(bw_log, start_time)
            write_bws.append(write_logs)
            read_bws.append(read_logs)
        write_bw = self.calc_summer_bw(write_bws)
        read_bw = self.calc_summer_bw(read_bws)
        return write_bw, read_bw

    def calc_summer_bw(self, logs):
        num_jobs = len(logs)
        sum_bw_list = list()
        time_list = list()
        for index in range(num_jobs):
            for item in logs[index]:
                if item["time"] not in time_list:
                    time_list.append(item["time"])
        for item in time_list:
            values_item = list()
            for jobs_index in range(num_jobs):
                values = [item_value["value"] for item_value in logs[jobs_index] if item_value["time"]==item]
                if values:
                    values_item.append(values[0])
            if len(values_item) == num_jobs:
                sum_bw_list.append({"time":item, "value": sum(values_item)})
        return sum_bw_list

    def analysis_bw_log(self, bw_log, start_time):
        write_logs, read_logs = list(), list()
        if os.path.exists(bw_log):
            print(bw_log)
            output = open(bw_log).read()
            try:
                results = re.findall("(\d+)\,\s(\d+)\, (\d+)\,", output)
                for result in results:
                    data = {"time": start_time+timedelta(seconds=round(int(result[0])/1000)), "value": float(result[1])*1024, "index":round(int(result[0])/1000) }
                    if result[2] == "0":
                        read_logs.append(data)
                    elif result[2] == "1":
                        write_logs.append(data)
            except Exception as all_exception:
                log.ERR(all_exception)
        return write_logs, read_logs

    def analysis_result(self, out_put, bw_logs, real_time, start_time):
        output, result = self.analysis_fio_report(out_put)
        if real_time != "enable":
            self.analysis_bw_logs(bw_logs, start_time)
        return output, result

    def run_main_fio_benchmark(self, parameters):
        out_put, bw_logs = self.set_fio_parameters(parameters["fio"])
        start_time = datetime.now(timezone(timedelta(hours=+8)))
        popen = self.popen_start_fio()
        status = self.collect_prints_util_finished(popen, parameters["real_time"])
        output, result = self.analysis_result(out_put, bw_logs, parameters["real_time"], start_time)
        return status, output, result
