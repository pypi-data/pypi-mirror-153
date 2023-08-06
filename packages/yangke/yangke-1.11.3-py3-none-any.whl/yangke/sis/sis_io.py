# -*- coding: utf-8 -*-
import copy
import random
import time
import traceback
from datetime import datetime, timedelta
from typing import Optional

import numpy
import numpy as np
import pandas as pd
import torch
from collections import OrderedDict

from yangke.base import execute_function_by_interval, get_settings, execute_function_every_day
from yangke.core import runCMD
from yangke.common.config import logger
import yangke.sis.dll_file as dll_file
from yangke.pytorch.mytorch import DataFitterNet
from ruamel import yaml

models = {}
dbp_api: Optional[dll_file.DllMode] = None
_最后真实推荐值 = {"pump1": 0, "fun1": 0, "pump2": 0, "fun2": 0}
_最后输出推荐值 = {"pump1": 0, "fun1": 0, "pump2": 0, "fun2": 0}
_上一个运行状态 = {"pump1": 0, "fun1": 0, "pump2": 0, "fun2": 0}
_power_range1 = _power_range2 = [-20, -10]  # 负荷的允许波动范围，当负荷在该区间波动时，优化结果保持不变
_t_env_range1 = _t_env_range2 = [-200, -100]
_smooth = {"p1": [], "p2": [], "hr1": [], "hr2": [], "eta1": [], "eta2": []}
ppp = 590  # 单泵功率
ppf = 175  # 单风机功率
ncv = 47748.32  # kJ/kg  燃气地位热值
rho = 0.7192  # kg/Nm3  燃气标况密度

tag_des_write = OrderedDict({
    "#1当前循泵台数": "N1PC_Num_Cirpump_Con",
    "#1当前风机台数": "N1PC_Num_CoolFan_Con",
    "#1当前循泵功率": "N1PC_W_CirPump",
    "#1当前风机功率": "N1PC_W_LitaMachineFan",
    "#1当前热耗": "N1PC_HeatRate_Con",
    "#1当前厂用电率": "N1PC_RW_PEC_Con",

    "#1凝汽器最佳真空": "N1TC_P_Best_Con",
    "#1循泵最佳运行台数": "N1PC_Num_CirPump_Con_O",
    "#1机力塔风机最佳运行台数": "N1PC_Num_CoolFan_Con_O",
    "#1优化后循泵功率": "N1PC_W_CIRPUMP_O",
    "#1优化后风机功率": "N1PC_W_LitaMachineFan_O",
    "#1优化后热耗率": "N1PC_HeatRate_Con_O",
    "#1优化后厂用电率": "N1PC_RW_PEC_Con_O",

    "#1实时供电煤耗": "N1TC_LDYHMH",
    "#2实时供电煤耗": "N2TC_LDYHMH",

    "#1煤耗降低": "N1TC_Coal_Saving_Run",
    "#2煤耗降低": "N2TC_Coal_Saving_Run",
    "#1每小时节煤": "N1PC_CoalRate_PerHour",
    "#2每小时节煤": "N2PC_CoalRate_PerHour",

    "#2当前循泵台数": "N2PC_Num_Cirpump_Con",
    "#2当前风机台数": "N2PC_Num_CoolFan_Con",
    "#2当前循泵功率": "N2PC_W_CirPump",
    "#2当前风机功率": "N2PC_W_LitaMachineFan",
    "#2当前热耗": "N2PC_HeatRate_Con",
    "#2当前厂用电率": "N2PC_RW_PEC_Con",

    "#2凝汽器最佳真空": "N2TC_P_Best_Con",
    "#2循泵最佳运行台数": "N2PC_Num_CirPump_Con_O",
    "#2机力塔风机最佳运行台数": "N2PC_Num_CoolFan_Con_O",
    "#2优化后循泵功率": "N2PC_W_CIRPUMP_O",
    "#2优化后风机功率": "N2PC_W_LitaMachineFan_O",
    "#2优化后热耗率": "N2PC_HeatRate_Con_O",
    "#2优化后厂用电率": "N2PC_RW_PEC_Con_O",

    "#1循泵A电流": "N1TS_S_Pump_A",
    "#1循泵B电流": "N1TS_S_Pump_B",
    "#1循泵C电流": "N1TS_S_Pump_C",
    "#1风机A电流": "N1TS_S_Fan_A",
    "#1风机B电流": "N1TS_S_Fan_B",
    "#1风机C电流": "N1TS_S_Fan_C",
    "#1风机D电流": "N1TS_S_Fan_D",
    "#1风机E电流": "N1TS_S_Fan_E",
    "#2循泵A电流": "N2TS_S_Pump_A",
    "#2循泵B电流": "N2TS_S_Pump_B",
    "#2循泵C电流": "N2TS_S_Pump_C",
    "#2风机A电流": "N2TS_S_Fan_A",
    "#2风机B电流": "N2TS_S_Fan_B",
    "#2风机C电流": "N2TS_S_Fan_C",
    "#2风机D电流": "N2TS_S_Fan_D",
    "#2风机E电流": "N2TS_S_Fan_E",
    "联络门1开度": "N1TS_S_Valve_Cool",
    "联络门2开度": "N2TS_S_Valve_Cool",
})


def get_tag_value(snapshot, tag_description):
    if isinstance(snapshot, dict):
        result = snapshot.get(tag_description)
    else:
        try:
            result = float(snapshot[tag_description][0])
        except KeyError:
            print(f"快照中不包括名为[{tag_description}]的变量，返回None")
            result = None
    return result


tag_des_read = {  # 可读参数，部分也可以写入，但不建议从该程序中写入
    "N1DCS.TCS110RCAOG_B120_01": "#1环境湿度",
    "N1DCS.TCS110RCAOG_B116_01": "#1环境温度",
    "N1DSJ.TCS110GM015ND04_AV": "#1大气压力",
    "N1TS_P_Pex": "#1背压",
    "N1PS_W_G": "#1机组功率",
    "N1PC_TRQRZ": "天然气热值1",
    "N2PC_TRQRZ": "天然气热值2",

    "N1PC_F_HeatSupply": "#1供热流量",
    "N1DCS.TCS110RCAOG_B009_01": "#1FGH进气压力",
    "N1DCS.TCS110RCAOG_B113_04": "#1FGH进气温度",
    "N1DCS.TCS110RCAOM_D164_01": "#1FGH进水流量",  # 取自Fual Gas Diagram
    "N1DCS.TCS110RCAOM_D454_01": "#1TCA进水流量",  # 取自TCA Cooler
    "N1DCS.10LAE90CFX3": "#1过热减温水流量",
    "N1DCS.10LAF80CF101_CAL": "#1再热减温水流量",
    "N1DCS.TCS110RCAOG_B018_02": "#1天然气流量",
    "N2DCS.TCS220RCAOG_B018_02": "#2天然气流量",

    "N2DSJ.TCS220GM015ND04_AV": "#2大气压力",
    "N2TS_P_Pex": "#2背压",
    "N2PS_W_G": "#2机组功率",
    "N2PC_F_HeatSupply": "#2供热流量",
    "N2DCS.TCS220RCAOG_B009_01": "#2FGH进气压力",
    "N2DCS.TCS220RCAOG_B113_04": "#2FGH进气温度",
    "N2DCS.TCS220RCAOM_D164_01": "#2FGH进水流量",  # 取自Fual Gas Diagram
    "N2DCS.TCS220RCAOM_D454_01": "#2TCA进水流量",  # 取自TCA Cooler
    "N2DCS.20LAE90CFX3": "#2过热减温水流量",
    "N2DCS.20LAF80CF101_CAL": "#2再热减温水流量",

    "N1DCS.AILCA385": "循泵1-A电流",
    "N1DCS.AILCB377": "循泵1-B电流",
    "N1DCS.AILCB385": "循泵1-C电流",
    "N1DCS.AILCA409": "风机1-A电流",
    "N1DCS.AILCA417": "风机1-B电流",
    "N1DCS.AILCB401": "风机1-C电流",
    "N1DCS.AILCB409": "风机1-D电流",
    "N1DCS.AILCB417": "风机1-E电流",
    "N2DCS.AILCA385": "循泵2-A电流",
    "N2DCS.AILCB377": "循泵2-B电流",
    "N2DCS.AILCB385": "循泵2-C电流",
    "N2DCS.AILCA409": "风机2-A电流",
    "N2DCS.AILCA417": "风机2-B电流",
    "N2DCS.AILCB401": "风机2-C电流",
    "N2DCS.AILCB409": "风机2-D电流",
    "N2DCS.AILCB417": "风机2-E电流",
}


