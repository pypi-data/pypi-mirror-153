"""
应城电厂的热耗优化软件，用于优化低压和中压两股抽汽的抽汽量
240,280,350

1、2号机供气量范围
煤耗数据数量
"""
import warnings  # 屏蔽MATPLOTLIBDATA警告

warnings.filterwarnings("ignore", "(?s).*MATPLOTLIBDATA.*", category=UserWarning)

from yangke.common.config import logger, initLogger
from yangke.common.fileOperate import write_func, read_func, writeAsPickle, readFromPickle, get_last_modified_time
from yangke.base import Line, interpolate_value_complex
import os
from yangke.base import get_settings, plot_3d, get_args, interpolate_2d

import pandas as pd
from yangke.common.qt import QYKFigure
import traceback

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QSplitter, QLabel, QTabWidget, QStatusBar, \
    QVBoxLayout, QFileDialog, QInputDialog, QLineEdit, QDesktopWidget, QHBoxLayout
from PyQt5.QtGui import QFont, QKeyEvent
from PyQt5.QtCore import Qt
import PyQt5.QtCore as QtCore
from yangke.common.qt import YkItem, layout_to_widget, set_menu_bar, YkDataTableWidget, YkInputPanel, YkWindow

# 如果需要打包exe，需要显式引入以下包，打包命令pyinstaller -w heat_power_dispatch.py即可，打包为文件夹运行效果更接近IDE运行结果
# -w是窗口模式打包，不暴露控制台，当-w打包命令行模式运行可能不正确
import yangke.common.loggingHandler

power1_func = None  # 1号机功率计算函数
coal_consume_1_func = None  # 1号机煤耗计算函数
coal_consume_2_func = None  # 2号机煤耗计算函数
hr_func = None  # 总热耗计算函数
fl1_range_points = {}  # 1号机中压抽汽对应的低压抽汽范围
need_update = True
data1 = None
data2 = None  # 2号机 (功率, 四段抽汽量, 热耗)
data3 = None  # 2号机 (功率, 四段抽汽量, 煤耗)


def get_hr1():
    """
    获取1号机组热耗，单位kJ/(kW.h)

    :return:
    """

    return 3800  # 1号机组热耗，假定不变，单位kJ/(kW.h)


def get_fl1_available(fm):
    """
    当中压供汽量给定时，获取低压供汽量调节范围

    :param fm: 中压供汽量
    :return:
    """
    if fm < 0 or fm > 430:
        # logger.error(f"中压抽汽量超范围。{fm} not in [0, 430]")
        print(f"中压抽汽量超范围。{fm} not in [0, 430]")
        exit(0)
    fm_keys = fl1_range_points.keys()
    fm1 = [float(d) for d in fm_keys]
    l1 = [fl1_range_points.get(key)[0] for key in fm_keys]
    h1 = [fl1_range_points.get(key)[1] for key in fm_keys]

    low_range = interpolate_value_complex(fm, x_list=fm1, y_list=l1)
    high_range = interpolate_value_complex(fm, x_list=fm1, y_list=h1)
    return low_range, high_range


def get_fl2_available(p2):
    """
    当2号机功率确定时，其低压供汽范围

    :param p2:
    :return:
    """
    if p2 <= 306.617:  # MW
        return 0, 300
    else:
        return 0, -3.929564 * p2 + 1506.416649


def get_power1(fl, fm):
    """
    获取指定中低压供汽量下的电功率。
    适用于“热定电”运行模式，给定中压供汽需求和低压供汽需求，会有一个确定的发电功率

    :param fl: 低压供汽量
    :param fm: 中压供汽量
    :return:
    """
    # 判断fl和fm的取值范围，不在范围内返回None
    # todo

    # noinspection PyCallingNonCallable
    return float(power1_func(fl, fm))


def get_hr2(power, extract4):
    """
    获取指定电功率和抽汽量的热耗率。
    适用于抽凝供热机组，一般使用再热蒸汽或四抽供热

    :param power: 电功率或机组所带负荷
    :param extract4: 四抽供汽量
    :return:
    """
    # noinspection PyCallingNonCallable
    return float(hr_func(power, extract4))


def get_coal_consume1(fl, fm):
    """
    获取1号机的煤耗

    :param fl:
    :param fm:
    :return:
    """
    # noinspection PyCallingNonCallable
    return float(coal_consume_1_func(fl, fm))


def get_coal_consume2(power2, flow_extract4):
    """
    获取2号机的煤耗

    :param power2: 2号机功率
    :param flow_extract4: 2号机
    :return:
    """
    # noinspection PyCallingNonCallable
    return float(coal_consume_2_func(power2, flow_extract4))


def cal_total_obj(fm1, fl1, p, p_type, fl2, object_func="hr"):
    """
    计算 目标函数

    :param fm1: 1号机中压供汽量
    :param fl1: 1号机低压供汽量
    :param p: 电功率
    :param p_type: 参数p的含义，默认是2号机功率，也可设置为全厂功率，可取值"p2"/"total"
    :param fl2: 2号机低压供汽量
    :param object_func: 目标函数类型，“hr”表示热耗，"coal"表示煤耗
    :return:
    """
    p1 = get_power1(fl=fl1, fm=fm1)
    if p_type == "p2":
        if object_func == "hr":
            hr1 = get_hr1()
            p2 = p
            hr2 = get_hr2(p, fl2)
            y = (p1 * hr1 + p2 * hr2) / (p1 + p2)
        else:
            c1 = get_coal_consume1(fl1, fm1)
            c2 = get_coal_consume2(p, fl2)
            y = (p1 * c1 + p * c2) / (p1 + p)
    else:  # p_type="total"
        if object_func == "hr":
            hr1 = get_hr1()
            p1 = get_power1(fl1, fm1)
            p2 = p - p1
            hr2 = get_hr2(p2, fl2)
            y = (p1 * hr1 + p2 * hr2) / (p1 + p2)
        else:
            c1 = get_coal_consume1(fl1, fm1)
            p1 = get_power1(fl1, fm1)
            p2 = p - p1
            c2 = get_coal_consume2(p2, fl2)
            y = (p1 * c1 + p2 * c2) / (p1 + p2)

    return y


