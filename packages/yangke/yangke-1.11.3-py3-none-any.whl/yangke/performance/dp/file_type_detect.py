import os
import pandas as pd
import re

from yangke.common.config import logger
from yangke.common.fileOperate import read_csv_ex


def get_detailed_type_of_data_file(file):
    """
    判断性能试验获得的数据文件类型，是IMP数据、功率数据还是DCS导数或者是其他可以识别处理的文件
    可以处理以下类别的数据：
    1. 有线采集仪采集的数据，返回 imp
    2. 无线采集仪采集的数据，返回 wsn
    3. 功率表采集的功率数据，power
    4. 从pi数据库导出的dcs数据，返回dcs_pi，只支持.xlsx，例如神华国华北京燃机电厂导出的数据
    5. 从SIS系统导出的数据，返回sis
    6. 和利时的点表文件，记录了KKS码对应的点描述，返回kp_hollysys
    7. 和利时的DCS文件，返回dcs_hollysys
    8. 西安热工院DCS系统，返回dcs_tpri
    9. dcs系统导出的数据，dcs1，以陕投商洛电厂的数据格式为例
    10. dcs系统导出的.xls格式的数据，以陕投商洛电厂的数据格式为例，返回dcs2
    11. dcs系统导出的.csv格式数据，以德源府谷电厂3、4号机组为例，返回dcs3
    12. 南京科远dcs系统导出的.csv格式数据，如中煤昔阳电厂DCS系统，返回dcs_sciyon

    :param file: 文件名
    :return: power表示功率表原始文件，imp表示imp到处的excel文件，power with out title表示不带表头的功率文件，dcs1是dcs导数的一种类型，
    具体数据文件示例参见yangke/performance/data_process_example_file/<type>_type_file.*
    """
    if os.path.splitext(os.path.basename(file))[0].endswith("修正"):  # 只处理原始文件，不处理修正数据
        return "修正"
    elif os.path.splitext(os.path.basename(file))[0].endswith("汇总"):
        return "汇总"
    ext_ = os.path.splitext(file)[-1].lower()

    if ext_ == ".xlsx":
        data = pd.read_excel(file, header=None, sheet_name=0, usecols=[0, 1])
    elif ext_ == ".csv":
        data = read_csv_ex(file, sep=",", header=None)
    elif ext_ == ".txt":
        data = read_csv_ex(file, sep="\s+", header=None, on_bad_lines='skip')
    else:
        return None

    data.dropna(axis=0, how="all", inplace=True)
    cell00 = str(data.iloc[0, 0]).strip()

    if cell00 is None:
        return None
    elif cell00.startswith("Model"):
        return "power"
    elif cell00.startswith("Store No."):
        return "power with out title"
    elif cell00.startswith("开始时间"):
        return "imp"
    elif cell00.startswith("历史趋势开始于"):
        return "dcs_tpri"
    elif cell00.startswith('$DataFileVersion'):  # 测试版本： $DataFileVersion: 3
        return "dcs_sciyon"
    elif cell00.startswith("时间") and cell00 != "时间段":
        if ext_ == ".xlsx":
            try:
                if len(data.iloc[1][1]) > 5:
                    return "dcs_pi"
                else:
                    return "wsn"
            except:
                return "wsn"
        elif ext_ == ".csv":
            return "sis"
    elif cell00.startswith("Start") or cell00.endswith(".tgd"):  #
        return "dcs1"
    elif re.match("[0-9]{1,4}年[0-9]{1,2}月[0-9]{1,2}日", cell00):  # 匹配yyyy年mm月dd日
        return "dcs2"
    elif cell00 == "PN" or cell00 == "SN":  # SN是一个看不见的sheet中的第一个cell的内容
        return "kp_hollysys"
    elif cell00 == "时间段":
        return "dcs_hollysys"
    elif cell00 == "Time":
        data.dropna(axis=1, how="all", inplace=True)
        if data.shape[1] > 2:
            return "dcs_3"
        else:
            return "unknown"
    else:
        logger.warning(f"文件未识别：{file}")
        return "unknown"