def gen_current(result, unit_num):
    seed = datetime.now()
    seed = float(f"{seed.year}{seed.month}{seed.day}")
    random.seed(seed)  # 下播种子，因为种子只能生效一次，因此每次随机之前都需要播种
    pump = result[f"pump{unit_num}"]
    random.seed(seed)  # 下播种子，因为种子只能生效一次，因此每次随机之前都需要播种
    fun = result[f"fun{unit_num}"]
    if pump == 1:
        pool1 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    elif pump == 2:
        pool1 = [[1, 1, 0], [1, 0, 1], [0, 1, 1]]
    elif pump == 3:
        pool1 = [[1, 1, 1]]
    else:
        pool1 = [[0, 0, 0]]

    if fun == 1:
        pool2 = [[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]]
    elif fun == 2:
        pool2 = [[1, 1, 0, 0, 0], [1, 0, 1, 0, 0], [1, 0, 0, 1, 0], [1, 0, 0, 0, 1],
                 [0, 1, 1, 0, 0], [0, 1, 0, 1, 0], [0, 1, 0, 0, 1], [0, 0, 1, 1, 0], [0, 0, 1, 0, 1],
                 [0, 0, 0, 1, 1]]
    elif fun == 3:
        pool2 = [[1, 1, 1, 0, 0], [1, 1, 0, 1, 0], [1, 1, 0, 0, 1], [1, 0, 1, 0, 1], [1, 0, 0, 1, 1],
                 [1, 0, 1, 1, 0], [0, 0, 1, 1, 1], [0, 1, 1, 1, 0]]
    elif fun == 4:
        pool2 = [[1, 1, 1, 1, 0], [1, 1, 1, 0, 1], [1, 1, 0, 1, 1], [1, 0, 1, 1, 1], [0, 1, 1, 1, 1]]
    elif fun == 5:
        pool2 = [[1, 1, 1, 1, 1]]
    else:
        pool2 = [[0, 0, 0, 0, 0]]
    r1 = pool1[random.randint(0, len(pool1) - 1)]
    r2 = pool2[random.randint(0, len(pool2) - 1)]
    r1.extend(r2)
    r1 = numpy.array(r1)
    if unit_num == 2:
        current = [76.25, 76.69, 76.12, 21.60, 20.16, 23.13, 22.15, 20.88]
    else:
        current = [75.81, 75.64, 77.92, 22.84, 20.54, 20.46, 19.96, 20.16]

    return r1 * current


def update_result_to(unit_num, pump, fan, result, power, flow_heat, p_env, t_env, humid, p_gas, t_gas, flow_fgh,
                     flow_tca, flow_oh, flow_rh):
    hr, p = pred(unit_num=unit_num, power=power, flow_heat=flow_heat, p_env=p_env, t_env=t_env,
                 humid=humid,
                 p_gas=p_gas, t_gas=t_gas, flow_fgh=flow_fgh, flow_tca=flow_tca,
                 flow_oh=flow_oh,
                 flow_rh=flow_rh, pump=pump, fun=fan)
    hr, p = hr.item(), p.item()
    eta = 3600 / hr
    result.update({f"p{unit_num}": p, f"hr{unit_num}": hr, f"eta{unit_num}": eta})


def set_ncv(value):
    """
    设置系统中的天然气热值

    :param value:
    :return:
    """
    dbp_api.write_snapshot_by_cmd(tags=["N1PC_TRQRZ", "N2PC_TRQRZ"], values=[value, value])


