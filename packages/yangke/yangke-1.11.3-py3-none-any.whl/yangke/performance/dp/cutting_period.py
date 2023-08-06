import copy
import datetime
import os
import re

import numpy as np
import pandas as pd

from yangke.base import save_as_xlsx, cut_time_period_of_dataframe, get_datetime_col_of_dataframe, is_number, \
    is_contain_chinese, is_datetime, set_dataframe_header, merge_two_dataframes
from yangke.common import fileOperate
from yangke.common.config import logger
from yangke.common.fileOperate import read_csv_ex, writeLines
from yangke.performance.dp.file_type_detect import get_detailed_type_of_data_file
from yangke.performance.dp.const_name import suffix_p_10, suffix_dcs_10, suffix_imp_20, suffix_dcs_20, suffix_p_20, \
    suffix_imp_10, suffix_p_01, suffix_dcs_01


def get_description_row(df):
    """
    获取pandas的dataframe中表示测点名称的行，一般测点名称为Description

    :param df:
    :return:
    """
    header = min(len(df), 4)
    for i in range(header):
        for j in range(len(df.iloc[i])):
            if (is_contain_chinese(str(df.iloc[i, j])) and "时间" not in str(df.iloc[i, j])) \
                    or " " in str(df.iloc[i, j]):
                return i


def get_kks_row(df):
    """
    获取pandas的dataframe中表示kks码的行

    :param df: dataframe数据
    :return:
    """
    possible_row = [0, 1, 2, 3]
    header = min(len(df), len(possible_row))
    for i in range(header):
        for j in range(len(df.iloc[i])):
            value = str(df.iloc[i, j])
            if value == 'nan' or value == '':
                continue
            if is_number(value):  # kks码不可能是纯数字，因此如果是纯数值，则说明该行不是kks码
                possible_row.remove(i)
                break  # 进行下一行
            elif is_contain_chinese(value) and not ("时间" in str(df.iloc[i, j])):  # kks码不可能包含中文汉字，因此包含中文，则说明该行不是kks码
                possible_row.remove(i)
                break  # 进行下一行

    if len(possible_row) == 1:
        return possible_row[0]
    elif len(possible_row) == 0:
        return None
    logger.warning("未能确定KKS码所在的行")
    return None


def power_file_pre_deal(file):
    """
    功率原始文件预处理：
    1.删除功率文件的表头行，只保留数据行
    2.合并功率表文件中date和time列

    :param file:
    :return:
    """
    try:
        data = read_csv_ex(file, sep="\t", header=None)
        start_line = 0
        for i, line in enumerate(data.values):
            line = line[0].strip()
            if line.startswith("Store No"):
                start_line = i
                break
        lines = [line[0].replace('"', '') for line in data.iloc[start_line:, :].values]
        outfile1 = os.path.join(os.path.dirname(file),
                                os.path.splitext(os.path.basename(file))[0] + f"{suffix_p_01}.csv")
        writeLines(outfile1, lines)
        data = read_csv_ex(outfile1)

        if data.columns[1] == "Date" and data.columns[2] == "Time":
            data["Date"] = data["Date"] + " " + data["Time"]
            data.rename(columns={"Date": "DateTime"}, inplace=True)
            data = data.drop(columns="Time")
            data.to_csv(outfile1, index=None)
        else:
            logger.warning(f"功率文件{file}的第2列和第三列数据不是‘Date’和‘Time’，请检查文件！")
            return None
        return outfile1
    except PermissionError:
        logger.error("无法写入文件，请检查目标文件是否占用！")


def sis_file_pre_deal(file):
    """
    预处理SIS系统导出的文件，将测点名称放置到第一行，删除首行以外的其他非数据行

    该方法会将任何数据文件中首行以外的非数据行删除，例如单位行、kks码行、表号行等删除
    该方法会保留测点名诚行，如果测点名称行不在第一行，该方法会识别测点名称行并将测点名称行移到第一行

    :param file:
    :return:
    """
    data = read_csv_ex(file, sep=",", header=None, index_col=0)
    row_des = get_description_row(data)
    row_kks = get_kks_row(data)
    data.loc["时间"] = data.iloc[row_des]
    data.rename(index={"时间": "DateTime"}, inplace=True)
    # --------------------------- 删除非数据和非测点名称行 -------------------------------------------
    drop_lines = []
    for i in range(1, min(len(data), 10)):
        col1_val = str(data.iloc[i, 0])
        if not is_datetime(col1_val) and not is_number(col1_val):
            drop_lines.append(i)
    data = data.reset_index().drop(drop_lines).set_index(0)  # 删除kks码所在的行
    # --------------------------- 删除非数据和非测点名称行 -------------------------------------------
    out_file = os.path.join(os.path.dirname(file), os.path.basename(file)[:-4] + suffix_dcs_01 + ".csv")
    data.to_csv(out_file, header=None)
    return out_file


