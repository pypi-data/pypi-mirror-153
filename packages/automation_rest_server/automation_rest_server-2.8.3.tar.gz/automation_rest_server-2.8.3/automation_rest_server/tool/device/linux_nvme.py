
import os
import re
from tool.device.library.nvme import NVMe
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
        dev_name = "/dev/nvme{}".format(self.dev_index)
        nvme_device = NVMe(dev_name)
        ret, prp = None, None
        if lid == 0x02:
            prp = Malloc(length=1, types=type_)
            ret = nvme_device.nvme_smart_log(nsid, prp.buffer())
        return ret, prp

    def identify(self, cns, cntid, nsid, types):
        dev_name = "/dev/nvme{}".format(self.dev_index)
        nvme_device = NVMe(dev_name)
        prp = Malloc(types=types)
        ret = -1
        if cns == 0x1:
            ret = nvme_device.nvme_identify_ctrl(prp.buffer())
        elif cns == 0x11:
            ret = nvme_device.nvme_identify_ns(nsid, False, prp.buffer())
        return ret, prp

    def upgrade_fw(self, fw_path, device_index, slot):
        dev_name = "/dev/nvme{}".format(device_index)
        nvme_device = NVMe(dev_name)
        length, pdata = self.get_firmware_buf(fw_path)
        download_length = length
        download_offset = 0
        ret = 0
        while download_length > 0 and ret == 0:
            temp_length = 4096 if download_length > 4096 else download_length
            temp_buf = self.get_download_buf(pdata, download_offset, temp_length)
            ret = nvme_device.nvme_fw_download(download_offset, temp_length, temp_buf.buffer())
            download_offset += temp_length
            download_length -= temp_length
        msg = "fw download:{}".format(ret)
        ret = nvme_device.nvme_fw_commit(int(slot), 1, bpid=0)
        msg = "{} \n fw commit: {}".format(msg, ret)
        if ret == 0:
            ret = nvme_device.nvme_reset_controller()
        result = True if ret == 0 else False
        print(msg)
        return result, msg

    @staticmethod
    def get_download_buf(source_buf, offset, length):
        buf = Malloc(length)
        buf.memmove(0, source_buf, offset, length)
        return buf

    @staticmethod
    def get_firmware_buf(fw_path):
        size = os.path.getsize(fw_path)
        print(size)
        fw_file = open(fw_path, "rb")
        fw_data = fw_file.read()
        f_buf = Malloc(size)
        f_buf.memcopy(fw_data, 0, size)
        return int(size), f_buf

    def format(self, name_space, lbaf):
        dev_name = "/dev/nvme{}".format(self.dev_index)
        nvme_device = NVMe(dev_name)
        ret = nvme_device.nvme_format(name_space, lbaf, ses=0, pi=0, pil=0, ms=0, timeout=5)
        print("NVME Format: {},  result: {}".format(dev_name, ret))
        return ret