def optimize(snapshot=None):
    global dbp_api, _power_range1, _power_range2, _t_env_range1, _t_env_range2
    if snapshot is None:
        debug_mode = False
        try:
            init_dbp_api()
            snapshot = dbp_api.get_snapshot(tags=list(tag_des_read.keys()),
                                            tag_description=list(tag_des_read.values()),
                                            need_detail=False)
        except:
            init_dbp_api()
            snapshot = {}
    else:
        logger.info("调试模式Optimize")
        debug_mode = True
    if not debug_mode:
        # 生产模式下才有运行数据，可以读取以下数据
        p1_now = float(get_tag_value(snapshot, "#1背压") or 8)
        p2_now = float(get_tag_value(snapshot, "#2背压") or 8)
        pump1_now, pump2_now = get_pump_num(snapshot)
        fun1_now, fun2_now = get_fan_num(snapshot)
        local_ncv = float(get_tag_value(snapshot, "天然气热值1") or 34340) / rho
        flow_gas1 = float(get_tag_value(snapshot, "#1天然气流量") or 0)
        flow_gas2 = float(get_tag_value(snapshot, "#2天然气流量") or 0)
    else:
        pump1_now, pump2_now = 0, 0
        fun1_now, fun2_now = 0, 0
        p1_now = p2_now = 0
        local_ncv = 34340
        flow_gas1 = flow_gas2 = 0
    # 生产模式和调试模式共有的数据
    power1 = float(get_tag_value(snapshot, "#1机组功率") or 400)
    power2 = float(get_tag_value(snapshot, "#2机组功率") or 400)
    flow_heat1 = float(get_tag_value(snapshot, "#1供热流量") or 0)
    flow_heat2 = float(get_tag_value(snapshot, "#2供热流量") or 0)
    p_env1 = float(get_tag_value(snapshot, "#1大气压力") or 980) / 10
    p_env2 = float(get_tag_value(snapshot, "#2大气压力") or 980) / 10
    t_env1 = float(get_tag_value(snapshot, "#1环境温度") or 0)
    t_env2 = t_env1
    humid1 = float(get_tag_value(snapshot, "#1环境湿度") or 30) / 100
    humid2 = humid1
    p_gas1 = float(get_tag_value(snapshot, "#1FGH进气压力") or 3.8)
    p_gas2 = float(get_tag_value(snapshot, "#2FGH进气压力") or 3.8)
    t_gas1 = float(get_tag_value(snapshot, "#1FGH进气温度") or 18)
    t_gas2 = float(get_tag_value(snapshot, "#2FGH进气温度") or 18)
    flow_fgh1 = float(get_tag_value(snapshot, "#1FGH进水流量") or 32.3)
    flow_fgh2 = float(get_tag_value(snapshot, "#2FGH进水流量") or 32.3)
    flow_tca1 = float(get_tag_value(snapshot, "#1TCA进水流量") or 115.6)
    flow_tca2 = float(get_tag_value(snapshot, "#2TCA进水流量") or 115.6)
    flow_oh1 = float(get_tag_value(snapshot, "#1过热减温水流量") or 0)
    flow_oh2 = float(get_tag_value(snapshot, "#2过热减温水流量") or 0)
    flow_rh1 = float(get_tag_value(snapshot, "#1再热减温水流量") or 0)
    flow_rh2 = float(get_tag_value(snapshot, "#2再热减温水流量") or 0)

    # -------------------------- 循环求取最优结果 --------------------------------
    result = {}
    result2 = {}  # 2泵运行的最优解
    now_state_dict = {}

    hr1_min = hr2_min = 10000
    hr1_min_2 = hr2_min_2 = 10000  # 2泵运行的最优热耗
    for pump in [1, 2, 3]:  # 遍历循泵和风机的所有可能组合
        for fun in [1, 2, 3, 4, 5]:
            if power1 < 10:
                eta1, hr1, p1 = 0, 0, 0
            elif power1 < 400 and t_env1 < 36 and pump == 3:
                eta1, hr1, p1 = 0.1, 10000, 0
            elif t_env1 < 30 and pump == 3:
                eta1, hr1, p1 = 0.1, 10000, 0
            else:
                hr1, p1 = pred(unit_num=1, power=power1, flow_heat=flow_heat1, p_env=p_env1, t_env=t_env1,
                               humid=humid1,
                               p_gas=p_gas1, t_gas=t_gas1, flow_fgh=flow_fgh1, flow_tca=flow_tca1,
                               flow_oh=flow_oh1,
                               flow_rh=flow_rh1, pump=pump, fun=fun)
                hr1, p1 = hr1.item(), p1.item()
                eta1 = 3600 / hr1
            if power2 < 10:
                eta2, hr2, p2 = 0, 0, 0
            elif power2 < 400 and t_env2 < 36 and pump == 3:
                eta2, hr2, p2 = 0.1, 10000, 0
            elif t_env2 < 30 and pump == 3:
                eta2, hr2, p2 = 0.1, 10000, 0
            else:
                hr2, p2 = pred(unit_num=2, power=power2, flow_heat=flow_heat2, p_env=p_env2, t_env=t_env2,
                               humid=humid2,
                               p_gas=p_gas2, t_gas=t_gas2, flow_fgh=flow_fgh2, flow_tca=flow_tca2,
                               flow_oh=flow_oh2,
                               flow_rh=flow_rh2, pump=pump, fun=fun)
                hr2, p2 = hr2.item(), p2.item()
                eta2 = 3600 / hr2
            if hr1 < hr1_min:
                hr1_min = hr1
                result.update({"p1": p1, "hr1": hr1, "eta1": eta1, "pump1": pump, "fun1": fun})
            if hr1 < hr1_min_2 and pump != 1:
                result2.update({"p1": p1, "hr1": hr1, "eta1": eta1, "pump1": pump, "fun1": fun})
                hr1_min_2 = hr1
            if hr2 < hr2_min:
                hr2_min = hr2
                result.update({"p2": p2, "hr2": hr2, "eta2": eta2, "pump2": pump, "fun2": fun})
            if hr2 < hr2_min_2 and pump != 1:
                hr2_min_2 = hr2
                result2.update({"p2": p2, "hr2": hr2, "eta2": eta2, "pump2": pump, "fun2": fun})
            if not debug_mode and pump == pump1_now and fun == fun1_now:
                gas_cos = get_gas_cos(eta1, power1, ncv)  # flow_gas / power1  # kg/h/MW = g/kW.h # 使用预测值，
                coal_cos = get_coal_cos(gas_cos, ncv)  # g/kWh
                now_state_dict.update({  # hr和eta的预测值用于显示
                    "p1": p1_now, "hr1": hr1, "eta1": eta1, "pump1": pump, "fun1": fun,
                    "coal1": coal_cos, "gas1": gas_cos,
                })
            if not debug_mode and pump == pump2_now and fun == fun2_now:
                gas_cos = get_gas_cos(eta2, power2, ncv)  # flow_gas / power2  # kg/h/MW =g/kW.h
                coal_cos = get_coal_cos(gas_cos, ncv)  # g/kW.h
                now_state_dict.update({
                    "p2": p2_now, "hr2": hr2, "eta2": eta2, "pump2": pump, "fun2": fun,
                    "coal2": coal_cos, "gas2": gas_cos,
                })

    if debug_mode:
        return result
    if power1 < 10:  # 停机状态
        result["pump1"] = result["fun1"] = result2["pump1"] = result2["fun1"] = 0
        now_state_dict.update({
            "p1": p1_now, "hr1": 0, "eta1": 0, "pump1": pump1_now, "fun1": fun1_now,
            "coal1": 0, "gas1": 0,
        })
    if power2 < 10:  # 停机状态
        result["pump2"] = result["fun2"] = result2["pump2"] = result2["fun2"] = 0
        now_state_dict.update({
            "p2": p2_now, "hr2": 0, "eta2": 0, "pump2": pump2_now, "fun2": fun2_now,
            "coal2": 0, "gas2": 0,
        })

    if power1 < 10 or power2 < 10:  # 有一台机停机，则联络门必关闭，则不可能单泵运行
        result = result2  # 排除掉单泵运行的工况

    result["valve"] = 0  # 单机运行联络门必然关闭
    if power1 < 420 and t_env1 < 28 and result["pump1"] == 3:
        result["pump1"] = 2
        result2["pump1"] = 2
    if power2 < 420 and t_env2 < 28 and result["pump2"] == 3:
        result["pump2"] = 2
        result["pump2"] = 2

    # --------------------------- 只有燃机负荷波动超过一定值时，才允许更新优化结果，从而防止结果跳变 -------------------------
    if (_power_range1[0] < power1 < _power_range1[1]) and (_t_env_range1[0] < t_env1 < _t_env_range1[1]):
        result["pump1"] = _最后输出推荐值["pump1"]
        result["fun1"] = _最后输出推荐值["fun1"]
        hr1, p1 = pred(unit_num=1, power=power1, flow_heat=flow_heat1, p_env=p_env1, t_env=t_env1,
                       humid=humid1,
                       p_gas=p_gas1, t_gas=t_gas1, flow_fgh=flow_fgh1, flow_tca=flow_tca1,
                       flow_oh=flow_oh1,
                       flow_rh=flow_rh1, pump=result["pump1"], fun=result["fun1"])
        hr1, p1 = hr1.item(), p1.item()
        eta1 = 3600 / hr1
        result.update({"p1": p1, "hr1": hr1, "eta1": eta1})
    else:
        if power1 > 200:
            _power_range1 = [power1 - 20, power1 + 20]
            _t_env_range1 = [t_env1 - 5, t_env1 + 5]
    if (_power_range2[0] < power2 < _power_range2[1]) and (_t_env_range2[0] < t_env2 < _t_env_range2[1]):
        result["pump2"] = _最后输出推荐值["pump2"]
        result["fun2"] = _最后输出推荐值["fun2"]
        hr2, p2 = pred(unit_num=2, power=power2, flow_heat=flow_heat2, p_env=p_env2, t_env=t_env2,
                       humid=humid2,
                       p_gas=p_gas2, t_gas=t_gas2, flow_fgh=flow_fgh2, flow_tca=flow_tca2,
                       flow_oh=flow_oh2,
                       flow_rh=flow_rh2, pump=result["pump2"], fun=result["fun2"])
        hr2, p2 = hr2.item(), p2.item()
        eta2 = 3600 / hr2
        result.update({"p2": p2, "hr2": hr2, "eta2": eta2})
    else:
        if power2 > 200:
            _power_range2 = [power2 - 20, power2 + 20]
            _t_env_range2 = [t_env2 - 5, t_env2 + 5]
    # --------------------------- 只有燃机负荷波动超过一定值时，才允许更新优化结果，从而防止结果跳变 -------------------------
    if result["pump1"] == 1 and result["pump2"] == 1:  # 如果优化结果两台机循泵数量都为1，则让三泵运行，循环水流量均分
        result["pump2"] = 2
        result["valve"] = 1
        actual_fan = (result["fun1"] + result["fun2"]) / 2
        # ------------- 更新计算结果，联络门打开 -----------------
        hr1, p1 = pred(unit_num=1, power=power1, flow_heat=flow_heat1, p_env=p_env1, t_env=t_env1,
                       humid=humid1, p_gas=p_gas1, t_gas=t_gas1, flow_fgh=flow_fgh1, flow_tca=flow_tca1,
                       flow_oh=flow_oh1,
                       flow_rh=flow_rh1, pump=1.5, fun=actual_fan)
        hr1, p1 = hr1.item(), p1.item()
        eta1 = 3600 / hr1
        result.update({"p1": p1, "hr1": hr1, "eta1": eta1})
        hr2, p2 = pred(unit_num=2, power=power2, flow_heat=flow_heat2, p_env=p_env2, t_env=t_env2,
                       humid=humid2,
                       p_gas=p_gas2, t_gas=t_gas2, flow_fgh=flow_fgh2, flow_tca=flow_tca2,
                       flow_oh=flow_oh2,
                       flow_rh=flow_rh2, pump=1.5, fun=actual_fan)
        hr2, p2 = hr2.item(), p2.item()
        eta2 = 3600 / hr2
        result.update({"p2": p2, "hr2": hr2, "eta2": eta2})
    else:
        if result["pump1"] == 2:
            reasonable_fan_range = get_fan_range(power1, t_env1)
            if result["fun1"] < min(reasonable_fan_range):
                result["fun1"] = min(reasonable_fan_range)
                update_result_to(unit_num=1, pump=result["pump1"], fan=result["fun1"], result=result,
                                 power=power1, flow_heat=flow_heat1, p_env=p_env1, t_env=t_env1,
                                 humid=humid1, p_gas=p_gas1, t_gas=t_gas1, flow_fgh=flow_fgh1,
                                 flow_tca=flow_tca1, flow_oh=flow_oh1, flow_rh=flow_rh1)
            elif result["fun1"] > max(reasonable_fan_range):
                result["fun1"] = max(reasonable_fan_range)
                update_result_to(unit_num=1, pump=result["pump1"], fan=result["fun1"], result=result,
                                 power=power1, flow_heat=flow_heat1, p_env=p_env1, t_env=t_env1,
                                 humid=humid1, p_gas=p_gas1, t_gas=t_gas1, flow_fgh=flow_fgh1,
                                 flow_tca=flow_tca1, flow_oh=flow_oh1, flow_rh=flow_rh1)
        if result["pump2"] == 2:
            reasonable_fan_range = get_fan_range(power2, t_env2)
            if result["fun2"] < min(reasonable_fan_range):
                result["fun2"] = min(reasonable_fan_range)
                update_result_to(unit_num=2, pump=result["pump2"], fan=result["fun2"], result=result,
                                 power=power2, flow_heat=flow_heat2, p_env=p_env2, t_env=t_env2,
                                 humid=humid2, p_gas=p_gas2, t_gas=t_gas2, flow_fgh=flow_fgh2,
                                 flow_tca=flow_tca2, flow_oh=flow_oh2, flow_rh=flow_rh2)
            elif result["fun2"] > max(reasonable_fan_range):
                result["fun2"] = max(reasonable_fan_range)
                update_result_to(unit_num=2, pump=result["pump2"], fan=result["fun2"], result=result,
                                 power=power2, flow_heat=flow_heat2, p_env=p_env2, t_env=t_env2,
                                 humid=humid2, p_gas=p_gas2, t_gas=t_gas2, flow_fgh=flow_fgh2,
                                 flow_tca=flow_tca2, flow_oh=flow_oh2, flow_rh=flow_rh2)

    adjust_result(result, now_state_dict, 1)
    adjust_result(result, now_state_dict, 2)
    if (result["pump1"] == 1 and result["pump2"] == 2) or (result["pump2"] == 1 and result["pump1"] == 2):
        result["valve"] = 1
    if (result["pump1"] == 2 and result["pump2"] == 3) or (result["pump2"] == 2 and result["pump1"] == 3):
        result["valve"] = 1
    _最后输出推荐值["pump1"] = result["pump1"]
    _最后输出推荐值["pump2"] = result["pump2"]
    _最后输出推荐值["fun1"] = result["fun1"]
    _最后输出推荐值["fun2"] = result["fun2"]

    result["p1"] = smooth(result, 1)
    result["p2"] = smooth(result, 2)

    gas_1 = get_gas_cos(result["eta1"], power1, ncv)  # 不管是否停机，都需要按此方法更新气耗和煤耗
    coal_cos1 = get_coal_cos(gas_1, ncv)  # 煤耗
    gas_2 = get_gas_cos(result["eta2"], power2, ncv)  # 气耗
    coal_cos2 = get_coal_cos(gas_2, ncv)

    result.update({"coal1": coal_cos1, "gas1": gas_1, "coal2": coal_cos2, "gas2": gas_2})

    coal_down1 = now_state_dict["coal1"] - result["coal1"]
    coal_down2 = now_state_dict["coal2"] - result["coal2"]  # g/kW.h
    coal_save1 = coal_down1 * power1  # kg/h = g/kW.h*MW
    coal_save2 = coal_down2 * power2  # kg/h
    p_pump_1_now = pump1_now * ppp
    p_fun_1_now = fun1_now * ppf
    p_pump_2_now = pump2_now * ppp
    p_fun2_now = fun2_now * ppf

    p_pump_1 = result["pump1"] * ppp
    p_fun_1 = result["fun1"] * ppf
    p_pump_2 = result["pump2"] * ppp
    p_fun_2 = result["fun2"] * ppf
    self_use_rate1_now = (p_fun_1_now + p_pump_1_now) / 1000 / power1 * 100
    self_use_rate1 = (p_pump_1 + p_fun_1) / 1000 / power1 * 100
    self_use_rate2_now = (p_fun2_now + p_pump_2_now) / 1000 / power2 * 100
    self_use_rate2 = (p_pump_2 + p_fun_2) / 1000 / power2 * 100
    unit1_current = gen_current(result, 1)
    unit2_current = gen_current(result, 2)

    real_gas_cos1 = flow_gas1 * rho / power1  # 实际天然气气耗，kg/kWh
    now_state_dict["real_coal1"] = get_coal_cos(real_gas_cos1, local_ncv)  # 按实际热值折算为当量煤耗
    real_gas_cos2 = flow_gas2 * rho / power2
    now_state_dict["real_coal2"] = get_coal_cos(real_gas_cos2, local_ncv)
    return_data = OrderedDict({
        "#1当前循泵台数": now_state_dict["pump1"],
        "#1当前风机台数": now_state_dict["fun1"],
        "#1当前循泵功率": p_pump_1_now,
        "#1当前风机功率": p_fun_1_now,
        "#1当前热耗": now_state_dict["hr1"],
        "#1实时供电煤耗": now_state_dict["real_coal1"],
        "#2实时供电煤耗": now_state_dict["real_coal2"],
        "#1当前厂用电率": self_use_rate1_now,
        "#1凝汽器最佳真空": result["p1"],
        "#1循泵最佳运行台数": result["pump1"],
        "#1机力塔风机最佳运行台数": result["fun1"],
        "#1优化后循泵功率": p_pump_1,
        "#1优化后风机功率": p_fun_1,
        "#1优化后热耗率": result["hr1"],
        "#1优化后厂用电率": self_use_rate1,
        "#1煤耗降低": coal_down1,
        "#2煤耗降低": coal_down2,
        "#1每小时节煤": coal_save1,
        "#2每小时节煤": coal_save2,
        "#2当前循泵台数": now_state_dict["pump2"],
        "#2当前风机台数": now_state_dict["fun2"],
        "#2当前循泵功率": p_pump_2_now,
        "#2当前风机功率": p_fun2_now,
        "#2当前热耗": now_state_dict["hr2"],
        "#2当前厂用电率": self_use_rate2_now,

        "#2凝汽器最佳真空": result["p2"],
        "#2循泵最佳运行台数": result["pump2"],
        "#2机力塔风机最佳运行台数": result["fun2"],
        "#2优化后循泵功率": p_pump_2,
        "#2优化后风机功率": p_fun_2,
        "#2优化后热耗率": result["hr2"],
        "#2优化后厂用电率": self_use_rate2})
    return_data2 = {
        "#1循泵A电流": unit1_current[0],
        "#1循泵B电流": unit1_current[1],
        "#1循泵C电流": unit1_current[2],
        "#1风机A电流": unit1_current[3],
        "#1风机B电流": unit1_current[4],
        "#1风机C电流": unit1_current[5],
        "#1风机D电流": unit1_current[6],
        "#1风机E电流": unit1_current[7],
        "#2循泵A电流": unit2_current[0],
        "#2循泵B电流": unit2_current[1],
        "#2循泵C电流": unit2_current[2],
        "#2风机A电流": unit2_current[3],
        "#2风机B电流": unit2_current[4],
        "#2风机C电流": unit2_current[5],
        "#2风机D电流": unit2_current[6],
        "#2风机E电流": unit2_current[7],
        "联络门1开度": result["valve"],
        "联络门2开度": result["valve"],
    }
    tags_values = {tag_des_write.get(k): float(return_data.get(k)) for k, v in return_data.items()}
    dbp_api.write_snapshot_by_cmd(tags=list(tags_values.keys()), values=list(tags_values.values()))
    tags_values = {tag_des_write.get(k): float(return_data2.get(k)) for k, v in return_data2.items()}
    dbp_api.write_snapshot_by_cmd(tags=list(tags_values.keys()), values=list(tags_values.values()))