def verify_opt(fl_total, fm1, fl1_range, fl2_range, p, p_type):
    """
    通过穷举校核遗传算法优化结果是否正确，

    :param fl1_range: 1号机的低压供汽量范围
    :param fl2_range: 2号机的低压供汽量范围
    :return:
    """
    import numpy as np
    coal_total = []
    x = []
    break_type = 0
    for fl1 in np.arange(round(fl1_range[0]), round(fl1_range[1]) + 1, 1):
        p1 = get_power1(fl1, fm1)
        coal1 = get_coal_consume1(fl1, fm1)
        fl2 = fl_total - fl1
        if fl2_range[0] <= fl2 <= fl2_range[1]:
            if p_type == "p2":  # 说明是#2负荷分配
                coal2 = get_coal_consume2(p, fl2)
                p_total = p1 + p
                coal_total.append((p1 * coal1 + p * coal2) / p_total)
                x.append(fl2)
            elif p_type == "total":  # 说明是全厂负荷分配
                p2 = p - p1
                if p2 > 350 or p2 < 210:
                    break_type = "p2"
                    continue
                coal2 = get_coal_consume2(p2, fl2)
                coal_total.append((p1 * coal1 + p2 * coal2) / p)
                x.append(fl2)
        elif fl2 < fl2_range[0]:
            break_type = "fl2"
            break  # 因为1号机低压供汽量是从小到大穷举的，如果fl1最小时，fl2取到的最大值仍小于fl2的可取值下限，则无法满足指定的供汽量
        else:
            break_type = "fl2_exceed_max"
            continue
    if len(coal_total) == 0:
        logger.debug("指定参数下没有合适的运行工况")
        break_type = "error 0:指定参数下没有合适的运行工况"
        return break_type, x, coal_total, 0, 0
    opt_coal = min(coal_total)
    opt_fl2 = x[coal_total.index(opt_coal)]
    opt_fl1 = fl_total - opt_fl2
    return break_type, x[::-1], coal_total[::-1], opt_fl1, opt_fl2


def get_optimum(fl_need: float = 200, fm1: float = 240, p: float = 350, p_type="p2", object_func="hr", settings={}):
    """
    获得给定参数下，1号机和2号机的低压供汽量最优值

    :param fl_need: 低压供汽量总需求
    :param fm1: 1号机中压供汽量
    :param p: 电功率
    :param p_type: 参数p的含义，默认是2号机功率，也可设置为全厂功率，可取值"p2"/"total"
    :param settings: 算法设置参数
    :param object_func: 优化目标，“hr”表示优化热耗率，“coal”表示优化煤耗率
    :return:
    """
    fl_need = float(fl_need)
    fm1 = float(fm1)
    p = float(p)

    def ga_func(paras: tuple):
        fl1 = paras[0]
        y = cal_total_obj(fm1=fm1, fl1=fl1, p=p, p_type=p_type, fl2=fl_need - fl1, object_func=object_func)
        return y

    from yangke.sko.GA import GA
    fl_l, fl_h = get_fl1_available(fm1)
    size_pop = settings.get("pop_size") or 20
    gens = settings.get("gens") or 40
    p_mutate = settings.get("p_mutate") or 0.001
    ga = GA(func=ga_func, n_dim=1, lb=[fl_l], ub=[fl_h], size_pop=size_pop, max_iter=gens,
            prob_mut=p_mutate)
    best_x, best_y = ga.run()
    print('best_x:', best_x, '\n', 'best_y:', best_y)
    Y_history = pd.DataFrame(ga.all_history_Y)
    # fig, ax = plt.subplots(2, 1)
    # ax[0].plot(Y_history.index, Y_history.values, '.', color='red')
    # Y_history.min(axis=1).cummin().plot(kind='line')
    # plt.show()
    print(1)

    if p_type == "p2":  # 给定的是2号机负荷时
        fl1_range = get_fl1_available(fm1)  # 定值
        fl1 = best_x[0]
        p2 = p  # 定值
        fl2_range = get_fl2_available(p2)  # 定值
        break_type, x_list, coal_total_list, fl1, fl2 = verify_opt(fl_need, fm1, fl1_range, fl2_range, p,
                                                                   p_type)  # 更新最优结果
    else:
        print(2)
        fl1_range = get_fl1_available(fm1)
        fl1 = best_x[0]
        p1 = get_power1(fl1, fm1)
        p2 = p - p1
        fl2_range = get_fl2_available(p2)
        fl2 = fl_need - fl1
        if fl2 > fl2_range[1]:  # 如果fl2超范围，则将fl2_range适当放大，在此求解最优值，这里fl2和fl2_range是相互影响的
            fl2_range = (fl2_range[0], (fl2_range[1] + fl2) / 2)
        break_type, x_list, coal_total_list, fl1, fl2 = verify_opt(fl_need, fm1, fl1_range, fl2_range, p,
                                                                   p_type)  # 更新最优结果
        print(3)
        if isinstance(break_type, str) and "error" in break_type:
            fl1 = best_x
            fl2 = fl_need - fl1
            return best_x, best_y, Y_history, fl1, fl2, x_list, coal_total_list, break_type
        p1 = get_power1(fl1, fm1)
        p2 = p - p1
        fl2_range = get_fl2_available(p2)
        print(4)
        flag = 0
        while fl2 < fl2_range[0] or fl2 > fl2_range[1]:
            fl2_range = (fl2_range[0], (fl2_range[1] + fl2) / 2)
            break_type, x_list, coal_total_list, fl1, fl2 = verify_opt(fl_need, fm1, fl1_range, fl2_range, p,
                                                                       p_type)  # 更新最优结果
            flag = flag + 1
            if flag > 10:
                break
        print(5)
    print(6)
    if isinstance(break_type, str) and "error" in break_type:  # 说明无法同时满足指定的热电负荷
        if fl_need > fl1_range[1] + fl2_range[1]:
            break_type = "error: 低压供汽量过大，无法满足"
        fl1 = best_x
        fl2 = fl_need - fl1

    # 返回值意义
    # best_x, best_y遗传算法优化得到的fl1和目标函数值的最优结果，但可能超出允许取值范围
    # Y_history遗传算法优化过程中的种群个体的目标函数值信息
    # fl1, fl2将优化结果限定到允许取值范围内得到的优化结果，即这两个参数时最终的优化结果
    # x_list, coal_total_list是2号机低压供汽量和对应的全场煤耗的数据，是在fl1和fl2允许取值范围内的所有情况
    # break_type是提示信息，0表示正常，否则会有相应提示
    print(7)
    return best_x, best_y, Y_history, fl1, fl2, x_list, coal_total_list, break_type


