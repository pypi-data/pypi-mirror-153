"""
数据分析软件
"""
import pandas as pd
from PyQt5 import QtCore

from yangke.performance.basic_para import Case, alternative_symbol
from yangke.base import extend_list_by_alternative_symbols, get_temp_para, save_temp_para
from yangke.core import strInList
from yangke.common.config import logger
import copy
from yangke.common.qt import YkWindow, YkDataTableWidget
from yangke.performance.data_process import suffix_imp_20, suffix_p_20, suffix_dcs_20
from PyQt5.QtWidgets import QApplication, QFileDialog, QProgressBar
from PyQt5.QtGui import QBrush, QRadialGradient
from PyQt5.QtCore import Qt, QObject, pyqtSignal
import sys
import os
from yangke.performance.da import update_data, generate_case_skeleton


class MainWindow(YkWindow, QObject):
    yk_signal = pyqtSignal(str, str)

    def __init__(self, data_folder=None):
        """
        初始化计算分析软件

        :param data_folder: 数据文件目录，可选参数，不指定时会读取save_temp_para("directory", folder)保存的目录（可能由其他软件保存），
        没有保存记录则为C盘根目录。
        :param
        """
        self.data_folder = data_folder or get_temp_para('directory',
                                                        get_func=lambda: "c:\\")  # 这个和data_process共用一个文件夹
        self.imp_data_file = ""  # imp采集文件，从data_folder中查找"imp汇总_修正.xlsx"文件
        self.dcs_data_file = ""  # 电厂导数数据，从data_folder中查找"dcs汇总_修正.xlsx"文件
        self.power_data_file = ""  # 功率表采集文件，从data_folder中查找"p汇总_修正.xlsx"文件
        # noinspection PyTypeChecker
        self.table_widget: YkDataTableWidget = None
        self.progressBar = QProgressBar()
        self.cases = {}  # 试验工况计算数据列表
        self.case_skeleton = None

        self.q_raidal_grad = QRadialGradient(0, 0, 200, 0, 0)
        self.q_raidal_grad.setColorAt(0, Qt.red)
        self.q_raidal_grad.setColorAt(0.5, Qt.cyan)
        self.q_raidal_grad.setColorAt(1, Qt.yellow)
        super(MainWindow, self).__init__()
        if self.data_folder:
            self.update_file(self.data_folder)

    def update_file(self, folder):
        """
        更新相关文件路径

        :param folder:
        :return:
        """
        self.data_folder = folder
        save_temp_para("directory", folder)
        file = os.path.join(self.data_folder, suffix_imp_20 + ".xlsx")
        if os.path.exists(file):
            self.imp_data_file = file
        else:
            self.imp_data_file = "文件不存在"
            x, y = self.table_widget.get_var_location("采集数据文件")
            if x == -1:
                logger.warning("表格中不存在工作目录变量！")
                return
            self.table_widget.item(x, y - 1).setBackground(QBrush(self.q_raidal_grad))
        file = os.path.join(self.data_folder, suffix_p_20 + ".xlsx")
        if os.path.exists(file):
            self.power_data_file = file
        else:
            self.power_data_file = "文件不存在"
            x, y = self.table_widget.get_var_location("功率数据文件")
            self.table_widget.item(x, y - 1).setBackground(QBrush(self.q_raidal_grad))
        file = os.path.join(self.data_folder, suffix_dcs_20 + ".xlsx")
        if os.path.exists(file):
            self.dcs_data_file = file
        else:
            self.dcs_data_file = "文件不存在"
            x, y = self.table_widget.get_var_location("dcs导数文件")
            self.table_widget.item(x, y - 1).setBackground(QBrush(self.q_raidal_grad))
        self.table_widget.set_value("数据文件目录", folder)
        self.table_widget.set_value("采集数据文件", self.imp_data_file)
        self.table_widget.set_value("功率数据文件", self.power_data_file)
        self.table_widget.set_value("dcs导数文件", self.dcs_data_file)

    def init_ui(self):
        """
        构建界面

        :return:
        """

        def choose_file(table: YkDataTableWidget):
            folder = QFileDialog.getExistingDirectory(parent=self, caption="选择数据存储目录", directory=self.data_folder)
            if folder != self.data_folder:
                self.update_file(folder)

        def deal(table: YkDataTableWidget):
            self.progressBar.setVisible(True)
            self.statusBar().showMessage("校验测点数据...")
            self.cases = update_data(imp_file=self.imp_data_file, dcs_file=self.dcs_data_file,
                                     p_file=self.power_data_file)
            # noinspection all
            # self.yk_signal.emit("eval", "self.cases_updated()")
            self.cases_updated()
            # self.progressBar.setValue(0)

        YkDataTableWidget.choose_file = choose_file  # 向YkDataTableWidget添加两个成员方法，以便其中的按钮绑定事件方法
        YkDataTableWidget.deal = deal
        self.table_widget = YkDataTableWidget(from_file="ui/table_data2.yaml")
        self.table_widget.set_value("采集数据文件", self.imp_data_file)
        self.table_widget.set_value("功率数据文件", self.power_data_file)
        self.table_widget.set_value("dcs导数文件", self.dcs_data_file)
        self.setCentralWidget(self.table_widget)
        if self.data_folder is not None and self.data_folder != "c:\\":
            self.table_widget.set_value("数据文件目录", self.data_folder)

        self.statusBar().addPermanentWidget(self.progressBar)
        self.progressBar.setGeometry(0, 0, 50, 2)
        self.progressBar.setValue(0)
        self.progressBar.setVisible(False)
        self.setGeometry(300, 300, 1200, 900)
        self.setWindowTitle("性能试验数据计算")

    def cases_updated(self):
        """
        将self.cases的结果显示出来

        :return:
        """
        if len(self.cases) == 0:
            logger.error("没有找到任何试验工况或试验工况数量为0")
            return None
        _, v = self.cases.popitem()
        self.case_skeleton = generate_case_skeleton(v)

    @QtCore.pyqtSlot(str, str)
    def on_message(self, command, content):
        if command == "eval":
            eval(content)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w1 = MainWindow()
    sys.exit(app.exec_())