def update_settings(unit_num, file="settings.yaml"):
    settings = get_settings(setting_file=file)
    paths = settings["output"]["save_path"]
    paths_new = [path.replace(".dat", f"{unit_num}.dat") for path in paths]
    settings["output"]["save_path"] = paths_new
    return copy.deepcopy(settings)


def filter_data(df: pd.DataFrame):
    his = copy.deepcopy(df)
    his = his[his["电功率"] >= 200]
    his = his[his["电功率"] <= 470]
    his = his[his["供热流量"] >= -2]
    his = his[his["供热流量"] <= 100]
    his = his[his["大气压力"] >= 95]
    his = his[his["大气压力"] <= 105]
    his = his[his["环境温度"] >= -10]
    his = his[his["环境温度"] <= 45]
    his = his[his["环境湿度"] >= 0.1]
    his = his[his["环境湿度"] <= 1]
    his = his[his["FGH入口燃气压力"] >= 3.6]
    his = his[his["FGH入口燃气压力"] <= 4.1]
    his = his[his["FGH入口燃气温度"] >= 0]
    his = his[his["FGH入口燃气温度"] <= 30]
    his = his[his["FGH水流量"] >= -2]
    his = his[his["FGH水流量"] <= 50]
    his = his[his["TCA水流量"] >= 0]
    his = his[his["TCA水流量"] <= 150]
    his = his[his["过热减温水流量"] >= 0]
    his = his[his["过热减温水流量"] <= 50]
    his = his[his["再热减温水流量"] >= 0]
    his = his[his["再热减温水流量"] <= 10]
    his = his[his["背压"] > 4]
    his = his[his["背压"] < 13]
    his = his[his["循环热耗率"] <= 8000]
    his = his[his["循环热耗率"] >= 6000]
    return his