def get_拐点(x_list, y_list, y0):
    """
    找出y=y0与x_list和y_list确定的折线的交点，本项目中，只可能有一个交点

    :param x_list:
    :param y_list:
    :param x:
    :return:
    """
    for i in range(1, len(x_list) - 1):
        point1 = (x_list[i], y_list[i])
        point2 = (x_list[i + 1], y_list[i + 1])
        line1 = Line(point1=point1, point2=point2)
        line2 = Line(k=0, b=y0)
        cross_point, is_cross = line1.cross_point(line2)
        if is_cross:
            if x_list[i] < cross_point[0] < x_list[i + 1]:  # 如果交点位于point1和point2之间，则返回
                return cross_point  # 本项目中最多一个交点，找到则返回
    return None


# ===========================界面部分=======================================

def read_fun_data():
    """
    判断是否需要读入data.xlsx文件
    :return:
    """
    try:
        global power1_func
        power1_func = read_func("power1_func.dat")
        global coal_consume_1_func
        coal_consume_1_func = read_func("coal_consume_1_func.dat")
        global hr_func
        hr_func = read_func("hr_func.dat")
        global coal_consume_2_func
        coal_consume_2_func = read_func("coal_consume_2_func.dat")
        global fl1_range_points
        fl1_range_points = readFromPickle("fl_range_points.dat")
        return True
    except:
        print("未找到函数文件power1_func.dat")
        return False


