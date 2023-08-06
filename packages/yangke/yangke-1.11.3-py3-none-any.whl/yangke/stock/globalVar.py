"""
定义全局变量的模块
程序使用的所有全局变量定义在这里
python模块自动是单例模式，因此，在多个py文件中引用该模块，多个py模块中的变量对象是同一个
"""
from yangke.stock.dataset.tushareData import StockData
import logging
import argparse
import os
import pickle
from pymysql.cursors import Cursor
from sqlalchemy.engine.base import Engine

encoding = 'utf-8'
logger: logging.Logger = None  # 日志输出类，这里表明对象所属的类，则使用时pycharm会提示类对应的方法
dataDirectory: str = None  # 股票数据存储的目录
tsd: StockData = None  # StockData类的对象，其构造函数会初始化tushare账户的口令
debugMode: str = None  # 程序运行模式，调试模式需要在命令行参数添加"--debug"，不加则默认没有调试信息输出
command: str = None  # 调用程序的命令
symbol: str = None  # 操作哪只股票，symbol对应股票代码
cursor: Cursor = None  # 操作mysql数据库的游标
mysql_engine: Engine = None
storage = "mysql"  # 数据的存储方式，默认是mysql，也可以取值为"file"，表示本地存储

namespace = argparse.Namespace()


class RunState:
    """
    储存一些软件运行状态参数
    """

    def __init__(self, last_update_time=None, stocks=None):
        # -------------- 最后更新的股票列表和更新时间 ----------------
        self.stocks = stocks
        self.last_update_time = last_update_time
        # -------------- 最后更新的股票列表和更新时间 ----------------

        folder = os.path.join(dataDirectory, 'state')
        self.file = os.path.abspath(os.path.join(folder, 'RunState'))

    def load(self):
        if os.path.exists(self.file):
            with open(self.file, 'rb') as f:
                state = pickle.load(f)
        else:
            return self
        return state

    def dump(self):
        os.makedirs(os.path.dirname(self.file), exist_ok=True)
        with open(self.file, 'wb') as f:
            pickle.dump(self, f, 0)

    def __repr__(self):
        return str(self.__dict__)


def test():
    state = RunState()
    state.__setattr__('code', 'updated')  # 可以动态向RunState中添加属性
    print(state)

    state.dump()

    state1 = RunState().load()
    print(state1)
