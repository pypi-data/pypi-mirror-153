# pylint: disable=broad-except, invalid-name
import datetime
from utils import log
from test_framework.database import SqlConnection
from test_framework.test_environment import Environment
from utils.system import get_time_stamp
from test_framework.state import State

CONFIG_TABLE_COLUM = [
    "config_file",
    "ioengine",
    "blocksize",
    "iodepth",
    "numjobs",
    "rw",
    "rwmixread",
    "size",
    "runtime",
    "type"
]


REAL_TIME_TABLE_COLUM = [
    {"name": "index", "type": "int(11) AUTO_INCREMENT PRIMARY KEY"},
    {"name": "read_iops", "type": "VARCHAR(45)"},
    {"name": "read_bw", "type": "VARCHAR(45)"},
    {"name": "write_iops", "type": "VARCHAR(45)"},
    {"name": "write_bw", "type": "VARCHAR(45)"},
    {"name": "temperature", "type": "VARCHAR(45)"},
    {"name": "time", "type": "datetime DEFAULT CURRENT_TIMESTAMP"}]


LIFE_TIME_TABLE_COLUM = [
    {"name": "index", "type": "int(11)"},
    {"name": "iops", "type": "FLOAT"},
    {"name": "bw", "type": "FLOAT"}]


class PerfSqlConnection(SqlConnection):

    test_index = None
    summary_result_index = None
    real_time_table = None
    life_time_table = None
    env = None

    def __init__(self, db_name="performance_test"):
        super(PerfSqlConnection, self).__init__(db_name=db_name)
        self.test_table = "_tests"
        self.env_table = "_environment"
        self.summary_table = "_summary_test_results"
        self.config_table = "_configuration"

    def create_real_time_table(self):
        table_name = "real_time_table_{}".format(get_time_stamp())
        self.create_table(table_name, REAL_TIME_TABLE_COLUM)
        return table_name

    def insert_real_time_record(self, read_bw, write_bw, read_iops, write_iops):
        temperature = PerfSqlConnection.env.get_temperature()
        self.insert_to_table(PerfSqlConnection.real_time_table, read_iops=read_iops, read_bw=read_bw,
                             write_iops=write_iops, write_bw=write_bw, temperature=str(temperature))

    def create_life_time_table(self):
        table_name = "life_time_table_{}".format(get_time_stamp())
        self.create_table(table_name, LIFE_TIME_TABLE_COLUM)
        return table_name

    def add_environment_record(self, dev_name):
        PerfSqlConnection.env = Environment(dev_name)
        kwargs = PerfSqlConnection.env.get_environments()
        self.insert_to_table(self.env_table, **kwargs)
        index = self.get_last_index(self.env_table)
        return index

    def add_summary_result_record(self):
        self.insert_to_table(self.summary_table, iops_read=0)
        index = self.get_last_index(self.summary_table)
        return index

    def update_record_with_index(self, table, index, **kwargs):
        str_date = ""
        for key, value in kwargs.items():
            temp_str = "{}='{}'".format(key, value)
            str_date = temp_str if str_date == "" else "{},{}".format(str_date, temp_str)
        update_command = "UPDATE {} SET {} where `index`='{}'".format(table, str_date, index)
        self.cursor.execute(update_command)
        self.conn.commit()

    def update_lifetime_bw(self, write_bws, read_bws):
        time_list = list()
        for item in [read_bws, write_bws]:
            for item_ in item:
                if item_["time"] not in time_list:
                    time_list.append(item_["time"])
        value_lists = list()
        for index in time_list:
            write_value =  [item["value"] for item in write_bws if item["time"]==index]
            read_value =  [item["value"] for item in read_bws if item["time"]==index]
            if write_value or read_value:
                rw_item = dict()
                rw_item["time"] = index
                rw_item["write"] = write_value[0] if write_value else 0
                rw_item["read"] = read_value[0] if read_value else 0
                value_lists.append(rw_item)
        for index in value_lists:
            dt = index["time"].strftime("%Y-%m-%d %H:%M:%S")
            self.insert_to_table(PerfSqlConnection.real_time_table, read_iops=0, read_bw=index["read"],
                                 write_iops=0, write_bw=index["write"], temperature=0, time=dt)

    def update_summary_record(self, result):
        read_result = result[0]["read"]
        write_result = result[1]["write"]
        self.update_record_with_index(self.summary_table, PerfSqlConnection.summary_result_index,
                                      iops_read=read_result["iops"], bw_read=read_result["bw"],
                                      io_read=read_result["io"],
                                      avg_latency_read=read_result["avg_latency"],
                                      max_latency_read=read_result["max_latency"],
                                      min_latency_read=read_result["min_latency"],
                                      percent_99_read=read_result["percentiles"][0],
                                      percent_999_read=read_result["percentiles"][1],
                                      percent_9999_read=read_result["percentiles"][2],
                                      percent_99999_read=read_result["percentiles"][3],
                                      percent_999999_read=read_result["percentiles"][4],
                                      percent_9999999_read=read_result["percentiles"][5],
                                      percent_99999999_read=read_result["percentiles"][6],
                                      iops_write=write_result["iops"], bw_write=write_result["bw"],
                                      io_write=write_result["io"],
                                      max_latency_write=write_result["max_latency"],
                                      min_latency_write=write_result["min_latency"],
                                      avg_latency_write=write_result["avg_latency"],
                                      percent_99_write=write_result["percentiles"][0],
                                      percent_999_write=write_result["percentiles"][1],
                                      percent_9999_write=write_result["percentiles"][2],
                                      percent_99999_write=write_result["percentiles"][3],
                                      percent_999999_write=write_result["percentiles"][4],
                                      percent_9999999_write=write_result["percentiles"][5],
                                      percent_99999999_write=write_result["percentiles"][6])

    def update_test_end_time(self):
        end_time = self.get_datetime()
        command = "UPDATE _tests SET end_time='{}' WHERE `index`={}".format(end_time, PerfSqlConnection.test_index)
        self.cursor.execute(command)
        self.conn.commit()

    def update_test_to_finished(self):
        command = "UPDATE _tests SET state='{}' WHERE `index`={}".format(State.PASS, PerfSqlConnection.test_index)
        self.cursor.execute(command)
        self.conn.commit()

    def add_test_configuration_record(self, parameters):
        kwargs = dict()
        kwargs["type"] = "fio"
        for key, value in parameters.items():
            if key in CONFIG_TABLE_COLUM:
                kwargs[key] = value
        self.insert_to_table(self.config_table, **kwargs)
        index = self.get_last_index(self.config_table)
        return index

    def add_new_test_record(self, args):
        env_index = self.add_environment_record(args["fio"]["filename"])
        config_index = self.add_test_configuration_record(args["fio"])
        PerfSqlConnection.summary_result_index = self.add_summary_result_record()
        PerfSqlConnection.real_time_table = self.create_real_time_table()
        # PerfSqlConnection.life_time_table = self.create_life_time_table()
        self.insert_to_table(self.test_table, test_env_index=env_index, key=args["key"],
                             summary_report_index=PerfSqlConnection.summary_result_index,
                             real_time_index=PerfSqlConnection.real_time_table,
                             # life_time_table_index=PerfSqlConnection.life_time_table,
                             config_index=config_index,
                             test_name=args["test_name"],
                             project_name=args["project_name"],
                             state=State.RUNNING,
                             group_name=args["group_name"],
                             group_key=args["group_key"],
                             tester=args["tester"])
        PerfSqlConnection.test_index = self.get_last_index(self.test_table)


