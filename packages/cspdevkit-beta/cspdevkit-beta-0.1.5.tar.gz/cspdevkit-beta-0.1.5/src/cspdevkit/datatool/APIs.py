#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/5/24 9:26
# @Author  : xgy
# @Site    : 
# @File    : Unst2st.py
# @Software: PyCharm
# @python version: 3.7.4
"""
import os

from cspdevkit.datatool.image_detection.split import det_split
from cspdevkit.datatool.image_detection.transform import det_transform
from cspdevkit.datatool.image_detection.check import det_check
from cspdevkit.datatool.image_detection.eva import det_eva
from cspdevkit.datatool.image_detection.eda import det_eda
from cspdevkit.datatool.image_detection.aug import det_aug

from cspdevkit.datatool.text_entity.check import entity_check
from cspdevkit.datatool.text_entity.split import entity_split
from cspdevkit.datatool.text_entity.eva import entity_eva

# 按任务类型，整合数据集处理 API

from cspdevkit.datatool.utils import task_l


def task_check(name, form: str):
    obj_det_l = ["VOC", "COCO"]
    if name not in task_l:
        raise KeyError("task should be one of {}".format(task_l))
    if name == "obj_det":
        if not form.upper() in obj_det_l:
            raise KeyError("obj_det's form should be VOC or COCO")


# 数据集切分
def split(data_dir, task, ratio: float, form=None, mode=None):
    if task == "obj_det":
        det_split(folder=data_dir, form=form, ratio=ratio, mode=mode)
    elif task == "text_entity_extra":
        entity_split(folder=data_dir, ratio=ratio)


# 数据集转换
def transform(data_dir, task, form, output=None):
    if task == "obj_det":
        det_transform(folder=data_dir, form=form, output=output)


# 数据集检查
def check(data_dir, task, form=None, output=None):
    if output and not os.path.exists(output):
        os.makedirs(output, exist_ok=True)
    if task == "obj_det":
        det_check(folder=data_dir, form=form, output=output)
    elif task == "text_entity_extra":
        entity_check(folder=data_dir, output=output)


# 预测结果评估
def eva(submit_file, gold_file, task, origin_image_dir=None, category_path=None, source_path=None, long_text_categories=None, output_dir=None):
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    if task == "obj_det":
        det_eva(submit_file, gold_file, origin_image_dir=origin_image_dir, output_dir=output_dir)
    elif task == "text_entity_extra":
        entity_eva(submit_file, gold_file, category_path, source_path, long_text_categories, output=output_dir)


# 数据集分析
def eda(data_dir, task, output_dir):
    if task == "obj_det":
        det_eda(data_dir, output_dir)


# 数据集增强
def aug(data_dir, task, aug_config, mode=None):
    if task == "obj_det":
        det_aug(data_dir, aug_config, mode)


if __name__ == '__main__':
    print("start")
