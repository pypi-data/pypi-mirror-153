
import os
import struct
import platform
from ctypes import windll, byref, string_at, PyDLL, WinDLL
from utils.buf import Malloc
from .library.nvme_cmd import SmartHealth, DevList


class NVME(object):

    def __init__(self, dev_index=None):
        self.dev_index = dev_index
        self.__dll = self.load_dll()

    def load_dll(self):
        path = self.get_dll_path()
        python_version = platform.python_version()
        versoin_list = python_version.split(".")
        if (int(versoin_list[0])==3 and int(versoin_list[1])>7) or (int(versoin_list[0])>3):
            print("load dll with windome")
            dll = WinDLL(path, winmode=0)
        else:
            print("load dll without windome")
            dll = WinDLL(path)
        return dll

    @staticmethod
    def get_dll_path():
        bit = struct.calcsize("P")
        if bit == 4:
            dll_path = os.path.realpath(os.path.join(os.path.dirname(__file__), "library", "nvme_ioctl_32.dll"))
        else:
            dll_path = os.path.realpath(os.path.join(os.path.dirname(__file__), "library", "nvme_ioctl_64.dll"))
        return dll_path

    def getlog(self, lid=0x01, numd=100, numdu=0, lpol=0, lpou=0, nsid=0, type_=SmartHealth):
        ret, prp = None, None
        if lid == 0x02:
            ret, prp = self.get_smart_log()
        return ret, prp

    def get_smart_log(self):
        prp = Malloc(types=SmartHealth)
        ret = self.__dll.get_smartlog(self.dev_index, prp.buffer())
        if ret != 0:
            print("get smart log failed")
        return ret, prp

    def identify(self, cns, cntid, nsid, types):
        prp = Malloc(types=types)
        ret = -1
        if cns == 0x1:
            ret = self.__dll.identify_controller(self.dev_index, prp.buffer())
        elif cns == 0x11:
            ret = self.__dll.identify_namespace(self.dev_index, prp.buffer())
        return ret, prp

    def upgrade_fw(self, fw_path, device_index, slot):
        print(fw_path, device_index, slot)
        char_pointer = bytes(fw_path, "gbk")
        char_ret = self.__dll.upgrade_fw(int(device_index), int(slot), char_pointer)
        result = string_at(char_ret).decode("gbk")
        print(result)
        if "Firmware activate succeeded" in result:
            return True, result
        return False, result

    def list_dev(self):
        dev_list = list()
        devs = DevList()
        self.__dll.list_device(byref(devs))
        print("get devs")
        for index in range(devs.number):
            dev = {"index": devs.index, "name": devs.name}
            dev_list.append(dev)
        if dev_list:
            self.dev_index = dev_list[0]["index"]
        return dev_list


a = NVME()