import datetime
import json
import os
import sys

import docx
import numpy as np
import pandas as pd
import win32com.client
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QCheckBox, QApplication, QPushButton, QFileDialog, QProgressBar, QDialog, \
    QVBoxLayout, QLabel, QButtonGroup, QHBoxLayout, QRadioButton, QDialogButtonBox, QMessageBox
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSignal

from yangke.base import get_temp_para, save_temp_para, yield_all_file, \
    start_threads, get_datetime_col_of_dataframe
from yangke.common.config import logger
from yangke.performance.basic_para import pressure_absolute, pressure_relative  # 不能删除，本文件有隐含式引用
from yangke.common.qt import YkWindow, YkDataTableWidget, set_menu_bar
from yangke.core import strInList
from yangke.common.fileOperate import read_csv_ex, writeAsPickle, readFromPickle
from yangke.base import merge_two_dataframes, save_as_xlsx
import time

from yangke.performance.dp.const_name import suffix_p_10, suffix_dcs_10, suffix_imp_20, suffix_dcs_20, suffix_p_20, \
    suffix_imp_10
from yangke.performance.dp.cutting_period import pre_deal_and_cutting_period

warning_info = {"imp": {}, "p": {}, "dcs": {}}  # 记录所有数据处理的警告信息，最后写入汇总文件


def func1():
    xl = win32com.client.Dispatch('Excel.Application')
    xl.Visible = True
    xla_file = r"D:\Users\2020\性能试验\陈会勇\数据处理\ReadTestData（最新）.xla"
    xl.Workbooks.Open(xla_file)

    # data_file = r"D:\Users\2020\性能试验\陈会勇\数据处理\试验数据\IMP数据\3VWO-背压16.8.dat"
    # new_data_file = os.path.join(os.path.dirname(data_file), os.path.basename(data_file).split(".")[0] + ".xlsx"
    # xl.Workbooks.Open(data_file)
    # xl.Application.Save()
    # xl.Application.Quit()
    # print("end")


def add_atmosphere(data_series: pd.Series):
    """
    对数据进行大气压修正，将修正的测点的单位改为MPa
    :param data_series: IMP或WSN试验采集仪采集的试验测点，data_series.index是试验测点名称，data_series.values是试验测点数值
    :return:
    """

    def get_p_env_idx(test_point_list: list) -> str:
        """
        找出参数列表中大气压对应的索引

        :param test_point_list:
        :return: 返回大气压对应的变量的名称，是一个str
        """
        for idx in test_point_list:
            name_str = idx
            if "大气压" in name_str:
                return idx
        logger.error("未找到大气压数据")
        raise ValueError("未找到大气压数据")

    p_env_idx = get_p_env_idx(data_series.index)
    p_env = data_series[p_env_idx]
    for name, value in data_series.items():
        name = str(name)
        if "pa" not in name.lower():  # 说明不是压力数据
            continue
        if "流量" in name or "差压" in name:
            continue
        # 有限依据表号判断

        if strInList(name, pressure_relative, revert=True):
            data_series[name] = (value + p_env) / 1000
            data_series.rename(index={name: name.replace("kPa", "MPa")}, inplace=True)  # 更改单位
        elif strInList(name, pressure_absolute, revert=True):
            continue
        else:
            logger.warning(f"无法判断压力数据是绝压还是表压，测点名称为：{name}")
    return data_series


def get_test_time(folder):
    """
    获取各工况的数据采集开始和结束时间

    :param folder:
    :return:
    """
    condition_time = {}
    name_idx = -1
    date_idx = -1
    time_idx = -1
    file = None
    for file in yield_all_file(folder, [".docx"]):
        if not strInList(os.path.splitext(os.path.basename(file))[0],
                         ["工况记录单", "工况确认时间", "试验工况时间", "工况确认单"],
                         revert=True):
            continue
        logger.debug("读取工况记录单数据...")
        doc = docx.Document(file)
        for table in doc.tables:
            row = table.rows[0]  # 根据表格第一行标题确定每列的数据是什么
            for col_idx, cell in enumerate(row.cells):
                if "名称" in cell.text.strip() or cell.text.strip() == "工况" or cell.text.strip() == "试验工况":
                    name_idx = col_idx
                elif cell.text.strip() == "日期":
                    date_idx = col_idx
                elif cell.text.strip() == "时间" or cell.text.strip() == "记录数据时间":
                    time_idx = col_idx
            if name_idx == -1:  # 说明按上述标准没有找到工况名称列，进一步检索表头"工况"
                for col_idx, cell in enumerate(row.cells):
                    if "工况" in cell.text.strip() and col_idx != date_idx and col_idx != time_idx:
                        name_idx = col_idx
                        break

            for row_idx, row in enumerate(table.rows[1:]):
                try:
                    cells = row.cells
                    condition_name = cells[name_idx].text.strip()
                    if condition_name == "":
                        continue
                    date_str = cells[date_idx].text.strip()
                    time_str = cells[time_idx].text.strip().replace("：", ":")
                    time_str = time_str.replace(" ", "")
                    if time_str == "":
                        logger.error(f"工况记录单{file}中存在数据不全的工况->工况名为：{condition_name}")
                        sys.exit(0)
                    date_str = str(pd.Timestamp(date_str)).split(" ")[0]  # 使用pd.Timestamp接受多种格式的字符串，返回%Y-%m-%d
                    start_time_str, end_time_str = time_str.split("-")
                    start_time = time.strptime(start_time_str, "%H:%M")
                    end_time = time.strptime(end_time_str, "%H:%M")
                    start_datetime_str = date_str + " " + time.strftime("%H:%M", start_time)
                    if end_time < start_time:  # 一般单工况持续时间小于3小时，如果结束时间比开始时间小，说明跨了一天，日期需要加1
                        date = datetime.datetime.strptime(date_str, "%Y-%m-%d") \
                               + datetime.timedelta(days=1)
                        end_datetime_str = date.strftime("%Y-%m-%d") + " " + time.strftime("%H:%M", end_time)
                    else:
                        end_datetime_str = date_str + " " + time.strftime("%H:%M", end_time)
                    condition_time.update(
                        {condition_name: {"start_time": start_datetime_str, "end_time": end_datetime_str}})
                    logger.debug(f"{condition_name} -> {json.dumps(condition_time.get(condition_name))}")
                except:  #
                    break  # 处理表格中某一行出错时，退出行遍历
            break  # 只便利word中的第一个table，第一个table出力完成后推出tables便利
        break  # 只处理检索到的第一个word文档，处理后则退出文件遍历
    return condition_time, file


