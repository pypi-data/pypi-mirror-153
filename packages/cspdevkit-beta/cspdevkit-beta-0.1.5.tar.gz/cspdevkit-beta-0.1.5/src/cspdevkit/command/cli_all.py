#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/4/24 11:04
# @Author  : xgy
# @Site    : 
# @File    : cli_all.py
# @Software: PyCharm
# @python version: 3.7.4
"""
from cspdevkit.command.cli import csptools

# datatool 命令引入
from cspdevkit.datatool.datatool_cli import datatool

# dataset 命令引入
from cspdevkit.dataset.dataset_cli import dataset

# resources 命令引入
from cspdevkit.resources.resources_cli import resources

# unst2st
from cspdevkit.thirdparty.unst2st.unst2st_cli import unst2st


if __name__ == '__main__':
    print("start")
