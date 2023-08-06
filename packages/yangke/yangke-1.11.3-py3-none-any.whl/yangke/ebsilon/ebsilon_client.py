import os
import time
import traceback
from typing import Optional
import pywintypes

import requests
from yangke.common.config import logger
from yangke.ebsilon.ebsilon import EbsApp, EbsModel, EbsUnits
import yangke.ebsilon.ebsilon_server as server
from yangke.common.fileOperate import writeLine

ebs: Optional[EbsApp] = None
model: Optional[EbsModel] = None
settings: Optional[dict] = None
file_summary = os.path.join(r"C:\Users\YangKe\Desktop\新建文件夹\15版", "summary.csv")


def read_model(power):
    global model, ebs
    if power > 370:
        model_name = "冷端优化-90%.ebs"
    elif power > 315:
        model_name = "冷端优化-75%.ebs"
    elif power > 275:
        model_name = "冷端优化-75%.ebs"
    elif power > 235:
        model_name = "冷端优化-75%.ebs"
    else:
        model_name = "冷端优化-75%.ebs"
    model_path = os.path.join(r"C:\Users\YangKe\Desktop\新建文件夹\15版", model_name)
    try:
        if model is not None and model.get_path() == model_path and model.model is not None:
            pass
        else:
            model = ebs.open(model_path)
    except AttributeError:  # 有时候会出现model不为空，但model.model为None的情况，这种情况下，model.get_path()会报错
        model = ebs.open(model_path)
    if model.model is None:
        ebs = EbsApp()  # 出现这种情况一般是ebs崩了，尝试重新初始化
        model = read_model(power)
    return model


def _solve(args):
    """
    每一个请求都是一个新线程，每一个线程都要单独初始化Ebsilon
    :param args:
    :return:
    """
    global ebs, model
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
    read_model(power)  # 读入ebsilon模型文件
    model.activate_profile("batch")  # 切换到专为批量计算设计的batch工况
    # ebs.show_window()
    try:
        for k, v in settings["input"].items():
            model.set_value(v["component"], v["para"], eval(v["para_id"]), v["unit"], save_flag=False)
        result = model.simulate_new()
        logger.debug(model.get_value("Gas", "M", "t/h"))
        result = model.simulate_new()
        logger.debug(model.get_value("Gas", "M", "t/h"))
        result = model.simulate_new()
        logger.debug(model.get_value("Gas", "M", "t/h"))
        logger.debug(f"{result.result_code=}, {result.result=}")
        if result.success(no_error_as_success=True):
            # 计算成功，则组装计算结果
            logger.debug(result.get_result_summary())
            for k, v in settings["output"].items():
                value = model.get_value(v["component"], v["para"], v["unit"])
                return_dict.update({v["para_id"]: value})
        else:
            # 输出错误信息
            return_dict = result.get_result_detail()
            logger.warning(f"{power=},{heat_flow=},{p_env=},{t_env=},"
                           f"{humid_env=},{p_gas=},{t_gas=},{flow_fgh=},{flow_tca=},"
                           f"{flow_oh=},{flow_rh=},{pump=},{fun=}")
            # input()
            return_dict.update({"flow_gas": 0.0, "p_out": 0.0})
    except (AttributeError, NameError):
        return_dict = {}
    return return_dict


def solve(power=348.75, heat_flow=0, p_env=98.6, t_env=33.2, humid=0.46, p_gas=3.823, t_gas=21.2, flow_fgh=29.989,
          flow_tca=106.802, flow_rh=2.56, flow_oh=3, pump=2, fun=3):
    """
    求解指定参数下的热耗

    :param power:
    :param heat_flow:
    :param p_env: 大气压力，kPa
    :param t_env: 环境温度，℃
    :param humid:
    :param p_gas:
    :param t_gas:
    :param flow_fgh:
    :param flow_tca:
    :param flow_rh:
    :param flow_oh:
    :param pump:
    :param fun:
    :return:
    """
    params = {
        "p_env": p_env,
        "t_env": t_env,
        "humid_env": humid,
        "power": power,
        "heat_flow": heat_flow,
        "p_gas": p_gas,
        "t_gas": t_gas,
        "fgh_flow_water": flow_fgh,
        "tca_flow_water": flow_tca,
        "flow_rh": flow_rh,
        "flow_oh": flow_oh,
        "pump": pump,
        "fun": fun,
    }
    result = _solve(params)
    power_pump = pump * 590
    power_fun = fun * 175
    _net_power = power * 1000 - power_fun - power_pump  # 扣除冷端设备功耗后的净出力，单位kW
    energy_fuel = 47748.32 * result.get("flow_gas") / 3600  # kJ/kg*kg/h
    if energy_fuel == 0:
        eta = 0
        hr = 0
    else:
        eta = _net_power / energy_fuel
        hr = 3600 / eta
    result.update({
        "power_pump": power_pump,
        "power_fun": power_fun,
        "eta": eta,
        "hr": hr,
        "model": model.get_name(),
    })
    result.update(params)
    logger.debug(result)
    return result


