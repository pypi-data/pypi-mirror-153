import copy
import math
from typing import List

import pandas as pd
import os

from yangke.base import plot_2d_scatter, yield_all_file, interpolate_value_complex, plot_2d_line, \
    update_matplotlib_font_config, get_datetime_col_of_dataframe
from yangke.core import strInList
from yangke.common.fileOperate import read_csv_ex, write_excel
from yangke.common.config import logger

velocity_min = 3  # 切入风速m/s
velocity_max = 20  # 切出风速m/s
diameter = 141  # 风力发电机转轮直径，单位m
r0 = 287.05  # 干燥空气的气体常数，单位J/(kg.K)
rho0 = 1.225
p0 = 87580  # 87580  # 替代的大气压力，如果没有大气压力测点，但计算过程需要大气压力，则会取该值
# 数据文件中应包括风速、有功功率、温度、大气压力
data_file = r"E:\热工院\2021\101工程风光储\导数\Data_20210702032750\A环线\SNTY02_20210101_20210702_ten_avg_val.csv"
data_folder = r"E:\热工院\2021\101工程风光储\导数\Data_20210702032750"
velocity_wind_design = [3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5,
                        14, 14.5, 15, 15.5, 16, 16.5, 17, 17.5, 18, 18.5, 19, 19.5, 20]
power_design = [45, 144, 254, 386, 544, 733, 958, 1223, 1532, 1886, 2288, 2730, 2989, 3116, 3176, 3198, 3200, 3200,
                3200, 3200, 3200, 3200, 3200, 3200, 3200, 3200, 3200, 3200, 3200, 3200, 3200, 3200, 3200, 3200, 3200]
power_design = [x * 1000 for x in power_design]
x_ticks = [x for x in range(0, 21, 4)]
y_ticks = [y for y in range(0, 4001, 500)]


class SectionData:
    """
    风力发电机的数据类，记录风力发电机的各类原始及计算数据
    """

    def __init__(self, section=None, dataframe: pd.DataFrame = None):
        self.section = section  # 风速区间
        self.dataframe = dataframe  # 在此风速区间内的所有运行数据点
        self.diameter = None  # 风力发电机转轮直径 m
        self.area = None  # 风机转轮扫略面积 m2
        self.velocity_mean = None  # 所有运行数据点的平均风速 m/s
        self.velocity_mean_standard = None  # 所有运行数据点的标准风速平均值
        self.power_mean = None  # 所有运行数据点的平均功率 W
        self.power_mean_standard = None  # 所有运行数据点的标准功率平均值
        self.temperature_mean = None  # 所有运行数据点的平均温度 K
        self.pressure_mean = None  # 所有运行数据点的平均气压 Pa
        self.rho_mean = None  # 所有运行数据点的平均空气密度 kg/m3
        self.ita = None  # 本风速区间对应的功率系数 %
        self.ita_standard = None  # 本风速区间对应的标准功率系数
        self.num_of_data = None  # 本风速区间的数据记录个数
        self.power_wind = None  # 本风速区间的平均风功率
        self.power_wind_standard = None  # 本风速区间的标准风功率的平均值
        self.rho_0 = None

    def set_wind_turbine_info(self, diameter):
        self.diameter = diameter
        self.area = math.pi * diameter * diameter / 4

    def calculate_wind_turbine(self):
        mean = self.dataframe.mean(numeric_only=True)
        self.velocity_mean = mean["风速"]
        self.power_mean = mean["有功功率"]
        self.temperature_mean = mean["温度"]
        if self.temperature_mean < 200:  # 如果环境温度单位是℃，则转换为K
            self.temperature_mean = self.temperature_mean + 273.15
        self.pressure_mean = mean["大气压力"]
        if self.pressure_mean < 70000:  # 如果大气压力的单位是KPa，则转换为Pa
            self.pressure_mean = self.pressure_mean * 1000
        self.rho_mean = self.pressure_mean / r0 / self.temperature_mean
        self.power_wind = 0.5 * self.area * self.rho_mean * math.pow(self.velocity_mean, 3)

        self.ita = 2 * self.power_mean / (self.rho_mean * self.area * math.pow(self.velocity_mean, 3)) * 100

        self.velocity_mean_standard = mean["标准风速"]
        self.power_mean_standard = mean["标准功率"]
        self.power_wind_standard = 0.5 * self.area * self.rho_mean * math.pow(self.velocity_mean_standard, 3)
        self.ita_standard = 2 * self.power_mean_standard / \
                            (rho0 * self.area * math.pow(self.velocity_mean_standard, 3)) * 100

    def set_data_num(self, num):
        self.num_of_data = num


