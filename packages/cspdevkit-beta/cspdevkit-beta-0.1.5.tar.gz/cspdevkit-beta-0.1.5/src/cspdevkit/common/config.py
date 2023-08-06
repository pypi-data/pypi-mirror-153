#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/5/18 10:39
# @Author  : xgy
# @Site    : 
# @File    : config.py
# @Software: PyCharm
# @python version: 3.7.4
"""
import os
import json
import yaml

parent_path = os.path.dirname(os.path.split(os.path.realpath(__file__))[0])
interface_file = os.path.join(parent_path, "common/config", "interface.yaml")


class Configure:

    def __init__(self, path=interface_file):
        self.path = path

    @property
    def data(self):
        with open(self.path, "r", encoding="utf-8") as fr:
            if self.path.endswith("yaml"):
                config_dict = yaml.load(fr, Loader=yaml.FullLoader)
            if self.path.endswith(".json"):
                config_dict = json.load(fr)

            return config_dict


if __name__ == '__main__':
    print("start")