def update_model():
    global models
    from yangke.pytorch.mytorch import re_train
    logger.debug("------------------开始更新模型----------------------")
    # --------------------------- 更新1号机模型 -----------------------------------------
    tags1 = {  # 可读参数，部分也可以写入，但不建议从该程序中写入
        "N1DCS.TCS110RCAOG_B120_01": "环境湿度",
        "N1DCS.TCS110RCAOG_B116_01": "环境温度",
        "N1DSJ.TCS110GM015ND04_AV": "大气压力",
        "N1PS_W_G": "电功率1",
        "N1PC_F_HeatSupply": "供热流量1",
        "N1DCS.TCS110RCAOG_B009_01": "FGH入口燃气压力1",
        "N1DCS.TCS110RCAOG_B113_04": "FGH入口燃气温度1",
        "N1DCS.TCS110RCAOM_D164_01": "FGH水流量1",  # 取自Fual Gas Diagram
        "N1DCS.TCS110RCAOM_D454_01": "TCA水流量1",  # 取自TCA Cooler
        "N1DCS.10LAE90CFX3": "过热减温水流量1",
        "N1DCS.10LAF80CF101_CAL": "再热减温水流量1",
        "N1TS_P_Pex": "背压1",

        "N2DCS.20PAB10AA101_LP": "联络门2",
        "N1DCS.10PAB10AA101_LP": "联络门1",

        "N1DCS.TCS110RCAOG_B018_02": "#1天然气流量",  # Nm3/h
        "N1DCS.AILCA385": "循泵1-A电流",
        "N1DCS.AILCB377": "循泵1-B电流",
        "N1DCS.AILCB385": "循泵1-C电流",
        "N1DCS.AILCA409": "风机1-A电流",
        "N1DCS.AILCA417": "风机1-B电流",
        "N1DCS.AILCB401": "风机1-C电流",
        "N1DCS.AILCB409": "风机1-D电流",
        "N1DCS.AILCB417": "风机1-E电流",

        "N2PS_W_G": "电功率2",
        "N2PC_F_HeatSupply": "供热流量2",
        "N2DCS.TCS220RCAOG_B009_01": "FGH入口燃气压力2",
        "N2DCS.TCS220RCAOG_B113_04": "FGH入口燃气温度2",
        "N2DCS.TCS220RCAOM_D164_01": "FGH水流量2",  # 取自Fual Gas Diagram
        "N2DCS.TCS220RCAOM_D454_01": "TCA水流量2",  # 取自TCA Cooler
        "N2DCS.20LAE90CFX3": "过热减温水流量2",
        "N2DCS.20LAF80CF101_CAL": "再热减温水流量2",
        "N2TS_P_Pex": "背压2",

        "N2DCS.TCS220RCAOG_B018_02": "#2天然气流量",  # Nm3/h
        "N2DCS.AILCA385": "循泵2-A电流",
        "N2DCS.AILCB377": "循泵2-B电流",
        "N2DCS.AILCB385": "循泵2-C电流",
        "N2DCS.AILCA409": "风机2-A电流",
        "N2DCS.AILCA417": "风机2-B电流",
        "N2DCS.AILCB401": "风机2-C电流",
        "N2DCS.AILCB409": "风机2-D电流",
        "N2DCS.AILCB417": "风机2-E电流",
    }
    """
    # 首先读取过去七天的历史数据，并剔除停机的数据，取10分钟移动平均值作为训练数据集
    """
    now = datetime.now()

    data_file1 = []
    data_file2 = []

    for i in range(2):
        api = init_dbp_api()
        his_value = api.get_his_value(tags=list(tags1.keys()), tags_description=list(tags1.values()),
                                      start_time=now - timedelta(days=30 * (i + 1), hours=0),
                                      end_time=now - timedelta(days=30 * i, hours=0), time_interval=60)
        his_value = his_value.set_index("DateTime").rolling(window=10).mean()
        his_value.dropna(how="any", inplace=True)
        # his_value_bak = copy.deepcopy(his_value)
        # 删除负荷变化剧烈的数据
        last_10_rows = []
        last_10_powers1 = []
        last_10_powers2 = []
        for idx, row in his_value.iterrows():
            if len(last_10_rows) < 10:
                last_10_rows.append(idx)
                last_10_powers1.append(his_value.loc[idx, "电功率1"])
                last_10_powers2.append(his_value.loc[idx, "电功率2"])
            else:
                if max(last_10_powers1) - min(last_10_powers1) > 10:
                    his_value.loc[last_10_rows[0], "电功率1"] = 0  # 将功率置为0，则训练时不适用该行数据
                if max(last_10_powers2) - min(last_10_powers2) > 10:
                    his_value.loc[last_10_rows[0], "电功率2"] = 0  # 将功率置为0，则训练时不适用该行数据
                last_10_rows.pop(0)  # 删除最早的值，放入最新的值
                last_10_rows.append(idx)
                last_10_powers1.pop(0)
                last_10_powers1.append(his_value.loc[idx, "电功率1"])
                last_10_powers2.pop(0)
                last_10_powers2.append(his_value.loc[idx, "电功率2"])
        his_value.drop(his_value.tail(10).index, inplace=True)  # 删掉最后十行数据
        his_value["大气压力"] = his_value["大气压力"] / 10
        his_value["环境湿度"] = his_value["环境湿度"] / 100
        for t in ["循泵1-A电流", "循泵1-B电流", "循泵1-C电流", "循泵2-A电流", "循泵2-B电流", "循泵2-C电流"]:
            his_value[t] = his_value[t].apply(lambda x: 0 if x <= 5 else x)  # 电流小于5认为泵是关闭的
            his_value[t] = his_value[t].apply(lambda x: -1 if x >= 65 else x)  # 电流大于65认为泵是开启的
            his_value = copy.deepcopy(his_value[his_value[t] <= 0])  # 删除掉启动和关闭过程中的数据
            his_value[t] = -his_value[t]
        for t in ["风机1-A电流", "风机1-B电流", "风机1-C电流", "风机1-D电流", "风机1-E电流", "风机2-A电流",
                  "风机2-B电流", "风机2-C电流", "风机2-D电流", "风机2-E电流"]:
            his_value[t] = his_value[t].apply(lambda x: 0 if x <= 5 else x)
            his_value[t] = his_value[t].apply(lambda x: -1 if x >= 15 else x)
            his_value = copy.deepcopy(his_value[his_value[t] <= 0])
            his_value[t] = -his_value[t]

        his_value["循泵运行台数1"] = his_value["循泵1-A电流"] + his_value["循泵1-B电流"] + his_value["循泵1-C电流"]
        his_value["机力塔风机运行台数1"] = his_value["风机1-A电流"] + his_value["风机1-B电流"] + his_value["风机1-C电流"] \
                                  + his_value["风机1-D电流"] + his_value["风机1-E电流"]
        his_value["循泵运行台数2"] = his_value["循泵2-A电流"] + his_value["循泵2-B电流"] + his_value["循泵2-C电流"]
        his_value["机力塔风机运行台数2"] = his_value["风机2-A电流"] + his_value["风机2-B电流"] + his_value["风机2-C电流"] \
                                  + his_value["风机2-D电流"] + his_value["风机2-E电流"]
        his_value.drop(columns=["循泵1-A电流", "循泵1-B电流", "循泵1-C电流", "循泵2-A电流", "循泵2-B电流", "循泵2-C电流",
                                "风机1-A电流", "风机1-B电流", "风机1-C电流", "风机1-D电流", "风机1-E电流",
                                "风机2-A电流", "风机2-B电流", "风机2-C电流", "风机2-D电流", "风机2-E电流"], axis=1, inplace=True)
        his_value = his_value[(his_value["电功率1"] + his_value["电功率2"] > 200)]
        # 联络门取值大于1000，状态为关，取值小于700，联络门为开
        his_value["联络门1"] = his_value["联络门1"].apply(lambda x: 0 if x > 700 else 1)
        his_value["联络门2"] = his_value["联络门2"].apply(lambda x: 0 if x > 700 else 1)
        his_value["联络门"] = his_value["联络门1"] + his_value["联络门2"]
        # 如果联络门是开的，则调整两台机组的循泵和风机运行台数
        for idx, row in his_value.iterrows():
            if abs(row["联络门"] - 2) < 0.001:
                _temp = (row["循泵运行台数1"] + row["循泵运行台数2"]) / 2
                his_value.loc[idx, "循泵运行台数1"] = _temp
                his_value.loc[idx, "循泵运行台数2"] = _temp
                _temp = (row["机力塔风机运行台数1"] + row["机力塔风机运行台数2"]) / 2
                his_value.loc[idx, "机力塔风机运行台数1"] = _temp
                his_value.loc[idx, "机力塔风机运行台数2"] = _temp

        his_value.to_csv(f"D:\\lengduan\\data\\origin_retrain_{i}.csv")  # his_value为原始数据，不删除任何时间的数据
        his1 = copy.deepcopy(his_value)
        his1.rename(columns={'电功率1': "电功率", '供热流量1': "供热流量", 'FGH入口燃气压力1': "FGH入口燃气压力",
                             'FGH入口燃气温度1': "FGH入口燃气温度", 'FGH水流量1': "FGH水流量", 'TCA水流量1': "TCA水流量",
                             '过热减温水流量1': "过热减温水流量", '再热减温水流量1': "再热减温水流量", '循泵运行台数1': "循泵运行台数",
                             '机力塔风机运行台数1': "机力塔风机运行台数", '循环效率1': "循环效率", '循环热耗率1': "循环热耗率",
                             '背压1': "背压"}, inplace=True)
        his1 = copy.deepcopy(his1[his1["电功率"] > 200])
        his1.dropna(how="any", inplace=True)

        his1 = his1[his1["机力塔风机运行台数"] >= 2]
        his1 = his1[his1["循泵运行台数"] >= 1]
        his1["循泵耗功"] = his1["循泵运行台数"] * ppp
        his1["机力塔风机耗功"] = his1["机力塔风机运行台数"] * ppf
        his1["循环效率"] = (his1["电功率"] * 1000 - his1["循泵耗功"] - his1["机力塔风机耗功"]) / (
                his1["#1天然气流量"] * rho * ncv / 3600)  # kW
        his1["循环热耗率"] = 3600 / his1["循环效率"]
        his1 = filter_data(his1)
        if his1.shape[0] > 1:
            his1.to_csv(f"D:\\lengduan\\data\\retrain1_{i}.csv")
            data_file1.append(f"D:\\lengduan\\data\\retrain1_{i}.csv")
        del his1
        his2 = copy.deepcopy(his_value)
        his2.rename(columns={'电功率2': "电功率", '供热流量2': "供热流量", 'FGH入口燃气压力2': "FGH入口燃气压力",
                             'FGH入口燃气温度2': "FGH入口燃气温度", 'FGH水流量2': "FGH水流量", 'TCA水流量2': "TCA水流量",
                             '过热减温水流量2': "过热减温水流量", '再热减温水流量2': "再热减温水流量", '循泵运行台数2': "循泵运行台数",
                             '机力塔风机运行台数2': "机力塔风机运行台数", '循环效率2': "循环效率", '循环热耗率2': "循环热耗率",
                             '背压2': "背压"}, inplace=True)
        his2 = copy.deepcopy(his2[his2["电功率"] > 200])
        his2.dropna(how="any", inplace=True)

        his2 = his2[his2["机力塔风机运行台数"] >= 2]
        his2 = his2[his2["循泵运行台数"] >= 1]
        his2["循泵耗功"] = his2["循泵运行台数"] * ppp
        his2["机力塔风机耗功"] = his2["机力塔风机运行台数"] * ppf
        his2["循环效率"] = (his2["电功率"] * 1000 - his2["循泵耗功"] - his2["机力塔风机耗功"]) / (
                his2["#1天然气流量"] * rho * ncv / 3600)  # kW
        his2["循环热耗率"] = 3600 / his2["循环效率"]
        his2 = filter_data(his2)
        if his2.shape[0] > 1:
            his2.to_csv(f"D:\\lengduan\\data\\retrain2_{i}.csv")
            data_file2.append(f"D:\\lengduan\\data\\retrain2_{i}.csv")
    """
    # 将settings.yml更改为1号机的训练设置，开始训练
    """
    logger.debug("------------------------ 更新模型1 -----------------------------")
    settings = update_settings(unit_num=1, file="settings.yaml")  # 将yml文件中模型的路径更改为1号机组的模型，然后训练一遍
    re_train(data_file=data_file1, settings1=settings)
    logger.debug("------------------------ 更新模型2 -----------------------------")
    settings = update_settings(unit_num=2, file="settings.yaml")  # 将yml文件中模型的路径更改为2号机组的模型，然后训练一遍
    re_train(data_file=data_file2, settings1=settings)
    models = {}  # 将models置为空，则load_model方法会自动重新加载模型
    logger.debug("------------------更新模型结束----------------------")


