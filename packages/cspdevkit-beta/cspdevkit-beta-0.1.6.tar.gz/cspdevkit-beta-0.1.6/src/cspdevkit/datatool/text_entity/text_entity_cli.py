#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/4/28 15:07
# @Author  : xgy
# @Site    : 
# @File    : text_entity_cli.py
# @Software: PyCharm
# @python version: 3.7.4
"""

import click
from cspdevkit.datatool.datatool_cli import datatool
from cspdevkit.datatool.text_entity import entity_check, entity_split, entity_eva


## 二级命令
## 文本实体抽取任务
@datatool.group("text_entity")
def text_entity():
    """
    CSPTools datatool text_entity line \n the tools for text_entity task
    """


### 三级命令
### 数据集检查
# @text_entity.command()
# @click.option("-d", "--dir", prompt="the dataset dir", help="the dataset dir", required=True)
# @click.option("-o", "--output", help="the dataset dir", required=True, default="./output")
# def check(dir, output):
#     """
#     CSPTools datatool text_entity check line
#     """
#     entity_check(dir, output)


### 三级命令
### 数据集切分
# @text_entity.command()
# @click.option("-d", "--dir", prompt="the dataset dir", help="the dataset dir", required=True)
# @click.option("-r", "--ratio", type=float, prompt="Proportion of training set", help="Proportion of training set", required=True, default=0.9)
# @click.option("-o", "--output", help="the dataset dir", required=True)
# def split(dir, ratio, output):
#     """
#     CSPTools datatool text_entity split line
#     """
#     entity_split(dir, ratio, output)


### 三级命令
### 文本实体抽取预测结果评估
@text_entity.command()
@click.option("--pre_path", "-p", prompt="the result json from the model",
              help="the path of the result json from the model", type=str)
@click.option("--eval_path", "-e", prompt="the eval file(json)",
              help="the path of the eval file to evaluate the model", type=str)
@click.option("--category_path", "-c", prompt="the json data of category",
              help="the path of labelcategory.json", type=str)
@click.option("--source_path", "-s", prompt="the sources.json",
              help="the path of the sources data", type=str)
@click.option("--output", "-o", prompt="the eval report of the model",
              help="the folder to store result files", type=str)
@click.argument('long_text_categoryids', nargs=-1)
def eva(pre_path, eval_path, category_path, source_path, long_text_categoryids, output):
    """
    CSPTools datatool text_entity eva line
    """
    entity_eva(pre_path, eval_path, category_path, source_path, long_text_categoryids, output)

if __name__ == '__main__':
    print("start")