def fix_data(file):
    """
    确保数据列完备，至少包括["风速", "有功功率", "温度", "大气压力"]


    :param file:
    :return:
    """
    data0: pd.DataFrame = read_csv_ex(file)
    columns = data0.columns
    columns_need = ["风速", "有功功率", "温度", "大气压力"]
    column_name = {}
    # 处理必要数据列：风速
    exist_v = strInList("风速", columns, need_item=True)  # 如果某一列的列名包含“风速”则摘出该列名，将列明更改为风速
    if exist_v[0]:
        column_name.update({exist_v[1]: "风速"})
    else:
        logger.error("数据中不存在必要数据列：风速")
    # 处理非必要数据列：温度
    exist_temp = strInList("温度", columns, need_item=True)
    if exist_temp[0]:
        column_name.update({exist_temp[1]: "温度"})
    else:
        exist_temp = strInList("气温", columns, need_item=True)
        if exist_temp[0]:
            column_name.update({exist_temp[1]: "温度"})
    # 处理非必要数据列：大气压力
    exist_pressure = strInList("大气压力", columns, need_item=True)
    if exist_pressure[0]:
        column_name.update({exist_pressure[1]: "大气压力"})
    else:
        exist_temp = strInList("压力", columns, need_item=True)
        if exist_temp[0]:
            column_name.update({exist_temp[1]: "大气压力"})
        else:
            logger.debug("未找到大气压力列")
            data0["大气压力"] = p0
    # 处理必要数据列：有功功率
    exist_power = strInList("有功功率", columns, need_item=True)
    if exist_power[0]:
        column_name.update({exist_power[1]: "有功功率"})
    else:
        exist_power = strInList("功率", columns, need_item=True)
        if exist_power[0]:
            column_name.update({exist_power[1]: "有功功率"})
        else:
            logger.error("数据中不存在必要数据列：有功功率")

    data0.rename(columns=column_name, inplace=True)
    col = get_datetime_col_of_dataframe(data0)
    if col is None:
        import datetime
        time = datetime.datetime(2021, 1, 1, 0, 0, 0)
        time_series = []
        for idx in range(data0.shape[0]):
            time_series.append(time)
            time = time + datetime.timedelta(minutes=10)
        data0["DateTime"] = time_series
    else:
        data0.rename(columns={col: "DateTime"}, inplace=True)
    return data0


def filter_data(data0):
    """
    筛选数据，获得在切入风速和切出风速之间正常运行的风机运行数据，同时统一数据单位为国际单位

    :param data0: 数据dataframe
    :return:
    """
    logger.debug(f"总数据量：{data0.shape}")
    data1 = data0.dropna()
    logger.debug(f"非空数据量：{data1.shape}")
    data2 = data1[data1["有功功率"] > 0]
    logger.debug(f"风力发电机在服务状态数据量：{data2.shape}")
    data3 = data2[data2["风速"] >= velocity_min]
    logger.debug(f"去掉风速小于切入风速的工况点，剩余数据量：{data3.shape}")
    data3 = data3[data3["风速"] <= velocity_max]
    logger.debug(f"去掉风速大于切出风速的工况点，剩余数据量：{data3.shape}")
    if data3.shape[0] >= 1:
        series = data3.mean()
        if series["有功功率"] < 5:  # 单个风机的功率不会大于5MW，因此如果功率值小于5，则必然单位是MW
            data3["有功功率"] = data3["有功功率"] * 1000000
        elif series["有功功率"] < 5000:  #
            data3["有功功率"] = data3["有功功率"] * 1000
        if series["温度"] < 200:  # 如果环境温度小于200，则单位必然是℃
            data3["温度"] = data3["温度"] + 273.15
        if series["大气压力"] > 800:  # 表明单位为Pa
            pass
        elif series["大气压力"] > 8:  # 表明单位为kPa
            series["大气压力"] = series["大气压力"] * 1000
        else:  # 单位为MPa
            series["大气压力"] = series["大气压力"] * 1000000

    return data3


