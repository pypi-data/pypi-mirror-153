#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/5/6 15:26
# @Author  : xgy
# @Site    : 
# @File    : dataset.py
# @Software: PyCharm
# @python version: 3.7.4
"""

import os
from datetime import datetime
from loguru import logger

from cspdevkit.dataset.dataset_server import data_download

from cspdevkit.datatool.utils import task_l


class Dataset:

    def __init__(self, database, target, task, mode=None, size=None, output=None):
        self.database = database
        self.target = target
        self.mode = mode
        self.size = size
        self.task = task
        self.dataset_dir = target if self.database == "local" else None
        self.output = output if output else "./data/"

        self.check_args()

        if database == "remote":
            self.download_data()

    def check_args(self):
        if self.database not in ["remote", "local"]:
            raise KeyError("the database should be in ['remote', 'local']")
        if self.database == "remote":
            if not self.mode or self.mode not in ['raw', 'eva', 'train']:
                raise KeyError("the database should be in ['raw', 'eva', 'train']")
        if self.task not in task_l:
            raise KeyError("the task should be in {}".format(task_l))

    def download_data(self):
        if self.database == "remote":
            # 按时间戳创建文件夹保存下载数据
            create_time = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S%f")
            data_folder = os.path.join(self.output, create_time)
            os.makedirs(data_folder, exist_ok=True)

            dataset_path = data_download(self.target, self.mode, self.size, data_folder)
            dataset_path = dataset_path.replace("\\", "/")
            logger.info("the dataset has been save in {}".format(dataset_path))

            import zipfile
            from tqdm import tqdm

            if dataset_path.lower().endswith(".zip"):
                zip_f = zipfile.ZipFile(dataset_path)
                list_zip_f = zip_f.namelist()  # zip文件中的文件列表名
                logger.info("start unzip the {}".format(dataset_path))
                for zip_fn in tqdm(list_zip_f):
                    zip_f.extract(zip_fn, data_folder)  # 第二个参数指定输出目录，此处保存在当前目录
                    # print("%s done" % zip_fn)
                zip_f.close()

                for item in os.listdir(data_folder):
                    if not item.lower().endswith(".zip"):
                        self.dataset_dir = os.path.join(data_folder, item)


if __name__ == '__main__':
    print("start")
