#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/4/28 16:08
# @Author  : xgy
# @Site    : 
# @File    : check.py
# @Software: PyCharm
# @python version: 3.7.4
"""
import os
import json
import xml.etree.ElementTree as ET
from loguru import logger
from cspdevkit.datatool.image_detection.utils import CheckDataset


class CheckVoc(CheckDataset):

    def __init__(self, dataset_dir, form="VOC", output_dir=None):
        super().__init__(dataset_dir, form, output_dir)
        self.labels_path = os.path.join(self.dataset_dir, "labels.txt")
        self.labels = []

    def get_labels(self):
        labels = []
        with open(self.labels_path, "r", encoding="utf-8") as fr:
            txt_list = fr.readlines()
            for index, item in enumerate(txt_list):
                item_list = item.split(" ")
                labels.append(item_list[0].replace("\n", ""))
        self.labels = labels

    # 判断标注数据(.xml)是否存在错误
    def is_anno_break(self):
        """
        需保证数据集根目录下存在labels.txt，用于判断是否存在类别错误
        """
        super().clear_out()
        self.get_labels()
        for xml in os.listdir(self.anno_dir):
            flag_size = True
            flag_cls = True
            flag_no_obj = True
            flag_box = True

            xml_name = os.path.splitext(xml)[0]
            xml_path = os.path.join(self.anno_dir, xml)
            tree = ET.parse(xml_path)
            annotation = tree.getroot()  # 获取根节点， Element类

            # 图片尺寸为0判断
            size = annotation.find("size")
            if not size:
                flag_size = False
                width = None
                height = None
            else:
                width = size.find("width")
                height = size.find("height")
                if int(width.text) == 0 or int(height.text) == 0 or width is None or height is None:
                    flag_size = False
            if not flag_size:
                with open(self.size_error_txt, "a+", encoding="utf-8") as fw:
                    fw.write(xml_name)
                    fw.write("\n")

            # 判断 object 节点相关字段
            # 判断有无 object 节点
            obj_flag = annotation.find("object")
            if obj_flag:
                for obj in annotation.iter('object'):
                    cls = obj.find('name').text

                    # 类别错误判断
                    if cls not in self.labels:
                        flag_cls = False

                    # box 坐标值错误判断
                    bndbox = obj.find('bndbox')
                    if not bndbox:
                        # 无 bndbox 节点
                        flag_box = False
                    else:
                        try:
                            # 无 xmin 等节点
                            xmin = int(bndbox.find('xmin').text)
                            ymin = int(bndbox.find('ymin').text)
                            xmax = int(bndbox.find('xmax').text)
                            ymax = int(bndbox.find('ymax').text)
                        except ValueError:
                            flag_box = False
                        else:
                            if width.text and height.text:
                                # 坐标值 错误
                                if xmin < 0 or xmax < 0 or ymin < 0 or ymax < 0 or xmin >= xmax or ymin >= ymax or xmax > int(width.text) or ymax > int(height.text):
                                    flag_box = False
                            if width is None and height is None:
                                if any(item < 0 for item in [xmin, ymin, xmax, ymax]) or xmin >= xmax or ymin >= ymax:
                                    flag_box = False

                if not flag_box and not flag_cls:
                    with open(self.box_error_txt, "a+", encoding="utf-8") as fw:
                        fw.write(xml_name)
                        fw.write("\n")
                    with open(self.cls_error_txt, "a+", encoding="utf-8") as fw:
                        fw.write(xml_name)
                        fw.write("\n")

                if not flag_box and flag_cls:
                    with open(self.box_error_txt, "a+", encoding="utf-8") as fw:
                        fw.write(xml_name)
                        fw.write("\n")

                if flag_box and not flag_cls:
                    with open(self.cls_error_txt, "a+", encoding="utf-8") as fw:
                        fw.write(xml_name)
                        fw.write("\n")

            else:
                flag_no_obj = False
                with open(self.no_obj_txt, "a+", encoding="utf-8") as fw:
                    fw.write(xml_name)
                    fw.write("\n")

            if not flag_size or not flag_cls or not flag_no_obj or not flag_box:
                with open(self.error_list_txt, "a+", encoding="utf-8") as fw:
                    fw.write(xml_name)
                    fw.write("\n")
        if os.path.exists(self.error_list_txt):
            logger.info("the error annotation name has been save to the {}".format(self.error_list_txt))
        else:
            print("there are not error annotations")


class CheckCoco(CheckDataset):

    def __init__(self, dataset_dir, form="COCO", output_dir=None):
        super().__init__(dataset_dir, form, output_dir)

    # 判断标注数据(.json)是否存在错误
    def is_anno_break(self):
        super().clear_out()

        for item in  os.listdir(self.dataset_dir):
            if item in self.img_folder_names:
                json_path = os.path.join(self.anno_dir, item + ".json")
                with open(json_path, "r", encoding="utf-8") as fr:
                    json_data = json.load(fr)

                error_all_list = []
                size_error_list = []
                box_error_list = []
                cls_error_list = []

                # img_id: [file_name, w, h] 键值对
                images = json_data["images"]
                img_dict = {}
                for img in images:
                    file_name_short = os.path.splitext(img["file_name"])[0]

                    height = img.get("height", None)
                    width = img.get("width", None)
                    img_dict[img["id"]] = [file_name_short, width, height]

                    # w, h 为 0 或 不存在
                    if not height or not width:
                        if file_name_short not in size_error_list:
                            # size_error_list.append(file_name_short)
                            error_item = [file_name_short, item]
                            size_error_list.append(error_item)
                        if file_name_short not in error_all_list:
                            # error_all_list.append(file_name_short)
                            error_item = [file_name_short, item]
                            error_all_list.append(error_item)

                # 类别 id 列表
                categories = json_data["categories"]
                category_id_list = []
                for category in categories:
                    category_id = category["id"]
                    category_id_list.append(category_id)

                annotations = json_data["annotations"]
                for anno in annotations:
                    image_id = anno["image_id"]
                    img_name = img_dict[image_id][0]
                    img_w = img_dict[image_id][1]
                    img_h = img_dict[image_id][2]

                    category_id = anno["category_id"]
                    # 非法类别 id
                    if category_id not in category_id_list:
                        if img_name not in cls_error_list:
                            # cls_error_list.append(img_name)
                            error_item = [img_name, item]
                            cls_error_list.append(error_item)
                        if img_name not in error_all_list:
                            # error_all_list.append(img_name)
                            error_item = [img_name, item]
                            error_all_list.append(error_item)
                    try:
                        # 因采用 x1, y1, w, h 排列方式，标注框只可能存在负数、超过边界两种错误
                        bbox = anno["bbox"]
                        x1, y1, w, h = bbox
                        x2 = x1 + w
                        y2 = y1 + h
                    except Exception:
                        # bbox 字段缺失或不完整
                        if img_name not in box_error_list:
                            # box_error_list.append(img_name)
                            error_item = [img_name, item]
                            box_error_list.append(error_item)
                        if img_name not in error_all_list:
                            # error_all_list.append(img_name)
                            error_item = [img_name, item]
                            error_all_list.append(error_item)
                    else:
                        # w, h 值正常
                        if img_w and img_h:
                            # 坐标值异常
                            if x1 < 0 or y1 < 0 or x2 < 0 or y2 < 0 or x2 <= x1 or y2 <= y1 or x2 > img_w or y2 > img_h:
                                if img_name not in box_error_list:
                                    # box_error_list.append(img_name)
                                    error_item = [img_name, item]
                                    box_error_list.append(error_item)
                                if img_name not in error_all_list:
                                    # error_all_list.append(img_name)
                                    error_item = [img_name, item]
                                    error_all_list.append(error_item)
                        # w 值正常， h 异常
                        elif img_w and not img_h:
                            if x1 < 0 or y1 < 0 or x2 < 0 or y2 < 0 or x2 <= x1 or y2 <= y1 or x2 > img_w:
                                if img_name not in box_error_list:
                                    # box_error_list.append(img_name)
                                    error_item = [img_name, item]
                                    box_error_list.append(error_item)
                                if img_name not in error_all_list:
                                    # error_all_list.append(img_name)
                                    error_item = [img_name, item]
                                    error_all_list.append(error_item)
                        # h 值正常， w 异常
                        elif img_h and not img_w:
                            if x1 < 0 or y1 < 0 or x2 < 0 or y2 < 0 or x2 <= x1 or y2 <= y1 or y2 > img_h:
                                if img_name not in box_error_list:
                                    # box_error_list.append(img_name)
                                    error_item = [img_name, item]
                                    box_error_list.append(error_item)
                                if img_name not in error_all_list:
                                    # error_all_list.append(img_name)
                                    error_item = [img_name, item]
                                    error_all_list.append(error_item)
                # 写入对应文件中（.txt）
                result_list = [error_all_list, size_error_list, box_error_list, cls_error_list]
                txt_path_list = [self.error_list_txt, self.size_error_txt, self.box_error_txt, self.cls_error_txt]

                for result, txt_path in zip(result_list, txt_path_list):
                    if result:
                        with open(txt_path, "a+",  encoding="utf-8") as fw:
                            for result_item in result:
                                fw.write(result_item[0] + "," + result_item[1])
                                fw.write("\n")

        if os.path.exists(self.error_list_txt):
            logger.info("the error annotation name has been save to the {}".format(self.error_list_txt))
        else:
            print("there are not error annotations")


def det_check(folder, form, output):
    if form.upper() == "VOC":
        data_check = CheckVoc(dataset_dir=folder, form="VOC", output_dir=output)
    elif form.upper() == "COCO":
        data_check = CheckCoco(dataset_dir=folder, form="COCO", output_dir=output)
    else:
        raise KeyError("The datatype should be VOC or COCO")
    data_check.is_anno_break()
    data_check.is_img_break()


if __name__ == '__main__':
    print("start")
