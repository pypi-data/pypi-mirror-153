import sys
import os
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QPushButton, QComboBox, QLineEdit, QTableWidgetItem, \
    QLabel, QCheckBox, QVBoxLayout, QWidget, QApplication, QAction, QDesktopWidget, QTableWidget, qApp, \
    QDialog, QInputDialog, QMessageBox, \
    QTextEdit
from PyQt5.QtGui import QIntValidator, QRegExpValidator, QKeyEvent, QBrush, QColor, QFont
import PyQt5.QtCore as QtCore
from yangke.core import runAsAdmin
from yangke.common.win.win_x64 import find_window, get_pid_by_hwnd
from yangke.common.mysql import connect_available
import pandas as pd
from gettext import gettext as _
import yaml

from yangke.common.config import logger
from yangke.base import get_settings, is_number


class YkDialog(QDialog):
    """
    对话框类，用于在其他界面中弹出自定义窗口，且窗口可以与父窗口通信
    """
    # 以下消息的传递参数时object，其包括(type, value)，其中type是消息想要传递的参数类型，value是想传递的值
    signal_close = QtCore.pyqtSignal(object)  # 用于对话框关闭时发送关闭消息，object=(dict:value)是YkDialog关闭时的对象的值
    signal_button_clicked = QtCore.pyqtSignal(object)  # object=(QPushButton, 按钮)，YkDialog对象会自动通过sender传递

    def __init__(self, title=_("对话框"), ui_file=None, values=None):
        """
        ui_file示例
----------------------------------------------------------------------------------------------------
size:
  width:
    - 80  # <label>的宽度
    - 340  # <textField>的宽度
    - 10  # <unit>的宽度

mysql:
  inputArea:
    - # 第一个设置项
      label: "host"
      value: "localhost"
    - # 第二个设置项
      label: "port"
      value: 3306
    - # 第三个设置项
      label: "user"
      value: "root"
    - # 第三个设置项
      label: "password"
      value: "111111"
  buttons:
    - # 第一个按钮
      text: "测试连接"
      on_click: "btn_clicked"  # 按钮点击触发的事件
    - text: "Apply"
      on_click: "btn_clicked"  # 按钮点击触发的事件
----------------------------------------------------------------------------------------------------

        :param title:
        :param ui_file:
        :param values:
        """
        super(YkDialog, self).__init__()
        self.setWindowTitle(title)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        if ui_file is not None:
            self.widget = YkInputPanel(parent=self, from_file=ui_file, domain="mysql")
        self.result_panel = QLabel()
        layout = QVBoxLayout()
        layout.addWidget(self.widget)
        layout.addWidget(self.result_panel)
        self.setLayout(layout)
        if values is not None:
            self.set_values(values)

    def set_values(self, values):
        self.widget.set_values(values)

    def btn_clicked(self):
        sender = self.sender()
        self.signal_button_clicked.emit((QPushButton, sender))

    def get_value(self):
        result = self.widget.get_values_and_units(need_dict=True, need_unit=False)
        return result

    def set_result_panel(self, info):
        """
        对话框按钮点击后，可能需要显示按钮事件处理后的消息，这里显示到面板上

        :param info:
        :return:
        """
        self.result_panel.setText(info)

    def closeEvent(self, e):
        value = self.get_value()
        self.signal_close.emit((dict, value))
        self.close()


