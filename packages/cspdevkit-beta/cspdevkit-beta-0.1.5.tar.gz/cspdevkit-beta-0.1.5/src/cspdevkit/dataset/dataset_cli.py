#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/5/18 9:44
# @Author  : xgy
# @Site    : 
# @File    : dataset_cli.py
# @Software: PyCharm
# @python version: 3.7.4
"""

import click
from cspdevkit.command.cli import csptools
from cspdevkit.dataset.dataset_server import data_list, data_download


# 一级命令 CSPtools dataset
@csptools.group("dataset")
def dataset():
    """
    CSPTools dataset Command line \n the tools for dataset,such as list and download
    """


## 数据集资源展示
@dataset.command()
@click.option("-n", "--name", help="the name of dataset", default=None)
def list(name):
    """
    CSPTools dataset list line
    """
    data_list(name)


## 数据集资源下载
@dataset.command()
@click.option("-n", "--name", help="the name of dataset", default=None)
@click.option("-m", "--mode", type=click.Choice(['raw', 'train', 'eva']),
              prompt="the mode of dataset", help="the model of dataset", required=True)
@click.option("-s", "--size", help="the size of dataset will be download", default=None)
@click.option("-o", "--output", help="the folder to save dataset", required=True)
def download(name, mode, size, output):
    """
    CSPTools dataset download line
    """
    data_download(name, mode, size, output)


if __name__ == '__main__':
    print("start")
