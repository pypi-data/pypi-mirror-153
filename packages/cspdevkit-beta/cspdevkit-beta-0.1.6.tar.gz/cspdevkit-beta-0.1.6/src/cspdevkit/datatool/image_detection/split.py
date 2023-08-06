#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/5/7 11:04
# @Author  : xgy
# @Site    : 
# @File    : split.py
# @Software: PyCharm
# @python version: 3.7.4
"""
import os
import shutil
import random
import json
from loguru import logger

from cspdevkit.datatool.image_detection.utils import load_json


class VocSplit:

    def __init__(self, data_dir, ratios=None):
        self.data_dir = data_dir
        self.ratios = ratios

    def split(self, mode=None):
        """
        VOC 数据集切分，优先级：
        1. train.txt, val.txt 同时存在删除后才能切分
        2. trainval.txt, train.txt 同时存在需指定其一作为切分依据（mode）
        3. train.txt, train.txt 有且只有一个时，以存在的文件为切分依据
        4. 无 txt 文件时，以Annotations 文件夹中所有文件为切分依据
        5. 切分后数据为train.txt, val.txt, 即原 train.txt 会被覆盖，trainval.txt 会被保留
        """

        if self.ratios is None:
            train_ratio = 0.9
        else:
            train_ratio = self.ratios

        xmlfilepath = os.path.join(self.data_dir, 'Annotations')
        txtsavepath = os.path.join(self.data_dir, 'ImageSets/Main')
        trainval_path = os.path.join(txtsavepath, "trainval.txt")
        train_path = os.path.join(txtsavepath, "train.txt")
        val_path = os.path.join(txtsavepath, "val.txt")

        if os.path.exists(train_path) and os.path.exists(val_path):
            logger.error("train.txt and val.txt already exists, and there is no need to split."
                        "If you want to re split, please delete them first")
            return False

        if not mode:
            if os.path.exists(trainval_path) and os.path.exists(train_path):
                logger.error("both train.txt and trainval.txt are exist, please specify one using the parameter 'mode'")
                return False

        total_xml = None
        if not mode:
            if os.path.exists(trainval_path):
                split_path = trainval_path
            elif os.path.exists(train_path):
                split_path = train_path
            else:
                os.makedirs(txtsavepath, exist_ok=True)
                total_xml = os.listdir(xmlfilepath)
                split_path = None
        else:
            os.makedirs(txtsavepath, exist_ok=True)
            split_name = mode + ".txt"
            split_path = os.path.join(txtsavepath, split_name)

        if not total_xml:
            with open(split_path, "r", encoding="utf-8") as fr:
                xml_l = fr.readlines()
            total_xml = []
            for item in xml_l:
                total_xml.append(item.replace("\n", "") + ".xml")

        num = len(total_xml)
        list_ids = range(num)

        len_train = int(num * train_ratio)
        train_l = random.sample(list_ids, len_train)

        ftrain = open(os.path.join(self.data_dir, 'ImageSets/Main/train.txt'), 'w', encoding='utf-8')
        fval = open(os.path.join(self.data_dir, 'ImageSets/Main/val.txt'), 'w', encoding='utf-8')

        for i in list_ids:
            name = total_xml[i][:-4] + '\n'
            if i in train_l:
                ftrain.write(name)
            else:
                fval.write(name)

        ftrain.close()
        fval.close()

        logger.info("the split result files saved in {}".format(os.path.join(self.data_dir, 'ImageSets/Main')))


class CocoSplit:

    def __init__(self, data_dir, ratios=None):
        self.data_dir = data_dir
        self.ratios = ratios
        self.ori_Annotations_dir = os.path.join(self.data_dir, "Annotations")
        # self.ori_Images_dir = os.path.join(self.data_dir, "train")

    def split(self, mode=None):
        """
        COCO 数据集切分，优先级：
        0. 应保证coco数据目录结构满足定义要求， 即图片文件夹与json文件一一对应，如train与train.json
        1. train, val 同时存在删除后才能切分
        2. trainval, train 同时存在需指定其一作为切分依据（mode）
        3. train, train 有且只有一个时，以存在的文件为切分依据
        4. 切分后数据为train, val, 即原 train 会被覆盖，trainval 会被保留
        5. 切分后 train.json, val.json 中  ["images"]["id"] 均从0开始编号
        """
        if not self.ratios:
            train_percent = 0.9
        else:
            train_percent = self.ratios

        trainval_path = os.path.join(self.data_dir, "trainval")
        train_path = os.path.join(self.data_dir, "train")
        val_path = os.path.join(self.data_dir, "val")

        if os.path.exists(train_path) and os.path.exists(val_path):
            logger.error("train and val already exists, and there is no need to split."
                        "If you want to re split, please delete them first")
            return False

        if not mode:
            if os.path.exists(trainval_path) and os.path.exists(train_path):
                logger.error("both train and trainval are exist, please specify one using the parameter 'mode'")
                return False

        if mode is None:
            if os.path.exists(trainval_path) and not os.path.exists(train_path):
                data_types = ["trainval"]
            elif not os.path.exists(trainval_path) and os.path.exists(train_path):
                data_types = ["train"]
            else:
                raise KeyError("train and trainval must have one in {}".format(self.data_dir))
        else:
            data_types = [mode]

        for i, datatype in enumerate(data_types):
            annFile = '{}.json'.format(datatype)
            annpath = os.path.join(self.ori_Annotations_dir, annFile)
            data = load_json(annpath)

            images = data["images"]
            categories = data["categories"]
            annotations = data["annotations"]
            coco_type = data["type"]

            # 按序号索引划分比例
            num = len(images)
            list_ids = range(num)

            len_train = int(num * train_percent)
            train = random.sample(list_ids, len_train)

            # 划分 images
            images_class, imgids_class, filename_class = self.split_images(images, list_ids, train)

            # 划分 annotations
            annotations_class = self.split_annotations(annotations, imgids_class)

            # 从0开始重新编号
            images_class, annotations_class = self.drop_index(images_class, annotations_class)

            train_json = {"images": images_class[0],
                          "type": coco_type,
                          "annotations": annotations_class[0],
                          "categories": categories}
            val_json = {"images": images_class[1],
                        "type": coco_type,
                        "annotations": annotations_class[1],
                        "categories": categories}

            class_json = ["train", "val"]
            list_json = [train_json, val_json]
            for json_name, json_item in zip(class_json, list_json):
                json_item_path = os.path.join(self.ori_Annotations_dir, json_name + ".json")
                with open(json_item_path, "w", encoding="utf-8") as fw:
                    json.dump(json_item, fw, ensure_ascii=False, indent=4)
            logger.info("the annotations has been splited in to ['train.json', 'val.json'] saving in {}".format(self.ori_Annotations_dir))

            # 划分图片文件夹
            self.split_im(filename_class, datatype)
            logger.info("the images has been splited in to ['train', 'val'] saving in {}".format(os.path.join(self.data_dir)))

    @staticmethod
    def drop_index(data_images, data_anno):
        # 从0开始重新编号
        n_data_images = []
        n_data_anno = []

        for imags, annos in zip(data_images, data_anno):
            n_imags = []
            n_annos = []
            imag_id_dict = {}
            for index, imag in enumerate(imags):
                imag_id_dict[str(imag["id"])] = index
                imag["id"] = index
                n_imags.append(imag)
            for index, anno in enumerate(annos):
                anno["id"] = index
                anno["image_id"] = imag_id_dict[str(anno["image_id"])]
                n_annos.append(anno)
            n_data_images.append(n_imags)
            n_data_anno.append(n_annos)
        return n_data_images, n_data_anno


    # 划分 images 字段
    @staticmethod
    def split_images(images, list_ids, train):
        images_train = []
        images_val = []

        images_train_imgids = []
        images_val_imgids = []

        images_train_filename = []
        images_val_filename = []

        for item in list_ids:
            if item in train:
                images_train.append(images[item])
                images_train_imgids.append(images[item]["id"])
                images_train_filename.append(images[item]["file_name"])
            else:
                images_val.append(images[item])
                images_val_imgids.append(images[item]["id"])
                images_val_filename.append(images[item]["file_name"])

        images_class = [images_train, images_val]
        imgids_class = [images_train_imgids, images_val_imgids]
        filename_class = [images_train_filename, images_val_filename]

        return images_class, imgids_class, filename_class

    # 划分 annotations 字段
    @staticmethod
    def split_annotations(annotations, imgids_class):
        annotations_train = []
        annotations_val = []

        # 划分 annotations
        for annotation in annotations:
            annotation_img_id = annotation["image_id"]
            if annotation_img_id in imgids_class[0]:
                annotations_train.append(annotation)
            else:
                annotations_val.append(annotation)

        annotations_class = [annotations_train, annotations_val]

        return annotations_class

    # 划分图片
    def split_im(self, filename_class, datatype):
        # 划分图片文件夹
        trainval_img_dir = os.path.join(self.data_dir, "trainval")
        train_img_dir = os.path.join(self.data_dir, "train")
        val_img_dir = os.path.join(self.data_dir, "val")

        os.makedirs(val_img_dir, exist_ok=True)
        # os.makedirs(train_img_dir, exist_ok=True)

        if datatype == "trainval":
            ori_Images_dir = trainval_img_dir
            os.makedirs(train_img_dir, exist_ok=True)
        elif datatype == "train":
            ori_Images_dir = train_img_dir
        else:
            raise KeyError("train and trainval must have one in {}".format(self.data_dir))

        for ori_Images_root, _, ori_img_files in os.walk(ori_Images_dir):
            for ori_img_file in ori_img_files:
                ori_img_path = os.path.join(ori_Images_root, ori_img_file)
                if ori_img_file in filename_class[0]:
                    if datatype == "trainval":
                        dst_img_val_path = os.path.join(train_img_dir, ori_img_file)
                        shutil.copy(ori_img_path, dst_img_val_path)
                    if datatype == "train":
                        pass
                else:
                    if datatype == "trainval":
                        dst_img_val_path = os.path.join(val_img_dir, ori_img_file)
                        shutil.copy(ori_img_path, dst_img_val_path)
                    if datatype == "train":
                        dst_img_test_path = os.path.join(val_img_dir, ori_img_file)
                        shutil.move(ori_img_path, dst_img_test_path)


def det_split(folder, form, ratio, mode=None):
    if form.upper() == "VOC":
        data_split = VocSplit(data_dir=folder, ratios=ratio)
    elif form.upper() == "COCO":
        data_split = CocoSplit(data_dir=folder, ratios=ratio)
    else:
        raise KeyError("The datatype should be VOC or COCO")
    data_split.split(mode=mode)


if __name__ == '__main__':
    print("start")

    # test_voc = "C:/Users/xgy/Desktop/CSPTools/0507/20220507154909278914/voc_ori_split"
    # det_split(folder=test_voc, form="voc", ratio=0.9, mode=None)

    # test_coco = "C:/Users/xgy/Desktop/CSPTools/0507/20220507154909278914/coco_split/"
    # det_split(folder=test_coco, form="COCO", ratio=0.9, mode=None)

