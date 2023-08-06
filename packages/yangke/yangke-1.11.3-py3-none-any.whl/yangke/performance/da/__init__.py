"""
data_analysis.py的数据处理方法
data_analysis.py负责维护GUI界面，这里放计算方法
"""
from yangke.performance.basic_para import Case, alternative_symbol
import pandas as pd
from yangke.core import strInList
from yangke.base import extend_list_by_alternative_symbols
import copy
from yangke.common.config import logger


def update_data(imp_file, p_file=None, dcs_file=None):
    """
    将试验测点名称对应的数据赋值给计算程序中相应参数

    :param df:
    :return:
    """
    cases = {}
    df = pd.read_excel(imp_file, index_col=0)
    values = df.values
    case_names = list(df.columns)  # 计算工况名称，每项对应一个工况
    var_names = list(df.index)
    current_case = Case()  # 当前工况，临时变量
    # 将各参数归类到Case类对应的变量上
    annotations = Case.__annotations__
    case_para_loc = {}  # 记录计算程序参数对应的试验测点在df数据结构中的位置
    for name in annotations.keys():  # 计算程序中参数名称
        case_para_loc.update({name: []})  # 每个计算程序参数可能对应多个试验测点，计算中取平均值，这里将多个测点位置记录在列表中
    # -------------------------- 首先确定试验测点对应哪个计算程序参数 ---------------------------------
    for i, name in enumerate(var_names):  # 试验测点的名称
        flag = False
        for k, v in annotations.items():  # 计算程序参数k，和其可能的名称v
            name_sub_str_list = v.split(",")  # 将可能的名称v转为列表
            name_sub_str_list = extend_list_by_alternative_symbols(name_sub_str_list, alternative_symbol)
            if strInList(name, name_sub_str_list, revert=True):  # 如果计算程序参数k可能的名称命中试验参数名称，则记录
                case_para_loc.get(k).append(i)
                flag = True
                break  # 如果当前试验测点已经对应一个计算程序参数，则不可能对应另一个计算程序参数，因此跳出当前循环
        if flag is False:  # 说明没有找到测点对应的计算程序中的参数名
            logger.warning(f"测点名称({name})对应的计算程序参数名未知！")

    logger.debug(case_para_loc)
    for i, case_name in enumerate(case_names):  # 遍历所有工况
        for k, loc in case_para_loc.items():  # 遍历所有测点
            if len(loc) != 0:
                # 将测点名和测点数值传给TestPoint对象，让其初始化测点数据
                temp_series = df[case_name].iloc[loc]
                name_list = list(temp_series.index)
                value_list = temp_series.values
                current_case.set_value_of_test_point(var_str=k, test_point_name_list=name_list,
                                                     value_list=value_list)
        cases.update({case_name: copy.deepcopy(current_case)})
    return cases


def generate_case_skeleton(case):
    """
    根据单个工况的数据，猜测生成机组的热力系统结构。

    :param case:
    :return:
    """
    logger.debug("生成热力系统结构")
    pass