def dcs_hollysys_file_pre_deal(file):
    """
    和利时DCS文件预处理，只需要更改时间列的列名（【时间列】->【DateTime】）
    :param file:
    :return:
    """

    def strip(text):
        try:
            return text.strip()
        except AttributeError:
            return text

    def add_prefix(string):
        return f"20{string}"

    outfile = os.path.join(os.path.dirname(file),
                           os.path.splitext(os.path.basename(file))[0] + suffix_dcs_01 + ".csv")
    # ---------- 删除文件中的\t和前后的空格，不删除会导致将数值读取为文本 --------------------
    data = read_csv_ex(file, low_memory=False, header=None)
    data = data.applymap(strip)  # 对data的每一个元素应用strip方法
    data.dropna(axis=1, how="all", inplace=True)  # 先去除空白字符，再丢弃空行，否则空白有可能被认为是有内容的
    data.dropna(axis=0, how="all", inplace=True)
    data.to_csv(outfile, index=False, header=False)
    # ---------- 删除文件中的\t，不删除会导致将数值读取为文本 --------------------
    data = read_csv_ex(outfile, low_memory=False)
    data.rename(columns={"时间段": "DateTime"}, inplace=True)
    data["DateTime"] = data["DateTime"].map(add_prefix)
    try:
        data.to_csv(outfile, index=False)
        return outfile
    except PermissionError:
        logger.error("无法写入文件，请检查目标文件是否占用！")


last_time = None  # 不能删除


def dcs_tpri_file_pre_deal(file):
    """
    处理热工院DCS导出的数据文件，该文件有多个时间列，需要特殊处理

    :param file:
    :return:
    """
    outfile = os.path.join(os.path.dirname(file),
                           os.path.splitext(os.path.basename(file))[0] + suffix_dcs_01 + ".csv")

    global last_time
    temp_ = None

    def change_title(text):
        """
        将DCS文件中的两个标题行合并成一行，使其变成以日期和点描述为标题的数据DataFrame

        :param text:
        :return:
        """
        global temp_  # 不能删除，否则内部函数会认为该变量是内部定义的变量，导致不适用外部的该参数
        if text == np.nan:
            return None
        if type(text) == str:
            text: str = text.strip()
            if "时间" in text:
                temp_ = text[:-2]
                return "DateTime"
            elif text.endswith("值"):
                if temp_ is None:
                    return text[:-1]
                else:
                    return text[:-1] + f"_{temp_}"
            elif "状态" in text:
                return "状态"
        else:
            return "状态"

    def add_date_to_time(text):
        """
        向原始数据的时间列添加日期，需要处理跨天的情况

        :param text:
        :return:
        """
        global last_time
        last_time_date_str = datetime.datetime.strftime(last_time, "%Y-%m-%d")
        current_time_str = f"{last_time_date_str} {text}"
        current_time = datetime.datetime.strptime(current_time_str, "%Y-%m-%d %H:%M:%S")
        if current_time < last_time:  # 说明跨天了，更新日期
            current_time = current_time + datetime.timedelta(days=1)
            last_time = current_time
            current_time_str = datetime.datetime.strftime(current_time, "%Y-%m-%d %H:%M:%S")
        return current_time_str

    data = read_csv_ex(file)
    # ------------------------- 获取数据记录日期 -----------------------------------
    cell = data.columns[0]
    date_list = re.findall("历史趋势开始于(\d{4})年(\d{1,2})月(\d{1,2})日(\d{1,2})时(\d{1,2})分(\d{1,2})秒", cell)
    if len(date_list) > 0:
        year = int(date_list[0][0])
        month = int(date_list[0][1])
        day = int(date_list[0][2])
        hour = int(date_list[0][3])
        minute = int(date_list[0][4])
        second = int(date_list[0][5])
        start_time = datetime.datetime(year, month, day, hour, minute, second)
        last_time = copy.deepcopy(start_time)  # 记录上一条数据的时间
    else:
        logger.debug("找不到工况记录的日期")
        return None
    # ------------------------- 获取数据记录日期 -----------------------------------
    row1: pd.Series = data.iloc[0]
    row1.fillna("", inplace=True)
    row2: pd.Series = data.iloc[1]
    row2.fillna("", inplace=True)
    title_series: pd.Series = row1 + row2
    title_series = title_series.map(change_title)
    title_series[0] = "序号"
    if data.shape[1] <= 2:
        logger.info(f"文件{file}中的数据量为0")
        return None
    data.drop(index=[0, 1], inplace=True)
    data.set_axis(axis=1, labels=title_series, inplace=True)
    # 删除状态列，删除重复列，删除某些人处理的平均行
    data: pd.DataFrame = data.T.drop(index=["状态", "序号"]).dropna(axis=1, how="any").drop_duplicates().T
    data["DateTime"] = data["DateTime"].map(add_date_to_time)
    data.to_csv(outfile, index=False)
    return outfile


