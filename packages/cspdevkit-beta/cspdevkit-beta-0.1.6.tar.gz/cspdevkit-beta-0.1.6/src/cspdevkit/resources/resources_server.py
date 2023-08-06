#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/5/16 11:11
# @Author  : xgy
# @Site    : 
# @File    : resources_server.py
# @Software: PyCharm
# @python version: 3.7.4
"""


from cspdevkit.common.http_client import HttpClient
from cspdevkit.common.config import Configure
from cspdevkit.common.utils import format


def res_get(name, res_dir=None, infer_type: str = None, config: Configure = None):
    assert infer_type in ["search", "list", "info"]

    if config:
        interface_config = config.data
    else:
        interface_config = Configure().data
    http_client = HttpClient()

    url = interface_config[infer_type]["resources"]
    if infer_type == "list":
        params = {"name": name}
    elif infer_type == "search":
        params = {"resName": name, "resDir": res_dir}
    elif infer_type == "info":
        params = {"name": name}
    else:
        raise KeyError("infer_type should be in {}".format(["search", "list", "info"]))

    res_dict = http_client.get(url, **params)

    if infer_type == "list" or infer_type == "search":
        title_dict = {"名称": "resName", "文件类型": "fileType", "目录": "resDir", "资源大小(KB)": "fileSize",
                      "创建时间": "createTime", "更新时间": "updateTime"}
        format(res_dict, title_dict)

    if infer_type == "info":
        title_dict = {"名称": "resName", "文件类型": "fileType", "目录": "resDir", "资源大小(KB)": "fileSize",
                      "创建时间": "createTime", "更新时间": "updateTime", "描述": "resDesc"}
        format(res_dict, title_dict)

    return res_dict


def res_download(name, output, charset="UTF-8"):
    interface_config = Configure().data
    http_client = HttpClient()

    url = interface_config["download"]["resources"]
    params = {"name": name, "charset": charset}
    res = http_client.download(url, output, **params)

    return res


if __name__ == '__main__':
    print("start")
