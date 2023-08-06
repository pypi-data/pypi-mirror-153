#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/4/24 15:28
# @Author  : xgy
# @Site    : 
# @File    : utils.py
# @Software: PyCharm
# @python version: 3.7.4
"""
import os
import json
import chardet
from loguru import logger
import numpy as np


task_l = ["obj_det", "image_classification", "text_entity_extra", "text_entity_relation_extra", "text_classification"]

class JsonLoad:

    def __init__(self, json_path):
        self.file_path = json_path

    def encodetype(self):
        with open(self.file_path, 'rb') as f:
            try:
                data = f.read()
            except Exception as e:
                logger.error(e)
                return False
            f_charInfo = chardet.detect(data)
            # {'encoding': 'utf-8', 'confidence': 0.99, 'language': ''}
            if f_charInfo["encoding"] != "utf-8":
                logger.warning("Documents shall be encoded in UTF-8 format not {}".format(encode_type))
        return f_charInfo["encoding"]

    @property
    def data(self):
        # encode_type = self.encodetype()
        # if encode_type != "utf-8":
        #     logger.warning("Documents shall be encoded in UTF-8 format not {}".format(encode_type))
        try:
            with open(self.file_path, "r", encoding="utf-8") as fr:
                json_data = json.load(fr)
            return json_data
        except Exception as e:
            print(e)


class Entity:

    def __init__(self, folder, output=None):
        self.folder = folder
        self.output = output
        self.label_categories_data = None
        self.labels_data = None
        self.sources_data = None
        self.src_ids = []
        self.cate_ids = []

    def get_dataset(self):
        abs_path = os.path.abspath(self.folder)
        label_categories_path = os.path.join(abs_path, "labelCategories.json")
        labels_path = os.path.join(abs_path, "labels.json")
        sources_path = os.path.join(abs_path, "sources.json")

        self.label_categories_data = JsonLoad(label_categories_path).data
        self.labels_data = JsonLoad(labels_path).data
        self.sources_data = JsonLoad(sources_path).data

    def get_sources_ids(self):
        for item in self.sources_data:
            self.src_ids.append(item["id"])

    def get_cate_ids(self):
        for item in self.label_categories_data:
            self.cate_ids.append(item["id"])


class TxtFileCheck:

    def __init__(self, folder):
        self.folder = folder

    def txt_file_check(self, output=None):
        """
        判断 txt 文件是否打开异常、是否为 utf-8 编码
        :param output:
        :return:
        """
        txt_file_error_l = []
        abs_path = os.path.abspath(self.folder)
        for root, _, files in os.walk(abs_path):
            for file in files:
                txt_path = os.path.join(root, file)
                txt_ = JsonLoad(txt_path)
                file_encode = txt_.encodetype()
                if not file_encode:
                    logger.error("can not open {}".format(txt_path))
                    txt_file_error_l.append(txt_path)
                else:
                    if file_encode != "utf-8":
                        txt_file_error_l.append(txt_path)
                        logger.error("Documents shall be encoded in 'UTF-8' format, but {} is encoded in {}".format(txt_path, file_encode))
        if txt_file_error_l:
            save_path = os.path.join(output, "txt_file_error.txt") if self.output else "txt_file_error.txt"
            with open(save_path, "w", encoding="utf-8") as fw:
                for item in txt_file_error_l:
                    fw.write(item + "\n")
            logger.info("the result has been saved in {}".format(save_path))
        else:
            logger.info("the are no truble txt files")


class Filter:

    def __init__(self, size):
        self.size = size

    def choice_random(self, ratio: float, seed=2):
        assert 0 < ratio <= 1, 'ratio should between 0 and 1 (0<ratio<=1)'
        np.random.seed(seed)
        num = int(self.size * ratio)
        filter_index = np.random.choice(self.size, num, replace=False)
        return list(filter_index)


if __name__ == '__main__':
    print("start")
    test_json = "C:/Users/xgy/Desktop/CSPTools/0424/文本实体标注格式/labelCategories.json"
    test = JsonLoad(test_json)
    res = test.encodetype()
    test_data = test.data
