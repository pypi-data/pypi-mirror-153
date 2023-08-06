import os
import re
import yaml
import shutil
import time
from tool.git.git_operator import GitOperator
from utils import log
from utils.system import execute, get_time_stamp


class FirmwareBuildEngine(object):

    def __init__(self):
        self.commit = ""
        self.root_path = None
        self.remote_path = None
        self.build_paras = None
        self.log_path = None

    def get_log_path(self):
        log_path = os.path.join(self.root_path, "log")
        if os.path.exists(log_path) is False:
            os.mkdir(log_path)
        return log_path

    def save_msg(self, msg):
        log_file = "Build_fw_{}_{}.log".format(self.commit, time.time())
        log_path = os.path.join(self.log_path, log_file)
        with open(log_path, "w", encoding='utf-8') as file_:
            file_.write(msg)
        return log_path

    def get_public_paras(self, project):
        ret = False
        git_config = os.path.join(os.path.dirname(__file__), "..", "..", "configuration", "firmware_build.yaml")
        with open(git_config, "r", encoding='utf-8') as f_:
            cont = f_.read()
            configs = yaml.load(cont)
            if project in configs.keys():
                self.root_path = configs["root_path"]
                self.remote_path = configs["remote_firmware"]
                self.build_paras = configs[project]
                ret = True
        return ret

    def check_root_path(self):
        if os.path.exists(self.root_path) is False:
            os.makedirs(self.root_path)

    def precondition(self, project):
        ret = self.get_public_paras(project)
        if ret is True:
            self.check_root_path()
            self.log_path = self.get_log_path()
        return ret

    def run(self, para):
        print("build parameter", para)
        if self.precondition(para["project"]):
            ret, update_msg = self.update_code(para["rep_user"], para["rep_password"], para["rep_url"], para["rep_branch"])
            if ret == 0:
                commit_path = self.is_commit_exist()
                if commit_path is None:
                    ret, fw_bin_path, build_msg = self.build_firmware()
                else:
                    ret, fw_bin_path, build_msg = 0, commit_path, "Find exist commit path"
            else:
                fw_bin_path, build_msg = "",  "Update code failed, skip build firmware"
            log_path = self.save_msg("{}\n{}".format(update_msg.message, build_msg))
        else:
            log_path = self.save_msg("Not found Project build config: {}".format(para["project"]))
            ret, fw_bin_path = -1, ""
        return ret, fw_bin_path, log_path, self.commit

    def is_commit_exist(self):
        if self.remote_path is not None and self.commit != "":
            for item in os.listdir(self.remote_path):
                if self.commit in item:
                    log.INFO("Find exist commit folder {} in {}".format(item, self.remote_path))
                    return os.path.join(self.remote_path, item)
        return None

    def build_firmware(self):
        ret = None
        msg = ""
        remote_path = os.path.join(self.remote_path, "{}_{}".format(get_time_stamp(), self.commit))
        if os.path.exists(remote_path) is False:
            log.INFO("Create folder: {}".format(remote_path))
            os.mkdir(remote_path)
        for build in self.build_paras:
            if build["output"] is not None:
                output_path = os.path.join(self.root_path, build["output"])
                self.clear_output(output_path, build["artifact"])
            ret, output = self.execute_build_command(build["cmd"])
            msg = "{}\n{}".format(msg, output)
            log.INFO("{}, result: {}".format(build["cmd"], ret))
            if ret == 0:
                if build["output"] is not None:
                    self.archiving_artifacts(build, remote_path)
        return ret, remote_path, msg

    def archiving_artifacts(self, build, remote_path):
        log.INFO("archiving_artifacts")
        if self.commit is not None:
            for item in os.listdir(os.path.join(self.root_path, build["output"])):
                if self.check_file_type(item, build["artifact"]):
                    new_file_name = self.get_new_artifact_name(item, self.commit)
                    scr_file = os.path.join(self.root_path, build["output"], item)
                    dest_file = os.path.join(remote_path, new_file_name)
                    log.INFO("Copy file: {} to {}".format(scr_file, dest_file))
                    shutil.copyfile(scr_file, dest_file)

    @staticmethod
    def get_new_artifact_name(file_name, commit):
        items = file_name.split(".")
        if len(items) == 2:
            new_name = "{}_{}.{}".format(items[0], commit, items[1])
        else:
            new_name = file_name
        return new_name

    def execute_build_command(self, command_line):
        cmd = "cd {} && {}".format(self.root_path, command_line)
        status, output = execute(cmd)
        return status, output

    def clear_output(self, path, file_types):
        for item in os.listdir(path):
            if os.path.isfile(os.path.join(path, item)):
                if self.check_file_type(item, file_types) is True:
                    os.remove(os.path.join(path, item))
                    log.INFO("Firmware build delete file: {}".format(item))

    @staticmethod
    def check_file_type(file_name, file_types):
        for item in file_types:
            if file_name.endswith(item) is True:
                return True
        return False

    @staticmethod
    def get_url_folder(url):
        rets = re.findall("/(\w*)\.git", url)
        if rets:
            folder_name = rets[0]
        else:
            folder_name = ""
        return folder_name

    def update_code(self, rep_user, rep_pwd, rep_url, rep_branch):
        rep_folder = os.path.join(self.root_path, self.get_url_folder(rep_url))
        if os.path.exists(rep_folder):
            git_operator = GitOperator(rep_user, rep_pwd, rep_folder)
            result = git_operator.update_code(rep_branch)
        else:
            git_operator = GitOperator(rep_user, rep_pwd, self.root_path)
            result = git_operator.clone(rep_url, rep_branch)
        self.commit = git_operator.commit
        return result, git_operator.message
