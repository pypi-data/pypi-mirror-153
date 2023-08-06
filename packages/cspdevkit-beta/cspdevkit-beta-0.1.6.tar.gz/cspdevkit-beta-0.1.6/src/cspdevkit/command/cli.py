#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/3/25 9:34
# @Author  : xgy
# @Site    : 
# @File    : cli.py
# @Software: PyCharm
# @python version: 3.7.4
"""
import click
import os
import sys


# 与setup.py中版本同步修改
__version__ = "0.1"
pgk_dir = os.path.join(os.path.dirname(os.path.abspath('__file__')))


# 主组命令 CSP
# 在setup的entry_points字段中指定
@click.group(context_settings={'help_option_names': ['-h', '--help']}, invoke_without_command=True)
@click.version_option('{0} from {1} (Python {2})'.format(__version__, pgk_dir, sys.version[:3]))
def csptools():
    """
    CSP Command line tools
    """


# @csptools.command()
# def cmd1():
#     """Command on cli1"""
#     print("cli1 cmd1")