class MainWindow(YkWindow):
    def __init__(self):
        self.data_file = None
        self.fm1 = 240  # 1号机中压供汽，已知值
        self.p2 = 300  # 2号机负荷，已知值
        self.fl_total = 240  # 低压供汽总需求，已知值
        self.p_total = 350  # 第二种优化类型中的已知值，此时，p2是未知的
        self.display = {}  # 显示设置
        self.algorithm = {}  # 算法设置
        self.result = {}  # 优化结果，包含键有"fl1", "fl2", "hr_aver", "history"
        self.digits = 2
        super(MainWindow, self).__init__()  # 调用super方法时，会自动调用init_ui方法，因此需要先定义在init_ui方法中使用到的变量
        read_fun_data()

    def init_ui(self):
        YkWindow.不知道有什么用但是有用删除就闪退 = self.init_ui
        if not os.path.exists(os.path.join(os.path.dirname(__file__), "ui/ui_menu.yaml")):
            QMessageBox.warning(self,
                                "警告",
                                "找不到UI设置文件，请检查相关yaml文件路径是否正确！",
                                QMessageBox.Ok)
            sys.exit(0)
        # ----------------------------菜单栏------------------------------
        set_menu_bar(self, from_file=os.path.join(os.path.dirname(__file__), "ui/ui_menu.yaml"))  # 设置菜单栏

        self.root_splitter = QSplitter(Qt.Vertical, self)

        self.splitter = QSplitter(Qt.Horizontal, self)  # 主面板分为左右两部分
        self.splitter_l = QSplitter(Qt.Vertical, self)
        self.splitter_r = QSplitter(Qt.Vertical, self.splitter)  # 右边部分是有一个分割面板，竖直分割
        self.tab = QTabWidget()
        self.splitter_rt = QSplitter(Qt.Horizontal, self.splitter_r)  # 右边最上面又是一个分割面板

        logger.debug("初始化tableWidget")
        self.table_widget = YkDataTableWidget(from_file=os.path.join(os.path.dirname(__file__), "ui/table_data.yaml"))
        self.splitter_rt.addWidget(QLabel("#1功率响应曲面"))
        self.splitter_rt.addWidget(QLabel("#2热耗响应曲面"))
        self.splitter_r.addWidget(self.splitter_rt)
        self.splitter_r.addWidget(QLabel("遗传种群个体分布"))
        self.splitter_r.addWidget(QLabel("最优个体随遗传代数变化"))
        self.tab.addTab(self.splitter_r, "图像")
        self.tab.addTab(self.table_widget, "数据")
        self.splitter_l.addWidget(YkInputPanel(parent=self,
                                               from_file=os.path.join(os.path.dirname(__file__),
                                                                      "ui/ui_data.yaml"),
                                               domain="calculate2"))
        self.result_panel = self.get_result_panel()
        self.splitter_l.addWidget(self.result_panel)
        self.result_panel.setHidden(True)
        self.splitter.addWidget(self.splitter_l)
        self.splitter.addWidget(self.tab)
        self.splitter.setSizes([500, 700])
        h_box = QHBoxLayout()
        h_box.addStretch()
        title_label = QLabel("华能应城电厂全厂热电负荷优化分配智能调度系统")
        title_label.setFont(QFont("楷体", 18))
        title_label.setStyleSheet("color:blue")
        h_box.addWidget(title_label)
        h_box.addStretch()
        self.root_splitter.addWidget(layout_to_widget(h_box))
        self.root_splitter.addWidget(self.splitter)
        self.root_splitter.setSizes([10, 890])
        self.setCentralWidget(self.root_splitter)

        self.setGeometry(0, 0, 1200, 900)
        self.setWindowTitle("应城电厂热电负荷分配优化")
        self.statusBar1: QStatusBar = self.statusBar()
        self.statusBar1.showMessage('就绪')
        self.statusBar1.addPermanentWidget(QLabel("西安热工研究院有限公司＆华能应城热电有限责任公司                     "
                                                  "        ©2020 TPRI. All Rights Reserved."))

    def show_result(self):
        """
        显示优化结果

        :return:
        """

        # 遗传算法最优个体变化图
        fig = QYKFigure(x=self.result.get('history').index,
                        y=self.result.get('history').min(axis=1).cummin(),
                        title="遗传算法最优个体",
                        ylim=None)
        # 遗传算法种群个体分布图
        scatter_fig = QYKFigure(x=self.result.get('history').index,
                                y=self.result.get('history').values, fig_type="scatter",
                                title="种群个体",
                                ylim=None)
        if self.display.get("y_min") is not None:
            fig.axes.set_ylim(bottom=float(self.display.get("y_min")))
            scatter_fig.axes.set_ylim(bottom=float(self.display.get("y_min")))
        if self.display.get("y_max") is not None:
            fig.axes.set_ylim(top=float(self.display.get("y_max")))
            scatter_fig.axes.set_ylim(top=float(self.display.get("y_max")))
        self.splitter_r.replaceWidget(1, fig)
        self.splitter_r.replaceWidget(2, scatter_fig)

        fl1_range = get_fl1_available(self.fm1)  # 定值
        fl1 = self.result.get("fl1")
        fl2 = self.result.get("fl2")
        fm1 = self.fm1  # 定值
        p1 = get_power1(fl1, fm1)
        coal1 = get_coal_consume1(fl1, fm1)
        hr1 = get_hr1()  # 定值
        if self.p2 is not None:  # 给定的是2号机负荷时
            p2 = self.p2  # 定值
        else:
            p2 = self.p_total - p1
        fl2_range = get_fl2_available(p2)  # 定值
        hr2 = get_hr2(p2, fl2)
        coal2 = get_coal_consume2(p2, fl2)
        p_total = p1 + p2
        coal_total_opt = (p1 * coal1 + p2 * coal2) / p_total
        self.result.update({"coal_aver": coal_total_opt})
        self.result_panel = self.get_result_panel()
        self.splitter_l.replaceWidget(1, self.result_panel)
        self.result_panel.setHidden(False)
        self.table_widget.set_value("#2低压供汽范围.下限", round(fl2_range[0], self.digits))
        self.table_widget.set_value("#2低压供汽范围.上限", round(fl2_range[1], self.digits))
        self.table_widget.set_value("#1号机.低压供汽量", round(fl1, self.digits))
        self.table_widget.set_value("#1号机.中压供汽量", round(fm1, self.digits))
        self.table_widget.set_value("#1号机.功率", round(p1, self.digits))
        # self.table_widget.setValue("#1号机.热耗", hr1)
        self.table_widget.set_value("#1号机.煤耗", round(coal1, self.digits))

        self.table_widget.set_value("#2号机.功率", round(p2, self.digits))
        self.table_widget.set_value("#2号机.4抽供汽量", round(fl2, self.digits))
        self.table_widget.set_value("#2号机.热耗", round(hr2, self.digits))
        self.table_widget.set_value("#2号机.煤耗", round(coal2, self.digits))

        self.table_widget.set_value("全厂（最优工况下）.总低压供汽量", round(self.fl_total, self.digits))
        self.table_widget.set_value("全厂（最优工况下）.全厂总负荷", round(p_total, self.digits))
        self.table_widget.set_value("全厂（最优工况下）.全厂平均热耗", round((p1 * hr1 + p2 * hr2) / p_total, self.digits))
        self.table_widget.set_value("全厂（最优工况下）.全厂平均煤耗", round(coal_total_opt, self.digits))
        # 计算1号机单独供汽的工况
        fl1 = self.fl_total
        p1 = get_power1(fl1, fm1)
        coal1 = get_coal_consume1(fl1, fm1)
        hr2 = get_hr2(p2, 0)
        coal2 = get_coal_consume2(p2, 0)
        p_total = p1 + p2
        coal_total_if_only_1 = (p1 * coal1 + p2 * coal2) / p_total

        if fl1 < fl1_range[0]:
            self.table_widget.set_value("备注", "1号机单独供汽工况下，低压供汽量小于已知的下限值，可能超出调节范围")
        elif fl1 > fl1_range[1]:
            self.table_widget.set_value("备注", "1号机单独供汽工况下，低压供汽量大于已知的上限值，可能超出调节范围")
        else:
            increase = (coal_total_if_only_1 - coal_total_opt) / coal_total_opt * 100
            self.table_widget.set_value("备注", "1号机单独供汽煤耗较最优工况增大 " +
                                        str(round(increase, 2)) + "%")
        self.table_widget.set_value("全厂（1号机单独供汽）.总低压供汽量", round(self.fl_total, self.digits))
        self.table_widget.set_value("全厂（1号机单独供汽）.全厂总负荷", round(p_total, self.digits))
        self.table_widget.set_value("全厂（1号机单独供汽）.全厂平均热耗", round((p1 * hr1 + p2 * hr2) / p_total, self.digits))
        self.table_widget.set_value("全厂（1号机单独供汽）.全厂平均煤耗", round(coal_total_if_only_1, self.digits))

        self.table_widget.set_value("#1低压供汽范围.下限", round(fl1_range[0], self.digits))
        self.table_widget.set_value("#1低压供汽范围.上限", round(fl1_range[1], self.digits))

        x_list = self.result.get("x_list")
        break_type = self.result.get("break_type")
        coal_total_list = self.result.get("coal_total_list")
        if len(x_list) == 1:
            if break_type == "fl2":
                self.table_widget.set_value("备注", "低压供汽需求量接近1号机低压供汽量下限，建议只使用1号机进行供汽")
            elif break_type == "p2":
                self.table_widget.set_value("备注", "#2功率超出调节范围")
            elif "error" in break_type:
                self.table_widget.set_value("备注", break_type)
            x_list.append(x_list[0] + 0.01)
            coal_total_list = coal_total_list * 2
        elif len(x_list) == 0:  # 因为寻优开始时已经判断了低压供汽总需求和1号机低压供汽量下限的大小关系，这里不会为0
            self.table_widget.set_value("备注", "无法同时满足热负荷和电负荷")
            QMessageBox.warning(self,
                                "警告",
                                "无法同时满足指定的热负荷和电负荷",
                                QMessageBox.Ok)
            return
        fig1 = QYKFigure(x_list, coal_total_list, fig_type="curve", title="全厂煤耗变化曲线", xlabel="#2低压抽汽量")
        self.table_widget.setSpan(14, 0, 12, 6)
        self.table_widget.setCellWidget(14, 0, fig1)
        x_temp = self.result.get("revert_fl2")
        if x_temp is not None and x_temp != 0:
            fig1.scatter(x_temp, coal_total_list[0])

    def get_result_panel(self):
        """
        构建结果显示面板

        :return:
        """
        if len(self.result) == 0:
            return QLabel("待求解")
        v_box = QVBoxLayout()
        size = get_settings("size", setting_file=os.path.join(os.path.dirname(__file__), "ui/ui_data.yaml"))
        v_box.addStretch()
        v_box.addWidget(YkItem("最优低压供汽#1", round(self.result.get("fl1"), 2),
                               unit=["t/h", "kg/s"], unit_selected="t/h",
                               size=size))
        v_box.addWidget(YkItem("最优低压供汽#2", round(self.result.get("fl2"), 2),
                               unit=["t/h", "kg/s"], unit_selected="t/h",
                               size=size))
        v_box.addWidget(YkItem("最优平均煤耗", round(self.result.get("coal_aver"), 2),
                               unit=["g/(kW.h)"], unit_selected="g/(kW.h)",
                               size=size))
        # v_box.addWidget(YkItem("蝶阀开度", ))
        return layout_to_widget(v_box)

    def btn_clicked(self):
        sender = self.sender()
        panel = sender.parent()
        if sender.text() == "应用":
            if panel.name == "calculate":
                values, units = panel.get_values_and_units()
                self.fm1 = values[0]
                self.fl_total = values[1]
                self.p2 = values[2]
            elif panel.name == "calculate2":
                values, units = panel.get_values_and_units()
                self.fm1 = values[0]
                self.fl_total = values[1]
                self.p_total = values[2]
            elif panel.name == "display":
                values, units = panel.get_values_and_units()
                self.display.update({"need_pop_fig": values[0], "method1": values[1],
                                     "method2": values[2], "pop_fig_type": values[3],
                                     "y_min": float(values[4]), "y_max": float(values[5])})
            elif panel.name == "algorithm":
                values, units = panel.get_values_and_units()
                self.algorithm.update({"pop_size": int(values[0]), "gens": int(values[1]),
                                       "p_mutate": float(values[2]), "p_cross": float(values[3]),
                                       "select_method": values[4]})
            self.statusBar().showMessage("就绪")
        elif sender.text() == "寻优":
            if hr_func is None:
                QMessageBox.warning(self,
                                    "警告",
                                    "请先设置数据文件！设置方法：【文件】->【设置数据文件】",
                                    QMessageBox.Ok)
                return
            current_index = self.tab.currentIndex()
            self.tab.setCurrentIndex(0)
            logger.debug("test2")
            # --------------------读入优化计算参数，并判断参数是否合理--------------------------------------
            values, units = panel.get_values_and_units()
            self.fm1 = float(values[0])
            self.fl_total = float(values[1])
            fl1_range = get_fl1_available(self.fm1)
            if self.fl_total < fl1_range[0]:
                QMessageBox.warning(self,
                                    "警告",
                                    f"低压供汽需求（{self.fl_total}）小于1号机最低供汽量（{fl1_range[0]}）,请重新设置输入参数！",
                                    QMessageBox.Ok)
                return
            if panel.name == "calculate":
                self.p2 = float(values[2])
                if self.p2 < 210:
                    QMessageBox.warning(self,
                                        "警告",
                                        f"#2功率（{self.p2}）小于2号机允许最小负荷（210）,请重新设置输入参数！",
                                        QMessageBox.Ok)
                    return
                elif self.p2 > 350:
                    QMessageBox.warning(self,
                                        "警告",
                                        f"#2功率（{self.p2}）大于2号机允许最大负荷（350）,请重新设置输入参数！",
                                        QMessageBox.Ok)
                    return
                self.p_total = None
            elif panel.name == "calculate2":
                self.p_total = float(values[2])
                self.p2 = None
            # --------------------读入优化计算参数，并判断参数是否合理--------------------------------------
            if panel.name == "calculate":
                bestX, bestY, y_his, fl1_true, fl2_true, x_list, coal_list, break_type = get_optimum(
                    fl_need=self.fl_total, fm1=self.fm1, p=self.p2,
                    object_func="coal", settings=self.algorithm)
                self.result.update({"fl1": float(fl1_true), "fl2": float(fl2_true), "revert_fl2": 0,
                                    "x_list": x_list, "coal_total_list": coal_list,
                                    "break_type": break_type, "history": y_his, "type": 1})
            else:  # if panel.name == "calculate2":
                bestX, bestY, y_his, fl1_true, fl2_true, x_list, coal_list, break_type = get_optimum(
                    fl_need=self.fl_total, fm1=self.fm1,
                    p=self.p_total, p_type="total",
                    object_func="coal", settings=self.algorithm)
                self.result.update({"fl1": float(fl1_true), "fl2": float(fl2_true), "revert_fl2": 0,
                                    "x_list": x_list, "coal_total_list": coal_list,
                                    "break_type": break_type, "history": y_his, "type": 1})
            if len(x_list) > 0:
                拐点 = get_拐点(x_list, coal_list, coal_list[0])
                if 拐点 is not None:
                    self.result.update({"revert_fl2": 拐点[0]})
            self.show_result()
            self.tab.setCurrentIndex(current_index)
            self.statusBar().showMessage("就绪")
        elif sender.text() == "确定":
            if panel.name == "algorithm":
                values, units = panel.get_values_and_units()
                self.algorithm.update({"pop_size": int(values[0]), "gens": int(values[1]),
                                       "p_mutate": float(values[2]), "p_cross": float(values[3]),
                                       "select_method": values[4]})
            elif panel.name == "display":
                values, units = panel.get_values_and_units()
                self.display.update({"need_pop_fig": values[0], "method1": values[1],
                                     "method2": values[2], "pop_fig_type": values[3],
                                     "y_min": float(values[4]), "y_max": float(values[5])})
                # 如果有计算结果，就在不计算的情况下，直接更新一次显示结果
                if len(self.result) > 0:
                    self.show_result()

    def init_model(self, debug: bool = True):
        """
        读取excel数据文件，获得原始煤耗、热耗、电功率等数据，并生成插值计算模型

        :param debug:
        :return:
        """
        if not need_update:
            return
        try:
            global power1_func
            num_1_file = self.data_file or r"E:\2020\科研项目\应城电厂热电分配\data.xlsx"
            modified_time = get_last_modified_time(file=num_1_file)
            modified_time_1 = readFromPickle("last_modified_time.dat")
            if modified_time != modified_time_1:
                writeAsPickle("last_modified_time.dat", modified_time)
            # ================================ 加载1号机功率数据==========================================
            logger.debug("加载1号机功率数据")
            # 默认用第一行作为列索引，使用index_col=0设置用第一列作为行索引
            data = pd.read_excel(num_1_file, sheet_name="1号机功率", index_col=0)
            data = data.dropna(how="all")  # 丢弃所有元素都为NAN的行
            data = data.dropna(how="all", axis=1)  # 丢弃所有元素都为NAN的列
            index_name_col = data.columns
            index_name_row = data.index
            flow_middle, flow_low, power = [], [], []  # 初始化三个数组，用于存放x,y,z，分别对应中压供汽流量...
            for fl in index_name_row:
                for fm in index_name_col:
                    if pd.notna(data[fm][fl]):
                        flow_low.append(fl)
                        flow_middle.append(fm)
                        power.append(data[fm][fl])

            if modified_time == modified_time_1:
                logger.debug("加载1号机功率插值函数")
                power1_func = read_func("power1_func.dat")
            else:
                logger.debug("生成1号机功率插值函数")
                self.statusBar1.showMessage("生成1号机功率插值函数...")
                logger.debug(f"{flow_low}, {flow_middle}, {power}")
                power1_func = interpolate_2d(flow_low, flow_middle, power, method="rbf")  # 生成插值模型
                logger.debug("2")
                write_func("power1_func.dat", power1_func)
                logger.debug("3")

            if debug:
                plot_3d(flow_low, flow_middle, power, method="rbf", projection=False)
            else:
                logger.debug("绘制功率响应曲面")
                fig1 = plot_3d(flow_low, flow_middle, power, method="rbf", projection=False, backend="pyqt5")
                if len(self.splitter_rt.children()) >= 2:
                    logger.debug("替换功率响应曲面")
                    self.splitter_rt.replaceWidget(0, fig1)
                else:
                    logger.debug("添加功率响应曲面")
                    self.splitter_rt.addWidget(fig1)
            # ================================ 加载1号机功率数据==========================================

            # ============================== 生成指定中压抽汽量下对应的低压抽汽量的取值范围=================================
            logger.debug("确定1号机低压供汽量取值范围")
            for fm in flow_middle:
                temp_series = data[:][fm].dropna().index
                # 因为小数涉及到精度问题，当用其作为字典的键时，最好转换为字符串
                fl1_range_points.update({str(fm): [temp_series.min(), temp_series.max()]})
            writeAsPickle("fl_range_points.dat", fl1_range_points)
            # ============================== 生成指定中压抽汽量下对应的低压抽汽量的取值范围=================================

            # =================================加载1号机煤耗数据===============================================
            logger.debug("加载1号机煤耗数据")
            # 默认用第一行作为列索引，使用index_col=0设置用第一列作为行索引
            data = pd.read_excel(num_1_file, sheet_name="1号机煤耗", index_col=0)
            data = data.dropna(how="all")  # 丢弃所有元素都为NAN的行
            data = data.dropna(how="all", axis=1)  # 丢弃所有元素都为NAN的列
            index_name_col = data.columns
            index_name_row = data.index
            flow_middle, flow_low, coal_consume = [], [], []  # 初始化三个数组，用于存放x,y,z，分别对应中压供汽流量...
            for fl in index_name_row:
                for fm in index_name_col:
                    if pd.notna(data[fm][fl]):
                        flow_low.append(fl)
                        flow_middle.append(fm)
                        coal_consume.append(data[fm][fl])
            self.statusBar().showMessage("生成1号机煤耗插值函数...")
            global coal_consume_1_func
            if modified_time == modified_time_1:
                coal_consume_1_func = read_func("coal_consume_1_func.dat")
            else:
                coal_consume_1_func = interpolate_2d(flow_low, flow_middle, coal_consume, method="rbf")  # 生成插值模型
                write_func("coal_consume_1_func.dat", coal_consume_1_func)
            if debug:
                plot_3d(flow_low, flow_middle, coal_consume, method="rbf", projection=False)
            # else:
            #     fig1 = plot_3d(flow_low, flow_middle, coal_consume, method="rbf", projection=False, backend="pyqt5")
            #     if len(self.splitter_rt.children()) >= 2:
            #         self.splitter_rt.replaceWidget(0, fig1)
            #     else:
            #         self.splitter_rt.addWidget(fig1)
            # =================================加载1号机煤耗数据===============================================

            # =================================加载2号机热耗数据===============================================
            logger.debug("加载2号机热耗数据")
            flow_extract4, power, heat_rate = [], [], []
            data = pd.read_excel(num_1_file, sheet_name="2号机热耗", index_col=0)
            data = data.dropna(how="all")  # 丢弃所有元素都为NAN的行
            data = data.dropna(how="all", axis=1)  # 丢弃所有元素都为NAN的列
            index_name_col = data.columns
            index_name_row = data.index
            for fe in index_name_row:
                for po in index_name_col:
                    if pd.notna(data[po][fe]):
                        flow_extract4.append(fe)
                        power.append(po)
                        heat_rate.append(data[po][fe])
            self.statusBar().showMessage("生成2号机热耗插值函数...")
            global hr_func, data2
            data2 = (power, flow_extract4, heat_rate)
            if modified_time == modified_time_1:
                hr_func = read_func("hr_func.dat")
            else:
                hr_func = interpolate_2d(power, flow_extract4, heat_rate, method="rbf")
                write_func("hr_func.dat", hr_func)
            if debug:
                plot_3d(power, flow_extract4, heat_rate, method="rbf", projection=False)
            else:
                fig1 = plot_3d(power, flow_extract4, heat_rate, method="rbf", projection=False, backend="pyqt5")
                if len(self.splitter_rt.children()) >= 2:
                    self.splitter_rt.replaceWidget(1, fig1)
                else:
                    self.splitter_rt.addWidget(fig1)
            # =================================加载2号机热耗数据===============================================

            # =================================加载2号机煤耗数据===============================================
            logger.debug("加载2号机煤耗数据")
            flow_extract4, power, coal_consume = [], [], []
            data = pd.read_excel(num_1_file, sheet_name="2号机煤耗", index_col=0)
            data = data.dropna(how="all")  # 丢弃所有元素都为NAN的行
            data = data.dropna(how="all", axis=1)  # 丢弃所有元素都为NAN的列
            index_name_col = data.columns
            index_name_row = data.index
            for fe in index_name_row:
                for po in index_name_col:
                    if pd.notna(data[po][fe]):
                        flow_extract4.append(fe)
                        power.append(po)
                        coal_consume.append(data[po][fe])
            self.statusBar().showMessage("生成2号机煤耗插值函数...")
            global coal_consume_2_func, data3
            data3 = (power, flow_extract4, coal_consume)
            if modified_time == modified_time_1:
                coal_consume_2_func = read_func("coal_consume_2_func.dat")
            else:
                coal_consume_2_func = interpolate_2d(power, flow_extract4, coal_consume, method="rbf")
                write_func("coal_consume_2_func.dat", coal_consume_2_func)
            # if debug:
            #     plot_3d(power, flow_extract4, coal_consume, method="rbf", projection=False)
            # else:
            #     fig1 = plot_3d(power, flow_extract4, coal_consume, method="rbf", projection=False, backend="pyqt5")
            #     if len(self.splitter_rt.children()) >= 2:
            #         self.splitter_rt.replaceWidget(1, fig1)
            #     else:
            #         self.splitter_rt.addWidget(fig1)
            # =================================加载2号机煤耗数据===============================================
            self.statusBar().showMessage("就绪")
        except Exception:
            logger.debug("初始化计算模型错误")
            self.statusBar().showMessage("初始化计算模型错误！")
            traceback.print_exc()

    def set_data_file(self):
        directory = None
        file = QFileDialog.getOpenFileName(parent=self, caption='选择数据文件', directory=directory)
        file = file[0]
        current_index = self.tab.currentIndex()
        self.tab.setCurrentIndex(0)
        if file is not None and os.path.exists(file):
            self.data_file = os.path.abspath(file)
            global need_update
            need_update = True
            self.statusBar().showMessage(f"数据文件更新：{file}")
            self.init_model(False)
            # start_threads(self.init_model, args_list=(False,))  # 子线程无法更新主线程的界面内容
        self.tab.setCurrentIndex(current_index)
        self.statusBar1.showMessage("就绪")

    def set_algorithm(self):
        input_panel = YkInputPanel(self, os.path.join(os.path.dirname(__file__), "ui/ui_data.yaml"), "algorithm")
        if self.display is not None and len(self.display) == len(input_panel.findChildren(YkItem)):
            t = self.display
            values = [t.get("pop_size"), t.get("gens"), t.get("p_mutate"), t.get("p_cross"),
                      t.get("select_method")]
            input_panel.set_values(values=values)
        self.splitter_l.replaceWidget(0, input_panel)
        self.statusBar1.showMessage("就绪")

    def set_display(self):
        input_panel = YkInputPanel(self, os.path.join(os.path.dirname(__file__), "ui/ui_data.yaml"), "display")
        if self.display is not None and len(self.display) == len(input_panel.findChildren(YkItem)):
            t = self.display
            values = [t.get("need_pop_fig"), t.get("method1"), t.get("method2"), t.get("pop_fig_type"),
                      t.get("y_min"), t.get("y_max")]
            input_panel.set_values(values=values)
        self.splitter_l.replaceWidget(0, input_panel)
        self.statusBar1.showMessage("就绪")

    def set_calculate(self):
        input_panel = YkInputPanel(self, os.path.join(os.path.dirname(__file__), "ui/ui_data.yaml"), "calculate")
        input_panel.set_values([self.fm1, self.fl_total, self.p2])
        self.splitter_l.replaceWidget(0, input_panel)
        self.statusBar1.showMessage("就绪")

    def set_calculate2(self):
        input_panel = YkInputPanel(self, os.path.join(os.path.dirname(__file__), "ui/ui_data.yaml"), "calculate2")
        input_panel.set_values([self.fm1, self.fl_total, self.p_total])
        self.splitter_l.replaceWidget(0, input_panel)
        self.statusBar1.showMessage("就绪")

    def single_calculate(self):
        def _single_calculate(table_widget: YkDataTableWidget):
            print("debug ...")
            if hr_func is None:
                QMessageBox.warning(self,
                                    "警告",
                                    "请先设置数据文件！设置方法：【文件】->【设置数据文件】",
                                    QMessageBox.Ok)
                return
            fm1 = float(table_widget.get_value("给定参数.#1中压供汽量"))
            fl1 = float(table_widget.get_value("给定参数.#1低压供汽量"))
            fl_total = float(table_widget.get_value("给定参数.低压供汽总需求"))
            p2 = float(table_widget.get_value("给定参数.#2功率"))

            p1 = get_power1(fl1, fm1)
            hr1 = get_hr1()
            coal1 = get_coal_consume1(fl1, fm1)

            fl2 = fl_total - fl1
            if (fl2 < 0):
                QMessageBox.warning(self,
                                    "警告",
                                    "#1低压供汽量大于低压供汽总需求",
                                    QMessageBox.Ok)
                return
            hr2 = get_hr2(p2, fl2)
            coal2 = get_coal_consume2(p2, fl2)

            coal_total = (p1 * coal1 + p2 * coal2) / (p1 + p2)
            hr_total = (p1 * hr1 + p2 * hr2) / (p1 + p2)

            table_widget.set_value("计算结果.#1功率", p1)
            table_widget.set_value("计算结果.#1热耗", hr1)
            table_widget.set_value("计算结果.#1煤耗", coal1)
            table_widget.set_value("计算结果.#1中压供汽", fm1)
            table_widget.set_value("计算结果.#1低压供汽", fl1)
            table_widget.set_value("计算结果.#2功率", p2)
            table_widget.set_value("计算结果.#2热耗", hr2)
            table_widget.set_value("计算结果.#2煤耗", coal2)
            table_widget.set_value("计算结果.#2四抽供汽", fl2)
            table_widget.set_value("计算结果.全厂总热耗", hr_total)
            table_widget.set_value("计算结果.全厂总煤耗", coal_total)

        # 因为YkDataTableWidget中使用了按钮事件，需要首先把事件方法绑定到类上，否则按钮的connect将报错
        YkDataTableWidget.single_calculate = _single_calculate
        self.table_widget_single = YkDataTableWidget(from_file=os.path.join(os.path.dirname(__file__),
                                                                            "ui/table_data_single_calculate.yaml"),
                                                     **{"single_calculate": _single_calculate})

        self.tab.addTab(self.table_widget_single, "")
        qua = len(self.tab.children()[1])
        self.tab.setTabText(qua - 1, f"单工况计算{qua - 2}")
        self.tab.setCurrentIndex(qua - 1)
        self.statusBar1.showMessage("就绪")


