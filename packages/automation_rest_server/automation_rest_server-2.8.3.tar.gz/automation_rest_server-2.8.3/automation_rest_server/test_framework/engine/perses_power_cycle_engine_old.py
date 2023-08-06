import os
import re
import time
import checksumdir
from nose.tools import assert_equal
from utils.ssh import SSH
from utils import log
from utils.message import Message
from test_framework.test_base import TestBase
from test_framework.state import State


class PowerCycleEngine(TestBase):

    def __init__(self):
        super(PowerCycleEngine, self).__init__()

    def initialization(self, parameters):
        self.target_ip = os.environ["target_ip"]
        self.user = os.environ.get('user', 'root')
        self.password = os.environ.get('password', 'nvme')
        self.adapter = os.environ.get('adapter', 'usbrelay')
        self.fw_path = os.environ.get('fw_path', 'not_set')
        self.commit = os.environ.get('commit', 'not_set')
        self.ssh = SSH(self.target_ip, username=self.user, password=self.password)
        self.ssh.open()
        self.ssh.command("mount -a")
        self.remote_env_path = self.get_remote_path()
        self.remote_env_perses_path = "{}/{}".format(self.remote_env_path, "perses")
        self.local_env_perses_path = os.environ["working_path"]
        self.setup_target_environment()

    def get_remote_path(self):
        network_path = r"/home/share/sqa/powercycle"
        if self.ssh.is_exist(network_path):
            remote_path = r"/home/share/sqa/powercycle/{}".format(self.target_ip)
        else:
            remote_path = r"/home/powercycle"
        return remote_path

    def remote_install(self, remote_path):
        command = "cd {} && python install.py".format(remote_path)
        status, output = self.ssh.command(command)
        if status != 0:
            print("remotes install failed")
        print(output)
        return status, output

    def dos2unit(self, remote_path):
        paths = ["{}/tools/fio".format(remote_path),
                 "{}/tools/vdbench504".format(remote_path),
                 "{}/tools/usbrelay".format(remote_path)]
        for item in paths:
            command = "cd {} && dos2unix *".format(item)
            status, output = self.ssh.command(command)
            if status != 0:
                print("dos2unit {} install failed".format(item))
            print(output)

    def chmod_files(self, remote_path):
        paths = ["{}/tools/fio/fio".format(remote_path),
                 "{}/tools/vdbench504/vdbench".format(remote_path),
                 "{}/tools/usbrelay/usbrelay".format(remote_path)]
        for item in paths:
            command = "chmod 777 {}".format(item)
            status, output = self.ssh.command(command)
            if status != 0:
                print("chmod  {}  failed".format(item))
            print(output)

    def upload_and_init_perses_2_target(self):
        if self.ssh.is_exist(self.remote_env_path) is False:
            self.ssh.make_dir(self.remote_env_path)
        if self.ssh.is_exist(self.remote_env_perses_path) is False:
            self.ssh.make_dir(self.remote_env_perses_path)
        self.ssh.sftp_put_dir(self.local_env_perses_path, self.remote_env_perses_path)
        self.remote_install(self.remote_env_perses_path)
        self.dos2unit(self.remote_env_perses_path)
        self.chmod_files(self.remote_env_perses_path)

    def update_modified_perses_2_target(self):
        compare_folder = ["configuration", "lib", "testcase", "testsuite", "testfile"]
        for folder in compare_folder:
            local_path = os.path.join(self.local_env_perses_path, folder)
            remote_path = r"{}/{}".format(self.remote_env_perses_path, folder)
            local_md5 = self.get_folder_md5(local_path)
            remote_md5 = self.get_folder_md5_by_ssh(remote_path)
            if local_md5 != remote_md5:
                temp_path = "{}/{}".format(self.remote_env_perses_path, folder)
                self.ssh.command("rm -r {}".format(temp_path))
                self.ssh.make_dir(temp_path)
                self.ssh.sftp_put_dir(local_path, temp_path)

    def update_run_file(self):
        local_path = os.path.join(self.local_env_perses_path, "run.py")
        remote_path = r"{}/{}".format(self.remote_env_perses_path,  "run.py")
        self.ssh.command("rm -r {}".format(remote_path))
        self.ssh.sftp_put(local_path, remote_path)

    def setup_target_environment(self):
        ret = self.ssh.is_exist(self.remote_env_perses_path)
        if ret is False:
            self.upload_and_init_perses_2_target()
        else:
            self.update_modified_perses_2_target()
            self.update_run_file()

    @staticmethod
    def get_folder_md5(path):
        md5hash = None
        if os.path.exists(path):
            md5hash = checksumdir.dirhash(path, 'md5', excluded_extensions=['pyc'])
        return md5hash

    def get_folder_md5_by_ssh(self, path):
        md5 = None
        cmd = "checksumdir -a md5 {}".format(path)
        status, output = self.ssh.command(cmd)
        if status == 0:
            md5 = output.replace("\n", "")
        return md5

    def get_loop(self, test):
        loop = 1
        test_path = re.findall("(.*):", test)[0]
        function_name = re.findall("\w*\:\w*\.(\w*)", test)
        file_ = open(test_path)
        content = file_.read()
        loops = re.findall(".*attr\(loop\=(\d+)\).*\n\s+def\s+{}\(self\)".format(function_name[0]), content)
        loop = loops[0]if loops else loop
        return loop

    def remote_run_test(self, test, loop=1, before_reboot=True):
        before_reboot = "true" if before_reboot is True else "false"
        parameter = "loop:{},before_reboot:{},adapter:{},fw_path:{},commit:{}".format(loop, before_reboot, self.adapter,
                                                                                   self.fw_path, self.commit)
        run_command = "cd {} && python run.py testcase -n {} -v {}".format(self.remote_env_perses_path, test, parameter)
        status, output = self.ssh.command(run_command)
        # log.INFO("Remote_run_test command: %s, status: %s, output:\n %s", run_command, status, output)
        return status, output

    def reboot(self):
        log.INFO("reboot......")
        self.ssh.command_without_result("reboot -nf", timeout=10)
        time.sleep(10)
        self.ssh.close()

    def wait_reboot_complete(self, time_out=600):
        result = False
        start_time = time.time()
        current_time = start_time
        duration = current_time - start_time
        while duration < time_out:
            log.INFO("try to connect target compute: time %s", duration)
            try:
                self.ssh.open(timeout=10)
            except RuntimeError:
                pass
            if self.ssh.is_active():
                self.ssh.command("mount -a")
                log.INFO("reboot succeed")
                result = True
                break
            duration = time.time() - start_time
        return result

    def save_log(self, out_put, test_case):
        log_file = os.path.join(self.get_log_path(), "power_cycle_%s_%s.xml" % (test_case, time.time()))
        file_ = open(os.path.join(log_file), "w")
        file_.write(out_put)
        file_.close()
        return log_file

    def run(self, test_case, test_path, parameters, queue):

        print("Test parameters", parameters)
        self.initialization(parameters)

        loop = self.get_loop(test_path)
        result = State.PASS
        test_message = Message()
        for index in range(int(loop)):
            test_message.add_message("Run Power Cycle test: {}, loop: {}".format(test_case, index))
            status, output1 = self.remote_run_test(test_case, loop=index, before_reboot=True)
            test_message.add_message(output1)
            if status != 0:
                result = State.FAIL
                break
            self.reboot()
            reboot_result = self.wait_reboot_complete()
            if reboot_result is False:
                test_message.add_message("Reboot failed at loop {}".format(index))
                result = State.FAIL
                break
            else:
                test_message.add_message("Reboot succeed at loop {}".format(index))
            status, output2 = self.remote_run_test(test_case, loop=index, before_reboot=False)
            test_message.add_message(output2)
            if status != 0:
                result = State.FAIL
                break
        log_path = self.save_log(test_message.message, test_case)
        result = {"name": test_case, "result": result, "log": log_path}
        queue.put(result)
        return result
