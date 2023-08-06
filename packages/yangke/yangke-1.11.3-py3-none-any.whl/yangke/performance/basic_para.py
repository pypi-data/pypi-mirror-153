import sys
import inspect
from iapws import IAPWS97, IAPWS95
from yangke.performance.iapws97 import get_p_by_th, get_h_by_pt, get_t_by_hp


class TestPoint:
    """
    机组测点的流量及热力参数
    """

    def __init__(self):
        self.p: float = -1
        self.t: float = -1
        self.h: float = -1
        self.mass_flow = -1  # 质量流量
        self.available: bool = False  # 参数是否可用，仅当所有参数都可用时为True
        self.necessary: bool = True  # 参数是否必要

    def init_state(self):
        pass

    def set_state_by_name_and_value_list(self, test_point_name_list, value_list):
        """
        根据试验测点中已有数据更新测点中水或水蒸汽气的状态数据

        :param test_point_name_list:
        :param value_list:
        :return:
        """
        t_n = 0
        p_n = 0
        t = 0
        p = 0
        for name, value in zip(test_point_name_list, value_list):
            if "温度" in name:
                t = (value + t_n * t) / (t_n + 1)
                t_n = t_n + 1
            elif "压力" in name:
                p = (value + p_n * p) / (p_n + 1)
                p_n = p_n + 1
            elif "流量" in name:
                self.mass_flow = value
        if t != 0:
            self.t = t
        if p != 0:
            self.p = p
        if self.p != -1 and self.t != -1:
            self.available = True
            self.h = get_h_by_pt(p, t + 273.15)


