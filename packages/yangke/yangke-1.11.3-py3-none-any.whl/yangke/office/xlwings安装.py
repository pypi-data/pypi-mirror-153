"""
1.安装office
2.pip install xlwings
3.xlwings addin install
4.在excel中xlwings下设置python解释器的路径
5.有必要的在excel中xlwings下设置模块的路径和需要引入的模块名

"""
import os
from yangke.base import find_file


def auto_set():
    """
    将python路径设置
    自动设置xlwings
    :return:
    """
    user_dir = os.path.expanduser("~")
    settings_file = find_file("*/xlwings.conf", user_dir)
    if len(settings_file) == 0:
        print("未找到xlwings的设置文件")
        return False
    setting_file = settings_file[0]
