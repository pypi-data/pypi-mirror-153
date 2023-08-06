#!/usr/bin/env python

# !/usr/bin/env python
"""
This is SSH commands

@author: Yingjun Yang
"""
import os
import sys
import binascii
import socket
import time

import paramiko

from utils import log


class SSH(object):
    def __init__(self, hostname, port=22, username='root', password='nvme', mode='rdma'):
        self._hostname = hostname
        self._port = port
        self._mac = None
        self._username = username
        self._password = password
        self._mode = mode

        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self._platform = None
        self._uptime = None
        self._lib_path = '/tmp'
        self._lib_name = 'lib.py'
        self._device = '/dev/nvme'

    @property
    def _local_time(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

    @property
    def platform(self):
        return self._platform

    @property
    def uptime(self):
        return self._uptime

    @property
    def mac(self):
        return self._mac

    def _get_mac(self):
        cmd = 'python -c "' \
              'import re, uuid; ' \
              'print(\'-\'.join(re.findall(r\'.{2}\', uuid.uuid1().hex[-12:].upper())))"'
        status, output = self.command(cmd, cmdline=False, console=False)
        if status:
            log.ERR(output)
            raise RuntimeError('Get MAC address failed!!')

        return output.strip()

    def open(self, timeout=30, interval=3):
        """
        Open ssh connection
        :param timeout:  timeout (in seconds) for open
        :param interval: timeout (in seconds) for ssh connect
        :return:
        """
        log.INFO("Connecting %s:%d", self._hostname, self._port)

        tm_bgn = time.time()
        while True:
            try:
                self._ssh.connect(self._hostname,
                                  port=self._port,
                                  username=self._username,
                                  password=self._password,
                                  timeout=interval)
                break
            except KeyboardInterrupt:
                raise
            except Exception:
                pass

            if time.time() - tm_bgn >= timeout:
                raise RuntimeError("Connect {}:{} timeout({}s)".format(self._hostname, self._port, timeout))

        self._platform = self._get_platform()
        self._uptime = self._get_uptime()
        self._mac = self._get_mac()

    def close(self):
        self._ssh.close()

    def __del__(self):
        self.close()

    def _get_platform(self):
        """
        Get platform of remote PC
        :return:
        """
        status, output = self.command(
            'python -c "import platform; print(platform.platform())"', cmdline=False, console=False)
        if status:
            log.ERR(output)
            raise RuntimeError("Get platform of remote system failed!")

        platform = output.strip()
        log.INFO(platform)
        return platform

    def _get_uptime(self):
        """
        Get boot time of remote PC
        :return:
        """
        status, output = self.command(
            'python -c "import psutil; print(psutil.boot_time())"', cmdline=False, console=False)
        if status:
            log.ERR(output)
            raise RuntimeError('Get uptime of remote system failed!')

        # log.INFO(datetime.datetime.fromtimestamp(uptime).strftime("%Y-%m-%d %H:%M:%S"))
        log.INFO('Up time: %.1fs', time.time() - float(output))
        return float(output)

    def is_active(self):
        """
        Check the connection of SSH is active or not
        :return:
        """
        if self._ssh:
            transport = self._ssh.get_transport()
            if transport:
                return transport.is_alive()
        return False

    def sftp_put(self, filename, filepath):
        """
        SFTP put file to remote path
        :param filename:
        :param filepath:
        :return:
        """
        sftp = self._ssh.open_sftp()
        sftp.put(filename, filepath)
        sftp.close()

    def is_exist(self, path):
        sftp = self._ssh.open_sftp()
        try:
            sftp.stat(path)
            sftp.close()
            return True
        except IOError:
            sftp.close()
            return False

    def make_dir(self, path):
        sftp = self._ssh.open_sftp()
        sftp.mkdir(path)
        sftp.close()

    def remove_dir(self, path):
        sftp = self._ssh.open_sftp()
        sftp.rmdir(path)
        sftp.close()

    def __get_all_files_in_local_dir(self, local_dir):
        all_files = list()
        files = os.listdir(local_dir)
        for file_name in files:
            file_ = os.path.join(local_dir, file_name)
            if os.path.isdir(file_):
                if file_ not in [os.path.join(local_dir, ".git"), os.path.join(local_dir, ".idea")]:
                    all_files.append((file_, "folder"))
                    all_files.extend(self.__get_all_files_in_local_dir(file_))
            else:
                all_files.append((file_, "file"))
        return all_files

    def sftp_put_dir(self, local_dir, remote_dir):
        sftp = self._ssh.open_sftp()
        all_files = self.__get_all_files_in_local_dir(local_dir)
        for item in all_files:
            rel_path = os.path.relpath(item[0], local_dir)
            remote_path = os.path.join(remote_dir, rel_path)
            remote_path = remote_path.replace("\\", "/")
            if item[1] == "file":
                sftp.put(item[0], remote_path)
            else:
                sftp.mkdir(remote_path)
        sftp.close()

    def execute(self, cmd, cmdline=True, timeout=None):
        """
        Execute command without waiting result
        :param cmd:     the command
        :param cmdline: print the command
        :param timeout: an optional timeout (in seconds) for the command
        :return:
        """
        if cmdline:
            log.INFO(cmd)

        if not self.is_active():
            self.open()

        self._ssh.exec_command(cmd, timeout=timeout)

    def command(self, cmd, cmdline=True, timeout=None, console=True):
        """
        Run command through ssh
        :param cmd:     the command
        :param cmdline: print the command
        :param timeout: an optional timeout (in seconds) for the command
        :param console: output to console
        :return:
        """
        if cmdline:
            log.INFO(cmd)

        if not self.is_active():
            self.open()

        _, stdout, stderr = self._ssh.exec_command(cmd, timeout=timeout)
        output = str()
        while True:
            line = stdout.readline()
            if not line:
                break

            output += line
            if console:
                sys.stdout.write(line)

        status = stdout.channel.recv_exit_status()
        output += stderr.read().decode('utf-8')
        return status, output

    def command_without_result(self, cmd, cmdline=True, timeout=None):
        if cmdline:
            log.INFO(cmd)
        if not self.is_active():
            self.open()
        self._ssh.exec_command(cmd, timeout=timeout)

    def list_disk(self):
        """
        List disk of remote PC
        :return:
        """
        status, output = self.command(
            'python -c "import psutil; print(psutil.disk_io_counters(perdisk=True))"',
            cmdline=False, console=False)
        if status:
            log.ERR(output)
            raise RuntimeError('List disk failed, status: {:#x}'.format(status))
        return output

    def reboot(self, overtime=30, option=''):
        """
        Reboot controlled computer
        :param overtime: overtime (in seconds) for reboot
        :param option:   option for reboot
        :return:
        """
        cmd = "reboot" if 'Linux' in self.platform else 'shutdown -r -t 1'
        if option:
            cmd = '{} {}'.format(cmd, option)

        self.execute(cmd, cmdline=True)
        self.close()
        time.sleep(overtime)

    def shutdown(self, overtime=30, option='', rmmod=True):
        """
        Shutdown controlled computer
        :param overtime: overtime (in seconds) for shutdown
        :param option:   option for shutdown
        :param rmmod:   rmmod nvme before power off
        :return:
        """
        if 'Linux' in self.platform:
            if rmmod:
                cmd = 'rmmod nvme'
                status, output = self.command(cmd, cmdline=True)
                assert status == 0, '{} failed!\nStatus: {:#x}\n{}'.format(cmd, status, output)

            cmd = "poweroff"
        else:
            cmd = 'shutdown -s -t 1'

        if option:
            cmd = '{} {}'.format(cmd, option)

        self.execute(cmd, cmdline=True)
        self.close()
        time.sleep(overtime)