def batch_all_conditions(start_from=0):
    writeLine(file_summary, "序号,电功率,供热流量,大气压力,环境温度,环境湿度,FGH入口燃气压力,FGH入口燃气温度,FGH水流量,TCA水流量,"
                            "过热减温水流量,再热减温水流量,循泵运行台数,"
                            "机力塔风机运行台数,循泵耗功,机力塔风机耗功,循环效率,循环热耗率,背压,燃气流量,模型文件\n")
    i = 0
    for power in range(460, 200, -20):  # 13
        for heat_flow in [0.0, 50]:  # 2
            for p_env in [98, 100]:  # 2
                for t_env in [0.0, 10, 20, 30]:  # 4，不能使用0
                    for humid in [0.3, 0.5, 0.7, 0.9]:  # [0.3, 0.5, 0.7, 0.9]:  # 4
                        for p_gas in [3.8, 3.9]:  # 2
                            for t_gas in [18, 22]:  # 2
                                for flow_oh in [0.0, 15]:  # 2
                                    for flow_rh in [0.0, 2]:  # 2
                                        for pump in [2, 3]:  # 2
                                            for fun in [3, 4, 5]:  # 3
                                                if i < start_from:
                                                    i = i + 1
                                                    continue
                                                logger.debug(
                                                    f"=========================={i} start===========================")
                                                logger.debug(f"{i=}")
                                                flow_fgh = 0.0442 * power + 14.6
                                                flow_tca = 0.2575 * power + 12.552
                                                try:
                                                    logger.info(f"{power=},{heat_flow=},{p_env=},{t_env=},"
                                                                f"{humid=},{p_gas=},{flow_fgh=},{flow_tca=},"
                                                                f"{flow_oh=},{flow_rh=},{pump=},{fun=}")
                                                    result = solve(power=power,
                                                                   heat_flow=heat_flow,
                                                                   p_env=p_env,
                                                                   t_env=t_env,
                                                                   humid=humid,
                                                                   p_gas=p_gas,
                                                                   t_gas=t_gas,
                                                                   flow_fgh=flow_fgh,
                                                                   flow_tca=flow_tca,
                                                                   flow_oh=flow_oh,
                                                                   flow_rh=flow_rh,
                                                                   pump=pump,
                                                                   fun=fun
                                                                   )
                                                    power_pump = result["power_pump"]
                                                    power_fun = result["power_fun"]
                                                    eta = result["eta"]
                                                    hr = result["hr"]
                                                    model1 = result["model"]
                                                    p_out = result["p_out"]
                                                    flow_gas = result["flow_gas"]
                                                    line = f"{i},{power:7.3f},{heat_flow:5.1f},{p_env:5.1f},{t_env:4.1f}," \
                                                           f"{humid:4.2f},{p_gas:5.3f},{t_gas:4.1f},{flow_fgh:5.1f}," \
                                                           f"{flow_tca:5.1f},{flow_oh:4.1f},{flow_rh:4.1f},{pump}," \
                                                           f"{fun},{power_pump:6.1f},{power_fun:5.1f},{eta:5.3f}," \
                                                           f"{hr:6.1f},{p_out:5.2f},{flow_gas:8.2f},{model1}\n"
                                                    writeLine(file_summary, line=line, append=True)
                                                    if hr == 0:
                                                        model.save_as(os.path.join(r"C:\Users\YangKe\Desktop\新建文件夹"
                                                                                   r"\15版\error",
                                                                                   f"error_model{i}.ebs"))
                                                except:  # 计算过程中出现任何异常，都只记录并继续
                                                    traceback.print_exc()
                                                    logger.error(traceback.format_exc())
                                                    time.sleep(10)
                                                    pass
                                                finally:
                                                    logger.debug(
                                                        f"=========================={i} end===========================")
                                                    i = i + 1


if __name__ == "__main__":
    settings = server.read_settings(r"C:\Users\YangKe\Desktop\新建文件夹\15版\settings.xlsx")
    ebs = EbsApp()
    ebs.describe()
    batch_all_conditions(start_from=6240)