def dcs2_file_pre_deal(data: pd.DataFrame, file):
    """
    处理dcs2格式的dataframe

    :param data:
    :return:
    """
    outfile = os.path.join(os.path.dirname(file),
                           os.path.splitext(os.path.basename(file))[0] + suffix_dcs_01 + ".csv")
    # ------------------------- 找到DCS文件中表头描述所在的区域 ------------------------------
    start1 = 0  # kks码和点位名称区域的开始行
    end1 = 0  # kks码和点位名称区域的结束行
    start2 = 0  # 数据区域的开始行
    during_point_description_section = False
    for i, line in enumerate(data.values):
        cell00 = str(line[0]).replace('"', '').strip()  # 将ndarray转换为字符串

        if during_point_description_section:  # 需要在空行判断之前进行
            try:
                _ = int(cell00)
                continue
            except ValueError:
                end1 = i
                during_point_description_section = False
                continue
        if cell00 == "" or cell00 == "nan":  # 元素为空
            continue

        if cell00.strip() == "1" and end1 == 0:
            start1 = i - 1
            during_point_description_section = True
        else:
            cell0 = cell00.strip().split(" ")[0]
            try:  # 找到第一个首元素可以转为日期的行
                _ = pd.Timestamp(str(cell0))
                start2 = i
                break
            except ValueError:
                continue
    if end1 == 0 or start2 == 0:
        return None
    # ---------------------- 找到DCS文件中表头描述所在的区域 ------------------------------
    # ---------------------- 将data分割为表头区域的DataFrame和数据区域的DataFrame -------------------------
    title_df = data[start1:end1]
    data_df = data[start2:].copy()
    data_df.dropna(axis=1, how="all", inplace=True)
    # ---------------------- 将data分割为表头区域的DataFrame和数据区域的DataFrame -------------------------
    title_list = list(set_dataframe_header(title_df)["Description"])
    title_list.insert(0, "DateTime")
    data_df.set_axis(title_list, axis=1, inplace=True)
    data_df.to_csv(outfile, sep=",", index=None)
    return outfile


def dcs_file_pre_deal(file):
    """
    dcs原始文件预处理：
    返回预处理得到的csv类型的文件的文件名

    :param file:
    :return:
    """
    try:
        outfile = os.path.join(os.path.dirname(file),
                               os.path.splitext(os.path.basename(file))[0] + suffix_dcs_01 + ".csv")
        ext_ = os.path.splitext(file)[-1].lower()
        sep = ","
        if ext_ == ".txt":
            sep = " "
        elif ext_ == ".csv":
            sep = ","
        data = read_csv_ex(file, sep=sep, header=None)  # sep不能取值"/t"，否则读取dcs1.csv格式时报错，可能与to_csv方法行为改变有关
        data.dropna(axis=1, how="all", inplace=True)
        data.to_csv(outfile, sep=",", index=False, header=False)  # 写出当前data到新文件，可以删除源文件中的空行
        start1 = 0  # kks码和点位名称区域的开始行
        end1 = 0  # kks码和点位名称区域的结束行
        start2 = 0  # 数据区域的开始行
        for i, line in enumerate(data.values):
            line1 = str(line[0]).replace('"', '')
            line2 = str(line[1]).replace('"', '')
            if line1 == "nan" and line2.startswith("Graph Visible"):
                start1 = i
            elif line1.strip().startswith("Date Time"):
                end1 = i - 1
            else:
                cell0 = line[0]
                if line1 == "nan":
                    continue
                try:  # 找到第一个首元素可以转为日期的行
                    _ = pd.Timestamp(str(cell0))
                    start2 = i
                    break
                except ValueError:
                    continue

        data_title_field = read_csv_ex(outfile, sep=",", skiprows=range(start1), nrows=end1 - start1)
        point_name = list(data_title_field["Description"])  # dcs测点名
        point_name.insert(0, "DateTime")
        data_value_field = read_csv_ex(outfile, sep=",", skiprows=range(start2 - 1))
        data_value_field.columns = point_name
        data_value_field.sort_values(by="DateTime", inplace=True)  # 写出数据前对时间进行排序
        data_value_field.to_csv(outfile, sep=",", index=False)
        return outfile
    except PermissionError:
        logger.error("无法写入文件，请检查目标文件是否占用！")


