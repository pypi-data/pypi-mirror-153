#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/5/27 15:25
# @Author  : xgy
# @Site    : 
# @File    : unst2st_cli.py
# @Software: PyCharm
# @python version: 3.7.4
"""

import click
from cspdevkit.command.cli import csptools
from cspdevkit.thirdparty import Unst2st


# 一级命令 CSPtools unst2st
@csptools.group("unst2st")
def unst2st():
    """
    CSPTools unst2st Command line
    """


## 纯文本抽取
@unst2st.command()
@click.option("-v", "--version", help="the version of server images", required=True)
@click.option("-p", "--port", help="the port for server container", required=True)
@click.option("-c", "--c_name", help="the container name", required=True, default=None)
@click.option('-r', is_flag=True, help="Re query image information.Indicates true when it appears")
@click.option("-i", "--file", help="the input file", required=True)
@click.option("-o", "--output", help="the folder to save output txt file", default=None)
def extract_text(version, port, c_name, r, file, output):
    """
    CSPTools unst2st extract_text line
    """
    unst2st = Unst2st(version=version, port=port, c_name=c_name, reload=r)
    result = unst2st.extract_text(file, output)
    print(result)


## 去水印
@unst2st.command()
@click.option("-v", "--version", help="the version of server images", required=True)
@click.option("-p", "--port", help="the port for server container", required=True)
@click.option("-c", "--c_name", help="the container name", required=True, default=None)
@click.option('-r', is_flag=True, help="Re query image information.Indicates true when it appears")
@click.option("-i", "--in_file", help="the input file", required=True)
@click.option("-o", "--out_file", help="the out file", required=True)
def remove_watermark(version, port, c_name, r, in_file, out_file):
    """
    CSPTools unst2st extract_text line
    """
    unst2st = Unst2st(version=version, port=port, c_name=c_name, reload=r)
    unst2st.remove_watermark(in_file, out_file)


if __name__ == '__main__':
    print("start")
