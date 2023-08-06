#!/usr/bin/env python
"""
Created on 2018/8/28

@author: Yingjun Yang
"""
import os
import sys
from ctypes import CDLL


class Load(object):
    """
    Class for load dll/shared library/class
    """
    def __init__(self):
        self.path = os.path.realpath(os.path.join(os.path.dirname(__file__)))

    def cdll_nvme(self):
        """
        Load nvme.so
        :return: Handle of nvme.so
        """
        if 'linux' not in sys.platform:
            raise EnvironmentError("Unsupported OS: {}".format(sys.platform))

        load_file = os.path.join(self.path, 'nvme.so')
        return CDLL(load_file)

    def cdll_dev(self):
        """
        Load dev.so
        :return: Handle of dev.so/dev.dll
        """
        dev = 'dev.so' if 'linux' in sys.platform else 'dev.dll'

        load_file = os.path.join(self.path, dev)
        return CDLL(load_file)

    def cdll_buf(self):
        """
        Load buf.so or class Buf
        :return: Handle of buf.so or Buf()
        """
        if "linux" in sys.platform:
            load_file = os.path.join(self.path, "buf.so")
            return CDLL(load_file)

    def cdll_pci(self):
        load_file = os.path.join(self.path, 'pci.so')
        return CDLL(load_file)
