#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/4/27 9:50
# @Author  : xgy
# @Site    : 
# @File    : eva.py
# @Software: PyCharm
# @python version: 3.7.4
"""

import os
import sys
import json
import pandas as pd
import numpy as np
from loguru import logger


class EntityEva:

    def __init__(self, pre_path, eva_patn, category_path, source_path, long_text_categories, output=None):
        self.pre_path = pre_path
        self.eva_patn = eva_patn
        self.category_path = category_path
        self.source_path = source_path
        self.long_text_categories = long_text_categories
        self.output = output


    @staticmethod
    def list_category_values(categoryid, df):
        """
        将labels.json中一个元素（{}）转为字符串，用于后续匹配判断正误
        拼接元素包含 "srcId + name + startIndex + endIndex"
        :return:
        """
        values = []
        df_category = df[df["categoryId"] == categoryid].reset_index(drop=True)
        len_category = len(df_category)
        for _, row in df_category.iterrows():
            key = str(row["srcId"]) + str(row["name"]) + str(row["startIndex"]) + str(row["endIndex"])
            values.append(key)

        return values, len_category

    @staticmethod
    def calculate(y_true, y_pred, len_true, len_pred):
        """
        计算 precision, recall
        """
        tp_count = 0
        for pred in y_pred:
            if pred in y_true:
                tp_count += 1

        precision = round(tp_count / len_pred, 6)
        recall = round(tp_count / len_true, 6)

        return precision, recall

    def df_proc(self, df):
        df_source_spilt = self.df_source[["id", "content"]]
        col_names_mid = ["id", "srcId", "categoryId", "startIndex", "endIndex", "name", "content"]
        col_names_final = ["id", "srcId", "categoryId", "category", "startIndex", "endIndex", "name", "content"]
        df = pd.merge(df, df_source_spilt, left_on="srcId", right_on='id', how="inner")
        df = df.iloc[:, np.r_[0:6, 7]]
        df.columns = col_names_mid
        df = pd.merge(df, self.df_category, left_on="categoryId", right_on='id', how="inner")
        df = df.iloc[:, np.r_[0:3, 8, 3:7]]
        df.columns = col_names_final

        return df

    def evaluate(self, output_eval):
        series = []
        final_precision = 0
        final_recall = 0
        final_f_score = 0
        for categoryid in self.categoryids:

            y_true, len_true = self.list_category_values(categoryid, self.df_true)
            y_pred, len_pred = self.list_category_values(categoryid, self.df_pred)

            precision, recall = self.calculate(y_true, y_pred, len_true, len_pred)

            final_precision += precision
            final_recall += recall
            f_score = 0
            if (precision + recall) > 0:
                f_score = 2 * precision * recall / (precision + recall)
            final_f_score += f_score
            result = {"cid": categoryid,
                      "precision": precision,
                      "recall": recall,
                      "f_score": f_score,
                      "category": self.category_dict[categoryid]}
            series.append(result)
        final_precision = round(final_precision / len(self.categoryids), 6)
        final_recall = round(final_recall / len(self.categoryids), 6)
        final_f_score = round(final_f_score / len(self.categoryids), 6)
        result = {"cid": "total",
                  "precision": final_precision,
                  "recall": final_recall,
                  "f_score": final_f_score,
                  "category": "total"}
        series.append(result)

        result_df = pd.DataFrame(series)
        print(result_df)
        result_df.to_csv(output_eval, sep=",", encoding="utf-8", index=False)

    def get_data(self):
        # 固定列顺序
        true_raw = pd.read_json(self.eva_patn)[["id", "srcId", "categoryId", "startIndex", "endIndex", "name"]]
        pred_raw = pd.read_json(self.pre_path)[["id", "srcId", "categoryId", "startIndex", "endIndex", "name"]]
        df_source = pd.read_json(self.source_path)
        df_category = pd.read_json(self.category_path)
        with open(self.category_path, "r", encoding="utf-8") as f:
            categories = json.load(f)

        self.true_raw = true_raw
        self.pred_raw = pred_raw
        self.df_source = df_source
        self.df_category = df_category
        self.categories = categories

        return true_raw, pred_raw, categories, df_source, df_category

    def data_filter_by_igcategory(self):
        logger.info("this categories will be ignore {}".format(self.long_text_categories))
        ignore_categoryids = []
        categoryids = []
        category_dict = {}
        for category in self.categories:
            categoryid = category["id"]
            label = category["text"]

            category_dict[categoryid] = label

            # if label in ["工程承包范围", "合同工期", "付款方式", "结算方式"]:
            if label in self.long_text_categories:
                ignore_categoryids.append(categoryid)
            else:
                categoryids.append(categoryid)

        if not ignore_categoryids:
            self.df_true = self.true_raw
            self.df_pred = self.pred_raw
        else:
            for item in ignore_categoryids:
                self.df_true = self.true_raw[self.true_raw["categoryId"] != item]
            for item in ignore_categoryids:
                self.df_pred = self.pred_raw[self.pred_raw["categoryId"] != item]
        self.category_dict = category_dict
        self.categoryids = categoryids

    def get_badcase(self):
        list_good = []
        list_bad = []
        true_keys = []
        for _, row_true in self.df_true.iterrows():
            row_true_split = list(row_true)[1:6]
            row_true_str = []
            for item in row_true_split:
                item_str = str(item)
                row_true_str.append(item_str)
            key_true = "_".join(row_true_str)
            true_keys.append(key_true)

        for _, row_pred in self.df_pred.iterrows():
            row_pred_split = list(row_pred)[1:6]
            row_pred_str = []
            for item in row_pred_split:
                item_str = str(item)
                row_pred_str.append(item_str)
            key_pred = "_".join(row_pred_str)

            if key_pred in true_keys:
                list_good.append(list(row_pred))
            else:
                list_bad.append(list(row_pred))

        col_names = ["id", "srcId", "categoryId", "startIndex", "endIndex", "name"]
        # df_good = pd.DataFrame(list_good, columns=col_names)
        # df_bad = pd.DataFrame(list_bad, columns=col_names)
        df_good = self.df_proc(pd.DataFrame(list_good, columns=col_names))
        df_bad = self.df_proc(pd.DataFrame(list_bad, columns=col_names))

        return df_good, df_bad

    @staticmethod
    def df2files(df, output_json, output_excel):
        df.to_json(output_json, orient="records", force_ascii=False, indent=4)
        df.to_excel(output_excel, index=False)

usage = "python ner_eva.py --submit_file ../01-data/submit_0630.json --test_file ../01-data/eval_labels.json --category_file categories.json --output ../01-data/reuslt_eva.csv '工程承包范围', '合同工期'"

def print_error_msg(msg, code):
    result_json = {}
    result_json['error_msg'] = msg
    result_json['error_code'] = code
    result_json['usage'] = usage
    print(json.dumps(result_json, ensure_ascii=False))


def entity_eva(pre_path, eval_path, category_path, source_path, long_text_categories, output):
    if not os.path.exists(pre_path) or not os.path.isfile(pre_path):
        print_error_msg(("未找到待评估的预测结果文件: %s" % pre_path), 1001)
        sys.exit(1)

    if not os.path.exists(eval_path) or not os.path.isfile(eval_path):
        print_error_msg(("未找到标注测试集文件: %s" % eval_path), 1002)
        sys.exit(1)

    if not os.path.exists(output) or not os.path.isdir(output):
        print_error_msg(("指定的输出目录不存在或不是个目录: %s" % output), 1003)
        sys.exit(1)


    file_good_json = "good" + ".json"
    file_bad_json = "bad" + ".json"
    file_good_excel = "good" + ".xlsx"
    file_bad_excel = "bad" + ".xlsx"
    file_eval = "eval" + ".csv"
    output_good_json = os.path.join(output, file_good_json)
    output_bad_json = os.path.join(output, file_bad_json)
    output_good_excel = os.path.join(output, file_good_excel)
    output_bad_excel = os.path.join(output, file_bad_excel)
    output_eval = os.path.join(output, file_eval)

    entityeva = EntityEva(pre_path, eval_path, category_path, source_path, long_text_categories, output=output)
    entityeva.get_data()
    entityeva.data_filter_by_igcategory()
    df_good, df_bad = entityeva.get_badcase()

    entityeva.df2files(df_good, output_good_json, output_good_excel)
    entityeva.df2files(df_bad, output_bad_json, output_bad_excel)

    entityeva.evaluate(output_eval)


if __name__ == '__main__':
    print("start")
    # test_dir = "C:/Users/xgy/Desktop/CSPTools/0424/文本实体标注格式EVA"
    # pre_path = os.path.join(test_dir, 'labels_pre.json')
    # eva_patn = os.path.join(test_dir, 'labels_test.json')
    # category_path = os.path.join(test_dir, 'labelCategories.json')
    # source_path = os.path.join(test_dir, 'sources.json')
    # # long_text_categories = []
    # long_text_categories = ["工程承包范围", "合同工期", "付款方式", "结算方式"]
    # out = "D:/document/pycharmpro/CSPTools/test/output"
    #
    # entity_eva(pre_path, eva_patn, category_path, source_path, long_text_categories, out)