class Case:
    """
    定义单个试验工况的数据组合，用于完成热耗、缸效率等的计算
    """
    parameters_available = {}  # 可用参数字典
    time_period = {}  # 性能试验数据采集时间段
    main_steam: "主蒸汽,主汽门前" = TestPoint()  # 不区分是左侧还是右侧主汽门
    adjust_steam: "调节级" = TestPoint()
    outlet_high: "高压缸排汽" = TestPoint()
    inlet_medium: "再热汽门前,热再,再热蒸汽" = TestPoint()
    outlet_medium: "中排,中压缸排汽" = TestPoint()
    inlet_low: "低压缸进汽" = TestPoint()
    outlet_low: "低压缸排汽" = TestPoint()
    outlet_turbine_pump: "小机排汽" = TestPoint()
    extract_1: "一段抽汽,一抽汽" = TestPoint()
    heater_1_vapor_in: "一号高加进汽,一高加进汽" = TestPoint()
    heater_1_vapor_out: "一号高加疏水,一高加疏水" = TestPoint()
    heater_1_water_in: "一号高加进水,一高加进水" = TestPoint()
    heater_1_water_out: "一号高加出水,一高加出水" = TestPoint()
    extract_2: "二段抽汽,二抽汽" = TestPoint()
    heater_2_vapor_in: "二号高加进汽,二高加进汽" = TestPoint()
    heater_2_vapor_out: "二号高加疏水,二高加疏水" = TestPoint()
    heater_2_water_in: "二号高加进水,二高加进水" = TestPoint()
    heater_2_water_out: "二号高加出水,二高加出水" = TestPoint()
    extract_3: "三段抽汽,三抽汽" = TestPoint()
    heater_pre_3_vapor_in: "蒸冷器进汽" = TestPoint()
    heater_pre_3_water_out: "蒸冷器出水" = TestPoint()
    heater_3_vapor_in: "三号高加进汽,三高加进汽" = TestPoint()
    heater_3_vapor_out: "三号高加疏水,三高加疏水" = TestPoint()
    heater_3_water_in: "三号高加进水,三高加进水" = TestPoint()
    heater_3_water_out: "三号高加出水,三高加出水" = TestPoint()
    extract_4: "四段抽汽,四抽汽" = TestPoint()
    heater_4_vapor_in: "四号高加进汽,四高加进汽" = TestPoint()
    heater_4_vapor_out: "四号高加疏水,四高加疏水" = TestPoint()
    heater_4_water_in: "四号高加进水,四高加进水" = TestPoint()
    heater_4_water_out: "四号高加出水,四高加出水" = TestPoint()
    extract_5: "五段抽汽,五抽汽" = TestPoint()
    heater_5_vapor_in: "五号低加进汽,五低加进汽" = TestPoint()
    heater_5_vapor_out: "五号低加疏水,五低加疏水" = TestPoint()
    heater_5_water_in: "五号低加进水,五低加进水" = TestPoint()
    heater_5_water_out: "五号低加出水,五低加出水" = TestPoint()
    extract_6: "六段抽汽,六抽汽" = TestPoint()
    heater_6_vapor_in: "六号低加进汽,六低加进汽" = TestPoint()
    heater_6_vapor_out: "六号低加疏水,六低加疏水" = TestPoint()
    heater_6_water_in: "六号低加进水,六低加进水" = TestPoint()
    heater_6_water_out: "六号低加出水,六低加出水" = TestPoint()
    extract_7: "七段抽汽,七抽汽" = TestPoint()
    heater_7_vapor_in: "七号低加进汽,七低加进汽" = TestPoint()
    heater_7_vapor_out: "七号低加疏水,七低加疏水" = TestPoint()
    heater_7_water_in: "七号低加进水,七低加进水" = TestPoint()
    heater_7_water_out: "七号低加出水,七低加出水" = TestPoint()
    extract_8: "八段抽汽,八抽汽" = TestPoint()
    heater_8_vapor_in: "八号低加进汽,八低加进汽" = TestPoint()
    heater_8A_vapor_in: "八A加热器进汽" = TestPoint()
    heater_8B_vapor_in: "八B加热器进汽" = TestPoint()
    heater_8_vapor_out: "八号低加疏水,八低加疏水" = TestPoint()
    heater_8A_vapor_out: "八A号低加疏水,八A低加疏水" = TestPoint()
    heater_8B_vapor_out: "八B号低加疏水,八B低加疏水" = TestPoint()
    heater_8_water_in: "八号低加进水,八低加进水" = TestPoint()
    heater_8A_water_in: "八A号低加进水,八B低加进水" = TestPoint()
    heater_8B_water_in: "八A号低加进水,八B低加进水" = TestPoint()
    heater_8_water_out: "八号低加出水,八低加出水" = TestPoint()
    heater_8A_water_out: "八A号低加出水,八A低加出水" = TestPoint()
    heater_8B_water_out: "八B号低加出水,八B低加出水" = TestPoint()
    heater_9A_vapor_in: "九A加热器进汽,九A号加热器进汽" = TestPoint()
    heater_9B_vapor_in: "九B加热器进汽,九A号加热器进汽" = TestPoint()
    heater_9A_vapor_out: "九A加热器疏水,九A号加热器疏水" = TestPoint()
    heater_9B_vapor_out: "九B加热器疏水,九B号加热器疏水" = TestPoint()
    heater_9A_water_in: "九A加热器进水,九A号加热器进水" = TestPoint()
    heater_9B_water_in: "九B加热器进水,九B号加热器进水" = TestPoint()
    heater_9A_water_out: "九A加热器出水,九A号加热器出水" = TestPoint()
    heater_9B_water_out: "九B加热器出水,九B号加热器出水" = TestPoint()
    seal_heater_1_water_in: "一号轴加进水,轴加进水" = TestPoint()
    seal_heater_2_water_in: "二号轴加进水,二轴加进水" = TestPoint()  # 包含二号轴加进水，排除轴加进水
    seal_heater_vapor_in: "汽封加热器进汽,轴封加热器进汽" = TestPoint()
    # seal_heater_vapor_out: "汽封加热器"
    seal_heater_water_in: "汽封加热器进水,轴封加热器进水,轴加进水" = TestPoint()
    seal_heater_water_out: "汽封加热器出水,轴封加热器出水,轴加出水" = TestPoint()
    # ------------------------------ 热井至加热器之间测点 ----------------------------
    heat_well_out: "热井出" = TestPoint()
    water_condense_pump_in: "凝泵进" = TestPoint()
    water_condense_pump_A_in: "凝泵A进" = TestPoint()
    water_condense_pump_B_in: "凝泵B进" = TestPoint()
    water_condense_pump_out: "凝泵出" = TestPoint()
    water_condense_pump_A_out: "凝泵A出" = TestPoint()
    water_condense_pump_B_out: "凝泵B出" = TestPoint()
    # ------------------------------ 低加出口至高加进口之间测点 ----------------------------
    main_condense_water: "主凝结水,进除氧器凝结水,除氧器进水,除氧器进口凝结水" = TestPoint()
    deaerator_vapor_in: "除氧器进汽" = TestPoint()
    deaerator_drain_water_in: "进除氧器疏水" = TestPoint()
    deaerator_out: "除氧器出水,除氧器下水" = TestPoint()
    pump_turbine_vapor_in: "小机进汽,给水泵汽轮机进汽" = TestPoint()
    pump_before_water_in: "前置泵进" = TestPoint()
    pump_before_water_out: "前置泵出" = TestPoint()
    feed_pump_in: "给水泵进,汽泵进" = TestPoint()
    feed_pump_out: "给水泵出,汽泵出" = TestPoint()
    final_feed_water: "最终给水" = TestPoint()
    water_reheater_reducing: "再热减温水,再减,再热器减温水" = TestPoint()
    water_overheat_reducing_1: "过热一级减温水" = TestPoint()
    water_overheat_reducing_2: "过热二级减温水" = TestPoint()
    p_env: "大气压力" = 0
    condenser_water_level: "凝汽器水位" = 0
    deaerator_water_level: "除氧器水位" = 0
    # ------------------------------------ 省煤器 ----------------------------------------
    economizer_water_outlet: "省煤器出,省煤器回" = TestPoint()  # 省煤器和低温省煤器的测点都会归到该勒种
    economizer_water_inlet: "省煤器进水" = TestPoint()
    # ------------------------------------ 漏气 ----------------------------------------
    leakage_hp_seal_main: "高压缸前.后轴封漏汽母管" = TestPoint()
    leakage_hp_to_extract_3: "高压门杆漏气至三抽" = TestPoint()
    leakage_hp_to_ssr: "高压门杆漏气至SSR" = TestPoint()
    leakage_hp_seal_to_extract_4: "高压缸前.后轴封漏汽至四" = TestPoint()
    leakage_tail_ip_seal_to_ssr: "中压缸后轴封二段漏气至SS,中压后轴封二漏至SS,中压后轴封二漏段漏汽至SS" = TestPoint()
    leakage_head_ip_seal_to_ssr: "中压缸前轴封二段漏气至SS" = TestPoint()
    # ------------------------------------ 循环水 ----------------------------------------
    condenser_recycled_water_in: "凝汽器循环水进水" = TestPoint()
    condenser_A_recycled_water_in: "凝汽器A侧循环水进水" = TestPoint()
    condenser_B_recycled_water_in: "凝汽器B侧循环水进水" = TestPoint()
    condenser_recycled_water_out: "凝汽器循环水出水" = TestPoint()
    condenser_A_recycled_water_out: "凝汽器A侧循环水出水" = TestPoint()
    condenser_B_recycled_water_out: "凝汽器B侧循环水出水" = TestPoint()

    def set_value_of_test_point(self, var_str, test_point_name_list, value_list):
        """
        根据计算程序参数对应的 所有测点的名称和值 给计算程序中测点水/水蒸气赋状态

        :param var_str:
        :param test_point_name_list:
        :param value_list:
        :return:
        """
        obj = getattr(self, var_str)
        if isinstance(obj, TestPoint):
            obj.set_state_by_name_and_value_list(test_point_name_list, value_list)
        else:
            setattr(self, var_str, float(value_list))


