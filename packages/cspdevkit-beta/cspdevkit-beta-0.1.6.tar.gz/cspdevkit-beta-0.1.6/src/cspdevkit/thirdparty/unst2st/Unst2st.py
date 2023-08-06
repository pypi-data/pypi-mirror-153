#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/5/19 17:55
# @Author  : xgy
# @Site    : 
# @File    : Unst2st.py
# @Software: PyCharm
# @python version: 3.7.4
"""
import base64
import os

from cspdevkit.common.docker_server import DockerServer
from cspdevkit.common.http_client import HttpClient


class Unst2st:

    def __init__(self, version, port, c_name=None, name="unst2st", reload=True):
        self.port = port
        self.server = DockerServer(name=name, version=version, port=port, c_name=c_name, reload=reload)
        self.server.start()

    def extract_text(self, file, output=None):
        http_client = HttpClient()
        url = "http://127.0.0.1:" + str(self.port) + "/web/aip/file2txt"
        files = {"file": open(file, 'rb')}

        # dt = http_client.convert(url, method="post", arg_type="files", **files)
        dt = http_client.post(url, arg_type="files", **files)
        result = dt["data"]

        if output:
            txt_name = os.path.splitext(file)[0] + ".txt"
            save_path = os.path.join(output, txt_name)
            with open(save_path, "w", encoding="utf-8") as fw:
                fw.write(result)

        return result

    def remove_watermark(self, file, output):
        http_client = HttpClient()
        url = "http://127.0.0.1:" + str(self.port) + "/web/aip/remove_watermark_pdf_txt"
        files = {"file": open(file, 'rb')}

        # dt = http_client.convert(url, method="post", arg_type="files", **files)
        dt = http_client.post(url, arg_type="files", **files)
        result = dt["data"]

        with open(output, 'wb') as f:
            f.write(base64.b64decode(result))
        print("the output has been saved in {}".format(output))

        return result


if __name__ == '__main__':
    print("start")

    # name = "unst2st"
    # version = 0.1
    # port = 9889
    # unst2st = Unst2st(version, port)
    # file_path = "C://Users/xgy/desktop/P020190630537259577129.pdf"
    # txt_1 = unst2st.extract_text(file_path)

    # test_pdf = "C:/Users/xgy/Desktop/doc_o.pdf"
    # out_file = "./out.pdf"
    # data_base64 = unst2st.remove_watermark(test_pdf, out_file)