class YkWindow(QMainWindow):
    button_clicked_signal = QtCore.pyqtSignal(object)

    def __init__(self, setting_file="default"):
        # noinspection PyArgumentList
        super(YkWindow, self).__init__()
        self.setting_file = setting_file
        self.toolbar = None
        self.init_ui()
        self.init_ui1()
        self.yk_info = {}  # 用于传递临时变量的变量

    def init_ui1(self):
        self.center()
        size = get_settings("mainframe.geometry", self.setting_file)
        if len(size) > 0:
            if size == "maximize":
                self.showMaximized()
            elif size == "fullscreen":
                self.showFullScreen()
            else:
                size = eval(size)
                x, y, w, h = size
                self.setGeometry(x, y, w, h)
        self.statusBar().showMessage(_('Ready'))
        logger.debug("窗口初始化完成")
        self.show()

    def init_ui(self):
        self.setToolTip('This is a <b>QWidget</b> widget')
        btn = QPushButton('Quit', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')

        btn.resize(btn.sizeHint())
        btn.move(50, 100)
        btn.clicked.connect(self.button_clicked)

        exit_action = QAction(_('Exit'), self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip(_('Exit application'))
        exit_action.triggered.connect(qApp.quit)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu(_('File'))
        file_menu.addAction(exit_action)

        self.toolbar = self.addToolBar(_('Exit'))
        self.toolbar.addAction(exit_action)

        self.setWindowTitle(_("yk demo"))
        # self.setWindowIcon(QIcon('web.png'))

    def button_clicked(self, anything=None, anything2=None, **kwargs):
        """
        处理点击事件

        :param anything: 触发该方法的信号传入的数据，可以是任何类型
        :param anything2: 接收点击事件传入的任何参数
        :return:
        """
        sender = self.sender()  # 发送事件的组件，可能是button、YkDialog等任何拥有signal的类
        if isinstance(sender, QPushButton):
            self.statusBar().showMessage(sender.text() + ' was pressed')
        elif isinstance(sender, YkDialog):  # 说明点击事件来自自定义的子对话框
            logger.debug(_("接收到自定义窗口信号！"))
            if sender.windowTitle() == "MySQL连接设置":  # 判断消息具体来自哪一个对话框实例
                if anything[0] == QPushButton:  # 说明是按钮点击事件
                    if anything[1].text() == _("测试连接"):
                        mysql_settings = sender.get_value()
                        if connect_available(**mysql_settings):
                            sender.set_result_panel("连接成功")
                        else:
                            sender.set_result_panel("连接失败")
                    elif anything[1].text() == _("应用"):
                        mysql_info = sender.get_value()
                        self.yk_info.update(mysql_info)
                        if self.setting_file is not None:
                            settings = get_settings(setting_file=self.setting_file)
                            mysql_ = settings.get("mysql") or {}
                            mysql_.update(mysql_info)
                            # settings.update({"mysql": mysql_})  # mysql_是浅拷贝，无需再次更新settings
                            with open(self.setting_file, "w") as f:
                                yaml.dump(settings, f)
                if anything[0] == dict:  # 说明是子对话框关闭时间，YkDialog关闭时会将对话框中收集的数据发送出来
                    # self.set_mysql(anything[1])
                    pass  # 关闭对话框时无需执行额外操作

    def center(self):
        qr = self.frameGeometry()  # 获得窗口
        cp = QDesktopWidget().availableGeometry().center()  # 获得屏幕中心点
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        #     reply = QMessageBox.question(self, "Message", "Are you sure to quit?",
        #                                  QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        #     if reply == QMessageBox.Yes:
        #         event.accept()
        #     else:
        #         event.ignore()
        print(_("close event triggered"))
        event.accept()

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        if a0.key() == QtCore.Qt.Key_Escape:
            self.close()

    def init_mysql(self, ui_file=None):
        """
        初始化mysql数据库，用户的更改会实时保存到settings_file中

        :param ui_file: mysql配置面板的ui文件，使用YkInputPanel(ui_file)进行面板生成，如果需要自定义面板，需要重写init_mysql方法
        :return:
        """
        mysql = get_settings("mysql", setting_file=self.setting_file) or {}
        host = mysql.get('host') or "localhost"
        port = mysql.get('port') or "3306"
        username = mysql.get('user') or "root"
        password = mysql.get('passwd') or '111111'
        self.yk_info["host"] = host
        self.yk_info["port"] = port
        self.yk_info["user"] = username
        self.yk_info["passwd"] = password

        dialog = YkDialog("MySQL连接设置", ui_file=ui_file, values=self.yk_info)
        dialog.signal_button_clicked.connect(self.button_clicked)  # 关联自定义对话框的按钮单击事件
        dialog.signal_close.connect(self.button_clicked)  # YkDialog关闭时发送yk_signal信号
        dialog.exec()

    def set_digits(self):
        digits_str, ok = QInputDialog.getText(self, "设置数据格式", "保留小数位数（最大位数）", QLineEdit.Normal, "2")
        if ok and digits_str.isnumeric():
            self.digits = int(digits_str)

    def set_font(self, font_size=10):
        font_size, ok_pressed = QInputDialog.getText(self, "设置界面字体大小", "字体大小（px）:", QLineEdit.Normal, "")
        if ok_pressed and font_size.isnumeric():
            font_size = int(font_size)
            self.setFont(QFont("Microsoft YaHei", font_size))

    def about(self, tag=None):
        """
        关于菜单的默认动作

        :return:
        """
        print(self.size())
        # QMessageBox.information(self, "关于", "Powered by open-source software", QMessageBox.Yes)
        dialog = QDialog()
        # 这个btn和上面的btn不是一个
        edit = QTextEdit()
        edit.setHtml('''
            <h1>lib4python<h1>
            <h2>yangke 1.6.3<h2>        
            <p>开发于PyCharm 2020.3.2 (Community Edition)<p>
            <p>构建与2021年03月05日<p>
            Runtime version: 11.0.9.1+11-b1145.63 amd64
            VM: OpenJDK 64-Bit Server VM by JetBrains s.r.o.
            Windows 10 10.0
            <p>Powered by open-source software<p>
        ''')
        # edit.setReadOnly(True)
        layout = QVBoxLayout(dialog)
        # dialog.setLayout()
        layout.addWidget(edit)

        dialog.setWindowTitle('关于')
        # 让对话框以模式状态显示，即显示时QMainWindow里所有的控件都不可用，除非把dialog关闭
        dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        dialog.resize(900, 300)
        dialog.exec()

    def help(self, tag=None):
        """
        帮助按钮的默认动作

        :return:
        """
        QMessageBox.information(self, "帮助", "暂不支持帮助", QMessageBox.Yes)


class YkItem(QWidget):
    def __init__(self, label="Label",
                 value=None, value_selected=None, value_validator=None,
                 unit=None, unit_selected=None,
                 size=None, **kwargs):
        """
        一种输入项，可以带下拉列表单位

        :param label:
        :param value:
        :param value_selected:
        :param unit:
        :param unit_selected:
        :param type: checkbox/None/textLine  -> kwargs
        :param checked: 复选框类型中，被选中的标签  -> kwargs
        :param labels: 复选框类型中，可选项的标签列表  -> kwargs
        """
        # noinspection PyArgumentList
        super(YkItem, self).__init__()
        self.type = kwargs.get("type")
        if self.type is None:
            self.label = _(label)
            self.value = None
            if value is not None:
                if isinstance(value, list):
                    self.value = QComboBox(self)
                    self.value.addItems(value)
                    self.value.setCurrentText(value_selected)
                else:
                    self.value = QLineEdit(str(value))
                    if value_validator is not None:
                        validator_types = value_validator.split(",")
                        if validator_types[0] == "int":
                            validator = QIntValidator(self.value)
                            validator.setRange(int(validator_types[1]), int(validator_types[2]))
                            self.value.setValidator(validator)
                            self.value.setPlaceholderText(value_validator)
                        elif validator_types[1] == "regexp":
                            validator = QRegExpValidator(self)
                            # todo 正则表达式设置QLineEdit的允许输入值
                            self.value.setValidator(validator)
            self.unit = None
            if unit is not None:
                if isinstance(unit, list):
                    self.unit = QComboBox(self)
                    self.unit.addItems(unit)
                    self.unit.setCurrentText(unit_selected)
            self.size = size
            self.init_ui()
        elif self.type == "checkbox":
            items = kwargs.get("items")
            checked = kwargs.get("checked")
            self.checkbox_layout = QHBoxLayout()

            self.label = label
            self.checkbox_layout.addWidget(QLabel(self.label))
            for item in items:
                checkbox = QCheckBox(item, self)
                if item in checked:
                    checkbox.setChecked(True)
                self.checkbox_layout.addWidget(checkbox)

            self.checkbox_layout.addStretch()
            self.value = self.checkbox_layout
            self.setLayout(self.checkbox_layout)
            # self.setStyleSheet("border:1px solid grey")

    def init_ui(self):
        # self.setPalette(QPalette(QtCore.Qt.red))
        # self.setAutoFillBackground(True)
        self.setMinimumSize(20, 5)

        h_box = QHBoxLayout()
        label = QLabel(self.label, self)
        # ----------------------------设置组件大小--------------------------------
        if self.size is not None:
            width = self.size.get("width")
            if isinstance(width, int):
                width = [width, width, width]
            if isinstance(width, list):
                if len(width) >= 1:
                    label.setFixedWidth(int(width[0]))
                if len(width) >= 2:
                    self.value.setFixedWidth(int(width[1]))
                if len(width) >= 3 and self.unit is not None:
                    self.unit.setFixedWidth(int(width[2]))
        # ----------------------------设置组件大小--------------------------------

        # noinspection PyArgumentList
        h_box.addWidget(label)
        # noinspection PyArgumentList
        h_box.addWidget(self.value)
        if self.unit is not None:
            h_box.addWidget(self.unit)
        # h_box.setSpacing(0)
        h_box.addStretch()
        self.setLayout(h_box)
        # self.setStyleSheet("background-color:green;padding:2;")

    def get_value(self):
        value = None
        if self.type is None or self.type.lower() == "textline":
            if isinstance(self.value, QLineEdit):
                value = self.value.text()
            elif isinstance(self.value, QComboBox):
                value = self.value.currentText()
            return value
        elif self.type.lower() == "checkbox":
            value = []
            for item in self.findChildren(QCheckBox):
                item: QCheckBox = item
                if item.isChecked():
                    value.append(item.text())
            return value

    def get_unit(self):
        unit = None
        if self.type is None or self.type.lower() == "textline":
            if self.unit is not None:
                unit = self.unit.currentText()
        return unit

    def get_value_and_unit(self):
        return self.get_value(), self.get_unit()

    def set_value(self, value):
        value = str(value)
        if isinstance(self.value, QLineEdit):
            self.value.setText(value)
        elif isinstance(self.value, QComboBox):
            self.value.setCurrentText(value)
        elif isinstance(self.value, QHBoxLayout):  # 说明是复选框
            for item in self.findChildren(QCheckBox):
                item: QCheckBox = item
                if item.text() in value:
                    item.setChecked(True)

    def set_unit(self, unit):
        if unit is not None:
            self.unit.currentText(unit)


# @auto_save_para  # 使用硬盘变量，即初始化为None的成员变量会以硬盘方式存储，任何改变都会直接写入硬盘
class InjectPanel(QWidget):
    def __init__(self):
        """
        初始化函数
        """
        # noinspection PyArgumentList
        super(InjectPanel, self).__init__()
        self.resize(800, 600)
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setAlignment(QtCore.Qt.AlignTop)
        # 硬盘变量行不要出现非注释用的“#”字符和多个”#“字符，否则可能会导致auto_save_para装饰器出错
        self.title = None  # 该变量会保存在硬盘上
        self.pid = None  # 初始化为0不是硬盘变量
        self.dll_path = None

        # 添加自定义部件（MyWidget）
        self.title_item = YkItem("目标窗口", self.title)
        self.pid_item = YkItem("目标进程", self.pid)
        self.dll_item = YkItem("待注入dll", self.dll_path)
        inject_btn = QPushButton("注入")
        inject_btn1 = QPushButton("注入")
        inject_btn2 = QPushButton("注入")

        h_box = QHBoxLayout()
        h_box.addStretch()
        # noinspection PyArgumentList
        h_box.addWidget(inject_btn)
        # noinspection PyArgumentList
        h_box.addWidget(inject_btn1)
        # noinspection PyArgumentList
        h_box.addWidget(inject_btn2)

        # 放入布局内
        # noinspection PyArgumentList
        layout.addWidget(self.title_item)
        # noinspection PyArgumentList
        layout.addWidget(self.pid_item)
        # noinspection PyArgumentList
        layout.addWidget(self.dll_item)
        layout.addStretch()
        layout.addLayout(h_box)

        self.setLayout(layout)
        # self.setStyleSheet("margin:2;padding:2")
        self.setWindowTitle("zr")
        self.show()
        inject_btn.clicked.connect(self.btn_clicked)

    def btn_clicked(self):
        sender = self.sender()
        if sender.text() == "注入":
            logger.debug("注入点击")
            zr_path = os.path.join(os.path.dirname(__file__), "zr.exe")
            if not os.path.exists(zr_path):
                logger.critical(f"zr.exe not found in {zr_path}")
            self.title = self.title_item.get_text_edit().text()
            windows_dict = find_window(self.title, exact=False)
            hwnds = [hwnd1 for hwnd1 in windows_dict.keys()]
            if len(windows_dict) == 0:
                logger.info(f"未找到窗口：{self.title}")
                return
            elif len(windows_dict) > 1:
                logger.warning(f"找到多个符合条件的窗口:{''.join(str(hwnds))}")

            hwnd = hwnds[0]
            title = windows_dict.get(hwnd)
            _, _pid = get_pid_by_hwnd(hwnd)
            self.pid = _pid
            self.dll_path = self.dll_item.get_text_edit().text()
            cmd = f'"{zr_path}" -pid {self.pid} -dll "{self.dll_path}"'
            runAsAdmin(cmd)


def layout_to_widget(layout):
    """
    讲PyQt5中的layout转换为Widget。
    用于：
    在QSplitter中添加内容时，只能使用QWidget类对象，如果是用户创建的QVBoxLayout内容，则无法添加，可以使用该方法转换后添加。

    :param layout:
    :return:
    """

    class YKWidget(QWidget):
        def __init__(self):
            super(YKWidget, self).__init__()
            self.setLayout(layout)

    widget = YKWidget()
    return widget


def QYKFigure(x=None, y=None, xlim=None, ylim=None,
              fig_type=None, figsize=None, dpi=None, facecolor=None, edgecolor=None,
              linewidth=0.0,
              frameon=None, subplotpars=None, tight_layout=None, constrained_layout=None,
              title=None, xlabel=None):
    """
    在PyQt5面板中绘制matplotlib图形，该方法返回一个QWidget图形对象

    :param ylim: (bottom: float, top: float)
    :param xlim: (bottom: float, top: float)
    :param xlabel:
    :param x:
    :param y:
    :param fig_type: scatter/bar/hist/curve
    :param figsize:
    :param dpi:
    :param facecolor:
    :param edgecolor:
    :param linewidth:
    :param frameon:
    :param subplotpars:
    :param tight_layout:
    :param constrained_layout:
    :param title:
    :return:
    """
    import matplotlib
    matplotlib.use("Qt5Agg")
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.font_manager import _rebuild
    import matplotlib.pyplot as plt
    from matplotlib.axes._subplots import Axes

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    import numpy as np

    _rebuild()

    class Qt5Figure(FigureCanvas):
        def __init__(self, figsize=None, dpi=None, facecolor=None, edgecolor=None, linewidth=0.0,
                     frameon=None, subplotpars=None, tight_layout=None, constrained_layout=None):
            self.figure = Figure(figsize=figsize, dpi=dpi, facecolor=facecolor, edgecolor=edgecolor,
                                 linewidth=linewidth, frameon=frameon, tight_layout=tight_layout,
                                 subplotpars=subplotpars, constrained_layout=constrained_layout)

            # 在父类中激活Figure窗口，此句必不可少，否则不能显示图形
            super(Qt5Figure, self).__init__(self.figure)
            self.axes: Axes = self.figure.add_subplot(111)
            if title is not None:
                self.figure.suptitle(title)
            self.axes.set_xlabel(xlabel)
            self.axes.set_ylim(auto=True)
            self.axes.set_xlim(auto=True)
            self.axes.grid(axis="both", color="y", linestyle=":", linewidth=1)

            if fig_type is not None:
                if fig_type == "scatter":
                    self.scatter(x, y)
                elif fig_type == "bar":
                    self.bar(x, y)
                elif fig_type == "hist":
                    self.hist(x)
                elif fig_type == "curve":
                    self.curve(x, y)
            else:
                self.curve(x, y)
            # self.figure.tight_layout()

        def add_fig(self, fig_type, x=None, y=None, **kwargs):
            """
            在当前图中添加图。
            一般用于同一个坐标系多条曲线的情况，添加第二条曲线时即可使用该方法。

            :param fig_type: 新图的类型，curve/scatter/bar/hist
            :param x:
            :param y:
            :return:
            """
            if fig_type == "scatter":
                self.scatter(x, y, **kwargs)
            elif fig_type == "bar":
                self.bar(x, y, **kwargs)
            elif fig_type == "hist":
                self.hist(x, **kwargs)
            elif fig_type == "curve":
                self.curve(x, y, **kwargs)
            self.figure.tight_layout()

        def curve(self, x, y, **kwargs):
            if isinstance(x, float) or isinstance(x, int):
                x = [x]
            if isinstance(y, float) or isinstance(y, int):
                y = [y]
            self.axes.plot(x, y, **kwargs)

        def scatter(self, x, y, **kwargs):
            """
            散点图
            :param x:
            :param y:
            :return:
            """
            if isinstance(x, float) or isinstance(x, int):
                x = [x]
            if isinstance(y, float) or isinstance(y, int):
                y = [y]
            x = np.array(x)
            y = np.array(y)
            if x.shape != y.shape:
                if x.shape[0] == y.shape[0]:
                    x = np.repeat(x, y.shape[1])
                elif x.shape[0] == y.shape[1]:
                    x = np.tile(x, y.shape[0])
                y = y.flatten()
            if x.shape != y.shape:
                raise ValueError("散点图的数据列表长度不等，且无法扩展到相同维度")
            self.axes.scatter(x, y, **kwargs)

        def bar(self, x, y, **kwargs):
            """
            柱状图
            :param x: 列表或数值
            :param y: 列表或数值
            :return:
            """
            if isinstance(x, float) or isinstance(x, int):
                x = [x]
            if isinstance(y, float) or isinstance(y, int):
                y = [y]
            self.axes.bar(x, y, **kwargs)

        def hist(self, value, bins=10):
            """
            直方图
            :param value:
            :param bins:
            :return:
            """
            self.axes.hist(value, 10)

        def show_control_panel(self):
            """
            显示图片的控制面板

            :return:
            """
            # todo
            pass

        def hide_control_panel(self):
            """
            隐藏控制面板

            :return:
            """
            # todo
            pass

    return Qt5Figure()


def set_menu_bar(window: QMainWindow, from_file="ui_menu.yaml"):
    """
    根据ui_menu.yaml文件定义的菜单栏菜单项信息设置window窗口的菜单栏

    ui_menu.yaml示例文件
------------------------------------------------------------------------------------
menu:
  - # 第一个菜单ribbon
    name: "文件"
    items:
      - action_name: "设置数据文件"
        short_cut: "Ctrl+Q"
        connect: "self.set_data_file"
  - # 种群图类型
    name: "设置"
    items:
      - action_name: "计算设置"
        connect: "self.set_calculate"
      - action_name: "遗传算法设置"
        connect: "self.set_algorithm"
      - action_name: "图像显示设置"
        connect: "self.set_display"
  -
    name: "帮助"
    items:
      - action_name: "关于"
      - action_name: "帮助"
------------------------------------------------------------------------------------

    :param window:
    :param from_file:
    :return:
    """
    menu_bar = window.menuBar()
    menus = get_settings("menu", setting_file=from_file)
    for ribbon in menus:
        temp_ribbon = menu_bar.addMenu(_(ribbon.get("name")))
        actions = ribbon.get("items")
        for item in actions:
            temp_action = QAction(item.get("action_name"), window)
            if item.get("short_cut") is not None:
                temp_action.setShortcut(item.get("short_cut"))
            temp_connect: str = item.get("connect")
            if temp_connect is not None:
                if temp_connect.startswith("self."):
                    temp_connect = temp_connect.replace("self.", "")
                temp_action.triggered.connect(eval(f"window.{temp_connect}"))
            temp_ribbon.addAction(temp_action)


logger.debug("加载YkDataTableWidget")


class YkDataTableWidget(QTableWidget):
    """
    数据表格组件，配置的table_data.yaml文件参见ui/table_data1.yaml;ui/table_data2.yaml;table_data_single_calculate.yaml

以下yaml文件内容向表格中添加一个按钮，按钮链接表格组件的self.single_calculate方法
---------------------- table.yaml ----------------------
button:
  - name: "计算"
    range: "(2,4)"  # 按钮位于表格的第三列四行
    connect: "self.single_calculate"
--------------------------------------------------------
    self.single_calculate方法必须先传入，然后初始化，例如：
---------------------- example.py ----------------------
def calculate:
    # calculate中需要完成的操作
    pass

YkDataTableWidget.single_calculate = calculate
table_widget = YkDataTableWidget(from_file = "table.yaml")
--------------------------------------------------------
    """

    def __init__(self, from_file="table_data.yaml", **kwargs):
        super(YkDataTableWidget, self).__init__()
        if not os.path.exists(from_file):
            logger.warning(f"YkDataTableWidget的数据设置文件<{from_file}>未找到，请确定文件路径是否正确！")

        settings = get_settings(setting_file=from_file)
        data = settings.get("data") or {}
        buttons = settings.get("button") or {}
        width1 = settings.get("width")

        self.columns = 20
        self.rows = 100
        self.setRowCount(self.rows)
        self.setColumnCount(self.columns)
        # 初始化var_loc用于存储表格中记录的数值，格式为：
        # {"title_1": {"label_1": (x_left_top, y_left_top), "label_2": (x1, y1)}, "title_2": {}, ...}
        # 对应table_data.yaml的格式
        self.var_loc = {}
        self.buttons = {}
        for domain in data:
            title = domain.get("title")
            # -------------------- 处理range参数，生成可以直接使用的x0,y_left_top,width,rows-------------------------------
            domain_range = eval(domain.get("range")) or (0, 0)
            x_left_top, y_left_top, width, height = (0, 0, 3, 0)
            if len(domain_range) == 2:
                x_left_top, y_left_top = domain_range
            elif len(domain_range) == 3:
                x_left_top, y_left_top, width = domain_range
            elif len(domain_range) == 4:
                x_left_top, y_left_top, width, height = domain_range
            # -------------------- 处理range参数，生成可以直接使用的x0,y_left_top,width,rows-------------------------------
            # -------------------- 处理background/foreground/align参数 -------------------------------
            background = domain.get("background") or "#ffffff"
            foreground = domain.get("foreground") or "#000000"
            if background.startswith("QBrush"):
                background = eval(background)
            else:
                background = QBrush(QColor(background))
            if foreground.startswith("QBrush"):
                foreground = eval(foreground)
            else:
                foreground = QBrush(QColor(foreground))
            row_index, col_index = y_left_top, x_left_top
            if title is not None:  # 表格中的小分区
                items = domain.get("items")
                height = len(items)

                if height == 0:
                    height = len(items)
                self._set_row_column_count(x_left_top, y_left_top, width, height)
                align = self._get_align(item_dict=domain, default="AlignCenter")

                # -------------将表格第一行单元格合并，并将标题内容填入第一行，且设置第一行style----------------
                self.setSpan(row_index, col_index, 1, width)
                self.setItem(row_index, col_index, QTableWidgetItem(title))
                self.item(row_index, col_index).setBackground(
                    background)  # 这里itemAt()用来设置颜色只有第一条设置语句有效，后续无效，测试发现item()函数可用
                self.item(row_index, col_index).setForeground(foreground)
                self.item(row_index, col_index).setTextAlignment(align)
                self.var_loc[title] = {}
                # -------------将表格第一行单元格合并，并将标题内容填入第一行，且设置第一行style----------------
                # --------------------------填充数据行内容------------------------------
                for i, item in enumerate(items):
                    label = item.get("label") or ""
                    value = item.get("value") or ""
                    unit = item.get("unit") or ""
                    x = row_index + i + 1
                    merge_label = item.get("merge_label_row_col")
                    if merge_label is not None:
                        merge_row, merge_col = eval(merge_label)
                        self.setSpan(x, col_index, merge_row, merge_col)
                    merge_value = item.get("merge_value_row_col")
                    if merge_value is not None:
                        merge_row, merge_col = eval(merge_value)
                        self.setSpan(x, col_index + 1, merge_row, merge_col)
                    self.setItem(x, col_index, QTableWidgetItem(label))
                    self.setItem(x, col_index + 1, QTableWidgetItem(value))
                    self.setItem(x, col_index + 2, QTableWidgetItem(unit))
                    self.var_loc[title].update({label: (x, col_index + 1)})
                # --------------------------填充数据行内容------------------------------
                # --------------------------设置数据行格式------------------------------
                for i in range(1, height + 1):
                    x = row_index + i
                    self.item(x, col_index).setBackground(background)
                    self.item(x, col_index).setForeground(foreground)
                    self.item(x, col_index + 1).setBackground(background)
                    self.item(x, col_index + 1).setForeground(foreground)
                    self.item(x, col_index + 2).setBackground(background)
                    self.item(x, col_index + 2).setForeground(foreground)
                # --------------------------设置数据行格式------------------------------
            else:
                label = domain.get("label")
                value = domain.get("value")
                unit = domain.get("unit")
                if height == 0:
                    height = 1
                self._set_row_column_count(x_left_top, y_left_top, width, height)
                merge_label = domain.get("merge_label_row_col")
                merge_row_label, merge_col_label = 1, 1
                if merge_label is not None:
                    merge_row_label, merge_col_label = eval(merge_label)
                    self.setSpan(row_index, col_index, merge_row_label, merge_col_label)
                merge_value = domain.get("merge_value_row_col")
                merge_row_value, merge_col_value = 1, 1
                if merge_value is not None:
                    merge_row_value, merge_col_value = eval(merge_value)
                    self.setSpan(row_index, col_index + 1, merge_row_value, merge_col_value)

                align = self._get_align(domain, "AlignLeft")

                # --------------------------------- 按照参数类型添加不同组件 ---------------------------------
                if isinstance(value, bool):  # 如果参数取值为bool类型，则使用QCheckBox组件就可以很好的满足要求
                    check_box = QCheckBox(label)
                    check_box.setChecked(value)
                    self.setSpan(row_index, col_index, merge_row_label, merge_col_label)
                    self.setCellWidget(row_index, col_index, check_box)
                else:
                    self.setItem(row_index, col_index, QTableWidgetItem(label))
                    self.setItem(row_index, col_index + merge_col_label, QTableWidgetItem(value))
                    self.setItem(row_index, col_index + merge_col_label + merge_col_value, QTableWidgetItem(unit))
                # --------------------------------- 按照参数类型添加不同组件 ---------------------------------

                # --------------------------------- 按照参数类型更新参数所在的位置 ---------------------------------
                if isinstance(value, bool):  # 布尔型设置项的取值就是布尔型组件本身的坐标
                    self.var_loc.update({label: (row_index, col_index)})
                else:
                    self.item(row_index, col_index).setTextAlignment(align)
                    self.item(row_index, col_index).setBackground(background)
                    self.item(row_index, col_index).setForeground(foreground)
                    self.item(row_index, col_index + merge_col_label).setBackground(background)
                    self.item(row_index, col_index + merge_col_label).setForeground(foreground)
                    self.item(row_index, col_index + merge_col_label + merge_col_value).setBackground(background)
                    self.item(row_index, col_index + merge_col_label + merge_col_value).setForeground(foreground)
                    self.var_loc.update({label: (row_index, col_index + merge_col_label)})
                # --------------------------------- 按照参数类型更新参数所在的位置 ---------------------------------
        for button in buttons:
            name = button.get("name")
            q_btn = QPushButton(name)
            col_index, row_index = eval(button.get("range"))
            self.setCellWidget(row_index, col_index, q_btn)
            if button.get("connect") is not None:
                func = eval(button.get("connect"))
                q_btn.clicked.connect(func)

            self.buttons.update({name: q_btn})

        if width1 is not None:
            width1 = eval(width1)
            for i, w in enumerate(width1):
                self.setColumnWidth(i, w)

    def _set_row_column_count(self, x, y, width, height):
        """
        根据小区域的大小和位置设置表格宽高，保证表格可以容纳整个小区域

        :param x:
        :param y:
        :param height:
        :param width:
        :return:
        """
        # 设置表格长宽
        if width + x > self.columns:
            self.columns = width + x
            self.setColumnCount(self.columns)
        if height + y > self.rows:
            self.rows = height + y
            self.setRowCount(self.rows)

    @staticmethod
    def _get_align(item_dict, default="AlignCenter"):
        """
        从当前字典中获取align值，如果不存在，则生成default对应的align值，返回QtCore.Qt.AlginCenter等对象

        :param item_dict:
        :param default:
        :return:
        """
        align = item_dict.get("align") or "AlignCenter"
        if align.startswith("Qt"):
            align = eval(f"QtCore.{align}")
        elif align.startswith("QtCore"):
            align = eval(align)
        else:
            align = eval(f"QtCore.Qt.{align}")
        return align

    def get_var_location(self, var_name: str):
        """
        获取某个变量在表格中的位置
        :param var_name: 参数名称，如果表格时按照小区域分割的，则参数名称以 domain.label 的格式传入
        :return: tuple(x,y)
        """
        var_name = var_name.split(".")
        temp = self.var_loc
        for lvl in var_name:
            temp = temp.get(lvl)
            if isinstance(temp, tuple):
                return temp
        print("所查找的变量不存在")
        return -1, -1

    def set_value(self, var_name: str, value=""):
        """
        设置表格中某个参数的值
        :param var_name: 参数名称，如果表格时按照小区域分割的，则参数名称以 domain.label 的格式传入
        :param value: 需要设置的值
        :return:
        """
        x, y = self.get_var_location(var_name)
        if x != -1:  # 说明存在制定字符串对应的变量
            if type(value) == bool:  # 布尔型变量设置checked状态
                self.cellWidget(x, y).setChecked(value)
            else:
                value = str(value)
                self.item(x, y).setText(value)  # 不能使用setItem()方法，否则会改变单元格样式
        else:
            logger.debug(f"{var_name}未找到")

    def get_value(self, var_name: str):
        """
        获取表格中某个参数的值
        :param var_name: 参数名称，如果表格时按照小区域分割的，则参数名称以 domain.label 的格式传入
        :return:
        """
        x, y = self.get_var_location(var_name)
        try:
            # 常规的文本类型直接返回text即可
            result = self.item(x, y).text()
        except AttributeError:  # 可能是QCheckBox类型，需要返回是否选中的bool值
            result = self.cellWidget(x, y)
            result = result.isChecked()
        return result

    def get_button(self, name):
        """
        根据按钮的文字获取按钮对象
        :param name:
        :return:
        """
        q_btn = self.buttons.get(name)
        return q_btn

    def display_dataframe(self, df: pd.DataFrame, row_index: int = 0, col_index: int = 0,
                          index="", header="", digits=None):
        """
        将pandas的DataFrame数据显示到YkDataTableWidget上

        :param df:
        :param df: dataframe数据
        :param row_index: 显示区域左上角的行索引
        :param col_index: 显示区域左上角的列索引
        :param index: 是否写入df的行标题，默认是写入的。如果是None，则不写入。
        :param header: 是否写入df的列标题，默认是写入原标题的。如果是None，则不写入。
        :param digits: 数据类型的最大小数点后显示位数
        :return:
        """
        if index is not None:
            df1 = df.reset_index()
        else:
            df1 = df
        if self.rowCount() < row_index + df1.shape[0] + 1:
            self.setRowCount(row_index + df1.shape[0] + 20)
        if self.columnCount() < col_index + df1.shape[1] + 1:
            self.setColumnCount(row_index + df1.shape[0] + 20)
        values = df1.values

        if header is not None:
            for j, col_name in enumerate(df1.columns):
                # setItem(row_index, col_index, QTableWidgetItem(label))
                self.setItem(row_index, j, QTableWidgetItem(str(col_name)))
            row_index = row_index + 1
        for i, row in enumerate(values):
            for j, cell in enumerate(row):
                cell = str(cell).strip()
                x = row_index + i
                y = col_index + j
                if is_number(cell) and digits is not None:
                    cell = str(round(float(cell), digits))
                self.setItem(x, y, QTableWidgetItem(cell))


def YkInputPanel(parent=None, from_file="ui_data.yaml", domain=None, return_type="widget",
                 values: list = None):
    """
    输入框面板

    # 输入界面类型一般如下：
    --------------------------------------
    |  <label1>  <textField1> <unit1>    |
    |  <label2>  <textField2> <unit2>    |
    |  <label3>  <textField3> <unit3>    |
    |                                    |
    |          <btn_apply>   <btn_ok>    |
    --------------------------------------

    实例ui_data.yaml文件
----------------------------------------------------------------
size:
  width:
    - 160  # <label>的宽度
    - 140  # <textField>的宽度
    - 80  # <unit>的宽度
algorithm:
  inputArea:
    - # 第一个设置项
      label: "种群大小"
      value: 50
    - # 第二个设置项
      label: "遗传代数"
      value: 200
  buttons:
    - # 第一个按钮
      text: "应用"
      on_click: "btn_clicked"  # 按钮点击触发的事件
    - text: "确定"
      on_click: "btn_clicked"  # 按钮点击触发的事件
----------------------------------------------------------------

    :param parent: 父组件，当有按钮时，必须传入父组件，因为按钮事件需要绑定父组件的方法
    :param values: 输入框的显示值，如果不设置，则为默认的初始值，设置的话必须一一对应每一个值，不能省略
    :param domain: ui定义文件中的选项，一个ui文件中中可以定义多个输入面板，该值表示选用哪个
    :param from_file: ui定义文件
    :param return_type: layout/widget，返回的类型，只有返回widget类型时，才拥有取值的方法
    :return:
    """
    if domain is None:  # 则将domain设置为第一个有inputArea的组件面板
        settings = get_settings(setting_file=from_file)
        for k, v in settings.items():
            if v.get("inputArea") is not None:
                domain = k
    if domain is None:
        return None
    settings = get_settings(domain, setting_file=from_file)
    inputArea = settings.get('inputArea')
    size = get_settings("size", setting_file=from_file)
    yk_items = []
    for i, item in enumerate(inputArea):
        if values is not None:
            item["value"] = values[i]  # 用调用方法传入的默认值替换ui文件中的默认值
        yk_items.append(YkItem(size=size, **item))

    btn_box = QHBoxLayout()
    btn_box.addStretch()
    for btn in settings.get('buttons'):
        btn1 = QPushButton(btn.get('text'))
        connected = f"parent.{btn.get('on_click')}"
        btn1.clicked.connect(eval(connected))
        btn_box.addWidget(btn1)

    v_box = QVBoxLayout()
    for item in yk_items:
        v_box.addWidget(item)
    v_box.addStretch()
    v_box.addItem(btn_box)

    class Panel(QWidget):
        def __init__(self):
            super(Panel, self).__init__()
            self.setLayout(v_box)
            self.name = domain
            self.values = []
            self.units = []

        def get_values_and_units(self, need_unit=True, need_dict=False):
            """
            获取YkInputPanel对象的数值和单位

            :param need_unit: 是否需要单位，不需要则只返回数值
            :param need_dict: 是否需要返回dict类型的数据，默认返回列表类型数据
            :return:
            """
            if not need_dict:
                self.values = []
                self.units = []
                for it in yk_items:
                    self.values.append(it.get_value())
                    self.units.append(it.get_unit())
                if need_unit:
                    return self.values, self.units
                else:
                    return self.values
            else:
                value_dict = {}
                unit_dict = {}
                for it in yk_items:
                    value_dict.update({it.label: it.get_value()})
                    unit_dict.update({it.label: it.get_unit()})
                if need_unit:
                    return {"value": value_dict, "unit": unit_dict}
                else:
                    return value_dict

        def set_values(self, values=None):
            """
            设置输入面板中各项的值（按顺序）

            :param values: 值的列表，或｛label:value｝的字典
            :return:
            """
            if values is None:
                return
            if isinstance(values, dict):
                for it in yk_items:
                    if it.label in values.keys():
                        it.set_value(values[it.label])
            elif isinstance(values, list):
                for i, it in enumerate(yk_items):
                    it.set_value(values[i])

    if return_type == "widget":
        return Panel()
    else:
        return v_box


if __name__ == "__main__":
    app = QApplication(sys.argv)

    w1 = InjectPanel()
    sys.exit(app.exec_())
