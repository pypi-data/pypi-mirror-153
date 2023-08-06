# 设置模型路径
import numpy as np
import pandas as pd

from yangke.common.config import logger
from yangke.ebsilon.ebsilon import EbsUnits, EbsApp, EbsModel, EbsObject

model_path = r"C:\Users\YangKe\Desktop\ebs\冷端优化-100%试验工况.ebs"
# data_path = r"C:\Users\杨可\Documents\WPS Cloud Files\217145378\6科研项目\2021\华能重庆两江燃机发电有限责任公司\重庆两江批量计算.xlsx"
data_path = r"C:\Users\YangKe\Documents\WPS Cloud Files\217145378\漫游文档\其他设备\重庆两江批量计算1.xlsx"


class Condition:
    def __init__(self, name):
        self.name = name
        self.data = []

    def append_parameters(self, component, variable, value, unit=None, profile=None):
        self.data.append({"component": component, "variable": variable, "value": value, "unit": unit})


def init_ebsilon():
    """
    初始化ebsilon
    :return:
    """
    ebsilon = EbsApp()
    ebsilon.describe()
    return ebsilon


def read_data_from_xlsx(filename: str):
    """
    读取xlsx文件中的数据，并组装为Conditions字典
    :param filename:
    :return:
    """
    sheet_data: pd.DataFrame = pd.read_excel(filename)
    sheet_data.dropna(subset=["变量名", "组件名"], inplace=True)  # 删除变量名和组件名为空的行
    sheet_data.dropna(axis=1, how="all")
    conditions = {}
    for name in sheet_data.columns[4:]:
        conditions.update({name: Condition(name)})
    for i, row in sheet_data.iterrows():
        # i：行号
        # row=Series(('参数', '压力') ('组件名', 'fgh') ('变量名', 'MEASM') ('单位', 'MPa') ('工况1', 3.8) ('工况2', 3.2)...)
        # row中前三项定义了本行是模型中哪个组件的哪个参数以及参数单位
        # row中从第四项开始是各个工况的数值
        component_name = row["组件名"]
        variable_name = row["变量名"]
        unit = row["单位"]

        for col in row[4:].iteritems():  # row中从第四项开始是各个工况的值
            conditions.get(col[0]).append_parameters(component_name, variable_name, col[1], unit)
    return conditions


def solve(ebsilon, condition):
    model_path_test = f"{model_path[:-4]}_{condition.name}.ebs"

    # 打开模型文件，并激活design的profile
    model: EbsModel = ebsilon.open(model_path)
    model.activate_profile("design")  # 激活当前操作的Profile，后续操作均在激活的Profile上进行

    # 设置组件参数
    for para in condition.data:
        comp = para.get("component")
        var = para.get("variable")
        value = para.get("value")
        unit = para.get("unit")
        model.set_value(comp, var, value, unit, save_flag=False)

    # 获取模型中的参数值
    # p_fgh_gas_in = model.get_value("p_fgh_in_gas", "MEASM", EbsUnits.MPa)
    # power1 = model.get_value("Generator_1","QREAL", EbsUnits.MW)

    model.save_as(model_path_test)  # 另存一份模型，后续在新模型上更改
    ebsilon.show_window()

    ebs_calc_result = model.simulate_new()
    logger.info(ebs_calc_result)

    power1 = power1 = model.get_value("Generator_1", "QREAL", EbsUnits.MW)
    logger.info(f"燃机发电机功率为{power1} MW")

    model.save()
    logger.info(f"工况{condition.name}计算完成！")


data: dict = read_data_from_xlsx(data_path)
ebs = init_ebsilon()
for key, condition in data.items():
    solve(ebs, condition)
