#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/5/12 15:54
# @Author  : xgy
# @Site    : 
# @File    : eda.py
# @Software: PyCharm
# @python version: 3.7.4
"""

import json
import os
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import xml.etree.ElementTree as ET
from tqdm import tqdm


class DataEda:

    def __init__(self, data_dir, output_dir=None):
        self.data_dir = data_dir
        self.xml_file_path = os.path.join(self.data_dir, "Annotations")
        self.output_dir = os.path.join(self.xml_file_path, "data_report") if not output_dir else output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def eda(self):
        # 相关变量
        count = 0
        objects_name = []
        objects_num = {}
        images_size_w = []
        images_size_h = []
        images_size_ratio = []
        boxes_size_w = []
        boxes_size_h = []
        boxes_size_ratio = []

        # 遍历每个xml文件
        names_xml = os.listdir(self.xml_file_path)
        for name in tqdm(names_xml):
            if name.endswith('.xml'):
                # 获得每份xml文件的根节点
                count += 1
                # tree = ET.parse(xml_file_path + '/' + name)  # 打开xml文档
                tree = ET.parse(os.path.join(self.xml_file_path, name))  # 打开xml文档
                root = tree.getroot()  # 获得root节点

                # 图像长宽信息
                img_size = root.find('size')
                img_height = img_size.find('height').text
                height = int(img_height)
                img_width = img_size.find('width').text
                width = int(img_width)
                images_size_w.append(width)
                images_size_h.append(height)
                images_size_ratio.append(height / width)

                # 遍历每个object，获取目标框长宽信息、各类标签目标框数
                for object in root.findall('object'):
                    # 各类标签个数累计
                    object_name = object.find('name').text
                    if object_name not in objects_name:
                        objects_name.append(object_name)
                        objects_num[object_name] = 1
                    else:
                        objects_num[object_name] += 1

                    # 目标框长宽信息
                    bndbox = object.find('bndbox')
                    dot = r'.'
                    if dot in bndbox.find('xmin').text:
                        xmin = bndbox.find('xmin').text
                        min_split = xmin.split('.')
                        x_min = int(min_split[0])
                        xmax = bndbox.find('xmax').text
                        max_split = xmax.split('.')
                        x_max = int(max_split[0])
                        ymin = bndbox.find('ymin').text
                        min_split = ymin.split('.')
                        y_min = int(min_split[0])
                        ymax = bndbox.find('ymax').text
                        max_split = ymax.split('.')
                        y_max = int(max_split[0])
                        # 目标框宽高
                        box_width = x_max - x_min
                        box_height = y_max - y_min
                    else:
                        xmin = bndbox.find('xmin').text
                        x_min = int(xmin)
                        xmax = bndbox.find('xmax').text
                        x_max = int(xmax)
                        ymin = bndbox.find('ymin').text
                        y_min = int(ymin)
                        ymax = bndbox.find('ymax').text
                        y_max = int(ymax)
                        # 目标框宽高
                        box_width = x_max - x_min
                        box_height = y_max - y_min
                    boxes_size_w.append(box_width)
                    boxes_size_h.append(box_height)
                    boxes_size_ratio.append(box_height / box_width)

        # 保存输出每类标签目标框个数信息文档
        labels_and_num_save_path = os.path.join(self.output_dir, "labels_and_num.json")
        with open(labels_and_num_save_path, "w", encoding="utf-8") as fj:
            json.dump(objects_num, fj, ensure_ascii=False, indent=4)

        dpi = 15
        # 散点图(图像) ###########################################labelrotation=90
        plt.figure(figsize=(80, 40))
        plt.xlabel('Width', fontsize=80)
        plt.ylabel('Height', fontsize=80)
        plt.title('Images', fontsize=100)
        plt.tick_params(which='both', direction='inout', pad=30, width=5, length=15, labelsize=50)
        x_major_locator = MultipleLocator(500)
        ax = plt.gca()
        ax.xaxis.set_major_locator(x_major_locator)
        plt.scatter(images_size_w, images_size_h, c='r')
        plt.savefig(os.path.join(self.output_dir, 'images.png'), dpi=dpi)

        # 图像宽度分布
        num_bins = (max(images_size_w) - min(images_size_w)) // 200 + 1  # 柱状条个数
        plt.figure(figsize=(80, 40))
        plt.xlabel('Width', fontsize=80)
        plt.ylabel('Number', fontsize=80)
        plt.title('Distribution of Width about Images', fontsize=100)
        plt.tick_params(which='both', direction='inout', pad=30, width=5, length=15, labelsize=50)
        x_major_locator = MultipleLocator(200)
        ax = plt.gca()
        ax.xaxis.set_major_locator(x_major_locator)
        plt.hist(images_size_w, num_bins, facecolor='red', alpha=0.5)
        plt.savefig(os.path.join(self.output_dir, 'images_width.png'), dpi=dpi)

        # 图像高度分布
        num_bins = (max(images_size_h) - min(images_size_h)) // 200 + 1  # 柱状条个数
        plt.figure(figsize=(80, 40))
        plt.xlabel('Height', fontsize=80)
        plt.ylabel('Number', fontsize=80)
        plt.title('Distribution of Height about Images', fontsize=100)
        plt.tick_params(which='both', direction='inout', pad=30, width=5, length=15, labelsize=50)
        x_major_locator = MultipleLocator(200)
        ax = plt.gca()
        ax.xaxis.set_major_locator(x_major_locator)
        plt.hist(images_size_h, num_bins, facecolor='red', alpha=0.5)
        plt.savefig(os.path.join(self.output_dir, 'images_height.png'), dpi=dpi)

        # 图像高/宽比分布
        num_bins = 20
        plt.figure(figsize=(80, 40))
        plt.xlabel('Height', fontsize=80)
        plt.ylabel('Number', fontsize=80)
        plt.title('Distribution of Ratio(Height/Width) about Images', fontsize=100)
        plt.tick_params(which='both', direction='inout', pad=30, width=5, length=15, labelsize=50)
        x_major_locator = MultipleLocator(0.1)
        ax = plt.gca()
        ax.xaxis.set_major_locator(x_major_locator)
        plt.hist(images_size_ratio, num_bins, facecolor='red', alpha=0.5)
        plt.savefig(os.path.join(self.output_dir, 'images_ratio.png'), dpi=dpi)

        # 散点图(目标框) ##########################################
        plt.figure(figsize=(80, 40))
        plt.xlabel('Width', fontsize=80)
        plt.ylabel('Height', fontsize=80)
        plt.title('Boxes', fontsize=100)
        plt.tick_params(which='both', direction='inout', pad=30, width=5, length=15, labelsize=50)
        x_major_locator = MultipleLocator(500)
        ax = plt.gca()
        ax.xaxis.set_major_locator(x_major_locator)
        plt.scatter(boxes_size_w, boxes_size_h, c='b')
        plt.savefig(os.path.join(self.output_dir, 'boxes.png'), dpi=dpi)

        # 目标框宽度分布
        num_bins = (max(boxes_size_w) - min(boxes_size_w)) // 200 + 1  # 柱状条个数
        plt.figure(figsize=(80, 40))
        plt.xlabel('Width', fontsize=80)
        plt.ylabel('Number', fontsize=80)
        plt.title('Distribution of Width about Boxes', fontsize=100)
        plt.tick_params(which='both', direction='inout', pad=30, width=5, length=15, labelsize=50)
        x_major_locator = MultipleLocator(200)
        ax = plt.gca()
        ax.xaxis.set_major_locator(x_major_locator)
        plt.hist(boxes_size_w, num_bins, facecolor='blue', alpha=0.5)
        plt.savefig(os.path.join(self.output_dir, 'boxes_width.png'), dpi=dpi)

        # 目标框高度分布
        num_bins = (max(boxes_size_h) - min(boxes_size_h)) // 200 + 1  # 柱状条个数
        plt.figure(figsize=(80, 40))
        plt.xlabel('Height', fontsize=80)
        plt.ylabel('Number', fontsize=80)
        plt.title('Distribution of Height about Boxes', fontsize=100)
        plt.tick_params(which='both', direction='inout', pad=30, width=5, length=15, labelsize=50)
        x_major_locator = MultipleLocator(200)
        ax = plt.gca()
        ax.xaxis.set_major_locator(x_major_locator)
        plt.hist(boxes_size_h, num_bins, facecolor='blue', alpha=0.5)
        plt.savefig(os.path.join(self.output_dir, 'boxes_height.png'), dpi=dpi)

        # 目标框高/宽比分布
        num_bins = 30
        plt.figure(figsize=(80, 40))
        plt.xlabel('Height', fontsize=80)
        plt.ylabel('Number', fontsize=80)
        plt.title('Distribution of Ratio(Height/Width) about Boxes', fontsize=100)
        plt.tick_params(which='both', direction='inout', pad=30, width=5, length=15, labelsize=50)
        x_major_locator = MultipleLocator(0.4)
        ax = plt.gca()
        ax.xaxis.set_major_locator(x_major_locator)
        plt.hist(boxes_size_ratio, num_bins, facecolor='blue', alpha=0.5)
        plt.savefig(os.path.join(self.output_dir, 'boxes_ratio.png'), dpi=dpi)

        print('Have finished EDA process, the result is in dir: {} !'.format(self.output_dir))


def det_eda(data_dir, output_dir):
    data_eda = DataEda(data_dir, output_dir)
    data_eda.eda()


if __name__ == '__main__':
    print("start")

    voc_dir = "C:/Users/xgy/Desktop/CSPTools/0507/20220507154756390569/train_eda"
    output = "C:/Users/xgy/Desktop/CSPTools/0507/20220507154756390569/voc_eda"

    data_eda = DataEda(voc_dir, output)
    data_eda.eda()
