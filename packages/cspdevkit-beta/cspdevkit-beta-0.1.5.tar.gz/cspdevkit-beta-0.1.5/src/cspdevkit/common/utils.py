#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/3/29 15:22
# @Author  : xgy
# @Site    : 
# @File    : utils.py
# @Software: PyCharm
# @python version: 3.7.4
"""

import subprocess
import shlex


class RunSys:
    """
    执行 shell 命令
    """

    def __init__(self, command: str = None):
        self.command = command
        self.output = None

    def run_cli(self):
        cmd = shlex.split(self.command)
        try:
            # output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            subprocess.check_call(cmd, stderr=subprocess.STDOUT)
            return True
            # self.output = output.decode()
        except subprocess.CalledProcessError as e:
            # print(traceback.print_exc())
            # print(e)
            return False


def format(data, title_dict: dict):
    try:
        from terminaltables import SingleTable
    except:
        RunSys(command="pip install terminaltables").run_cli()
        from terminaltables import SingleTable
    res_l = data["data"]

    table_data = []
    title = []
    for k, v in title_dict.items():
        title.append(k)
    table_data.append(title)

    if res_l:
        if isinstance(res_l, list):
            for item in res_l:
                item_l = []
                for k, v in title_dict.items():
                    if item[title_dict[k]]:
                        item_l.append(item[title_dict[k]])
                    else:
                        item_l.append('')
                table_data.append(item_l)
        if isinstance(res_l, dict):
            item_l = []
            for k, v in title_dict.items():
                if res_l[title_dict[k]]:
                    item_l.append(res_l[title_dict[k]])
                else:
                    item_l.append('')

            table_data.append(item_l)
    table_instance = SingleTable(table_data)
    table_instance.inner_heading_row_border = False
    table_instance.inner_row_border = True
    print(table_instance.table)


if __name__ == '__main__':
    print("start")