def split_section(step=1.0, number=10, mode="step"):
    """
    分割风速区间

    :param step: 区间步长
    :param number: 需要分割的区间个数，需要设置mode="number"
    :return:
    """
    result = []
    if mode == "step":
        x_min = velocity_min
        while x_min < velocity_max:
            x_max = x_min + step
            if x_max <= velocity_max:
                result.append([x_min, x_max])
                x_min = x_max
    elif mode == "number":
        pass
    logger.debug(f"风速区间为：{result}")
    return result


def dispatch_data_to_section(data, sections):
    """
    按照风速区间将运行数据分割；并计算每个区间的各项风力发电系统参数

    :param data: 风力发电系统筛选后的运行数据
    :param sections: 区间信息
    :return: 不同风速区间对应的运行数据的列表
    """
    section_data_list = []
    for section in sections:
        data1 = data[(data["风速"] <= section[1]) & (data["风速"] >= section[0])]  # 筛选出风速在区间内的数据
        logger.debug(f"风速在区间{section}中的数据量：{data1.shape[0]}")
        if data1.shape[0] == 0:  # 该风速区间没有数据记录
            section_datum = copy.deepcopy(section_data_list[-1])
            section_datum.velocity_mean = (section[0] + section[1]) / 2
            section_datum.velocity_mean_standard = (section[0] + section[1]) / 2
        else:
            section_datum = SectionData(section, data1)
            section_datum.set_wind_turbine_info(diameter)
            section_datum.set_data_num(data1.shape[0])
            section_datum.calculate_wind_turbine()
            # 如果当前功率比上一个风速区间的功率小，则说明当前区间功率点较少或存在限功率数据，需要将当前区间功率修正到上一个风速区间的功率
            if len(section_data_list) > 0 and section_datum.power_mean < 0.99 * section_data_list[-1].power_mean:
                section_datum.power_mean = section_data_list[-1].power_mean
        section_data_list.append(section_datum)
    return section_data_list


def get_cp_vs_v(section_data_list: List[SectionData]):
    """
    写出每个风机
    :param section_data_list:
    :return:
    """
    velocity = []
    ita = []
    for sect in section_data_list:
        velocity.append(sect.velocity_mean)
        ita.append(sect.ita)
    _data = {"风速": velocity, "功率系数": ita}
    result = pd.DataFrame(_data)
    return result


def get_p_vs_v(section_data_list: List[SectionData]):
    """
    获取功率随风速的变化曲线数据

    :param section_data_list:
    :return:
    """
    if len(velocity_wind_design) == len(power_design) == 0:
        velocity = velocity_wind_design
        power = power_design
    else:
        velocity = []
        power = []
        for sect in section_data_list:
            velocity.append(sect.velocity_mean)
            power.append(sect.power_mean)
    _data = {"风速": velocity, "有功功率": power}
    result = pd.DataFrame(_data)
    return result


