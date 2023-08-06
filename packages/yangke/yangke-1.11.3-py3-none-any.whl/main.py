"""
lib4python库的总入口，所有的子模块可以由此处启动
"""
import sys
import os

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QAction, QMainWindow, QLabel

from yangke.base import get_settings
from yangke.common.qt import YkWindow, set_menu_bar
from yangke.common.config import logger

# 国际化
import gettext
from babel import Locale

gettext.install('main', 'locale')  # 将 _() 函数全局安装到内建命名空间中，使得所有模块都可以调用
locale = Locale.parse('zh_CN')


def init_get_text(domain=None):
    """
    国际化设置，使得各国语言包可以加载

    :param domain:
    :return:
    """
    if domain is None:
        domain = os.path.basename(__file__).split(".")[0]
    locale_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locale')
    gettext.bindtextdomain(domain, locale_dir)
    gettext.textdomain(domain)
    gettext.find(domain, "locale", languages=["zh_CN", "en_US"])
    return gettext.gettext


class MainFrame(YkWindow):
    def __init__(self, setting_file=os.path.abspath("settings.yaml")):
        # super(MainFrame, self).__init__(setting_file)
        super(MainFrame, self).__init__()
        self.w = None

    def init_ui(self):
        set_menu_bar(self, "config/ui_menu.yaml")

    def init_mysql(self):
        super(MainFrame, self).init_mysql(ui_file=os.path.abspath("config/ui_mysql_config.yaml"))

    def start_program(self):
        """
        根据菜单项启动对应的软件

        :return:
        """
        if isinstance(self.sender(), QAction):
            if 'HPD' in self.sender().text():
                command = "start_hpd"
            elif self.sender().text() == "DP(性能试验)":
                command = "start_dp"
            elif self.sender().text() == "热力系统图":
                command = "start_system_figure"

        if command == "start_dp":
            from yangke.performance.data_process import MainWindow
            self.w = MainWindow()
        elif command == "start_hpd":
            from yangke.performance.heat import MainWindow
            self.w = MainWindow()
        elif command == "start_system_figure":
            self.w = QMainWindow(parent=self)  # 共享父类的app.exec_方法
            self.w.setCentralWidget(QLabel("测试"))
            self.w.show()

        self.w.setFont(QFont("Microsoft YaHei", 12))


init_get_text()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w1 = MainFrame()
    sys.exit(app.exec_())
