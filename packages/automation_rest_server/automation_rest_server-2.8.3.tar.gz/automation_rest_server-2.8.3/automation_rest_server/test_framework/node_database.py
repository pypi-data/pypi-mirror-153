# pylint: disable=broad-except, invalid-name
import os
from datetime import datetime, timezone, timedelta
from utils import log
from test_framework.database import SqlConnection
from test_framework.state import NodeState
from utils.system import get_ip_address, get_automation_platform


NODE_STATE_TABLE_COLUM = [
    {"name": "index", "type": "int(11) AUTO_INCREMENT PRIMARY KEY"},
    {"name": "state", "type": "VARCHAR(45)"},
    {"name": "time", "type": "datetime DEFAULT CURRENT_TIMESTAMP"}]


class NodeSqlConnection(SqlConnection):

    def __init__(self, db_name="nodes"):
        super(NodeSqlConnection, self).__init__(db_name=db_name)
        self.node_table = "node"

    def get_datetime(self):
        tz = timezone(timedelta(hours=+8))
        current_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return current_time

    def create_node_state_table(self, node_ip, port):
        table_name ="{}:{}".format(node_ip, port)
        if self.is_exist_table(table_name) is False:
            self.create_table(table_name, NODE_STATE_TABLE_COLUM)
        return table_name

    def create_new_node(self, node, port):
        table_name = self.create_node_state_table(node["ip"], port)
        update_time = self.get_datetime()
        self.insert_to_table("node", vendor=node["vendor_name"],
            ip=node["ip"],
            name="env_{}".format(node["ip"]),
            system=node["operating_system"],
            capacity=node["capacity"],
            fw=node["fw_version"],
            state=NodeState.verdicts_map[NodeState.Idle],
            state_table=table_name,
            port=port,
            update_time=update_time)

    def update_exist_node(self, node, port):
        update_time = self.get_datetime()
        platform = get_automation_platform()
        str_date = "`system`='{}',capacity='{}',fw='{}',vendor='{}', update_time='{}',platform='{}'".format(
            node["operating_system"], node["capacity"], node["fw_version"],
            node["vendor_name"], update_time, platform)
        update_command = "UPDATE node SET {} WHERE ip='{}' AND port='{}'".format(str_date, node["ip"], port)
        self.cursor.execute(update_command)
        self.conn.commit()

    def is_exist_node(self, node, port):
        sql_command = "SELECT * from node WHERE ip='{}' AND port='{}'".format(node["ip"], port)
        self.cursor.execute(sql_command)
        gets = self.cursor.fetchone()
        result = True if gets else False
        return result

    def get_node_table_name(self, ip, port):
        sea_string = "SELECT state_table FROM node WHERE `ip`='{}' AND `port`={}".format(ip, port)
        table_name = self.execute_sql_command(sea_string)
        table_name = table_name[0][0] if table_name else None
        return table_name

    def update_node_state(self, state):
        ip_address = get_ip_address()
        port = os.environ.get('prun_port', '5000')
        table = self.get_node_table_name(ip_address, port)
        if table is not None:
            self.insert_to_table(table, state=NodeState.verdicts_map[state])

    def node_heart_beat(self, state):
        ip_address = get_ip_address()
        port = os.environ.get('prun_port', '5000')
        update_time = self.get_datetime()
        str_date = "`state`='{}', update_time='{}'".format(state, update_time)
        update_command = "UPDATE node SET {} WHERE ip='{}' AND port='{}'".format(str_date, ip_address, port)
        self.cursor.execute(update_command)
        self.conn.commit()


    def update_power_cycle_node_state(self, state):
        if "TARGETIP" in os.environ.keys():
            target_ip = os.environ['TARGETIP']
            port = os.environ.get('prun_port', '5000')
            if target_ip != "0.0.0.0":
                table = "`{}:{}`".format(target_ip, port)
                if self.is_exist_table(target_ip) is True:
                    self.insert_to_table(table, state=NodeState.verdicts_map[state])


def update_env_state(func):
    def func_wrapper(*args, **kwargs):
        node = func(*args, **kwargs)
        try:
            port = os.environ.get('prun_port', '5000')
            sql_connection = NodeSqlConnection()
            if sql_connection.is_exist_node(node, port) is True:
                sql_connection.update_exist_node(node, port)
            else:
                sql_connection.create_new_node(node, port)
        except Exception as all_exception:
            log.ERR(all_exception)
        return node
    return func_wrapper


def update_node_state(func):
    def func_wrapper(*args, **kwargs):
        is_updated, state = func(*args, **kwargs)
        if is_updated is True:
            try:
                sql_connection = NodeSqlConnection()
                sql_connection.update_node_state(state)
                sql_connection.update_power_cycle_node_state(state)
            except Exception as all_exception:
                log.ERR(all_exception)
        return is_updated, state
    return func_wrapper


def node_heart_beat(func):
    def func_wrapper(*args, **kwargs):
        state = func(*args, **kwargs)
        try:
            sql_connection = NodeSqlConnection()
            sql_connection.node_heart_beat(state)
        except Exception as all_exception:
            log.ERR(all_exception)
        return state
    return func_wrapper
