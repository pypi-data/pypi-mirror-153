#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/5/7 16:54
# @Author  : xgy
# @Site    : 
# @File    : eva.py
# @Software: PyCharm
# @python version: 3.7.4
"""

import os
import logging.handlers
import sys
import traceback
import numpy as np, math, time
from tqdm import tqdm

# from terminaltables import AsciiTable
from cspdevkit.common.utils import RunSys
from cspdevkit.datatool.image_detection.utils import init_log, load_json, get_file_names, get_class, get_pre_data, get_ann, image_detection,  \
    plot_boxes, create_legend, create_top

from cspdevkit.datatool.image_detection.voc_xml import gen_voc_xml, gen_object

logger = logging.getLogger(__name__)

class DetEva:

    def __init__(self, submit_file, gold_file, origin_image_dir=None, output_dir=None):
        self.submit_file = submit_file # 目标检测待评估的json文件
        self.gold_file = gold_file  # 测试集标注数据的JSON文件，该文件为coco格式的文件
        self.origin_image_dir = origin_image_dir # 测试集图片文件路径
        self.output_image_dir = os.path.join(output_dir, "image") if output_dir else None # 输出badcase混合图片文件存储路径（允许不传，不传即不生成）
        self.output_voc_file_dir = os.path.join(output_dir, "voc") if output_dir else None # 输出badcase的voc格式xml文件存储路径（允许不传，不传即不生成）

        self.gt_data = load_json(self.gold_file)
        self.pred_data = load_json(self.submit_file)

    def eva(self):
        # initialize log output configuration
        init_log(logging.INFO)

        # set predicted and gold json file paths
        predicted_file_json_path = self.submit_file
        gold_json_file_path = self.gold_file
        origin_image_file_path = self.origin_image_dir
        output_image_file_path = self.output_image_dir
        output_voc_file_path = self.output_voc_file_dir

        logger.info('predicted_file_json_path: {}'.format(predicted_file_json_path))
        logger.info('gold_json_file_path: {}'.format(gold_json_file_path))
        logger.info('origin_image_file_path: {}'.format(origin_image_file_path))
        logger.info('output_image_file_path: {}'.format(output_image_file_path))
        logger.info('output_voc_file_path: {}'.format(output_voc_file_path))

        score, message, status, bad_cases = self.entrance()
        t1 = time.time()
        if output_image_file_path:
            os.makedirs(output_image_file_path, exist_ok=True)
            self.gen_img_badcase(bad_cases)
        # processing_treat(gen_img_badcase, predicted_file_json_path,gold_json_file_path,bad_cases,origin_image_file_path,output_image_file_path)#

        if output_voc_file_path:
            os.makedirs(output_voc_file_path, exist_ok=True)
            self.gen_voc_badcase(bad_cases)
        # processing_treat(gen_voc_badcase, predicted_file_json_path,gold_json_file_path,bad_cases,origin_image_file_path,output_voc_file_path)
        print('time cost:', time.time() - t1)


    def entrance(self):
        score, message, bad_cases = self.evaluate_image_score(iou_threshold=0.5, false_detection_weight=0.3,
                                                         missed_detection_weight=0.5, object_detection_weight=0.2)
        if message != "评测成功":
            status = 0
        else:
            status = 1

        return score, message, status, bad_cases


    def evaluate_image_score(self, iou_threshold: float, false_detection_weight: float,
                             missed_detection_weight: float, object_detection_weight: float):
        """ calculate the  image score by the predicted and gold json file """
        try:
            # gt_data的数据中，是(x1,y1,w, h)
            # id_file_name是字典，id: filename
            # file_name_id与id_file_name相反， filename:id
            id_file_name, file_name_id = get_file_names(self.gt_data['images'])
            # class_name_list是将所有类别名称，用列表表示
            # class_name_dict是字典格式，将类别名称与id号进行关联映射，类别名称：id
            # catid_name_dict与class_name_dict相反，id: 类别名称
            class_name_list, class_name_dict, catid_name_dict = get_class(self.gt_data)

            pred_data = get_pre_data(self.pred_data, file_name_id, class_name_dict)
            # load the names of categories

            ap_table = [["category", "false detection rate", "missed detection rate", "object detection correct rate",
                         "image score"]]

            sum_false_detection_rate = 0
            sum_missed_detection_rate = 0
            sum_object_detection_correct_rate = 0
            sum_image_score = 0
            bad_cases = []
            for class_name in class_name_list:  # 逐个遍历类别，统计每个类别的检测结果。
                # traverse the images, a batch of one picture
                false_detection_count = 0
                detection_total_count = 0
                missed_detection_count = 0
                gold_total_count = 0
                object_detection_correct_count = 0
                object_detection_total_count = 0

                for i in range(len(self.gt_data['images'])):
                    image_id = self.gt_data['images'][i]['id']
                    # load gold annotations，ann_gt = n * [cls_id, x1, y1, x2, y2]
                    ann_gt = get_ann(image_id, self.gt_data['annotations'])
                    # load predicted annotations，ann_pred = n * [x1, y1, x2, y2, pred_score, cls_id]
                    ann_pred = get_ann(image_id, pred_data)  # 要注意ann_pred的数据格式，与ann_gt略有不同
                    # sort the ann pred list by the confidence pred scores in a descending order
                    # predicted no_wear boxes and labels
                    if len(ann_pred) == 0:
                        pred_no_wear_indices, pred_labels, pred_boxes = [], [], []
                    else:
                        # 获取预测类别为class_name的矩形框数据索引号，即第几个数据为指定类别
                        pred_no_wear_indices = np.where(ann_pred[:, 0] == class_name_dict[class_name])
                        pred_boxes = ann_pred[:, 1:][pred_no_wear_indices]

                    # target no_wear boxes and labels
                    if len(ann_gt) == 0:
                        target_no_wear_indices, target_labels, target_boxes = [], [], []
                    else:
                        target_no_wear_indices = np.where(ann_gt[:, 0] == class_name_dict[class_name])
                        target_boxes = ann_gt[:, 1:][target_no_wear_indices]
                    false_detection_number, missed_detection_number, detection_number, target_number = image_detection(
                        pred_boxes=pred_boxes, target_boxes=target_boxes, iou_threshold=iou_threshold)
                    object_detection_correct_number = target_number - missed_detection_number

                    false_detection_count += false_detection_number
                    detection_total_count += detection_number

                    missed_detection_count += missed_detection_number
                    gold_total_count += target_number

                    object_detection_correct_count += object_detection_correct_number
                    object_detection_total_count += target_number

                    if false_detection_number > 0 or missed_detection_number > 0:
                        bad_cases.append(image_id)

                false_detection_rate = round(false_detection_count / detection_total_count, 4) if (
                            detection_total_count != 0) else 0
                missed_detection_rate = round(missed_detection_count / gold_total_count, 4) if (
                            gold_total_count != 0) else 0
                object_detection_correct_rate = round(object_detection_correct_count / object_detection_total_count, 4) if (
                            object_detection_total_count != 0) else 0
                logger.info('checking the class of {}'.format(class_name))
                logger.info("false_detection_rate: {} / {} = {}".format(false_detection_count, detection_total_count,
                                                                        false_detection_rate))
                logger.info("missed_detection_rate: {} / {} = {}".format(missed_detection_count, gold_total_count,
                                                                         missed_detection_rate))
                logger.info("object_detection_correct_rate: {} / {} = {}".format(object_detection_correct_count,
                                                                                 object_detection_total_count,
                                                                                 object_detection_correct_rate))

                image_score = round(1 - (
                            false_detection_weight * false_detection_rate + missed_detection_weight * missed_detection_rate + object_detection_weight * (
                                1 - object_detection_correct_rate)), 4)

                logger.info("evaluation for {} and {}\n".format(self.submit_file, self.gold_file))

                ap_table += [
                    [class_name, false_detection_rate, missed_detection_rate, object_detection_correct_rate, image_score]]

                sum_false_detection_rate = sum_false_detection_rate + false_detection_rate
                sum_missed_detection_rate = sum_missed_detection_rate + missed_detection_rate
                sum_object_detection_correct_rate = sum_object_detection_correct_rate + object_detection_correct_rate
                sum_image_score = sum_image_score + image_score
            ap_table += [['total', round(sum_false_detection_rate / len(class_name_list), 4),
                          round(sum_missed_detection_rate / len(class_name_list), 4),
                          round(sum_object_detection_correct_rate / len(class_name_list), 4),
                          round(sum_image_score / len(class_name_list), 4)]]

            try:
                from terminaltables import AsciiTable
            except ImportError:
                logger.warning("there is no terminaltables try to install it, pip install terminaltables")
                install_cmd = "pip install terminaltables"
                RunSys(command=install_cmd).run_cli()
                from terminaltables import AsciiTable

            logger.info("\n{}\n".format(AsciiTable(ap_table).table))

            return float('{:.8f}'.format(sum_image_score / len(class_name_list))), "评测成功", list(set(bad_cases))
        except Exception as e:
            traceback.print_exc()
            return -1, "格式错误", []
        except AssertionError:
            traceback.print_exc()
            _, _, tb = sys.exc_info()
            traceback.print_tb(tb)
            tb_info = traceback.extract_tb(tb)
            filename, line, func, text = tb_info[-1]

            logger.info('an error occurred on line {} in statement {}'.format(line, text))

            return -1, "格式错误", []

    def gen_img_badcase(self, bad_cases: list):
        '''
        生成badcase (拼接图片)
        '''
        import skimage.io as io
        id_file_name, file_name_id = get_file_names(self.gt_data['images'])
        class_name_list, class_name_dict, catid_name_dict = get_class(self.gt_data)
        pred_data = get_pre_data(self.pred_data, file_name_id, class_name_dict)
        for image_id in tqdm(bad_cases):
            ann_gt = get_ann(image_id, self.gt_data['annotations'])
            origin_image_path = os.path.join(self.origin_image_dir, id_file_name[image_id])  # step 2原始的coco的图像存放位置
            origin_draw_img = plot_boxes(origin_image_path, ann_gt, catid_name_dict)
            ori_size = origin_draw_img.size
            legend = create_legend(ori_size[1], catid_name_dict)  # 创建标签图片
            pj1 = np.zeros((ori_size[1], ori_size[0] * 2 + legend.size[0], 3), dtype=np.uint8)  # 横向拼接
            pj1[:, ori_size[0]: ori_size[0] * 2, :] = origin_draw_img  # 原始图片在中间
            pj1[:, ori_size[0] * 2:, :] = legend  # 标签铭牌在右
            del origin_draw_img, legend  # 为减少内存占用，事先提早删除不必要的数组

            ann_pred = get_ann(image_id, pred_data)
            pred_draw_img = plot_boxes(origin_image_path, ann_pred, catid_name_dict)
            pj1[:, :ori_size[0], :] = pred_draw_img  # 预测图片在左
            del pred_draw_img

            top = create_top(ori_size)  # 增加抬头标题， top是Image的格式，形状是W * H
            final = np.ones((top.size[1] + pj1.shape[0], pj1.shape[1], 3), dtype=np.uint8) * 255  # H * W * 3的形状
            final[:top.size[1], : top.size[0], :] = top
            final[top.size[1]:, :, :] = pj1
            del pj1
            final = np.array(final, dtype=np.uint8)
            output_image = os.path.join(self.output_image_dir, id_file_name[image_id])
            io.imsave(output_image, final)  # 保存拼接后的图片
            del final, top

    def gen_voc_badcase(self, bad_cases: list):
        '''
        生成voc
        '''
        id_file_name, file_name_id = get_file_names(self.gt_data['images'])
        class_name_list, class_name_dict, catid_name_dict = get_class(self.gt_data)
        pred_data = get_pre_data(self.pred_data, file_name_id, class_name_dict)
        id_img_dict = {img_info['id']: img_info for img_info in self.gt_data['images']}
        for image_id in tqdm(bad_cases):
            objs = []
            # _, ann_gt = get_ann(image_id, gt_data['annotations'])
            img_info = id_img_dict[image_id]
            ann_pred = get_ann(image_id, pred_data)
            for ann in ann_pred:
                xmin = int(ann[1])
                ymin = int(ann[2])
                xmax = int(ann[3])
                ymax = int(ann[4])

                obj = gen_object(catid_name_dict[int(ann[0])], xmin, ymin, xmax, ymax)
                objs.append(obj)
            xml_name = os.path.splitext(id_file_name[image_id])[0] + '.xml'
            xml_name = os.path.join(self.output_voc_file_dir, xml_name)
            gen_voc_xml(img_info['file_name'], objs, img_info['width'], img_info['height'], xml_name)


def det_eva(submit_file, gold_file, origin_image_dir=None, output_dir=None):
    """
    需注意 submit_file, gold_file 的格式，见 example/obj_det/
    """
    json_eva = DetEva(submit_file, gold_file, origin_image_dir=origin_image_dir, output_dir=output_dir)
    json_eva.eva()


if __name__ == '__main__':
    print("start")
    # submit_file = "D:/document/pycharmpro/cspdataset/examples/datatools/eva/det/test_pred_simple.json"
    # submit_file = "D:/document/pycharmpro/cspdataset/examples/datatools/eva/det/test1.json"
    # gold_file = "D:/document/pycharmpro/cspdataset/examples/datatools/eva/det/test.json"
    # origin_image_dir = ""
    # output_dir = "D:/document/pycharmpro/CSPTools/test/output"

    # submit_file = "C:/Users/xgy/Desktop/CSPTools/0507/20220507154909278914/coco_ori_eva/Annotations/pred.json"
    # gold_file = "C:/Users/xgy/Desktop/CSPTools/0507/20220507154909278914/coco_ori_eva/Annotations/test.json"
    # origin_image_dir = "C:/Users/xgy/Desktop/CSPTools/0507/20220507154909278914/coco_ori_eva/trainval"
    # output = "C:/Users/xgy/Desktop/CSPTools/0507/20220507154909278914/coco_ori_eva/eva_output"
    #
    # test_eva = DetEva(submit_file, gold_file, origin_image_dir=origin_image_dir, output_dir=output)
    # test_eva.eva()

    # C:\Users\xgy\Desktop\CSPTools\0507\20220507154909278914\coco_ori_eva\Annotations