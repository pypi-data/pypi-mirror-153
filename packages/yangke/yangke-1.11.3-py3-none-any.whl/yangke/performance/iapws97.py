"""
本模块使用iapws-97水及水蒸汽参数计算公式计算
"""
import iapws
from iapws.iapws97 import IAPWS97
from iapws.iapws95 import IAPWS95


def get_p_by_th(t, h):
    """
    根据h和t求p

    :param h: 焓，单位为 kJ/kg
    :param t: 温度，单位为 ℃
    :return: 压力，单位为 MPa
    """
    t_K = t + 273.15
    # 因为IAPWS97不能根据 焓 和 温度 求 压力，这里借助IAPWS95进行查找求解
    # 即多次计算 get_h_by_pt，对比计算的焓值与给定焓值相等则返回对应的p
    p = IAPWS95(h=h, T=t_K).P
    h_1 = get_h_by_pt(p=p, t=t)
    if h_1 > h:  # 温度不变时，压力越大，焓越低，考虑绝热管道的蒸汽流动，等焓，pt都降低
        # 说明估计的p偏小
        p_min = p
        p_max = p + 0.01
        while get_h_by_pt(p=p_max, t=t) > h:
            p_max = p_max + 0.01

    else:
        # 说明估计的p偏大
        p_max = p
        p_min = p - 0.01
        while get_h_by_pt(p=p_min, t=t) < h:
            p_min = p_min - 0.01
    # 真实的压力值位于p_min和p_max之间，二分法求解
    p_ave = (p_min + p_max) / 2
    h0 = get_h_by_pt(p=p_ave, t=t)
    while abs(h0 - h) > 0.000000001 and p_max - p_min > 0.000000001:
        if h0 > h:
            p_min = p_ave
        else:
            p_max = p_ave
        p_ave = (p_min + p_max) / 2
        h0 = get_h_by_pt(p=p_ave, t=t)

    return p_ave


def get_h_by_pt(p, t):
    """
    根据p和t求h

    :param p: 压力，单位为 MPa
    :param t: 温度，单位为 ℃
    :return: 焓，单位为 kJ/kg
    """
    h2o = IAPWS97(P=p, T=t + 273.15)
    return h2o.h


def get_s_by_pt(p, t):
    """
    根据p和t求熵

    :param p: 压力，单位为 MPa
    :param t: 温度，单位为 ℃
    :return: 焓，单位为 kJ/kg
    """
    h2o = IAPWS97(P=p, T=t + 273.15)
    return h2o.s


def get_t_by_hp(h, p):
    """
    根据h和p求t

    :param h: 焓，单位为 kJ/kg
    :param p: 压力，单位为 MPa
    :return: 温度，单位为 K
    """
    h2o = iapws.iapws97.IAPWS97_Ph(P=p, h=h)
    return h2o.T - 273.15


def get_h_by_px(p, x):
    """
    根据p和x求h

    :param p: 压力，单位为 MPa
    :param x: 蒸汽干度
    :return: 焓，单位为 kJ/kg
    """
    h2o = iapws.iapws97.IAPWS97_Px(P=p, x=x)
    return h2o.h


def get_t_by_p(p):
    """
    根据压力求对应的饱和温度

    :param p: MPa
    :return:
    """
    return iapws.iapws97._TSat_P(p) - 273.15


def get_p_by_t(t):
    """
        根据温度求对应的饱和压力

        :param t: ℃
        :return:
        """
    return iapws.iapws97._PSat_T(t + 273.15)


H_PT = get_h_by_pt
S_PT = get_s_by_pt
P_T = get_p_by_t
T_P = get_t_by_p
P_TH = get_p_by_th

if __name__ == "__main__":
    print(f"{H_PT(10, 500)=}")
    print(f"{S_PT(10, 500)=}")
    print(f"{T_P(1)=}")
    print(f"{P_T(200)=}")
    print(f"{P_TH(500, 3300)=}")