def delete_error_data(df, bound=0.3, method="relative_error"):
    """
    删除数据集中偏差过大的数据，df数据的columns是变量名，index是数字索引或时间索引，values全是变量值

    :param df:
    :param bound:
    :param method: 剔除错误数据的方法，relative_error—根据相对误差剔除跳数，trend—根据数据趋势剔除跳数
    :return:
    """
    time_col = get_datetime_col_of_dataframe(df)
    if time_col != -1:
        data_no_time = df.set_index("DateTime")
    else:
        data_no_time = time_col
    name_series = data_no_time.columns
    mean_v = data_no_time.mean()
    min_v = data_no_time.min()
    max_v = data_no_time.max()
    criteria = (max_v - min_v) / mean_v > bound  # 选出最大值最小值差超过平均50%的Series
    data_no_time = data_no_time.T
    need_modified_series = data_no_time[criteria]
    need_modified_series_idx = need_modified_series.index
    for idx in need_modified_series_idx:
        current_series: pd.Series = need_modified_series.loc[idx, :]
        if "减温水" in idx or "水位" in idx or "液位" in idx:  # 减温水的数据不判断，因为减温水会间歇运行，其数据就是波动的
            # 将修改后的series替换到元数据dataframe中
            continue
        max_s = current_series.max()
        min_s = current_series.min()
        mean_s = current_series.mean()
        idx_deleted = []
        while (max_s - mean_s) / mean_s > bound or (mean_s - min_s) / mean_s > bound:
            # 找出参数行中需要删除的值，并将其置为np.nan，则后续求mean、max、min等参数时会忽略np.nan值
            low_bound, high_bound = mean_s * (1 - bound), mean_s * (1 + bound)
            # noinspection All
            del_idx = current_series[(current_series < low_bound) | (current_series > high_bound)].index
            idx_deleted.extend(list(del_idx))
            current_series[del_idx] = np.nan
            # 再次计算该数据列最大最小值的差别是否超出平均数的bound之外
            max_s = current_series.max()
            min_s = current_series.min()
            mean_s = current_series.mean()

        logger.info(f"剔除的数据索引 第{idx}列， 第{str(idx_deleted)}行")  # 这里提示的相当于原数据的行列
        data_temp = data_no_time.copy()
        data_temp.loc[idx] = current_series  # 将修改后的series替换到元数据dataframe中
        data_no_time = data_temp
    data_no_time = data_no_time.T
    df = data_no_time.reset_index()
    return df


def deal_liquid_level(data: pd.DataFrame, **kwargs):
    """
    处理数据中的液位测点，将测点名改为 ”*水位下降_*"，例如原测点名称为"除氧器水位_mm"，则处理后的测点名成为"除氧器水位下降_mm"，处理后data中
    液位列的所有数据都是下降的数值。

    2021.03.20添加功能：在最终结果中输出水位数据的前{n}个与后{n}个的平均值

    默认inplace=True，且不可更改

    :param data: 测点数据
    :return:
    """
    num = int(kwargs.get("水位计算点数"))
    data.sort_values(by="DateTime", inplace=True)
    for col_name in data.columns:
        if ("水位" in col_name or "液位" in col_name) and ("平均值" not in col_name and "下降值" not in col_name):
            name_new = col_name + "_下降值"
            header_mean = data[col_name].head(num).mean()
            tail_mean = data[col_name].tail(num).mean()
            lvl_drop = header_mean - tail_mean
            if lvl_drop < 0:
                condition = kwargs.get("condition")
                logger.warning(f"{condition}试验期间{col_name}上升，存在不明流量或泄露阀门")
                insert_warning("imp", "水位警告", f"{condition}试验期间，（{col_name}）上升，存在不明流量或泄露阀门")
            data[col_name] = lvl_drop
            data.rename(columns={col_name: name_new}, inplace=True)
            cols_ = data.columns.get_loc(name_new)
            data.insert(cols_, f"{col_name}_前{num}个平均值", header_mean)
            data.insert(cols_ + 1, f"{col_name}_后{num}个平均值", tail_mean)
    return data


