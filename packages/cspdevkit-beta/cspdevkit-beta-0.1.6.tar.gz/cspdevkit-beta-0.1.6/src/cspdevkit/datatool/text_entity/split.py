#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/4/26 15:58
# @Author  : xgy
# @Site    : 
# @File    : split.py
# @Software: PyCharm
# @python version: 3.7.4
"""

import os
import json
from loguru import logger

from cspdevkit.datatool.utils import Entity, Filter


class EntitySplit(Entity):

    def __init__(self, folder, output=None):
        super(EntitySplit, self).__init__(folder, output)

    def filter_by_scr(self, ratio=0.9):
        self.get_sources_ids()
        size = len(self.src_ids)
        filter = Filter(size)
        index_train = filter.choice_random(ratio=ratio)

        source_train = []
        source_test = []
        test_id = []
        for index, item in enumerate(self.sources_data):
            if index in index_train:
                source_train.append(item)
            else:
                source_test.append(item)
                test_id.append(item["id"])

        label_train = []
        label_test = []
        for label in self.labels_data:
            srcId = label["srcId"]
            if srcId in test_id:
                label_test.append(label)
            else:
                label_train.append(label)

        data_dict = {"labels_train": label_train,
                     "sources_train": source_train,
                     "sources_test": source_test,
                     "labels_test": label_test,
                     "labelCategories": self.label_categories_data}

        for k, v in data_dict.items():
            file_name = k + ".json"
            # output_item = os.path.join(self.output, file_name) if self.output else file_name
            output_item = os.path.join(self.output, file_name) if self.output else os.path.join(self.folder, file_name)
            with open(output_item, "w", encoding="utf-8") as f:
                json.dump(v, f, ensure_ascii=False, indent=4)
            logger.info("the result has been saved in {}".format(output_item))

        return source_train, source_test


def entity_split(folder, ratio=0.9, output=None):
    filter_entity = EntitySplit(folder, output=output)
    filter_entity.get_dataset()
    filter_entity.filter_by_scr(ratio=ratio)


if __name__ == '__main__':
    print("start")
    # test_dir = "C:/Users/xgy/Desktop/CSPTools/0424/文本实体标注格式"
    # out = "D:/document/pycharmpro/CSPTools/test/output"
    # entity_split(test_dir, output=out)