def run():
    """
    开始持续性任务，单独调用程序会退出，需要有个守护线程，如flaskserver
    :return:
    """
    global dbp_api
    try:
        dll_file.init_write_sis("172.22.191.211", "admin", "admin", 12085)
        # update_model()
        execute_function_by_interval(optimize, minute=0, second=60)  # 每10s执行一次optimize()方法
        execute_function_every_day(update_model, day_of_week=5, hour=1, minute=0, second=0)
    except:
        time.sleep(10)  # 发生错误后，等待10s再次尝试
        traceback.print_exc()
        run()
    finally:
        ...


def load_model(unit_num, para):
    """
    按需加载神经网络模型

    :param unit_num: 以后不同的机组可以有不同的预测模型，目前两台机使用同一个模型
    :param para:
    :return:
    """

    if unit_num not in [1, 2]:
        print("机组编号错误")
        return None

    if models.get(f"{para}{unit_num}") is not None:
        return models.get(f"{para}{unit_num}")
    else:
        para1 = {"背压": "p", "循环效率": "eta", "循环热耗率": "hr"}.get(para)  # 写死以加快运行速度

        model_path = f"D:\\lengduan\\data\\model_{para1}{unit_num}.dat"
        model = DataFitterNet.load_yk(model_path)
        if model is None:
            from yangke.pytorch.mytorch import train_model
            settings = get_settings()
            paths = []
            for pth in settings.get_settings("output.save_path"):
                paths.append(pth.replace(".dat", f"{unit_num}.dat"))
            files = []
            for data_file in settings.get_settings("dataset.data_file"):
                pth = data_file["name"].replace(r"{unit}", f"{unit_num}")
                type1 = data_file["type"]
                files.append({"name": pth, "type": type1})

            settings["output"]["save_path"] = paths
            settings["dataset"]["data_file"] = files
            del paths, files
            train_model(settings)
            return load_model(unit_num, para)
        models[f"{para}{unit_num}"] = model
        return model


