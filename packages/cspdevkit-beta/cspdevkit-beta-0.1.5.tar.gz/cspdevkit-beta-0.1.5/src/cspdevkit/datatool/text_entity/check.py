#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/4/24 16:14
# @Author  : xgy
# @Site    : 
# @File    : check.py
# @Software: PyCharm
# @python version: 3.7.4
"""
import os
from loguru import logger

from cspdevkit.datatool.utils import Entity


class EntityCheck(Entity):

    def __init__(self, folder, output=None):
        super(EntityCheck, self).__init__(folder, output)

    def check_sources(self):
        """
        公共检查，sources.json 字段值为空
        :return:
        """
        sources_error_l = []
        # 检查字段全为空为空
        for index, item in enumerate(self.sources_data):
            if not item["id"] and not item["title"] and not item["content"]:
                return False
            if item["id"]:
                if not item["title"] or not item["content"]:
                    sources_error_l.append(item["id"])

        if sources_error_l:
            save_path = os.path.join(self.output, "sources_error.txt") if self.output else "sources_error.txt"
            with open(save_path, "w", encoding="utf-8") as fw:
                for item in sources_error_l:
                    fw.write(item + "\n")
                logger.info("the result has been saved in {}".format(save_path))
            return False
        else:
            logger.info("the is no truble in sources.json")
            return True
        # return sources_error_l

    def check_labelcategory(self):
        """
        公共检查，labelcategory.json 字段值为空
        :return:
        """
        labelcategory_error_l = []
        # 检查字段全为空为空
        for item in self.label_categories_data:
            if not item["id"] and not item["text"]:
                return False
            if item["id"] and not item["text"]:
                labelcategory_error_l.append(item["id"])

        if labelcategory_error_l:
            save_path = os.path.join(output, "labelcategory_error.txt") if self.output else "labelcategory_error.txt"
            with open(save_path, "w", encoding="utf-8") as fw:
                for item in labelcategory_error_l:
                    fw.write(item + "\n")
                logger.info("the result has been saved in {}".format(save_path))
            return False
        else:
            logger.info("the is no truble in labelcategory.json")
            return True

    def check_labels(self):
        srcId_error_l = []
        categoryId_error_l = []
        self.get_sources_ids()
        self.get_cate_ids()
        for index, item in enumerate(self.labels_data):
            if item["srcId"] not in self.src_ids:
                srcId_error_l.append(item["srcId"])
            if item["categoryId"] not in self.cate_ids:
                categoryId_error_l.append(item["categoryId"])

        if srcId_error_l:
            save_path = os.path.join(self.output, "labels_srcid_error.txt") if self.output else "labels_srcid_error.txt"
            with open(save_path, "w", encoding="utf-8") as fw:
                for item in srcId_error_l:
                    fw.write(item + "\n")
                logger.info("the result has been saved in {}".format(save_path))
        if categoryId_error_l:
            save_path = os.path.join(self.output, "labels_categoryid_error.txt") if self.output else "labels_categoryid_error.txt"
            with open(save_path, "w", encoding="utf-8") as fw:
                for item in categoryId_error_l:
                    fw.write(item + "\n")
                logger.info("the result has been saved in {}".format(save_path))
        if not srcId_error_l and not categoryId_error_l:
            logger.info("the is no truble in labels.json")


def entity_check(folder, output=None):
    check_entity = EntityCheck(folder, output=output)
    check_entity.get_dataset()

    flag_sources = check_entity.check_sources()
    flag_labelcategory = check_entity.check_labelcategory()

    if flag_sources and flag_labelcategory:
        check_entity.check_labels()


if __name__ == '__main__':
    print("start")
    # test_json = "C:/Users/xgy/Desktop/CSPTools/0424/文本实体标注格式/labelCategories.json"
    # test_dir = "C:/Users/xgy/Desktop/CSPTools/0424/文本实体标注格式"
    # entity_check(test_dir, output=None)