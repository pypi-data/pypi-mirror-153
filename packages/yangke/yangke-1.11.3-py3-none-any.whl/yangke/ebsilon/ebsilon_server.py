"""
ebsilon计算服务端
用户先上传*.ebs模型文件和settings.xlsx设置文件（目前尚未定义上传方法，可以通过mstsc远程上传），然后服务端加载设置文件信息，
获取用户传入参数和*.ebs模型中的组件参数的对应关系。
后续用户计算某个工况时，只需要通过restful接口传入指定参数的值，即可获得计算服务端返回的计算结果

EbsApp的对象全局初始化时，在处理新请求时会报错：pywintypes.com_error: (-2147221008, '尚未调用 CoInitialize。', None, None)。
因此，只能在每一个请求时都单独初始化EbsApp.
flask对每一个请求对新建一个线程进行处理，而不同线程创建的EbsApp等COM组件互相之间无法通信，因此，智能在每一个请求中单独初始化EbsApp
"""

import os.path
import json5
import pandas as pd
import pythoncom

from yangke.ebsilon.ebsilon import EbsApp, EbsModel, EbsUnits
from yangke.web.flaskserver import start_server_app
from yangke.common.config import logger
from typing import Optional

settings: Optional[dict] = None  # read_settings(r"C:\Users\YangKe\Desktop\新建文件夹\15版\settings.xlsx")


def read_settings(file):
    settings = {"input": {}, "output": {}}
    excel_data = pd.read_excel(file)
    section = "输入参数"
    for idx, row in excel_data.iterrows():
        if row[0]:
            if row[0] == "输入参数":
                section = "输入参数"
                continue
            elif row[0] == "计算结果":
                section = "计算结果"
                continue
            if section == "输入参数":
                settings["input"].update({row.get("参数"): {
                    "para_id": row.get("参数id"),
                    "component": row.get("组件名"),
                    "para": row.get("变量名"),
                    "unit": row.get("单位")}
                })
            elif section == "计算结果":
                settings["output"].update({row.get("参数"): {
                    "para_id": row.get("参数id"),
                    "component": row.get("组件名"),
                    "para": row.get("变量名"),
                    "unit": row.get("单位")}
                })
    return settings


def read_model(ebs, power):
    if power > 370:
        model_name = "冷端优化-90%.ebs"
    elif power > 315:
        model_name = "冷端优化-75%.ebs"
    elif power > 280:
        model_name = "冷端优化-70%.ebs"
    elif power > 235:
        model_name = "冷端优化-60%.ebs"
    else:
        model_name = "冷端优化-50%.ebs"
    model_path = os.path.join(r"C:\Users\YangKe\Desktop\新建文件夹\15版", model_name)
    # if model is not None and model.get_path() == model_path:
    #     return model
    # else:
    #     model = ebs.open(model_path)
    #     return model
    model = ebs.open(model_path)
    return model


def get_leakage(power):
    return 0.026 * power + 6.3976


def solve(args):
    """
    每一个请求都是一个新线程，每一个线程都要单独初始化Ebsilon
    :param args:
    :return:
    """

    pythoncom.CoInitialize()  # 新线程需要先初始化，否则EbsApp对象无法使用
    ebs = EbsApp()
    return_dict = {}
    p_env = float(args.get("p_env") or 98.6)  # 环境压力
    t_env = float(args.get("t_env") or 33.2)  # 环境温度
    humid_env = float(args.get("humid_env") or 0.46)  # 环境湿度
    power = float(args.get("power") or 348.75)  # 电负荷
    heat_flow = float(args.get("heat_flow") or 0)  # 供热流量

    p_gas = float(args.get("p_gas") or 3.823)  # FGH进气压力
    t_gas = float(args.get("t_gas") or 21.2)  # FGH进气温度
    flow_fgh = float(args.get("fgh_flow_water") or 29.989)  # FGH进水流量
    flow_tca = float(args.get("tca_flow_water") or 106.802)  # TCA进水流量
    flow_rh = float(args.get("flow_rh") or 2.56)  # 再热减温水流量
    flow_oh = float(args.get("flow_oh") or 3)  # 过热减温水流量
    pump = int(args.get("pump") or 2)
    fun = int(args.get("fun") or 4)
    if pump == 1:
        flow_cycle = 8780
    elif pump == 2:
        flow_cycle = 16330
    elif pump == 3:
        flow_cycle = 20870
    elif pump == 5:
        flow_cycle = 37976 / 2  # 双机共用冷端情况
    if fun <= 5:
        power_fun = fun * 175
    else:
        power_fun = fun * 175 / 2  # 双机共用冷端情况
    flow_leakage = get_leakage(power)
    model: EbsModel = read_model(ebs, power)  # 读入ebsilon模型文件
    model.activate_profile("batch")  # 切换到专为批量计算设计的batch工况
    profile = model.get_profile("batch")
    try:
        for k, v in settings["input"].items():
            model.set_value(v["component"], v["para"], eval(v["para_id"]), v["unit"], save_flag=False)
        result = model.simulate()
        if result.success(no_error_as_success=True):
            """
            计算成功，则组装计算结果
            """
            logger.debug(result.get_result_summary())
            for k, v in settings["output"].items():
                value = model.get_value(v["component"], v["para"], v["unit"])
                return_dict.update({v["para_id"]: value})
        else:
            # 输出错误信息
            return_dict = result.get_result_detail()
    except (AttributeError, NameError):
        return_dict = {}
    finally:
        pythoncom.CoUninitialize()
    return return_dict


def start_server():
    global settings
    settings = read_settings(r"C:\Users\YangKe\Desktop\新建文件夹\15版\settings.xlsx")
    # solve({})
    start_server_app(solve)


if __name__ == "__main__":
    start_server()
