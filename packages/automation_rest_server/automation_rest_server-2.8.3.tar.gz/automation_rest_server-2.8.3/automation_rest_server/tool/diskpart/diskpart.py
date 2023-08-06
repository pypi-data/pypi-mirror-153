#! /usr/bin/python
## -*- coding: utf-8 -*-
import os
import subprocess


def format_raw():
    disk_part_cfg = os.path.join(os.path.dirname(__file__), "..", "..", "..", "Tools", "diskpart")
    cmd_dp = "cd /d {} && Diskpart -s raw.txt".format(disk_part_cfg)
    subprocess.call(cmd_dp, shell=True)

def format_x():
    disk_part_cfg = os.path.join(os.path.dirname(__file__), "..", "..", "..", "Tools", "diskpart")
    cmd_dp = "cd /d {} && Diskpart -s x.txt".format(disk_part_cfg)
    subprocess.call(cmd_dp, shell=True)

def format_gpt():
    disk_part_cfg = os.path.join(os.path.dirname(__file__), "..", "..", "..", "Tools", "diskpart")
    cmd_dp = "cd /d {} && Diskpart -s gpt.txt".format(disk_part_cfg)
    subprocess.call(cmd_dp, shell=True)