def insert_warning(main_type, sub_type, content):
    """
    插入警告信息

    :param main_type: 警告的主类别，只可能是 "imp", "p", "dcs"
    :param sub_type: 警告的子类别，可自由定义
    :param content: 警告信息内容
    :return:
    """
    warn_dict: dict = warning_info.get(main_type)
    if warn_dict is None:
        logger.warning("警告主类别不存在")
        return
    temp = warn_dict.get(sub_type)
    if temp is None:
        warn_dict.update({sub_type: [content]})
    else:
        temp.append(content)
        warn_dict.update({sub_type: temp})


class ConfirmDialog(QDialog):
    """
    用于确认压力测点是表压还是绝压的弹出式对话框
    """

    def __init__(self, parent=None, var_list=None, abs_list=None, rel_list=None):
        super(ConfirmDialog, self).__init__(parent=parent)
        if var_list is None:
            var_list = []
        self.var_list = var_list
        self.abs_list = abs_list
        self.rel_list = rel_list
        self.button_group = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("表压/绝压确认输入窗口")
        self.setGeometry(400, 400, 500, 200)

        v_box = QVBoxLayout()
        for i, var in enumerate(self.var_list):
            tag = str(var).split("_")[2]
            btn_group = QButtonGroup()
            h_box = QHBoxLayout()
            label = QLabel(str(var))
            label.setFixedWidth(300)
            radio_btn_y = QRadioButton('绝压')
            radio_btn_n = QRadioButton('表压')
            if self.abs_list is None and self.rel_list is None:
                if "pg" in tag.lower():
                    radio_btn_n.setChecked(True)
                else:  # PD或PA，差压或绝压
                    radio_btn_y.setChecked(True)
            elif self.abs_list is not None and self.rel_list is not None:
                if var in self.abs_list:
                    radio_btn_y.setChecked(True)
                else:
                    radio_btn_n.setChecked(True)
            btn_group.addButton(radio_btn_y)
            btn_group.addButton(radio_btn_n)
            self.button_group.append(btn_group)
            h_box.addWidget(label)
            h_box.addWidget(radio_btn_y)
            h_box.addWidget(radio_btn_n)
            v_box.addLayout(h_box)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok)

        v_box.addWidget(buttons)
        # noinspection all
        buttons.accepted.connect(self.accept)

        self.setLayout(v_box)

    def get_data(self):  # 定义用户获取数据的方法
        value = []
        for i, var in enumerate(self.var_list):
            value.append(self.button_group[i].checkedButton().text())
        return self.var_list, value


def deal_poor_or_bad_parameters(poor_series: pd.Series):
    """
    处理DCS导出的质量较差的数据。
    DCS数据以B结尾，表示该数据是错误的。
    DCS数据以P结尾，表示该数据质量较差

    :param poor_series:
    :return:
    """
    values = []
    try:
        for value in poor_series:
            value = str(value).replace("B", "")  # DCS数据以B结尾，表示该数据是错误的
            value = value.replace("P", "")  # DCS数据以P结尾，表示该数据质量较差
            if value.strip() == "":
                continue
            values.append(float(value))
        return pd.Series(values).mean()
    except ValueError:
        return None


