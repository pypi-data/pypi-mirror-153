import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import PyQt5.QtCore as QtCore
import iapws


class YkWindow(QMainWindow):
    def __init__(self):
        # noinspection PyArgumentList
        super(YkWindow, self).__init__()
        self.toolbar = None
        self.init_ui()

    def init_ui(self):
        button1 = QPushButton("new")

        self.setGeometry(300, 300, 600, 500)
        self.setWindowTitle("yk demo")
        # self.setWindowIcon(QIcon('web.png'))
        self.center()
        self.statusBar().showMessage('Ready')
        self.show()

    def button_clicked(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + ' was pressed')

    def center(self):
        qr = self.frameGeometry()  # 获得窗口
        cp = QDesktopWidget().availableGeometry().center()  # 获得屏幕中心点
        qr.moveCenter(cp)
        self.move(qr.topLeft())


app = QApplication(sys.argv)
w1 = YkWindow()
sys.exit(app.exec_())