def dcs_sciyon_file_pre_deal(file):
    """
    预处理南京科远DCS系统导出的数据文件： *.csv
    :param file:
    :return:
    """
    outfile = os.path.join(os.path.dirname(file),
                           os.path.splitext(os.path.basename(file))[0] + suffix_dcs_01 + ".csv")
    data: pd.DataFrame = read_csv_ex(file)  # 跳过前三行，前三行是文件信息描述，不是数据区域
    start_row = 2
    for i in range(data.shape[0]):
        if data.iloc[i][0].startswith('$TagDesc'):
            start_row = i + 1  # 第一行已经被识别为标题，因此开始行=i+1
            break
    data = read_csv_ex(file, skiprows=start_row)
    data.drop(index=[0], inplace=True)  # 删除第一行，该行描述了标签的格式，也不是数据区域
    data.rename(columns={"$TagDesc": "DateTime"}, inplace=True)  # 重命名时间列
    data['DateTime'] = data['DateTime'].apply(lambda x: (x.replace("@", "")))  # 删除时间之前的@符号
    data = data.applymap(lambda x: (x.replace("(GOOD)", "")))  # 删除数据后的质量标签
    data = data.applymap(lambda x: (x.replace("(BAD)", "")))
    try:
        data.to_csv(outfile, sep=",", index=False)
    except PermissionError:
        logger.error("无法写入文件，请检查目标文件是否占用！")
    return outfile


def deal_dcs_pre_file(file, time_dict):
    """
    处理dcs预处理得到的csv文件，该文件是由该软件生成的中间文件，所有不同的dcs系统都将转为统一的格式，格式示例如下：
    DateTime,左侧主汽压力1,左侧主汽压力2
    2021-12-17 09:00:00,12.11,11.99
    2021-12-17 09:00:12,12.11,11.29

    :param file:
    :param time_dict: 工况确认单里的各工况时间，是一个字典，格式为
    {condition_name: {"start_time": datetime_str, "end_time": datetime_str}}
    :return:
    """
    try:
        if file is None:
            logger.warning("dcs数据处理失败！")
            return None
        else:
            data = read_csv_ex(file, index_col=0)
            conditions = []
            out_files = []
            for condition_name, start_end_time_dict in time_dict.items():
                start_time = start_end_time_dict.get("start_time")
                end_time = start_end_time_dict.get("end_time")
                data1 = cut_time_period_of_dataframe(data, start_time, end_time)
                if len(data1) > 0:
                    out_file2 = os.path.join(os.path.dirname(file), f"temp_{condition_name}{suffix_dcs_10}.csv")
                    out_files.append(out_file2)
                    data1 = data1.sort_values(by="DateTime")  # 根据DateTime对数据排序
                    data1.to_csv(out_file2)
                    conditions.append(condition_name)
            return "dcs_slice", out_files, conditions
    except PermissionError:
        logger.error("文件写入失败，请检查目标文件是否被占用！")


def unified_unit(df: pd.DataFrame, unit_series):
    """
    统一df中各个测点的单位，统一后的单位为 压力-kPa，温度-℃，流量差压-kPa

    :param df:
    :param unit_series:
    :return:
    """
    for col, unit in enumerate(unit_series):
        if str(unit).lower().strip() == "mpa":
            df.iloc[:, col] = df.iloc[:, col] * 1000
    return df