def decorate_run_benchmark(func):
    def func_wrapper(*args, **kwargs):
        try:
            perf_sql = PerfSqlConnection()
            perf_sql.add_new_test_record(args[1])
        except Exception as all_exception:
            log.ERR(all_exception)
        ret = func(*args, **kwargs)
        return ret
    return func_wrapper


def decorate_collect_real_time_bw_iops(func):
    def func_wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        try:
            perf_sql = PerfSqlConnection()
            perf_sql.insert_real_time_record(ret[0], ret[1], ret[2], ret[3])
        except Exception as all_exception:
            log.ERR(all_exception)
        return ret
    return func_wrapper


def decorate_collect_summary_result(func):
    def func_wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        try:
            perf_sql = PerfSqlConnection()
            perf_sql.update_test_end_time()
            perf_sql.update_test_to_finished()
            perf_sql.update_summary_record(ret)
        except Exception as all_exception:
            log.ERR(all_exception)
        return ret
    return func_wrapper


def decorate_collect_lifetime_bw(func):
    def func_wrapper(*args, **kwargs):
        ret1, ret2 = func(*args, **kwargs)
        try:
            perf_sql = PerfSqlConnection()
            perf_sql.update_lifetime_bw(ret1, ret2)
        except Exception as all_exception:
            log.ERR(all_exception)
        return ret1, ret2
    return func_wrapper