def get_valve_openness(fl2):
    """
    根据2号低压供汽流量计算2号机低压液控阀开度

    :param fl2:
    :return:
    """
    o = (fl2 - 2.18380941107531) / 4.75368946518066
    if o < 0:
        o = 0
    return o


def command_calculate(fm1, fl_total, p2=None, p_total=None, type_cal="0"):
    """
    如果是命令行调用该程序

    :param fm1:
    :param fl_total:
    :param p2:
    :param p_total:
    :param type_cal:
    :return:
    """
    import json
    if not read_fun_data():
        result = {"type": type_cal, "opt_fl1": 0, "opt_fl2": 0, "opt_coal": 0, "revert_fl2": 0,
                  "opt_p1": 0, "opt_p2": 0, "opt_coal1": 0, "opt_coal2": 0, "break_type": "error:1初始化函数失败"}
        result = json.dumps(result, ensure_ascii=False)
        print(result)
        return result
    if type_cal == "1":
        p = p2
        p_type = "p2"
    elif type_cal == "2":
        p = p_total
        p_type = "total"
    best_x, best_y, Y_history, fl1, fl2, x_list, coal_total_list, break_type = get_optimum(fl_need=fl_total,
                                                                                           fm1=fm1, p=p,
                                                                                           p_type=p_type,
                                                                                           object_func="coal")

    if isinstance(break_type, str) and "error" in break_type:
        result = {"type": type_cal, "opt_fl1": 0, "opt_fl2": 0, "opt_coal": 0, "revert_fl2": 0,
                  "opt_p1": 0, "opt_p2": 0, "opt_coal1": 0, "opt_coal2": 0, "break_type": break_type}
        result = json.dumps(result, ensure_ascii=False)
        print(result)
        return result
    coal1 = get_coal_consume1(fl1, fm1)
    hr1 = get_hr1()
    p1 = get_power1(fl1, fm1)
    if type_cal == "1":
        p_total = p1 + p2
    elif type_cal == "2":
        p2 = p_total - p1
    hr2 = get_hr2(p2, fl2)
    coal2 = get_coal_consume2(p2, fl2)

    coal_total = (p1 * coal1 + p2 * coal2) / (p1 + p2)
    hr_total = (p1 * hr1 + p2 * hr2) / (p1 + p2)
    result = {"type": type_cal, "opt_fl1": fl1, "opt_fl2": fl2, "opt_coal": coal_total,
              "valve": get_valve_openness(fl2), "revert_fl2": 0,
              "opt_p1": p1, "opt_p2": p2, "opt_coal1": coal1, "opt_coal2": coal2, "break_type": break_type}
    if len(x_list) > 0:
        拐点 = get_拐点(x_list, coal_total_list, coal_total_list[0])
        if 拐点 is not None:
            result.update({"revert_fl2": 拐点[0]})
    result = json.dumps(result, ensure_ascii=False)
    print(result)
    return result