# power_station_annotations = sys.modules[__name__].__annotations__
alternative_symbol = {"1": "一", "2": "二", "3": "三", "4": "四", "5": "五", "6": "六", "7": "七",
                      "8": "八", "9": "九", "汽": "气", "0": "零", "零": "〇", "进": "入", "一轴加": "一号轴加", "A": "a",
                      "B": "b", "高加": "加热器", "低加": "加热器", "凝泵": "凝结水泵"}

# 数据采集系统中为绝对压力的测点
pressure_absolute = ["低排", "低压缸排汽", "小机排汽", "七段抽汽", "八段抽汽", "高压汽源至汽封蒸汽冷却器进汽压力",
                     "大气压", "环境压力", "七号低加", "7号低加", "8A低加", "8B低加", "9A低加", "9B低加",
                     # "高压缸前后轴封", "中压缸前轴封", "中压缸后轴封","轴封加热器进汽压力", "高压缸前后轴封漏汽母管",
                     ]

# 数据采集系统中为相对压力的测点
pressure_relative = ["主汽门", "调节级", "高压缸排汽", "再热蒸汽", "再热汽门", "中压缸进汽", "中压缸排汽",
                     "低压缸进汽", "一段抽汽", "二段抽汽",
                     "三段抽汽", "四段抽汽", "五段抽汽",
                     "一抽", "二抽", "三抽", "四抽", "五抽",
                     "高加进汽", "高加", "5号低加", "小机进汽",
                     "除氧器进汽",
                     "最终给水", "给水泵出水", "凝泵", "再热减温水", "高压门杆漏汽",
                     "蒸汽冷却器",
                     "低温省煤器进水压力", "低温省煤器",
                     "蒸冷器", "低省", "凝结水", "前置泵", "汽泵", "循环水"]
