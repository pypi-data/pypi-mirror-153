import copy
import os.path

import numpy as np

from yangke.common.fileOperate import read_csv_ex, writeLines
from yangke.common.config import logger
from yangke.base import merge_dataframes_simple

folder = r"D:\lengduan"
files = [
    r"origin_retrain_0.csv",
    r"origin_retrain_1.csv",
    r"origin_retrain_2.csv",
    r"origin_retrain_3.csv",
    r"origin_retrain_4.csv",
    r"origin_retrain_5.csv",
    r"origin_retrain_6.csv",
    r"origin_retrain_7.csv",
    r"origin_retrain_8.csv",
    r"origin_retrain_9.csv",
    r"origin_retrain_10.csv",
    r"origin_retrain_11.csv",
]


def collect_data(files, unit_num):
    """
    统计files文件中的所有工况数据，根据温度和功率区间将数据划分至不同的数据集

    :param files: 数据文件名，csv格式文件
    :param unit_num: 机组编号
    :return:
    """

    def collect_t(temperature):
        """
        temperature为长度为12的列表，包括了同温度区间的所有工况数据，每一个元素为一个月的数据。
        本方法将12个月的全部数据合并后，按照功率分别分配到不同的功率范围中，返回五个功率范围中的数据的dataframe。
        五个功率范围分别为：200~250， 250~300， 300~350， 350~400， 400以上，单位为MW

        :param temperature:
        :return:
        """
        p1 = []
        p2 = []
        p3 = []
        p4 = []
        p5 = []
        for x in temperature:
            if x.get("p:200~250") is not None:
                p1.append(copy.deepcopy(x.get("p:200~250")))
            if x.get("p:250~300") is not None:
                p2.append(copy.deepcopy(x.get("p:250~300")))
            if x.get("p:300~350") is not None:
                p3.append(copy.deepcopy(x.get("p:300~350")))
            if x.get("p:350~400") is not None:
                p4.append(copy.deepcopy(x.get("p:350~400")))
            if x.get("p:>400") is not None:
                p5.append(copy.deepcopy(x.get("p:>400")))
        p1 = merge_dataframes_simple(p1)
        p2 = merge_dataframes_simple(p2)
        p3 = merge_dataframes_simple(p3)
        p4 = merge_dataframes_simple(p4)
        p5 = merge_dataframes_simple(p5)
        return p1, p2, p3, p4, p5

    data_whole_section = []
    lines = []
    t_list = []
    p_list = []
    for file in files:
        file = os.path.join(folder, file)
        logger.debug(file)
        df = read_csv_ex(file)
        print(f"{df.shape=}")
        if unit_num == 1:
            df.rename(columns={'电功率1': "电功率", '供热流量1': "供热流量", 'FGH入口燃气压力1': "FGH入口燃气压力",
                               'FGH入口燃气温度1': "FGH入口燃气温度", 'FGH水流量1': "FGH水流量", 'TCA水流量1': "TCA水流量",
                               '过热减温水流量1': "过热减温水流量", '再热减温水流量1': "再热减温水流量", '循泵运行台数1': "循泵运行台数",
                               '机力塔风机运行台数1': "机力塔风机运行台数", '循环效率1': "循环效率", '循环热耗率1': "循环热耗率",
                               '背压1': "背压"}, inplace=True)
        elif unit_num == 2:
            df.rename(columns={'电功率2': "电功率", '供热流量2': "供热流量", 'FGH入口燃气压力2': "FGH入口燃气压力",
                               'FGH入口燃气温度2': "FGH入口燃气温度", 'FGH水流量2': "FGH水流量", 'TCA水流量2': "TCA水流量",
                               '过热减温水流量2': "过热减温水流量", '再热减温水流量2': "再热减温水流量", '循泵运行台数2': "循泵运行台数",
                               '机力塔风机运行台数2': "机力塔风机运行台数", '循环效率2': "循环效率", '循环热耗率2': "循环热耗率",
                               '背压2': "背压"}, inplace=True)

        t_10 = copy.deepcopy(df[df['环境温度'] < 10])
        t_20 = copy.deepcopy(df[(10 <= df['环境温度']) & (df['环境温度'] < 20)])
        t_30 = copy.deepcopy(df[(20 <= df['环境温度']) & (df['环境温度'] < 30)])
        t_40 = copy.deepcopy(df[(30 <= df['环境温度']) & (df['环境温度'] < 40)])
        t_50 = copy.deepcopy(df[40 <= df['环境温度']])
        t_range = {"<10": t_10, "10~20": t_20, "20~30": t_30, "30~40": t_40, ">40": t_50}
        range_statistics = {}
        for k, _t in t_range.items():
            if _t.shape[0] > 0:
                p_10 = _t[_t["电功率"] < 10]
                p_200 = _t[(_t["电功率"] >= 10) & (_t["电功率"] < 200)]
                p_250 = _t[(_t["电功率"] >= 200) & (_t["电功率"] < 250)]
                p_300 = _t[(_t["电功率"] >= 250) & (_t["电功率"] < 300)]
                p_350 = _t[(_t["电功率"] >= 300) & (_t["电功率"] < 350)]
                p_400 = _t[(_t["电功率"] >= 350) & (_t["电功率"] < 400)]
                p_500 = _t[_t["电功率"] >= 400]
            else:
                p_10 = None
                p_200 = None
                p_250 = None
                p_300 = None
                p_350 = None
                p_400 = None
                p_500 = None
            p_t_range = {f"t:{k}": {f"p:停机": p_10, f"p:10~200": p_200,
                                    f"p:200~250": p_250, f"p:250~300": p_300,
                                    f"p:300~350": p_350, f"p:350~400": p_400,
                                    f"p:>400": p_500,
                                    }}
            range_statistics.update(p_t_range)

        cols = 0
        for t, v in range_statistics.items():
            t_list.append(t)
            num_p_list = []
            for p, _ in v.items():
                if p not in p_list:
                    p_list.append(p)
                num = 0 if _ is None else _.shape[0]
                num_p_list.append(f"{num:>8}")

            lines.append(",".join(num_p_list))
            cols = len(num_p_list)

        lines.append("," * (cols - 1))
        data_whole_section.append(copy.deepcopy(range_statistics))
    lines.insert(0, ",".join(p_list))
    writeLines("temp.csv", lines)
    t_10 = [x.get('t:<10') for x in data_whole_section]
    t_20 = [x.get('t:10~20') for x in data_whole_section]
    t_30 = [x.get('t:20~30') for x in data_whole_section]
    t_40 = [x.get('t:30~40') for x in data_whole_section]
    pt_10_250, pt_10_300, pt_10_350, pt_10_400, pt_10_450 = collect_t(t_10)
    pt_20_250, pt_20_300, pt_20_350, pt_20_400, pt_20_450 = collect_t(t_20)
    pt_30_250, pt_30_300, pt_30_350, pt_30_400, pt_30_450 = collect_t(t_30)
    pt_40_250, pt_40_300, pt_40_350, pt_40_400, pt_40_450 = collect_t(t_40)
    return {
        "p:200~250,t:<10": pt_10_250, "p:250~300,t:<10": pt_10_300, "p:300~350,t:<10": pt_10_350,
        "p:350~400,t:<10": pt_10_400, "p:>400,t:<10": pt_10_450,
        "p:200~250,t:10~20": pt_20_250, "p:250~300,t:10~20": pt_20_300, "p:300~350,t:10~20": pt_20_350,
        "p:350~400,t:10~20": pt_20_400, "p:>400,t:10~20": pt_20_450,
        "p:200~250,t:20~30": pt_30_250, "p:250~300,t:20~30": pt_30_300, "p:300~350,t:20~30": pt_30_350,
        "p:350~400,t:20~30": pt_30_400, "p:>400,t:20~30": pt_30_450,
        "p:200~250,t:30~40": pt_40_250, "p:250~300,t:30~40": pt_40_300, "p:300~350,t:30~40": pt_40_350,
        "p:350~400,t:30~40": pt_40_400, "p:>400,t:30~40": pt_40_450,
    }


