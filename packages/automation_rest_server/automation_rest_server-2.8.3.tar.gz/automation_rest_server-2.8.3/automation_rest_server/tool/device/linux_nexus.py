
import os
import re
from tool.device.library.nexus import Ioctl
from tool.device.library.nvme_cmd import SmartHealth, NamespaceDataStructure
from utils.buf import Malloc
from utils.system import execute


class NVME(object):

    def __init__(self, dev_index=0):
        self.dev_index = dev_index

    def list_dev(self):
        dev_list = list()
        cmd = "lsblk"
        _, outs = execute(cmd)
        rets = re.findall("((nexus|nvme)\w+)", outs, re.DOTALL)
        if rets:
            for item in rets:
                ret_index = re.findall("(nexus|nvme)(\d+)n", item[0])
                if ret_index:
                    dev_index = ret_index[0][1]
                    dev = {"index": dev_index, "name": item[0]}
                    dev_list.append(dev)
        if dev_list:
            self.dev_index = dev_list[0]["index"]
        print(dev_list)
        return dev_list

    def getlog(self, lid=0x01, numd=100, numdu=0, lpol=0, lpou=0, nsid=0, type_=SmartHealth):
        dev_name = "/dev/nexus{}".format(self.dev_index)
        nvme_device = Ioctl(dev_name)
        ret, prp = None, None
        if lid == 0x02:
            prp = Malloc(length=1, types=type_)
            ret = nvme_device.get_log_page(nsid=nsid, lid=lid, ndw=numd, lsi=0, prp1_off=0, prp2_off=0, pdata=prp)
        return ret, prp

    def identify(self, cns, cntid, nsid, types):
        dev_name = "/dev/nexus{}".format(self.dev_index)
        nvme_device = Ioctl(dev_name)
        ret = 0
        prp = nvme_device.identify(cns, nsid, 0, 0, 0)
        return ret, prp

    def upgrade_fw(self, fw_path, device_index, slot):
        dev_name = "/dev/nexus{}".format(device_index)
        nvme_device = Ioctl(dev_name)
        length, pdata = self.get_firmware_buf(fw_path)
        ret = nvme_device.fw_download(length // 4, 0, 0, pdata)
        msg = "fw download:{}".format(ret)
        ret = nvme_device.fw_active(int(slot), 1, 0)
        msg = "{} \n fw commit: {}".format(msg, ret)
        if ret == 0:
            ret = nvme_device.controller_reset()
        result = True if ret == 0 else False
        print(msg)
        return result, msg

    @staticmethod
    def get_download_buf(source_buf, offset, length):
        buf = Malloc(length)
        buf.memmove(0, source_buf, offset, length)
        return  buf

    @staticmethod
    def get_firmware_buf(fw_path):
        size = os.path.getsize(fw_path)
        print(size)
        fw_file = open(fw_path, "rb")
        fw_data = fw_file.read()
        f_buf = Malloc(size)
        f_buf.memcopy(fw_data, 0, size)
        return int(size), f_buf
