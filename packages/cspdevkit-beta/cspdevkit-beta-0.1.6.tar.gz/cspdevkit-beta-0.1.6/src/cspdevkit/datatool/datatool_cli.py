#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/4/24 10:17
# @Author  : xgy
# @Site    : 
# @File    : datatool_cli.py
# @Software: PyCharm
# @python version: 3.7.4
"""
import click
from cspdevkit.command.cli import csptools
from cspdevkit.datatool.APIs import split as data_split
from cspdevkit.datatool.APIs import transform as data_trasform
from cspdevkit.datatool.APIs import check as data_check
from cspdevkit.datatool.APIs import eva as data_eva
from cspdevkit.datatool.APIs import eda as data_eda
from cspdevkit.datatool.APIs import aug as data_aug


# 一级命令 CSPtools datatool
@csptools.group("datatool")
def datatool():
    """
    CSPTools datatool Command line \n the tools for dataset,such as checking and transform
    """


## 二级命令
## 数据集切分 split
@datatool.command()
@click.option("-d", "--dir", prompt="the dataset dir", help="the dataset dir", required=True)
@click.option("-t", "--task", type=click.Choice(["obj_det", "image_classification", "text_entity_extra", "text_entity_relation_extra", "text_classification"]),
              prompt="the task type", help="the task type", required=True)
@click.option("-r", "--ratio", type=float, prompt="ratio of training data", help="ratio of training data", required=True)
@click.option("-f", "--form", type=str, help="the dataset type, voc or coco case insensitive")
@click.option("-m", "--mode", type=click.Choice(['train', 'trainval']), help="identification of data to be split which will work in obj_det", default=None)
def split(dir, task, ratio, form, mode):
    """
    CSPTools datatool split line
    """
    data_split(dir, task, ratio, form=form, mode=mode)


## 二级命令
## 数据集转换 transform
@datatool.command()
@click.option("-d", "--dir", prompt="the dataset dir", help="the dataset dir", required=True)
@click.option("-t", "--task", type=click.Choice(["obj_det", "image_classification", "text_entity_extra", "text_entity_relation_extra", "text_classification"]),
              prompt="the task type", help="the task type", required=True)
@click.option("-f", "--form", type=str, help="the dataset type, voc or coco case insensitive")
@click.option("-o", "--output", prompt="the folder to save out files", help="the folder to save out files", required=True)
def transform(dir, task, form, output):
    """
    CSPTools datatool transform line
    """
    data_trasform(dir, task, form=form, output=output)


## 二级命令
## 数据集检查 check
@datatool.command()
@click.option("-d", "--dir", prompt="the dataset dir", help="the dataset dir", required=True)
@click.option("-t", "--task", type=click.Choice(["obj_det", "image_classification", "text_entity_extra", "text_entity_relation_extra", "text_classification"]),
              prompt="the task type", help="the task type", required=True)
@click.option("-f", "--form", type=str, prompt="the dataset type, voc or coco case insensitive", help="the dataset type, voc or coco case insensitive", default=None)
@click.option("-o", "--output", help="the dataset dir", required=True, default="./output")
def check(dir, task, form, output):
    """
    CSPTools datatool check line
    """
    data_check (dir, task, form, output)


## 二级命令
## 预测结果评估 eva
@datatool.command()
@click.option("-s", "--submit_file", prompt="the predict json file", help="the predict json file", required=True)
@click.option("-g", "--gold_file", prompt="the gold json file",
              help="the gold json file. In the obj_det task, it must be type of coco", required=True)
@click.option("-t", "--task", type=click.Choice(["obj_det", "image_classification", "text_entity_extra", "text_entity_relation_extra", "text_classification"]),
              prompt="the task type", help="the task type", required=True)
@click.option("-m", "--origin_image_dir", help="the origin image folder, using in obj_det", default=None)
@click.option("-c", "--category_path", help="Play a role in the text_entity_extra. the path of labelcategory.json",
              type=str, default=None)
@click.option("-s", "--source_path", help="Play a role in the text_entity_extra. the path of the sources data",
              type=str, default=None)
@click.option("-o", "--output_dir", help="the folder to save badcase", default=None)
@click.argument('long_text_categories', nargs=-1)
def eva(submit_file, gold_file, task, origin_image_dir, category_path, source_path, long_text_categories, output_dir):
    """
    CSPTools datatool eva line
    """
    data_eva(submit_file, gold_file, task, origin_image_dir=origin_image_dir, category_path=category_path, source_path=source_path, long_text_categories=long_text_categories, output_dir=output_dir)


## 二级命令
## 预测结果分析 eda
@datatool.command()
@click.option("-d", "--dir", prompt="the dataset dir", help="the dataset dir", required=True)
@click.option("-t", "--task", type=click.Choice(["obj_det", "image_classification", "text_entity_extra", "text_entity_relation_extra", "text_classification"]),
              prompt="the task type", help="the task type", required=True)
@click.option("-o", "--output", prompt="the folder to save results", help="he folder to save results", default=None)
def eda(dir, task, output):
    """
    CSPTools datatool obj_det eda line only support voc
    """
    data_eda(dir, task, output)


## 二级命令
## VOC数据集增强 aug
@datatool.command()
@click.option("-d", "--dir", prompt="the dataset dir, only for VOC", help="the dataset dir, only for VOC", required=True)
@click.option("-t", "--task", type=click.Choice(["obj_det", "image_classification", "text_entity_extra", "text_entity_relation_extra", "text_classification"]),
              prompt="the task type", help="the task type", required=True)
@click.option("-c", "--aug_file", prompt="the yml for imgaug", help="the yml for imgaug", required=True)
@click.option("-m", "--mode", type=click.Choice(['train', 'trainval']), help="identification of data to be aug which will work in obj_det", default=None)
def aug(dir, task, aug_file, mode):
    """
    CSPTools datatool obj_det aug line
    """
    data_aug(dir, task, aug_file, mode)


if __name__ == '__main__':
    print("start")
