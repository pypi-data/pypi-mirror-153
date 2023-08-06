flow_全厂补水 = 100
flow_三期供热回水 = 10000
flow_四期供热回水 = 11000
flow_5号供热 = 4500
flow_6号供热 = flow_三期供热回水 - flow_5号供热 + flow_全厂补水 / 2
flow_7号供热 = 6000
flow_8号供热 = flow_四期供热回水 - flow_7号供热 + flow_全厂补水 / 2
flow_全厂供水 = flow_5号供热 + flow_6号供热 + flow_7号供热 + flow_8号供热

t_供热计划温度 = 90

t_modify_供热回水 = 0
t_dif_三四期 = 2

# 机组额定出力
power_design = [300, 300, 300, 300]
# 调峰补贴负荷上限，按照辅助调峰服务考核细则，调峰报价仅在低于70%负荷率的情况下填报，70%负荷以上的成本价格可用于分析调峰分摊的盈亏情况。
power_补贴上限 = [p * 0.7 for p in power_design]

# 是否供热
heat_supply_no5 = True
heat_supply_no6 = True
heat_supply_no7 = True
heat_supply_no8 = True

三期供热机组台数 = 0
四期供热机组台数 = 0
供热机组台数 = 0
if heat_supply_no5:
    供热机组台数 = 供热机组台数 + 1
    三期供热机组台数 = 三期供热机组台数 + 1
if heat_supply_no6:
    供热机组台数 = 供热机组台数 + 1
    三期供热机组台数 = 三期供热机组台数 + 1
if heat_supply_no7:
    供热机组台数 = 供热机组台数 + 1
    四期供热机组台数 = 四期供热机组台数 + 1
if heat_supply_no8:
    供热机组台数 = 供热机组台数 + 1
    四期供热机组台数 = 四期供热机组台数 + 1

# 是否切缸
cut_no5 = True
cut_no6 = True
cut_no7 = False
cut_no8 = True

t_供热回水 = 45 + (t_供热计划温度 - 80) / 2 + t_modify_供热回水
供热负荷_全厂 = flow_全厂供水 / 3.6 * (t_供热计划温度 - t_供热回水) * 4.19 / 1000

t_no5_供热回水 = t_供热回水 + t_dif_三四期 / 2
t_no6_供热回水 = t_供热回水 + t_dif_三四期 / 2
t_no7_供热回水 = t_供热回水 - t_dif_三四期 / 2
t_no8_供热回水 = t_供热回水 - t_dif_三四期 / 2
三期偏置 = 0

五号偏置 = 10
七号偏置 = 0

供热负荷_no5 = 0
供热负荷_no6 = 0
供热负荷_no7 = 0
供热负荷_no8 = 0
if heat_supply_no5:
    供热负荷_no5 = 供热负荷_全厂 / 供热机组台数 + 三期偏置 * 4.2
    供热负荷_no5 = 供热负荷_no5 + 五号偏置 * 4.2 if heat_supply_no6 else 供热负荷_no5
if heat_supply_no6:
    供热负荷_no6 = 供热负荷_全厂 / 供热机组台数 + 三期偏置 * 4.2
    供热负荷_no6 = 供热负荷_no6 - 五号偏置 * 4.2 if heat_supply_no5 else 供热负荷_no6
if heat_supply_no7:  # 在该情况下，四期供热机组台数必然大于0
    供热负荷_no7 = 供热负荷_全厂 / 供热机组台数 - 三期偏置 * 4.2 * 三期供热机组台数 / 四期供热机组台数
    供热负荷_no7 = 供热负荷_no7 + 七号偏置 * 4.2 if heat_supply_no8 else 供热负荷_no7
if heat_supply_no8:
    供热负荷_no8 = 供热负荷_全厂 / 供热机组台数 - 三期偏置 * 4.2 * 三期供热机组台数 / 四期供热机组台数
    供热负荷_no8 = 供热负荷_no7 - 七号偏置 * 4.2 if heat_supply_no7 else 供热负荷_no8

t_no5_供热 = 供热负荷_no5 * 1000 / flow_5号供热 * 3.6 / 4.19 + t_no5_供热回水
t_no6_供热 = 供热负荷_no6 * 1000 / flow_6号供热 * 3.6 / 4.19 + t_no6_供热回水
t_no7_供热 = 供热负荷_no7 * 1000 / flow_7号供热 * 3.6 / 4.19 + t_no7_供热回水
t_no8_供热 = 供热负荷_no8 * 1000 / flow_8号供热 * 3.6 / 4.19 + t_no8_供热回水

energy_no5_供热 = flow_5号供热 * (t_no5_供热 - t_no5_供热回水) * 4.19 * 24 / 1000
energy_no6_供热 = flow_5号供热 * (t_no6_供热 - t_no5_供热回水) * 4.19 * 24 / 1000
energy_no7_供热 = flow_5号供热 * (t_no7_供热 - t_no5_供热回水) * 4.19 * 24 / 1000
energy_no8_供热 = flow_5号供热 * (t_no8_供热 - t_no5_供热回水) * 4.19 * 24 / 1000

供热当量电负荷_no5 = 供热负荷_no5 / 4.42
供热当量电负荷_no6 = 供热负荷_no6 / 4.56
供热当量电负荷_no7 = 供热负荷_no7 / 4.5
供热当量电负荷_no8 = 供热负荷_no8 / 4.8
供热当量电负荷 = 供热当量电负荷_no5 + 供热当量电负荷_no6 + 供热当量电负荷_no7 + 供热当量电负荷_no8

电负荷_max_no5 = 320 - 供热当量电负荷_no5 if heat_supply_no5 else 300
电负荷_max_no6 = 320 - 供热当量电负荷_no6 if heat_supply_no6 else 300
电负荷_max_no7 = 320 - 供热当量电负荷_no7 if heat_supply_no7 else 300
电负荷_max_no8 = 320 - 供热当量电负荷_no8 if heat_supply_no8 else 300
电负荷_max = 电负荷_max_no5 + 电负荷_max_no6 + 电负荷_max_no7 + 电负荷_max_no8


def 下限电负荷(is_供热, is_cut, 供热当量电负荷_local=0):
    if is_供热:
        if is_cut:
            result = max(供热当量电负荷_local * 2, 150 - 供热当量电负荷_local)
        else:
            result = max(供热当量电负荷_local * 1.65 + 70, 120 - 供热当量电负荷_local)
    else:
        result = 120
    return result


电负荷_min_no5 = 下限电负荷(heat_supply_no5, cut_no5, 供热当量电负荷_no5)
电负荷_min_no6 = 下限电负荷(heat_supply_no6, cut_no6, 供热当量电负荷_no6)
电负荷_min_no7 = 下限电负荷(heat_supply_no7, cut_no7, 供热当量电负荷_no7)
电负荷_min_no8 = 下限电负荷(heat_supply_no8, cut_no8, 供热当量电负荷_no8)

电负荷_min = 电负荷_min_no5 + 电负荷_min_no6 + 电负荷_min_no7 + 电负荷_min_no8

price_coal = 806
price_elec = 0.33
price_heat = 25.69
考虑电量比例 = 0
单位煤耗变动 = 2.74

效率成本变化 = price_coal * 单位煤耗变动 / 1000 + price_elec
上限供热成本 = 10000 / 65 * (price_heat - 20 * price_coal / 1000 - 3 * price_elec) / 10
下限供热成本 = 3.6 * 10 * 2.5 * (price_heat - 20 * price_coal / 1000 - 3 * price_elec) / 10

电负荷_list = range(80, 301, 10)