def section_data_to_df(section_data_list: List[SectionData]):
    velocity = []
    power = []
    power_kw = []
    cp = []
    num = []
    temperature = []
    power_wind = []
    velocity_standard = []
    power_standard = []
    cp = []
    cp_standard = []
    power_wind_standard = []
    for sect in section_data_list:
        velocity.append(sect.velocity_mean)
        power.append(sect.power_mean)
        power_kw.append(sect.power_mean / 1000)
        cp.append(sect.ita)
        num.append(sect.num_of_data)
        temperature.append(sect.temperature_mean)
        power_wind.append(sect.power_wind)
        velocity_standard.append(sect.velocity_mean_standard)
        power_standard.append(sect.power_mean_standard)
        cp_standard.append(sect.ita_standard)
        power_wind_standard.append(sect.power_wind_standard)
    _data = {"风速": velocity, "有功功率": power, "功率系数": cp, "数据量": num, "风功率": power_wind, "温度": temperature,
             "标准风速": velocity_standard, "标准功率": power_standard, "标准功率kW": power_kw, "标准功率系数": cp_standard,
             "标准风功率": power_wind_standard}
    result = pd.DataFrame(_data)
    return result


def delete_noise_record(raw_data, reference_line, tolerance=0.4, method=None):
    """
    删除噪点数据记录

    :param raw_data:
    :param reference_line:
    :param tolerance:
    :param method: 可以取值"对称剔除"
    :return:
    """
    reference_points = []
    result = []
    for idx, point in reference_line.iterrows():
        reference_points.append((point[0], point[1]))
    for (row_num, series) in raw_data.iterrows():
        v = series["风速"]
        p_item = series["有功功率"]  #
        p_inter = interpolate_value_complex(v, reference_points)
        if method == "对称剔除":
            if abs(p_inter - p_item) / p_inter < tolerance:  # 只有当前测点小于平均值的时候，才可能舍弃测点数据
                result.append(series)
        else:
            if (p_inter - p_item) / p_inter < tolerance:  # 只有当前测点小于平均值的时候，才可能舍弃测点数据
                result.append(series)
            elif v < 10:
                if (p_inter - p_item) / p_inter < tolerance + (1 - v / 10) * (1.3 - tolerance):
                    result.append(series)
    return pd.DataFrame(result)


