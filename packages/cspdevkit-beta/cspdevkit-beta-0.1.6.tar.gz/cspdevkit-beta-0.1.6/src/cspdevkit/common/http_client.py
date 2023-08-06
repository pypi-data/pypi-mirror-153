#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/5/17 17:34
# @Author  : xgy
# @Site    : 
# @File    : http_client.py
# @Software: PyCharm
# @python version: 3.7.4
"""
import os
import urllib

import requests
import json
from loguru import logger
from tqdm import tqdm


class HttpClient:

    def __init__(self):

        self.info_list = None
        self.info_download = None

    def get(self, url, **kw):
        params = kw
        res = requests.get(url, params=params)
        res_dict = json.loads(res.text)
        if res_dict["code"] == 200:
            self.info_list = res_dict
            return res_dict
        else:
            # raise IOError(self.error_msg(res_dict))
            self.error_msg(res_dict)
        # return res_dict

    def post(self, url, arg_type=None, **kw):
        if arg_type == "files":
            res = requests.post(url, files=kw)
        elif arg_type == "data":
            res = requests.post(url, data=kw)
        elif arg_type == "json":
            res = requests.post(url, json=kw)
        else:
            raise KeyError("the arg_type for post should be in {}".format(['files', 'data', 'json']))

        res_dict = json.loads(res.text)
        if res_dict["code"] == 200:
            self.info_list = res_dict
            return res_dict
        else:
            self.error_msg(res_dict)

    def download(self, url, output=None, **kw):
        params = kw
        res = requests.post(url, data=params, stream=True)

        total = int(res.headers.get('content-length', 0))
        # 获取头部信息
        disposition = str(res.headers.get('Content-Disposition'))
        # 截取头部信息文件名称
        filename = disposition.replace('attachment;filename=', '')

        # 转码
        filename = urllib.parse.unquote(filename)
        save_path = os.path.join(output, filename)

        # 添加保存路径
        with open(save_path, 'wb') as file, tqdm(desc=save_path, total=total, unit='iB', unit_scale=True, unit_divisor=1024) as bar:
            for data in res.iter_content(chunk_size=1024):
                size = file.write(data)
                bar.update(size)

        return save_path

    def error_msg(self, data):
        if data["code"] != 200:
            error_code = data["code"]
            logger.error(error_code, data["msg"])
            raise ConnectionError("Call server error")

    # def convert(self, url, method, arg_type, **kwargs):
    #     if method.upper() == "POST":
    #         if arg_type == "files":
    #             res = requests.post(url, files=kwargs)
    #         elif arg_type == "data":
    #             res = requests.post(url, data=kwargs)
    #         elif arg_type == "json":
    #             res = requests.post(url, json=kwargs)
    #         else:
    #             raise KeyError("the arg_type for post should be in {}".format(['files', 'data', 'json']))
    #     elif method.upper() == "GET":
    #         res = requests.get(url, params=kwargs)
    #     else:
    #         raise KeyError("the HTTP method should be POST or GET")
    #     res_dict = json.loads(res.text)
    #     self.error_msg(res_dict)
    #
    #     return res_dict


if __name__ == '__main__':
    print("start")
