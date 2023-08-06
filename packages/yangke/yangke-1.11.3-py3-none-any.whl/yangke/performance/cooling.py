"""
本程序涉及到的所有物理参数的单位均为国际标准单位
"""
import math
import numpy as np

pressure_larynx_total = 160.70  # 喉部压力全压 Pa
pressure_larynx_dynamic = 160.7 - 120.49  # 喉部压力动压
pressure_larynx_static = 120.49  # 喉部压力静压 Pa
temperature_water_in = 39.06 + 273.15  # K
temperature_water_out = 30.68 + 273.15  # K
temperature_environment_dry = 30.29 + 273.15  # K
temperature_environment_wet = 23.20 + 273.15  # K
pressure_environment = 99470  # Pa
flowrate_water = 5889 / 3600  # m3/s
flowrate_air = 255.97 * 10000 / 3600  # m3/s
ratio_air2water = 0.4844  # 气水比


def get_partial_pressure_of_saturated_vapour(t):
    """
    计算指定温度下饱和水蒸汽的分压

    计算公式参考DL/T1027-2006电力部《工业冷却塔测试规程》第13-14页

    :param t: 温度，K
    :return:
    """
    log_p = 5.005717 - 3.142305 * (1000 / t - 1000 / 373.116) + 8.2 * math.log10(373.16 / t) - 0.0024804 * (373.16 - t)
    p = math.pow(10, log_p)
    return p


def get_relative_humidity_of_moist_air(t_dry, t_wet, p_env=101325, a=3):
    """
    计算空气相对湿度

    参考DL/T1027-2006电力部《工业冷却塔测试规程》第13-14页
    系数A取值参考DL/T1027-2006电力部《工业冷却塔测试规程》第8页

    :param t_dry: 干球温度，K
    :param t_wet: 湿球温度，K
    :param p_env: 环境压力，Pa
    :param a: 干湿球温度计系数列表，可以取0~4，分别对应阿斯曼通风干湿表，标准百叶箱通风干湿表，阿费古斯特湿度表，百叶箱柱状干湿表，百叶箱球状干湿表
    :return: 相对湿度fai，取值范围为0~1
    """
    a_list = [0.000662, 0.000667, 0.0007947, 0.000815, 0.000857]
    p_wet = get_partial_pressure_of_saturated_vapour(t_wet)
    p_dry = get_partial_pressure_of_saturated_vapour(t_dry)
    return (p_wet - a_list[a] * p_env * (t_dry - t_wet)) / p_dry


def get_rho_of_moist_air(fai, t, p_env=101325):
    """
    计算湿空气密度

    :param fai: 空气的相对湿度，%，即空气中水汽压与饱和水汽压的百分比，计算取值范围为0~1
    :param t: 空气的开尔文温度
    :param p_env: 大气压力，Pa，默认101325
    :return:
    """
    return 1 / t * (0.003483 * p_env - 0.001316 * fai * get_partial_pressure_of_saturated_vapour(t))


def get_moisture_of_moist_air(fai, t, p_env=101325):
    """
    计算空气的含湿量，即湿空气中与一千克干空气同时并存的水蒸气的质量（克）

    :param fai: 空气的相对湿度，%，即空气中水汽压与饱和水汽压的百分比
    :param t: 温度，K
    :param p_env: 大气压力，Pa，默认101325
    :return:
    """
    p_theta = get_partial_pressure_of_saturated_vapour(t)  # 饱和空气中水蒸汽的分压
    return 0.622 * fai * p_theta / (p_env - fai * p_theta)


def get_enthalpy_of_moist_air(t_dry, moisture, gama=2500000, cd=1005, cv=1846):
    """
    计算湿空气的比焓

    :param t_dry: 空气的干球温度
    :param moisture: 空气的含湿量
    :param gama: 水在0℃时的汽化热
    :param cd: 干空气的比热容
    :param cv: 水蒸汽的比热容
    :return: 返回比焓，注意单位为J/kg
    """
    return cd * t_dry + moisture * (gama + cv * t_dry)


def get_air_flow_m3ph(f, rho2, p, k0=1):
    """
    冷却塔进塔空气量计算

    :param f: 有效通风面积
    :param k0: 毕托管校正系数，一般为1
    :param rho2: 出塔空气密度
    :param p: 风筒喉部动压
    :return:
    """
    return f * k0 * math.sqrt(2 / rho2) * p


def cal_air_flow_p_from_exp(p_d):
    """
    根据测量值计算风机喉部动压

    一般在风筒喉部四个方向打小孔，深入皮托管测量动压值，在喉部截面不同半径处测量得到一系列动压值，本方法根据所有测得的动压值计算平均动压

    :param p_d: 测点的动压值列表
    :return:
    """
    return np.array(p_d).mean()


def fan_pressure_total(rho_a, v1_m, v2_m, delta_p, zita=0.16):
    """
    计算风机全压，风机全压即整塔阻力

    塔进风口至风机下的总阻力为delta_p，为风量测量截面各测点全压与大气压插值的算数平均值

    :param rho_a: 出塔空气密度
    :param v1_m: 风量测量断面平均风速
    :param v2_m: 风筒出口断面平均风速
    :param delta_p: 塔进风口至风机下的总阻力，为风量测量断面各测点全压与大气压差值的算数平均值
    :param zita: 风筒气流阻力系数。与风筒扩散角有关，默认取值0.16
    :return:
    """
    ksi = zita * (1 - math.pow(v2_m / v1_m, 2))
    delta_p_f = 0.5 * rho_a * v2_m * v2_m + ksi * 0.5 * rho_a * v1_m * v1_m - delta_p
    return delta_p_f


def cal_omega(t1, t2, n=20, c_w=4.1868, method='simpson'):
    """
    计算冷却塔冷却数

    逆流塔热力数学模型是 Ka*V/Q=integrate(c_w/(h_t-h_theta), (t, t2, t1))，冷却塔数及方程右侧的积分数值，参考冷却塔性能试验规程
    式中，h_t是与水温相应的饱和空气比焓，h_theta是湿空气比焓，按进塔空气湿度计算

    :param t1: 冷却塔进水温度
    :param t2: 冷却塔出水温度
    :param n: simpson积分的分段数，最好取偶数
    :param c_w: 4.1868kJ/(kgK)，水的比热
    :param method: 积分方法，‘simpson'，’Chebyshev‘
    :return:
    """
    if method != 'simpson':
        print('暂不支持其他积分方法')
        return None
    delta_t = t1 - t2
    t_list = []  # 将t2到t1的温度等分为n段，分段的温度列表，对应t2, t2+dt, t2+2dt, t2+3dt,...
    h_list = []  # 对应于t_list中温度的饱和空气的比焓
    h_theta_list = []  # 第i个等份的空气焓
    dt = delta_t / (n - 1)

    for i in range(n):
        t_list.append(t2 + dt * i)
        # todo
        h_list.append()
        k_i = 1 - (t2 + i * dt) / (586 - 0.56 * (t2 + i * dt - 20))
        h_theta_list.append()
    sigma = 0
    for i in range(n):
        if i == 0 or i == (n - 1):
            sigma = sigma + 1 / (h_list[i] - h_theta_list[i])
        elif i % 2 == 0:
            sigma = sigma + 2 / (h_list[i] - h_theta_list[i])
        else:
            sigma = sigma + 4 / (h_list[i] - h_theta_list[i])
    return c_w * delta_t * sigma / 3 / n


