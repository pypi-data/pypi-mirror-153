import math

from CoolProp.HumidAirProp import HAPropsSI
from CoolProp.CoolProp import PropsSI


def get_RH_by_T_Twb(t_dry, t_wet, p):
    """
    根据大气压和干湿球温度求相对湿度
    :param t_dry: 干球温度，℃
    :param t_wet: 湿球温度，℃
    :param p: 大气压力，Pa
    :return:
    """
    r = HAPropsSI('R', 'T', t_dry + 273.15, 'P', p, 'Twb', t_wet + 273.15)
    return r


def get_W_by_T_Twb(t_dry, t_wet, p):
    """
    根据大气压和干湿球温度求湿空气的含湿量

    :param t_dry: 干球温度，℃
    :param t_wet: 湿球温度，℃
    :param p:
    :return:
    """
    w = HAPropsSI('W', 'T', t_dry + 273.15, 'P', p, 'Twb', t_wet + 273.15)
    return w


def get_Pw_by_T(t):
    """
    获取指定温度下空气中饱和水蒸气分压

    :param t: 温度，℃
    :return: 饱和水蒸气分压，Pa
    """
    t_k = t + 273.15
    lgp = 5.005717 - 3.142305 * (1000 / t_k - 1000 / 373.116) + 8.21 * math.log10(373.16 / t_k) - 0.0024804 * (
            373.16 - t_k)
    pw = 10 ^ lgp
    return pw