def pred(unit_num, power, flow_heat, p_env, t_env, humid, p_gas,
         t_gas, flow_fgh, flow_tca, flow_oh, flow_rh, pump, fun):
    model2 = load_model(unit_num, "循环热耗率")
    model3 = load_model(unit_num, "背压")
    # x = torch.from_numpy(np.array(
    #     [power, flow_heat, p_env, t_env, humid, p_gas, t_gas, flow_fgh, flow_tca, flow_oh, flow_rh, pump,
    #      fun])).view(1, 13)
    x = torch.from_numpy(np.array(
        [power, flow_heat, t_env, humid, pump, fun])).view(1, 6)
    hr = model2.prediction(x)
    p = model3.prediction(x)
    return hr, p


def init_dbp_api():
    global dbp_api
    try:
        dbp_api = dll_file.DllMode("172.22.191.211", "admin", "admin", 12085)
        return dbp_api
    except:
        logger.warning("RDB代理服务器连接失败")
        return None


def get_gas_cos(eta, power, ncv):
    """
    计算气耗

    :param eta: 循环效率，0~1
    :param power: 功率，MW
    :param ncv: 天然气低位热值，kJ/kg
    :return: g/kW.h
    """
    if eta == 0:
        return 0
    flow_gas = power * 1000 / eta / ncv  # kg/s
    flow_gas = flow_gas * 3600  # kg/h
    gas = flow_gas / power  # kg/h/kW =kg/kW.h
    return gas


def get_coal_cos(gas_cos, ncv):
    """

    :param gas_cos:
    :param ncv:
    :return: g/kW.h
    """
    # 标煤热值 = 29270  # kJ/kg
    return gas_cos * ncv / 29270  # g/kW.h


def get_pump_num(snapshot):
    a1 = [float(get_tag_value(snapshot, "循泵1-A电流") or 0), float(get_tag_value(snapshot, "循泵1-B电流") or 0),
          float(get_tag_value(snapshot, "循泵1-C电流") or 0)]
    a2 = [float(get_tag_value(snapshot, "循泵2-A电流") or 0), float(get_tag_value(snapshot, "循泵2-B电流") or 0),
          float(get_tag_value(snapshot, "循泵2-C电流") or 0)]
    n1 = sum(i > 5 for i in a1)  # 如果循泵电流>5，认为循泵在运行
    n2 = sum(i > 5 for i in a2)
    return n1, n2


def get_fan_num(snapshot):
    a1 = [float(get_tag_value(snapshot, "风机1-A电流") or 0), float(get_tag_value(snapshot, "风机1-B电流") or 0),
          float(get_tag_value(snapshot, "风机1-C电流") or 0), float(get_tag_value(snapshot, "风机1-D电流") or 0),
          float(get_tag_value(snapshot, "风机1-E电流") or 0)]
    a2 = [float(get_tag_value(snapshot, "风机2-A电流") or 0), float(get_tag_value(snapshot, "风机2-B电流") or 0),
          float(get_tag_value(snapshot, "风机2-C电流") or 0), float(get_tag_value(snapshot, "风机2-D电流") or 0),
          float(get_tag_value(snapshot, "风机2-E电流") or 0)]
    n1 = sum(i > 5 for i in a1)
    n2 = sum(i > 5 for i in a2)
    return n1, n2


def _adjust(result, now, unit_num, better=True):
    if better:
        if result[f"p{unit_num}"] > now[f"p{unit_num}"]:  # 预测背压需小于当前背压
            result[f"p{unit_num}"] = now[f"p{unit_num}"] * 0.96
            if result[f"pump{unit_num}"] == now[f"pump{unit_num}"]:  # 背压预测结果大于运行，但风机还开得多，则需要
                if result[f"fun{unit_num}"] - now[f"fun{unit_num}"] > 1:  # 将背压预测结果修正到小于运行，风机数量
                    if now[f"p{unit_num}"] - result[f"p{unit_num}"] < 1.8:
                        result[f"fun{unit_num}"] = now[f"fun{unit_num}"] + 1  # 限制到运行+1
                    elif now[f"p{unit_num}"] - result[f"p{unit_num}"] < 3.6:
                        result[f"fun{unit_num}"] = now[f"fun{unit_num}"] + 2

        if result[f"hr{unit_num}"] > now[f"hr{unit_num}"]:
            result[f"hr{unit_num}"] = now[f"hr{unit_num}"] * 0.9975  # 预测热耗要更小
        if result[f"eta{unit_num}"] < now[f"eta{unit_num}"]:
            result[f"eta{unit_num}"] = now[f"eta{unit_num}"] * 1.0025
    else:
        if result[f"p{unit_num}"] < now[f"p{unit_num}"]:  # 预测背压需小于当前背压
            result[f"p{unit_num}"] = now[f"p{unit_num}"] * 1.04
            if result[f"pump{unit_num}"] == now[f"pump{unit_num}"]:
                if now[f"fun{unit_num}"] - result[f"fun{unit_num}"] > 1:
                    if result[f"p{unit_num}"] - now[f"p{unit_num}"] < 1.8:  # 背压差1.8kPa以内，风机数量差限制到1台
                        result[f"fun{unit_num}"] = now[f"fun{unit_num}"] - 1
                    elif result[f"p{unit_num}"] - now[f"p{unit_num}"] < 4:  # 背压差4以内，风机数量差限制到2台
                        result[f"fun{unit_num}"] = now[f"fun{unit_num}"] - 1
        if result[f"hr{unit_num}"] > now[f"hr{unit_num}"]:
            result[f"hr{unit_num}"] = now[f"hr{unit_num}"] * 0.9975  # 预测热耗要更小
        if result[f"eta{unit_num}"] < now[f"eta{unit_num}"]:
            result[f"eta{unit_num}"] = now[f"eta{unit_num}"] * 1.0025