def is_unit_series(series: pd.Series):
    """
    判断给定的Series是不是表示单位的Series

    :param series:
    :return:
    """
    for index, value in series.items():
        value = str(value).strip()
        if value == "" or value == "nan":
            continue
        if value.lower() in ["kpa", "℃", "mm", "m", "mpa", "t/h", "kg/s", "v", "a", "kw"]:
            return True
    return False


def cutting_period_of_dataframe(df, time_dict):
    """
    依次查询time_dict中的时间段是否在df数据集中，如果存在返回对应时间段的子数据集，则记录该数据集在time_dict中的key和其对应的子数据集，如果
    所有的time_dict都不存在，则返回None

    :param df:
    :param time_dict:
    :return: {"工况名": pd.DataFrame, ...}，如果未找到任何工况数据，返回None
    """

    name_data_dict = {}
    for condition_name, start_end_time_dict in time_dict.items():
        start_time = start_end_time_dict.get("start_time")
        end_time = start_end_time_dict.get("end_time")
        data1 = cut_time_period_of_dataframe(df, start_time, end_time)
        if len(data1) > 0:
            name_data_dict.update({condition_name: data1})
    return name_data_dict


def deal_kp_hollysys(data):
    point_description = {}
    for sheet_name, content in data.items():
        # 判断content是否包含PN和DS两列，分别代表KKS码和点描述
        content: pd.DataFrame = set_dataframe_header(content)  # 将第一行转为Header，这一行是英文标题
        content.reset_index(inplace=True)  # 将Index转为列
        if "PN" in content.columns and "DS" in content.columns:
            pass
        else:
            continue  # 略过后续操作处理下一个表单
        content.drop(content.index[0], inplace=True)  # 删除第二行，第二行是中文标题

        for pn, ds in zip(content["PN"], content["DS"]):
            point_description[pn] = ds
    return point_description