if __name__ == "__main__":
    for data_file in yield_all_file(data_folder, filter_=[".csv"]):
        base_name = os.path.basename(data_file)
        pure_name = os.path.splitext(base_name)[0]
        xlsx_path = os.path.join(data_folder, f"{pure_name}.xlsx")
        pic_path_ps1 = os.path.join(data_folder, f"{pure_name}_功率散点1.png")
        pic_path_ps2 = os.path.join(data_folder, f"{pure_name}_功率散点2.png")
        pic_path_p = os.path.join(data_folder, f"{pure_name}_功率曲线.png")
        pic_path_p2 = os.path.join(data_folder, f"{pure_name}_功率曲线2.png")
        pic_path_p3 = os.path.join(data_folder, f"{pure_name}_功率曲线3.png")
        pic_path_cp = os.path.join(data_folder, f"{pure_name}_功率系数曲线.png")
        pic_path_cp2 = os.path.join(data_folder, f"{pure_name}_功率系数曲线2.png")

        data = fix_data(data_file)  # 确保存在必要的数据列
        data = filter_data(data)  # 剔除切入、切出风速范围以外和功率为负的数据记录

        # 数据标准化
        data["标准空气密度"] = 1.225
        data["空气气体常数"] = 287.05
        data["rho10"] = data["大气压力"] / data["空气气体常数"] / data["温度"]
        data["标准风速"] = data["风速"] * (data["rho10"] / data["标准空气密度"]) ** (1 / 3)
        data["标准功率"] = data["有功功率"] * data["标准空气密度"] / data["rho10"]

        update_matplotlib_font_config()
        plot_2d_scatter(data["风速"], data["有功功率"] / 1000, show=False, s=10, point_color="#0072BD",
                        x_ticks=x_ticks,
                        x_label="风速（m/s）", y_label="发电机有功功率（kW）", save_to=pic_path_ps1)  # 绘制功率散点图
        sections = split_section(step=0.5)
        section_data = dispatch_data_to_section(data, sections)
        p_vs_v = get_p_vs_v(section_data)
        data_pure = delete_noise_record(raw_data=data, reference_line=p_vs_v, tolerance=0.15)  # 按参考线删除噪点数据
        # data_pure = delete_noise_record(raw_data=data_pure, reference_line=p_vs_v, tolerance=0.3)  # 按参考线删除噪点数据
        # data_pure = delete_noise_record(raw_data=data_pure, reference_line=p_)

        plot_2d_scatter(data_pure["风速"], data_pure["有功功率"] / 1000, show=False, s=10, point_color="#0072BD",
                        x_label="风速（m/s）", y_label="发电机有功功率（kW）", x_ticks=x_ticks, save_to=pic_path_ps2)  # 绘制功率散点图

        section_data = dispatch_data_to_section(data_pure, sections)
        df_sections = section_data_to_df(section_data)
        # plot_2d_line(df_sections["风速"], df_sections["有功功率"] / 1000,
        #              x_label="风速（m/s）", y_label="发电机有功功率（kW）", save_to=pic_path_p)
        # plot_2d_line(df_sections["风速"], df_sections["功率系数"], x_label="风速（m/s）",
        # y_label="功率系数（%）", save_to=pic_path_cp)
        df_sections.sort_values(by=["标准风速", "风速"])
        plot_2d_line(df_sections["风速"], df_sections["有功功率"] / 1000, show=False, x_ticks=x_ticks,
                     x_label="风速（m/s）", y_label="发电机有功功率（kW）", save_to=pic_path_p)
        plot = plot_2d_line(df_sections["风速"], df_sections["有功功率"] / 1000, show=False, line_label="实际功率曲线",
                            x_label="风速（m/s）", y_label="发电机有功功率（kW）", x_ticks=x_ticks)
        plot_2d_line(velocity_wind_design, [p / 1000 for p in power_design], method="append", line_color="blue",
                     plot=plot, show=False,
                     line_label="设计功率曲线", save_to=pic_path_p2, draw_legend=True)
        del plot
        plot = plot_2d_line(df_sections["标准风速"], df_sections["标准功率"] / 1000, show=False, line_label="实际标准功率曲线",
                            x_label="风速（m/s）", y_label="发电机有功功率（kW）", x_ticks=x_ticks, line_color="#41FFA2")
        plot = plot_2d_line(df_sections["风速"], df_sections["有功功率"] / 1000, show=False, line_label="实际功率曲线",
                            plot=plot)
        plot_2d_line(velocity_wind_design, [p / 1000 for p in power_design], method="append", line_color="blue",
                     plot=plot, show=False,
                     line_label="设计功率曲线", save_to=pic_path_p3, draw_legend=True)

        plot_2d_line(df_sections["风速"], df_sections["功率系数"], x_label="风速（m/s）", y_label="功率系数（%）",
                     x_ticks=x_ticks, save_to=pic_path_cp, show=False)
        plot_2d_line(df_sections["风速"], df_sections["标准功率系数"], x_label="风速（m/s）", y_label="标准功率系数（%）",
                     x_ticks=x_ticks, save_to=pic_path_cp2, show=False)
        total_num = df_sections["数据量"].sum()
        sigma_pt = (df_sections["有功功率"] * df_sections["数据量"] / total_num).mean()
        sigma_pw = (df_sections["风功率"] * df_sections["数据量"] / total_num).mean()
        ita_all_section = sigma_pt / sigma_pw
        y = interpolate_value_complex(9, x_list=list(df_sections["风速"]), y_list=list(df_sections["功率系数"]))
        df_ita = pd.DataFrame({"风频加权有功功率平均值": [sigma_pt], "总风功率平均值": [sigma_pw],
                               "单机整体效率": [ita_all_section], "额定功率系数": [y]})
        data_output = {"剔除后的数据": data_pure, "数据点": df_sections, "单机整体效率": df_ita}
        write_excel(xlsx_path, data_output)
    print("done")