class MainWindow(YkWindow, QObject):
    yk_signal = pyqtSignal(str, str)

    def __init__(self):
        # noinspection PyTypeChecker
        self.table_widget: YkDataTableWidget = None
        self.data_folder = None
        self.project_file = None
        self.test_time_file = None  # 工况记录单文件
        self.test_time = {}  # 工况记录单中对应的工况时间信息
        self.bound = 0.3
        self.progressBar = QProgressBar()
        self.config = {}  # 配置项
        super(MainWindow, self).__init__()
        self.imp_file = None
        self.dcs_file = None
        self.power_file = None
        self.unknown_file = None  # 无法识别格式的文件中数据的汇总文件
        self.dropped_dcs_cols = []  # dcs数据处理过程总丢弃的非数值型数据列
        self.point_description = None  # 和利时DCS的点表文件，记录了KKS对应的点名，用于更新导出的数据文件中的KKS码
        self.temp_para = None  # 用于子线程和主线程传递数据时使用
        self.project = {}  # 项目文件，保存时保存该参数
        # noinspection all
        self.yk_signal.connect(self.on_message_changed)
        set_menu_bar(self, from_file=os.path.join(os.path.dirname(__file__), "ui/ui_menu_dp.yaml"))  # 设置菜单栏
        self.resize(1200, 800)
        self.center()
        self.setWindowTitle("性能试验数据处理v2.0")

    def gather_imp_or_wsn(self, files: list):
        """
        汇总imp或wsn数据到一个文件中，这里files读入的数据格式是固定的

        :param files:
        :return:
        """
        if len(files) == 0:
            return
        conditions = []
        df = None
        tmp_file = None
        data_list = []
        for file in files:
            data = read_csv_ex(file)
            condition = os.path.basename(file).split("_")[0]
            data = delete_error_data(data, bound=0.3)  # 清洗数据
            kwargs_ = {"condition": condition}
            kwargs_.update(self.config)
            data = deal_liquid_level(data, **kwargs_)
            data_mean = data.mean(numeric_only=True)  # 拿到评测点平均值
            self.temp_para = data_mean
            # noinspection all
            self.yk_signal.emit("eval", "self.ask_for_absolute_or_relative()")
            while self.temp_para is not None:  # 当self.temp_para is None时，表示信号调用的新线程处理完毕
                time.sleep(0.5)
            try:
                data_series = add_atmosphere(data_mean)  # 添加大气压修正，且将单位修正带表压MPa，绝压kPa
            except:  # 有些特殊试验，现场采集数据没有大气压数据，则不进行大气压力修正
                data_series = data_mean
            data_series.name = condition
            data_list.append(data_series)

        df = pd.concat(data_list, axis=1)
        df.dropna(how="all", inplace=True)
        df = self.sort_conditions_add_time_section(df)
        outfile = self.imp_file
        try:
            df.to_excel(outfile, sheet_name="大气压修正汇总")
        except PermissionError:
            logger.error(f"文件被占用，无法写入：{outfile}")
        self.table_widget.display_dataframe(df, row_index=3, col_index=0, digits=4)

        self.table_widget.setColumnWidth(0, 200)  # 第一列是参数名称，将其宽度调宽一点

        return outfile

    def gather_power(self, files: list):
        """
        汇总所有工况的功率数据到一个excel中

        :param files:
        :return:
        """
        if len(files) == 0:
            return
        series = []
        for file in files:
            data = read_csv_ex(file, index_col=0)
            data_no_time = data.iloc[:, 1:].copy()
            mean = data_no_time.mean(axis=0)
            condition_name = os.path.splitext(os.path.basename(file))[0].replace(suffix_p_10, "")
            mean.name = condition_name
            series.append(mean)
        df = pd.concat(series, axis=1)
        # 将df中工况按工况记录单排序
        df = self.sort_conditions_add_time_section(df)
        outfile = self.power_file
        df.to_excel(outfile)
        return outfile

    def gather_dcs(self, files: list):
        if len(files) == 0:
            return
        series = []
        for file in files:
            data = read_csv_ex(file, index_col=0)
            data_no_time = data
            condition = os.path.basename(file).split("_")[0]
            kwargs_ = {"condition": condition}
            kwargs_.update(self.config)
            data_no_time = deal_liquid_level(data_no_time, **kwargs_)
            mean: pd.Series = data_no_time.mean(axis=0)
            if len(mean) < data_no_time.shape[1]:
                # 说明有列在求平均后丢失了
                # 找到丢失的列名
                columns_origin = set(data_no_time.columns)
                columns_mean = set(mean.index)
                columns_dropped = columns_origin - columns_mean
                for column in columns_dropped:
                    temp = deal_poor_or_bad_parameters(data_no_time[column])
                    if temp is not None:
                        mean[column + "_poor"] = temp
            condition_name = os.path.splitext(os.path.basename(file))[0].replace(suffix_dcs_10, "")
            mean.name = condition_name
            mean.sort_index(inplace=True)
            series.append(mean)
        df = pd.concat(series, axis=1)
        if self.point_description is not None:  # 表明存在点表文件，需要根据点表文件更新DCS导数中的KKS码
            def split(text: str):
                return text.split(".")[0]

            df.set_index(df.index.map(split), inplace=True)  # 删除导出的点名后表示值计算方法的后缀，如.AV：平均值等
            df.rename(index=self.point_description, inplace=True)  # 将KKS码替换为点描述

        df = self.sort_conditions_add_time_section(df)
        outfile = self.dcs_file
        df.to_excel(outfile)
        return outfile

    def gather_unknown(self, files: list):
        """
        汇总未识别格式的文件的内容

        :param files:
        :return:
        """
        if len(files) == 0:
            return
        series = []
        for file in files:
            data = read_csv_ex(file, index_col=0)
            # 删掉标题带有序号的列
            filter_cols = [col for col in list(data.columns) if "序号" not in col]
            data_no_time = data[filter_cols].copy()
            condition = os.path.basename(file).split("_")[0]
            kwargs_ = {"condition": condition}
            kwargs_.update(self.config)
            data_no_time = deal_liquid_level(data_no_time, **kwargs_)
            mean = data_no_time.mean(axis=0)
            mean.name = condition
            series.append(mean)
        df = pd.concat(series, axis=1)
        outfile = self.unknown_file
        df = self.sort_conditions_add_time_section(df)
        df.to_excel(outfile)
        return outfile

    def sort_conditions_add_time_section(self, df: pd.DataFrame):
        """
        按照工况记录单对结果文件中的列进行排序，在数据区域前三行添加每个工况的起止时间

        :param df:
        :return:
        """
        missing_cols = set(self.test_time.keys()) - set(df.columns)
        for c in missing_cols:  # 如果数据处理结果中缺少某个工况的数据，则用np.nan代替
            df[c] = np.nan
        df = df[list(self.test_time.keys())]
        start_date = []
        start_time = []
        end_time = []
        for k, v in self.test_time.items():
            start_date.append(v['start_time'][:10])
            start_time.append(v['start_time'][11:])
            end_time.append(v['end_time'][11:])
        df = df.T
        df.insert(0, '结束时间', end_time)
        df.insert(0, '开始时间', start_time)
        df.insert(0, '开始日期', start_date)
        df = df.T
        return df

    def init_ui(self):
        self.data_folder = get_temp_para('directory', get_func=lambda: "c:\\")
        self.project_file = os.path.join(self.data_folder, "project.dat")

        self.config.update(readFromPickle(self.project_file) or {})

        def choose_file(table: YkDataTableWidget):
            folder = QFileDialog.getExistingDirectory(parent=self, caption="选择数据存储目录", directory=self.data_folder)
            if folder != self.data_folder:
                self.data_folder = folder
                save_temp_para("directory", folder)
            table.set_value("目录", folder)

        def deal(table: YkDataTableWidget):
            self.progressBar.setVisible(True)
            self.statusBar().showMessage("处理试验数据...")
            self.progressBar.setValue(0)
            self.config.update({"水位计算点数"     : self.table_widget.get_value("水位计算点数"),
                                "使用表号确定压力类型" : self.table_widget.get_value("使用表号确定压力类型"),
                                "未知类型文件区分文件名": self.table_widget.get_value("未知类型文件区分文件名")})

            def task_func():
                """
                启动新线程运行耗时较长的方法
                不能在该线程中创建或修改父线程的GUI元素，如果需要修改GUI，必须使用yk_signal触发QEvent事件调用父线程的方法
                :return:
                """
                folder = table.get_value("目录")
                self.imp_file = os.path.join(folder, suffix_imp_20 + ".xlsx")
                self.dcs_file = os.path.join(folder, suffix_dcs_20 + ".xlsx")
                self.power_file = os.path.join(folder, suffix_p_20 + ".xlsx")
                self.unknown_file = os.path.join(folder, "unk汇总_修正.xlsx")  # 未识别格式的文件的统计数据
                self.test_time, self.test_time_file = get_test_time(folder)  # 查询工况记录单
                logger.debug(f"工况记录单文件为：{self.test_time_file}")
                number_con = len(self.test_time.keys())
                logger.info(f"工况记录单中查寻到的工况共{number_con}个！")
                logger.info(str(list(self.test_time.keys())))
                dcs_tested = []
                dcs_individual_file = []  # dcs预处理后的单个储存文件
                imp_or_wsn_tested = []
                imp_individual_file = []  # imp数据预处理后的单个储存文件列表
                power_tested = []
                power_individual_file = []  # 功率数据预处理后的单个储存文件列表
                unknown_tested = []
                unknown_individual_file = []
                step = 0
                for file in yield_all_file(folder, [".csv", ".xlsx", ".dat", ".docx", ".txt", ".xls"]):
                    step = step + 1 if step < 100 else 0
                    # self.progressBar.setValue(step)
                    # noinspection all
                    self.yk_signal.emit("eval", "self.progressBar.setValue(" + str(step) + ")")
                    if os.path.splitext(os.path.basename(file))[0].endswith("修正") or "ignore" in os.path.abspath(
                            file) or "忽略该文件" in os.path.abspath(file):
                        logger.info(f"忽略文件{file}")
                        continue
                    logger.debug(f"处理文件 {file}...")
                    if os.path.splitext(file)[1] == ".xls":
                        # 将xls格式文件另存为csv文件，csv的兼容性最好，然后进行进一步的处理
                        file = save_as_xlsx(file, engine="WPS", ext="xlsx")
                    # 预处理文件，如果文件中包含“时间-数据”条目，则剪切到对应工况的时间段，返回文件类型及剪切后的文件
                    cutting_result = pre_deal_and_cutting_period(file, self.test_time, self.bound, self.config)
                    if cutting_result:
                        if isinstance(cutting_result, tuple) and cutting_result[0] == "power_slice":
                            power_tested.extend(cutting_result[2])
                            power_individual_file.extend(cutting_result[1])
                        elif isinstance(cutting_result, tuple) and cutting_result[0] == "imp_slice":
                            imp_or_wsn_tested.extend(cutting_result[2])
                            imp_individual_file.extend(cutting_result[1])
                            self.config.update({"imp_or_wsn_tested": imp_or_wsn_tested})
                        elif isinstance(cutting_result, tuple) and cutting_result[0] == "wsn_slice":
                            for condition in cutting_result[2]:
                                file1 = cutting_result[1][
                                    cutting_result[2].index(condition)]  # 找到condition的索引，然后按该索引拿到对应的文件名
                                if condition in imp_or_wsn_tested:
                                    file2 = imp_individual_file[imp_or_wsn_tested.index(condition)]
                                    data1 = pd.read_csv(file1)
                                    data2: pd.DataFrame = pd.read_csv(file2)
                                    data2, dropped_cols = merge_two_dataframes(data1, data2)
                                    data2[data2 == 0.000] = np.nan
                                    data2.to_csv(file2, index=False)
                                    os.remove(file1)
                                else:
                                    file2 = os.path.join(os.path.dirname(file1), f"{condition}{suffix_imp_10}.csv")
                                    if os.path.exists(file2):
                                        os.remove(file2)
                                    os.rename(file1, file2)
                                    imp_or_wsn_tested.append(condition)
                                    imp_individual_file.append(file2)
                        elif isinstance(cutting_result, tuple) and cutting_result[0] == "dcs_slice":
                            # cutting_result[1] 为DCS处理后文件
                            for condition in cutting_result[2]:
                                file1 = cutting_result[1][
                                    cutting_result[2].index(condition)]  # 找到condition的索引，然后按该索引拿到对应的文件名
                                if condition in dcs_tested:
                                    # 如果已经存在当前工况的数据，则合并已有数据和当前数据
                                    file2 = dcs_individual_file[dcs_tested.index(condition)]
                                    data1 = pd.read_csv(file1)
                                    data2 = pd.read_csv(file2)
                                    # 合并两个dataframe，自动判断按行还是按列合并
                                    # 合并的两种情况：
                                    # 1. 两个data的列名相同，但时间段不同，则将data2续到data1的最后一行之后，作为新行
                                    # 2. 两个data的时间段相同，但列名（即参数不同，一般来自DCS系统中导出的不同的趋势组数据）不同，
                                    #    则将data1和data2的列拼接起来。可能还存在更复杂的情况，目前已测试完成。
                                    data2, dropped_cols = merge_two_dataframes(data1, data2)
                                    # data2[data2 == 0.000] = np.nan  # dcs中的数据就有可能全是0，不能替换为np.nan，否则0不显示
                                    self.dropped_dcs_cols = list(set(self.dropped_dcs_cols).union(set(dropped_cols)))
                                    data2.to_csv(file2, index=False)
                                    os.remove(file1)
                                else:
                                    file2 = os.path.join(os.path.dirname(file1), f"{condition}{suffix_dcs_10}.csv")
                                    # 否则，将当前工况的数据文件名更改为最终数据文件名，并在存在工况列表中添加当前工况
                                    if os.path.exists(file2):
                                        os.remove(file2)
                                    os.rename(file1, file2)
                                    dcs_tested.append(condition)
                                    dcs_individual_file.append(file2)
                        elif isinstance(cutting_result, tuple) and cutting_result[0] == "unk_slice":
                            for condition in cutting_result[2]:
                                file1 = cutting_result[1][
                                    cutting_result[2].index(condition)]  # 找到condition的索引，然后按该索引拿到对应的文件名
                                if condition in unknown_tested:
                                    # 如果已经存在当前工况的数据，则合并已有数据和当前数据
                                    file2 = unknown_individual_file[unknown_tested.index(condition)]
                                    data1 = pd.read_csv(file1)
                                    data2 = pd.read_csv(file2)
                                    data2, dropped_cols = merge_two_dataframes(data1, data2)
                                    # data2[data2 == 0.000] = np.nan  # 有些数如循泵功率一直为0，不能替换为np.nan
                                    data2.to_csv(file2, index=False)
                                    os.remove(file1)
                                else:
                                    file2 = os.path.join(os.path.dirname(file1), f"{condition}_剪切unk时间_修正.csv")
                                    # 否则，将当前工况的数据文件名更改为最终数据文件名，并在存在工况列表中添加当前工况
                                    if os.path.exists(file2):
                                        os.remove(file2)
                                    os.rename(file1, file2)
                                    unknown_tested.append(condition)
                                    unknown_individual_file.append(file2)
                        elif isinstance(cutting_result, tuple) and cutting_result[0] == "kp_hollysys":
                            logger.debug("发现和利时点表文件")  # 和利时的点表文件
                            if self.point_description is None:
                                self.point_description = cutting_result[1]
                            else:
                                self.point_description.update(cutting_result[1])
                # noinspection all
                self.yk_signal.emit("eval", "self.statusBar().showMessage('汇总试验数据...')")
                # noinspection all
                self.yk_signal.emit("eval", "self.progressBar.setValue(0)")

                if len(imp_or_wsn_tested) != len(self.test_time.keys()):
                    logger.warning(f"imp采集数据工况找到{len(imp_or_wsn_tested)}个，少于工况记录单记录"
                                   f"工况数量{len(self.test_time.keys())}")
                if len(power_tested) != len(self.test_time.keys()):
                    logger.warning(f"功率表记录工况找到{len(power_tested)}个，少于工况记录单记"
                                   f"录工况数量{len(self.test_time.keys())}")
                if len(self.dropped_dcs_cols) > 0:
                    logger.warning(f"dcs数据中部分列不是数值型数据，已丢弃。"
                                   f"{json.dumps(self.dropped_dcs_cols, ensure_ascii=False)}｝")
                self.gather_imp_or_wsn(imp_individual_file)
                # noinspection all
                self.yk_signal.emit("eval", "self.progressBar.setValue(33)")
                self.gather_power(power_individual_file)
                # noinspection all
                self.yk_signal.emit("eval", "self.progressBar.setValue(66)")
                self.gather_dcs(dcs_individual_file)
                # noinspection all
                self.yk_signal.emit("eval", "self.progressBar.setValue(100)")
                self.gather_unknown(unknown_individual_file)
                # noinspection all
                self.yk_signal.emit("eval", "self.statusBar().showMessage('就绪')")
                # noinspection all
                self.yk_signal.emit("eval", "self.progressBar.setVisible(False)")
                # noinspection all
                self.yk_signal.emit("done", "")
                logger.debug("数据处理完毕！")

            # task_func()
            # self.table_widget.get_button() # 将按钮置为不可用
            self.table_widget.get_button("自动处理").setEnabled(False)
            start_threads(targets=task_func)

        YkDataTableWidget.choose_file = choose_file  # 向YkDataTableWidget添加两个成员方法，以便其中的按钮绑定事件方法
        YkDataTableWidget.deal = deal
        # YkDataTableWidget.calculate = calculate
        self.table_widget = YkDataTableWidget(from_file=os.path.join(os.path.dirname(__file__), "ui/table_data1.yaml"))
        for k, v in self.config.items():  # 按项目配置文件设置表格属性
            self.table_widget.set_value(k, v)
        self.setCentralWidget(self.table_widget)
        if self.data_folder is not None and self.data_folder != "c:\\":
            self.table_widget.set_value("目录", self.data_folder)

        self.statusBar().addPermanentWidget(self.progressBar)
        self.progressBar.setGeometry(0, 0, 50, 2)
        self.progressBar.setValue(0)
        self.progressBar.setVisible(False)

    def button_clicked(self):
        sender = self.sender()
        if sender.text() == "保存当前项目":
            self.config.update({"水位计算点数"     : self.table_widget.get_value("水位计算点数"),
                                "使用表号确定压力类型" : self.table_widget.get_value("使用表号确定压力类型"),
                                "未知类型文件区分文件名": self.table_widget.get_value("未知类型文件区分文件名")})
            self.project.update(self.config)
            writeAsPickle(self.project_file, self.project)
        self.statusBar().showMessage("当前项目已保存")

    def post(self, check_box: QCheckBox):
        """
        数据处理完成后的后处理阶段。

        打开计算分析软件，关闭当前界面

        :return:
        """
        from yangke.performance.data_analysis import MainWindow

        MainWindow(data_folder=self.data_folder).show()
        if check_box.isChecked():
            self.close()

    @QtCore.pyqtSlot(str, str)
    def on_message_changed(self, title, description):
        if title == "progressBar.value":
            self.progressBar.setValue(int(description))
        elif title == "statusBar.showMessage":
            self.statusBar().showMessage(description)
        elif title == "eval":
            eval(description)
        elif title == "done":
            self.table_widget.get_button("自动处理").setEnabled(True)
            # self.table_widget.setItem(2, 2, QTableWidgetItem("初始化计算数据"))
            btn_init_cal = QPushButton("Analysis")
            q_check_box = QCheckBox("关闭当前界面")
            q_check_box.setChecked(True)
            # noinspection all
            btn_init_cal.clicked.connect(lambda: self.post(q_check_box))
            self.table_widget.setSpan(2, 3, 1, 2)
            self.table_widget.setCellWidget(2, 2, btn_init_cal)
            self.table_widget.setCellWidget(2, 3, q_check_box)

    def setting_abs_or_rel(self):
        """
        主动设置绝压/表压测点信息。设置窗口会在软件无法确认测点是绝压还是表压时自动弹出一次，之后要在此设置，需要单独调用该方法。

        :return:
        """
        self.project.update(readFromPickle(self.project_file) or {})
        pressure_abs_specific = self.project.get("pressure_abs") or []
        pressure_rel_specific = self.project.get("pressure_rel") or []
        temp_list = pressure_abs_specific.copy()
        temp_list.extend(pressure_rel_specific)
        if len(temp_list) == 0:
            QMessageBox.warning(self,
                                "警告",
                                "待确认测点清单为空，请检查后再试！",
                                QMessageBox.Ok)
            return
            # ===================查找当前处理文件夹中是否存在额外的配置文件，配置文件中是否记录压力测点的信息======================
        # 如果没有找到测点的额外信息，则弹出窗口，提示用户确定测点是表压还是绝压
        temp_list = list(set(temp_list))
        temp_list.sort()
        dialog = ConfirmDialog(var_list=temp_list, abs_list=pressure_abs_specific, rel_list=pressure_rel_specific)

        # 让对话框以模式状态显示，即显示时QMainWindow里所有的控件都不可用，除非把dialog关闭
        dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        dialog.exec()

        var_list, value_list = dialog.get_data()
        pressure_abs_specific = []  # 记录前清空两个列表
        pressure_rel_specific = []
        for var, value in zip(var_list, value_list):
            if value == "绝压":
                pressure_abs_specific.append(var)
            elif value == "表压":
                pressure_rel_specific.append(var)

        # 保存用户输入的测点信息到配置文件，便于下次启动软件是加载
        pressure_abs_specific = list(set(pressure_abs_specific))
        pressure_rel_specific = list(set(pressure_rel_specific))
        self.project.update({"pressure_abs": pressure_abs_specific, "pressure_rel": pressure_rel_specific})
        # 更新现有的绝压/表压列表
        # noinspection all
        global pressure_absolute, pressure_relative
        pressure_absolute = list(set(pressure_absolute) - set(temp_list))  # 恢复默认绝压列表
        pressure_relative = list(set(pressure_relative) - set(temp_list))  # 恢复默认表压列表
        pressure_absolute.extend(pressure_abs_specific)
        pressure_relative.extend(pressure_rel_specific)
        self.project.update(self.config)
        writeAsPickle(self.project_file, self.project)

    def ask_for_absolute_or_relative(self):
        # 查找试验测点中的压力测点是绝压还是表压
        data_series = self.temp_para

        def get_unknown_list(p_relative, p_absolute, var_list=None):
            """
            查找无法判断绝压还是表压的测点名称

            :return: 返回无法判断的测点列表
            """
            temp_list1 = []
            if isinstance(var_list, pd.Series):
                for name, _ in var_list.items():
                    if "pa" not in name.lower():  # 说明不是压力数据
                        continue
                    if "流量" in name or "差压" in name:
                        continue
                    # 如果使用表号判断压力表类型
                    if self.config.get("使用表号确定压力类型"):
                        tag = name.split("_")[2]
                        if "pg" in tag.lower():
                            p_relative.append(name)
                        elif "pa" in tag.lower():
                            p_absolute.append(name)

                    if strInList(name, p_relative, revert=True) or strInList(name, p_absolute, revert=True):
                        continue
                    else:
                        temp_list1.append(name)
            else:
                for name in var_list:
                    if "pa" not in name.lower():  # 说明不是压力数据
                        continue
                    if "流量" in name or "差压" in name:
                        continue
                    # 如果使用表号判断压力表类型
                    if self.config.get("使用表号确定压力类型"):
                        tag = name.split("_")[2]
                        if "pg" in tag.lower():
                            p_relative.append(name)
                        elif "pa" in tag.lower():
                            p_absolute.append(name)

                    if strInList(name, p_relative, revert=True) or strInList(name, p_absolute, revert=True):
                        continue
                    else:
                        temp_list1.append(name)

            return temp_list1

        # noinspection all
        global pressure_absolute, pressure_relative

        temp_list = get_unknown_list(p_relative=pressure_relative, p_absolute=pressure_absolute, var_list=data_series)

        if len(temp_list) == 0:  # 如果不存在未知的测点，则直接返回
            self.temp_para = None
            return

        # ===================查找当前处理文件夹中是否存在额外的配置文件，配置文件中是否记录压力测点的信息======================
        self.project.update(readFromPickle(self.project_file) or {})

        pressure_rel_specific = self.project.get("pressure_rel") or []
        pressure_abs_specific = self.project.get("pressure_abs") or []

        temp_list = get_unknown_list(p_relative=pressure_rel_specific, p_absolute=pressure_abs_specific,
                                     var_list=temp_list)
        pressure_absolute.extend(pressure_abs_specific)
        pressure_relative.extend(pressure_rel_specific)
        pressure_absolute = list(set(pressure_absolute))
        pressure_relative = list(set(pressure_relative))

        if len(temp_list) == 0:
            self.temp_para = None
            return
        # ===================查找当前处理文件夹中是否存在额外的配置文件，配置文件中是否记录压力测点的信息======================
        # 如果没有找到测点的额外信息，则弹出窗口，提示用户确定测点是表压还是绝压
        temp_list = list(set(temp_list))
        temp_list.sort()
        dialog = ConfirmDialog(var_list=temp_list)

        # 让对话框以模式状态显示，即显示时QMainWindow里所有的控件都不可用，除非把dialog关闭
        dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        dialog.exec()

        var_list, value_list = dialog.get_data()
        for var, value in zip(var_list, value_list):
            if value == "绝压":
                pressure_abs_specific.append(var)
            elif value == "表压":
                pressure_rel_specific.append(var)

        # 保存用户输入的测点信息到配置文件，便于下次启动软件是加载
        self.project.update({"pressure_abs": pressure_abs_specific, "pressure_rel": pressure_rel_specific})
        # 更新现有的绝压/表压列表
        pressure_absolute.extend(pressure_abs_specific)
        pressure_relative.extend(pressure_rel_specific)

        # 当前线程执行完毕，将temp_para置为None，以便通知调用者当前线程结束
        self.temp_para = None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setFont(QFont("Microsoft YaHei", 12))
    # app.setStyleSheet("font-size: 20px")
    w1 = MainWindow()
    w1.setFont(QFont("Microsoft YaHei", 12))
    sys.exit(app.exec_())