def pre_deal_and_cutting_period(file, time_dict, bound, config: dict):
    """
    预处理文件，如果文件中包含“时间-数据”条目，则剪切到对应工况的时间段，返回文件类型及剪切后的文件
    从file中裁取指定时间段的试验数据，并剔除数据列中的错误数据

    :param time_dict:
    :param file:
    :return: 返回第一个参数为数据文件类型，可能取值"imp_slice"/"power_slice"/"dcs_slice"，第二个参数为生成的预处理文件列表，第三个参数为
    预处理的工况名称列表，如果出错，则返回None
    """
    if os.path.splitext(os.path.basename(file))[0].endswith("修正"):  # 只处理原始文件，不处理修正数据
        return None
    ext_ = os.path.splitext(file)[-1].lower()
    type_ = get_detailed_type_of_data_file(file)
    if ext_ == ".xls":  # 老版本的excel文件，另存为新版本的再处理
        file = save_as_xlsx(file, ext="csv", engine="WPS")
        pre_deal_and_cutting_period(file, time_dict, bound)
    if ext_ == ".xlsx":
        # =========================== 读入现有的采集数据，构造本步骤的输出文件名 ======================================
        data = pd.read_excel(file, header=None, sheet_name=None)
        conditions = []
        out_file_list = []
        out_file_dir = os.path.join(os.path.dirname(file), "imp")
        os.makedirs(out_file_dir, exist_ok=True)
        # =========================== 读入现有的采集数据，构造本步骤的输出文件名 ======================================
        if type_ == "imp":
            # =========================== 有线采集仪数据处理 ======================================
            for sheet_name, df in data.items():
                if df.shape != (0, 0):
                    name_series = df.iloc[1, :].str.strip()
                    tag_series = df.iloc[2, :].str.strip()
                    tag_series.replace(to_replace=np.nan, value="", inplace=True)
                    unit_series = df.iloc[3, :].str.strip()
                    unit_series.replace(to_replace=np.nan, value="", inplace=True)
                    name_series[1:] = name_series[1:] + "_" + unit_series[1:] + "_" + tag_series[1:]
                    data1 = df.set_axis(labels=name_series, axis='columns')
                    data_no_title = data1.drop(index=[0, 1, 2, 3])
                    data_no_title.rename(columns={"名称": "DateTime"}, inplace=True)
                    logger.info("sheet: " + sheet_name + "处理中...")
                    data_no_title = unified_unit(data_no_title, unit_series)
                    cut_result = cutting_period_of_dataframe(data_no_title, time_dict)
                    if cut_result is not None:
                        imp_tested = config.get("imp_or_wsn_tested")
                        for condition_name, current_data in cut_result.items():
                            out_file = os.path.join(out_file_dir, f"{condition_name}{suffix_imp_10}.csv")
                            current_data = current_data.sort_values(by="DateTime")  # 写出数据前对时间排序
                            # 是否有其他原始数据文件中存在当前工况数据
                            exist_in_whole = imp_tested is not None and condition_name in imp_tested
                            if exist_in_whole:  # 有则合并当前工况数据和其他原始数据文件中的数据
                                _exist = read_csv_ex(out_file)
                                current_data = merge_two_dataframes(current_data, _exist)[0]
                            current_data.to_csv(out_file, index=None)
                            if out_file not in out_file_list and not exist_in_whole:  # 如果每输出过，则输出
                                out_file_list.append(out_file)
                            if condition_name not in conditions and not exist_in_whole:
                                conditions.append(condition_name)
                            else:
                                logger.warning("imp采集数据单个工况对应的时间段存在多个文件中")
            return "imp_slice", out_file_list, conditions
            # =========================== 有线采集仪数据处理 ======================================
        elif type_ == "wsn" or type_ == "dcs_pi":
            # =========================== 无线采集仪数据处理 ======================================
            for sheet_name, df in data.items():
                if df.shape != (0, 0):
                    name_series = df.iloc[0].str.strip()
                    unit_series: pd.Series = df.iloc[1].str.strip()
                    if type_ == "dcs_pi":
                        if not is_unit_series(unit_series):
                            unit_series = df.iloc[2].apply(str).str.strip()
                        if not is_unit_series(unit_series):
                            logger.warning("dcs_pi数据未找到单位行，默认使用第三行作为单位行")
                    else:
                        # 这里使用series.str必须先经过series.apply(str)转换，否则，当series全是数值类型时会报错如下：
                        # {AttributeError}Can only use .str accessor with string values!
                        tag_series: pd.Series = df.iloc[2].apply(str).str.strip()
                        tag_series.replace(to_replace=np.nan, value="", inplace=True)
                        unit_series[1:] = unit_series[1:] + "_" + tag_series[1:]
                    unit_series.replace(to_replace=np.nan, value="", inplace=True)
                    name_series[1:] = name_series[1:] + "_" + unit_series[1:]
                    data_no_title: pd.DataFrame = df.drop(index=[0, 1, 2])
                    data_no_title = data_no_title.set_axis(labels=name_series, axis='columns')
                    data_no_title.replace(to_replace="INVALID", value=np.nan, inplace=True)
                    if type_ == "wsn":  # wsn需要单独处理时间列
                        year_str = ""
                        for condition, start_end_time in time_dict.items():
                            start_time_str = start_end_time.get("start_time")
                            if year_str != "":
                                if start_time_str[0:4] != year_str:
                                    logger.warning("工况确认单中数据跨年了，暂时不支持跨年数据处理")
                            year_str = start_time_str[0:4]
                        if year_str == '':
                            logger.error("wsn年份查询失败，可能是工况记录单未找到或工况记录单中条目数为0或数据目录错误")
                        data_no_title["时间"] = year_str + "." + data_no_title["时间"]
                        data_no_title["时间"] = pd.to_datetime(data_no_title['时间'], format="%Y.%m.%d %H:%M:%S")
                        data_no_title.rename(columns={"时间": "DateTime"}, inplace=True)
                        data_no_title = unified_unit(data_no_title, unit_series)  # 统一数据集中测点数据的单位
                    else:  # pi数据库导出的dcs数据
                        time_col = get_datetime_col_of_dataframe(data_no_title)
                        data_no_title.rename(columns={time_col: "DateTime"}, inplace=True)
                    name_data_dict = cutting_period_of_dataframe(data_no_title, time_dict)  # 裁剪对应工况时间段
                    if len(name_data_dict) > 0:
                        conditions.extend(name_data_dict)
                        for condition, c_df in name_data_dict.items():
                            condition: str = condition.strip()
                            if type_ == "wsn":
                                temp_suffix = suffix_imp_10
                            else:
                                temp_suffix = suffix_dcs_10
                            c_out_file = os.path.join(out_file_dir,
                                                      "temp_" + condition + f"{temp_suffix}.csv")
                            c_df = c_df.sort_values(by="DateTime")  # 写出数据前对时间排序
                            c_df.to_csv(c_out_file, index=None)
                            out_file_list.append(c_out_file)
            if type_ == "wsn":
                return "wsn_slice", out_file_list, conditions
            else:
                return "dcs_slice", out_file_list, conditions
            # =========================== 无线采集仪数据处理 ======================================
        elif type_ == "dcs2":  # .xls格式的DCS数据文件会在预处理时转换为.xlsx格式，然后会返回dcs2类型
            for sheet_name, df in data.items():
                if df.shape != (0, 0):
                    df.dropna(axis=0, how="all")
                    df.dropna(axis=1, how="all")
                    outfile1 = dcs2_file_pre_deal(df, file)  # 将原始dcs文件转换为统一的中间格式
                    if outfile1 is None:
                        logger.info(f"DCS文件不包含任何可识别数据，文件路径为：{file}")
                        return None
                    return deal_dcs_pre_file(outfile1, time_dict)
        elif type_ == "kp_hollysys":
            # 和利时的点表文件
            point_description = deal_kp_hollysys(data)
            return "kp_hollysys", point_description
    elif ext_ == ".csv":  # 功率数据一般为CSV
        if type_ == "power":
            outfile1 = power_file_pre_deal(file)
            if outfile1 is None:
                logger.warning("功率数据处理失败！")
                return None
            else:
                data = read_csv_ex(outfile1, index_col=0)
                name_data_dict = cutting_period_of_dataframe(data, time_dict)
                if name_data_dict is None:
                    return None
                out_files = []
                folder = os.path.join(os.path.dirname(file), "power")
                os.makedirs(folder, exist_ok=True)
                conditions = []
                for name, data in name_data_dict.items():
                    outfile1 = os.path.join(folder, f"{name}{suffix_p_10}.csv")
                    data = data.sort_values(by="DateTime")  # 写出数据前对时间排序
                    data.to_csv(outfile1)
                    out_files.append(outfile1)
                    conditions.append(name)
                return "power_slice", out_files, conditions
        elif type_ == "dcs1":
            outfile1 = dcs_file_pre_deal(file)  # 将原始dcs文件转换为统一的中间格式
            return deal_dcs_pre_file(outfile1, time_dict)
        elif type_ == "dcs2":
            df = read_csv_ex(file)
            outfile1 = dcs2_file_pre_deal(df, file)  # 将原始dcs文件转换为统一的中间格式
            if outfile1 is None:
                logger.info(f"DCS文件不包含任何可识别数据，文件路径为：{file}")
                return None
            return deal_dcs_pre_file(outfile1, time_dict)
        elif type_ == "dcs_hollysys":
            # ----------------------------- 和利时的DCS数据测点标题是KKS码，需要电表进一步处理为点描述 --------------------------
            outfile1 = dcs_hollysys_file_pre_deal(file)  # 将原始dcs文件转换为统一的中间格式
            return deal_dcs_pre_file(outfile1, time_dict)
        elif type_ == "dcs_tpri":
            outfile1 = dcs_tpri_file_pre_deal(file)
            return deal_dcs_pre_file(outfile1, time_dict)
        elif type_ == "dcs_sciyon":
            outfile1 = dcs_sciyon_file_pre_deal(file)
            return deal_dcs_pre_file(outfile1, time_dict)
        elif type_ == "sis":
            outfile1 = sis_file_pre_deal(file)
            if outfile1 is None:
                logger.warning("DCS数据处理失败！（SIS）")
                return None
            else:
                data = read_csv_ex(outfile1, index_col=0)
                name_data_dict = cutting_period_of_dataframe(data, time_dict)
                if name_data_dict is None:
                    return None
                out_files = []
                folder = os.path.join(os.path.dirname(file), "dcs")
                os.makedirs(folder, exist_ok=True)
                conditions = []
                for name, data in name_data_dict.items():
                    outfile1 = os.path.join(folder, f"{name}{suffix_dcs_01}.csv")
                    data = data.sort_values(by="DateTime")
                    data.to_csv(outfile1)
                    out_files.append(outfile1)
                    conditions.append(name)
                return "dcs_slice", out_files, conditions
        elif type_ == "unknown":
            # 未知格式的文件，尝试按时间分割文件
            logger.info(f"未识别的文件类型，{file}")
            data = read_csv_ex(file)
            time_col_name = get_datetime_col_of_dataframe(data)
            if time_col_name is None:
                return
            data.rename(columns={time_col_name: "DateTime"}, inplace=True)
            out_file = os.path.join(os.path.dirname(file),
                                    os.path.basename(file)[:-4] + "_unk预处理_修正.csv")
            title_rows = []
            for i in range(10):  # 判断前10行是数据行还是标题行，如果是标题信息行，则合并各行
                cell0 = data["DateTime"].iloc[i]
                try:  # 找到第一个首元素可以转为日期的行
                    if str(cell0).strip() == "":
                        continue
                    _ = pd.Timestamp(str(cell0))
                    break
                except ValueError:
                    title_rows.append(i)
            if len(title_rows) > 0:
                title = data.columns
                for i in title_rows:
                    title = title + "_" + data.iloc[i]
                data.set_axis(title, axis=1, inplace=True)

            time_col_name = get_datetime_col_of_dataframe(data)
            data.rename(columns={time_col_name: "DateTime"}, inplace=True)
            data.to_csv(out_file, index=None)
            name_data_dict = cutting_period_of_dataframe(data, time_dict)
            if name_data_dict is None:
                return None
            out_files = []
            folder = os.path.join(os.path.dirname(out_file), "UNK")
            os.makedirs(folder, exist_ok=True)
            conditions = []
            discriminate_unk_file = config.get("未知类型文件区分文件名")  # 在点名中是否添加文件名进行区分

            for name, data in name_data_dict.items():
                outfile1 = os.path.join(folder, f"{name}_unk预处理_修正.csv")
                data.dropna(axis=1, how="all", inplace=True)
                data = data.sort_values(by="DateTime")
                if discriminate_unk_file:
                    # 将文件名添加到列明上，因为位置类型文件的文件名可能是数据点的名称
                    name_map = {item: f"{os.path.basename(file)[:-4]}-{item}" for item in list(data.columns) if
                                item != "DateTime"}
                    data.rename(columns=name_map, inplace=True)
                data.to_csv(outfile1, index=None)
                out_files.append(outfile1)
                conditions.append(name)
            return "unk_slice", out_files, conditions
    elif ext_ == ".txt":
        if type_ == "dcs1":
            outfile1 = dcs_file_pre_deal(file)  # 将原始dcs文件转换为统一的中间格式
            return deal_dcs_pre_file(outfile1, time_dict)
        elif type_ == "dcs2":
            # 难以使用dcs2_file_pre_deal，这里单独处理
            outfile1 = os.path.join(os.path.dirname(file),
                                    os.path.splitext(os.path.basename(file))[0] + suffix_dcs_01 + ".csv")
            lines = fileOperate.read_lines(file, dropna=True)  # 删除文件中的空行，以防pandas出现莫名其妙的问题
            writeLines(outfile1, lines)
            start1 = 0
            end1 = 0
            start2 = 0
            fix_end1 = False  # 是否允许end1变化
            for i in range(len(lines)):
                line = lines[i].strip()
                if not line:  # 跳过空行
                    continue
                if line.startswith("G"):
                    start1 = i
                    end1 = 1
                elif line.startswith(str(end1)) and not fix_end1:
                    end1 = end1 + 1
                else:
                    if line.startswith("Date Time"):
                        fix_end1 = True
                    try:  # 找到第一个首元素可以转为日期的行
                        cell0 = line.split("\t")[0]
                        if cell0:
                            _ = pd.Timestamp(cell0)
                            start2 = i
                            break
                    except ValueError:
                        continue

            data_title = read_csv_ex(file, sep="\t", skiprows=start1, nrows=(end1 - 1))
            data_value = read_csv_ex(file, sep="\t", skiprows=start2 - 1)
            data_value = data_value.applymap(lambda x: np.nan if str(x).strip() == "" else x)
            data_value.dropna(axis=1, how="all", inplace=True)  # 剔除空值
            name = ""
            for name in data_title.columns:  # 列标题中有空白字符，直接用"Description"取不到描述列
                if str(name).strip().startswith("Description"):
                    break
            if name == "":
                logger.warning(f"未找到{file}点名中的描述列，请检查")
                return None
            point_name = list(data_title[name])
            point_name = [p.strip() for p in point_name]  # 删除点名中的空白字符
            point_name.insert(0, "DateTime")
            data_value.set_axis(point_name, axis=1, inplace=True)
            data_value.to_csv(outfile1, index=False)
            return deal_dcs_pre_file(outfile1, time_dict)