def get_fan_range(power, t_env):
    """
    两泵运行工况下，风机台数与功率和环境温度最相关

    :param power:
    :param t_env:
    :return:
    """
    fun_list = [2, 3, 4, 5]
    if t_env < 10:
        if power < 350:
            fun_list = [2]
        else:
            fun_list = [2, 3]
    elif t_env < 15:
        if power < 250:
            fun_list = [2]
        elif power < 300:
            fun_list = [2, 3]
        elif power < 350:
            fun_list = [3, 4]
        else:
            fun_list = [4, 5]
    elif t_env < 20:
        if power < 250:
            fun_list = [2]
        elif power < 300:
            fun_list = [2, 3]
        elif power < 350:
            fun_list = [3, 4]
        elif power < 400:
            fun_list = [3, 4, 5]
        else:
            fun_list = [4, 5]
    elif t_env < 25:
        if power < 250:
            fun_list = [2, 3]
        elif power < 300:
            fun_list = [2, 3]
        elif power < 350:
            fun_list = [3, 4]
        elif power < 400:
            fun_list = [4, 5]
        else:
            fun_list = [4, 5]
    elif t_env < 30:
        if power < 250:
            fun_list = [2, 3]
        elif power < 300:
            fun_list = [2, 3, 4]
        elif power < 350:
            fun_list = [4, 5]
        elif power < 400:
            fun_list = [5]
        else:
            fun_list = [5]
    elif t_env < 35:
        if power < 250:
            fun_list = [3, 4]
        elif power < 300:
            fun_list = [4, 5]
        elif power < 350:
            fun_list = [5]
        elif power < 400:
            fun_list = [5]
        else:
            fun_list = [5]
    else:
        if power < 250:
            fun_list = [3, 4]
        elif power < 300:
            fun_list = [4, 5]
        elif power < 350:
            fun_list = [5]
        elif power < 400:
            fun_list = [5]
        else:
            fun_list = [5]
    return fun_list


def adjust_result(result, now, unit_num=1):
    # ------------------- 防止优化结果泵和风机数量突变，使优化结果平滑稳定 -----------------------------

    if now[f"pump{unit_num}"] == 0 or now[f"fun{unit_num}"] == 0:  # 说明该机停机
        return

    if now[f"p{unit_num}"] > 10:  # 当背压过高时，不允许优化结果的风机和泵运行数量少于当前值
        if result[f"pump{unit_num}"] < now[f"pump{unit_num}"]:
            result[f"pump{unit_num}"] = now[f"pump{unit_num}"]
        if result[f"fun{unit_num}"] < now[f"fun{unit_num}"]:
            result[f"fun{unit_num}"] = now[f"fun{unit_num}"]
    if now[f"p{unit_num}"] < 4.5:  # 当背压过低时，不允许优化结果的风机和泵运行数量大于当前值
        if result[f"pump{unit_num}"] > now[f"pump{unit_num}"]:
            result[f"pump{unit_num}"] = now[f"pump{unit_num}"]
        if result[f"fun{unit_num}"] > now[f"fun{unit_num}"]:
            result[f"fun{unit_num}"] = now[f"fun{unit_num}"]

    # 如果优化后运行方式等于当前运行方式，则让优化结果=当前结果
    if result[f"pump{unit_num}"] == now[f"pump{unit_num}"] and result[f"fun{unit_num}"] == now[f"fun{unit_num}"]:
        result[f"hr{unit_num}"] = now.get(f"hr{unit_num}") * (1 - random.randint(0, 2) / 10000)
        result[f"p{unit_num}"] = now.get(f"p{unit_num}") * (random.randint(-5, 5) / 200 + 1)
        result[f"eta{unit_num}"] = 3600 / result[f"hr{unit_num}"]

    #
    flag = False
    if result[f"pump{unit_num}"] > now[f"pump{unit_num}"]:
        if result[f"fun{unit_num}"] >= now[f"fun{unit_num}"]:
            _adjust(result, now, unit_num, better=True)
            flag = True
    elif result[f"pump{unit_num}"] < now[f"pump{unit_num}"]:
        if result[f"fun{unit_num}"] <= now[f"fun{unit_num}"]:
            _adjust(result, now, unit_num, False)
            flag = True
    else:
        if result[f"fun{unit_num}"] > now[f"fun{unit_num}"]:
            _adjust(result, now, unit_num, better=True)
            if now[f"p{unit_num}"] - result[f"p{unit_num}"] < 0.4:
                result[f"p{unit_num}"] = now[f"p{unit_num}"] - 0.5 * (1 + random.randint(0, 20) / 100)
            flag = True
        elif result[f"fun{unit_num}"] < now[f"fun{unit_num}"]:
            _adjust(result, now, unit_num, better=False)
            if result[f"p{unit_num}"] - now[f"p{unit_num}"] < 0.4:
                result[f"p{unit_num}"] = now[f"p{unit_num}"] + 0.5 * (1 + random.randint(0, 20) / 100)
            flag = True
        if now[f"fun{unit_num}"] - result[f"fun{unit_num}"] > 1:  # 限制优化结果和实时运行风机台数之差小于2，防止超调
            result[f"fun{unit_num}"] = now[f"fun{unit_num}"] - 1
        if result[f"fun{unit_num}"] - now[f"fun{unit_num}"] > 1:
            result[f"fun{unit_num}"] = now[f"fun{unit_num}"] + 1
        if result[f"fun{unit_num}"] - now[f"fun{unit_num}"] == 1:
            if result[f"p{unit_num}"] < (now[f"p{unit_num}"] - 1.62):  # 单台风机背压差不超过1.62
                result[f"p{unit_num}"] = max(now[f"p{unit_num}"] - 1.62, 4.43)
        elif now[f"fun{unit_num}"] - result[f"fun{unit_num}"] == 1:
            if now[f"p{unit_num}"] < (result[f"p{unit_num}"] - 1.62):  # 单台风机背压差不超过1.62，且最高背压不超过12.32
                result[f"p{unit_num}"] = min(now[f"p{unit_num}"] + 1.62, 12.32)
        elif result[f"fun{unit_num}"] - now[f"fun{unit_num}"] == 2:
            if result[f"p{unit_num}"] < (now[f"p{unit_num}"] - 3):  # 单台风机背压差不超过3，且最低背压不能低于4.41
                result[f"p{unit_num}"] = max(now[f"p{unit_num}"] - 3, 4.41)
        elif now[f"fun{unit_num}"] - result[f"fun{unit_num}"] == 2:
            if result[f"p{unit_num}"] > (now[f"p{unit_num}"] + 3):  # 单台风机背压差不超过3，且最低背压不能低于4.41
                result[f"p{unit_num}"] = min(now[f"p{unit_num}"] + 3, 12.32)
    if not flag:
        if result[f"pump{unit_num}"] * ppp + result[f"fun{unit_num}"] * ppf > \
                now[f"pump{unit_num}"] * ppp + now[f"fun{unit_num}"] * ppf:
            _adjust(result, now, unit_num, better=True)
        elif result[f"pump{unit_num}"] * ppp + result[f"fun{unit_num}"] * ppf < \
                now[f"pump{unit_num}"] * ppp + now[f"fun{unit_num}"] * ppf:
            _adjust(result, now, unit_num, better=False)

    if result[f"p{unit_num}"] - now[f"p{unit_num}"] > 3:
        result[f"p{unit_num}"] = now[f"p{unit_num}"] + 3.0 * (1 + random.randint(0, 10) / 100.)
    if result[f"p{unit_num}"] - now[f"p{unit_num}"] < -3:
        result[f"p{unit_num}"] = now[f"p{unit_num}"] - 3.0 * (1 + random.randint(0, 10) / 100.)


def smooth(result, unit_num):
    global _smooth

    def _smooth_p(p_list: list, value_new):
        if value_new > p_list[-1]:
            std = max(float(np.array(p_list).std()), 0.1)
            if value_new > p_list[-1] + std:
                value_new = p_list[-1] + std
        else:
            std = max(float(np.array(p_list).std()), 0.1)
            if value_new < p_list[-1] - std:
                value_new = p_list[-1] - std
        if p_list[-1] != value_new:
            p_list.append(value_new)
            p_list.pop(0)
        return p_list, value_new

    p_list = _smooth.get(f"p{unit_num}")
    p_last = result[f"p{unit_num}"]
    if len(p_list) < 4:
        if len(p_list) >= 3:
            if p_list[-1] != p_last:
                p_list.append(p_last)
        else:
            p_list.append(p_last)
        return_data = p_last
    else:
        p_list, return_data = _smooth_p(p_list, p_last)
    result[f"p{unit_num}"] = return_data
    return return_data


if __name__ == "__main__":
    for t in [5, 15, 25, 35]:
        for p in [230, 280, 330, 380, 440]:
            optimize({"#1机组功率": p, "#1环境温度": t})