def dispatch(df_pt_section):
    """
    将df中的数据按照循泵和风机数量划分到不同的数据集中，每个数据集对应一个单独的dataframe。返回的数据及分别表示：
    其中，第一个数据表示循泵运行台数，第二个数字表示风机运行台数。例如pf23表示2泵3风机

    :param df_pt_section:
    :return:
    """

    def dispatch_fan(pump):
        """
        将数据按照风机运行台数划分到[1,2,3,4,5]五个区间中
        返回一个列表，列表的每个元素分别代表风机运行1台、2台、3台、4台、5台时的时间
        :param pump:
        :return:
        """
        p = []
        for i in range(1, 6, 1):
            _ = pump[pump["机力塔风机运行台数"] == i]
            num = _.shape[0]
            power = _["电功率"].mean()  # 统计工况发电量时使用, MW.h
            p.append(power)
            # p.append(num)
        p = np.array(p)
        # 某些工况下风机正在启停，运行台数是错误的
        # if pump.shape[0] > p.sum() > 0:
        #     k_ = pump.shape[0] / p.sum()
        #     p = p * k_
        return p

    p_data1 = df_pt_section[df_pt_section["循泵运行台数"] == 1]
    p_data2 = df_pt_section[df_pt_section["循泵运行台数"] == 2]
    p_data3 = df_pt_section[df_pt_section["循泵运行台数"] == 3]

    p1 = dispatch_fan(p_data1)
    p2 = dispatch_fan(p_data2)
    p3 = dispatch_fan(p_data3)
    # total = p1.sum() + p2.sum() + p3.sum()
    # k_ = df_pt_section.shape[0] / total
    # p1, p2, p3 = p1 * k_, p2 * k_, p3 * k_
    return p1, p2, p3


pt_section = collect_data(files, unit_num=1)
lines = []
for k, v in pt_section.items():
    logger.debug(f"功率和温度范围为：{k}")
    lines.append(f"功率和温度范围为：{k}")
    pump1, pump2, pump3 = dispatch(v)
    logger.info(pump1)
    logger.info(pump2)
    logger.info(pump3)
    lines.append(",".join([str(x) for x in list(pump1)]))
    lines.append(",".join([str(x) for x in list(pump2)]))
    lines.append(",".join([str(x) for x in list(pump3)]))

writeLines(file="temp1.csv", lines=lines)