print("start")
if __name__ == "__main__":
    args = {'kv': [{'short': 'data_file', 'default': None, 'description': '数据文件路径'},
                   {'short': 'p2', 'default': None, 'description': '#2功率'},
                   {'short': 'p_total', 'default': None, 'description': '全厂总负荷'},
                   {'short': 'fl_total', 'default': None, 'description': '低压供气总需求'},
                   {'short': 'fm1', 'default': None, 'description': '#1中压抽汽量'},
                   {'short': 'log_level', 'default': 30, 'description': '日志输出级别'},
                   {'short': 't', 'long': 'type', 'default': None,
                    'description': '优化算法计算类型，1-#2功率优化：需要指定(p2, fm1, fl_total)，'
                                   '2-全场负荷优化：需要指定(p_total, fm1, fl_total)'},
                   ],
            'k': [{'short': 'c', 'long': 'command', 'default': False, 'description': '运行模式'}]}
    args = get_args(args_name=args)  # 返回的是字典，返回值不分类
    type_cal = args.type
    p_total = None
    p2 = None
    logger.setLevel(int(args.log_level))
    print("version 1.0.0")
    if type_cal is None or type_cal == "0":
        app = QApplication(sys.argv)
        # app.setFont(QFont("Microsoft YaHei", 12))
        # app.setStyleSheet("font-size: 20px")
        w1 = MainWindow()
        w1.setFont(QFont("Microsoft YaHei", 12))
        sys.exit(app.exec_())
    else:
        fm1 = float(args.fm1)
        fl_total = float(args.fl_total)
        data_file = args.data_file
        if type_cal == "1":
            p2 = float(args.p2)
            assert p2 and fm1 and fl_total
        elif type_cal == "2":
            p_total = float(args.p_total)
            print(f"type_cal={type_cal},p_total={p_total},fm1={fm1},fl_total={fl_total}")
            assert p_total and fm1 and fl_total
    command_calculate(fm1=fm1, fl_total=fl_total, p_total=p_total, p2=p2, type_cal=type_cal)
