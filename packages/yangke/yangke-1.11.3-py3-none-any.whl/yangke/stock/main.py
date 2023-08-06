"""
股票功能的入口文件
"""
import os

import yangke.stock.globalVar as gv  # 所有的全局变量定义在该模块中，使用全局变量需要引入该模块
from yangke.stock.dataset.tushareData import StockData
import io
from yangke.common.config import *
from yangke.common.mysql import *
from yangke.common.crawler import start_scrapy_start

from yangke.stock.db_tables_schema import holiday_table, symbols_table


def config_program():
    """
    配置项目相关的文件夹路径、项目架构等信息
    这里定义全局变量
    :return:
    """
    # 设置标准输出流数据格式为utf-8，否则在java中调用输出的中文是乱码
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')  # 不同系统甚至不同开发环境中sys.stdout都可能不同
    except AttributeError:  # IDLE中，sys.stdout对象没有buffer属性
        logger.info("sys.stdout没有buffer属性，IDLE的默认输出会出现该问题")
    # -----------------初始化所有全局变量-----------------
    res = connect_mysql(user='root', passwd='111111', db='stocks', return_type="engine", use_pymysql=False)
    # res = connect_mysql(host="rm-bp1bjlvw6u3pmo742bo.mysql.rds.aliyuncs.com", user="yangke007",
    #                     passwd="YangKe08", db='stocks', return_type="engine")
    if res is None:
        logger.warning('数据库连接失败')
        gv.storage = "file"
    else:
        gv.mysql_engine = res

    # 处理命令行参数
    # 调用示例：python sis_io.py -c debug --symbol 600006 --debug
    args_define = {"kv": [
        {"short": 'c', "long": "command", "default": "debug"},
        {"short": 's', "long": "symbol", "default": "600006"},

    ], 'k': [
        {'short': 'd', 'long': 'debug', 'default': True, 'description': 'run in debug mode'}
    ]
    }
    args = get_args(args_name=args_define)
    if args is None:
        print("未传入配置参数，使用默认参数'-s 600007 --debug'")
        gv.command, gv.symbol, gv.debugMode = 'debug', '600006', True
    else:
        try:
            gv.command, gv.symbol, gv.debugMode = args.command, args.symbol, args.debug
        except AttributeError:
            print(f"传入参数{args}错误，使用默认参数'-s 600007 --debug'")
            gv.command, gv.symbol, gv.debugMode = 'debug', '600006', True
    if gv.debugMode:
        gv.logger = initLogger(logging.DEBUG)
        holdLoggingLevel(logging.DEBUG, outer=False)  # paddle会覆盖configLogging(logging.DEBUG)的设置，用该方法顶掉paddle的日志设置
    else:
        gv.logger = initLogger(logging.WARNING)
        holdLoggingLevel(logging.WARNING, outer=False)  # paddle会覆盖configLogging(logging.WARNING)的设置

    # gv.dataDirectory = os.path.split(os.path.realpath(__file__))[0]  # 这个是该文件所在的路径
    # gv.dataDirectory = os.path.dirname(gv.dataDirectory)
    gv.dataDirectory = os.getcwd()  # 使用项目所在的目录作为数据储存目录，以便可以在项目删除时方便的删除数据文件
    gv.dataDirectory = os.path.join(gv.dataDirectory, "StockData")
    if not os.path.exists(gv.dataDirectory):
        os.mkdir(gv.dataDirectory)
    if gv.storage == "file":
        gv.tsd = StockData(gv.dataDirectory)
        gv.logger.debug("股票数据存储目录：" + gv.dataDirectory)
    else:
        # 初始化假日数据表
        if not has_table("holiday"):
            # 如果节假日日历数据表不存在，则创建
            create_table(cursor=gv.mysql_engine, metadata=holiday_table)
        # 初始化符号数据表
        if not has_table("symbols"):
            create_table(cursor=gv.mysql_engine, metadata=symbols_table)

        # 股票交易数据和新闻的表无法提前初始化，因为必须知道股票代码才能创建对应的表
        gv.tsd = StockData(gv.dataDirectory, mysql_engine=res)
        gv.logger.debug("股票数据存储于mysql数据库")
    # -----------------初始化所有全局变量-----------------

    # 判断相关库是否安装
    # if existModule("tushare"):
    #     import tushare as ts
    #     gv.logger.debug("检测到tushare {}已经安装！".format(ts.__version__))
    # if existModule("tensorflow"):
    #     import tensorflow as tf
    #     gv.logger.debug("检测到tensorflow {}已经安装！".format(tf.__version__))
    # if existModule("paddle"):
    #     import paddle
    #     gv.logger.debug("检测到paddle {}已经安装！".format(paddle.__version__))
    # if existModule("torch"):
    #     import torch
    #     gv.logger.debug("检测到pytorch {}已经安装！".format(torch.__version__))


def start():
    # 程序全局设置
    config_program()

    start_time = datetime.datetime.now()  # 用来统计执行时间

    if gv.command == "download":
        gv.tsd.download(gv.symbol, append=True)

    elif gv.command == "getName":
        gv.tsd.get_name()

    elif gv.command == "getOpenLimitUp":
        gv.tsd.get_open_limit('up')

    elif gv.command == "getOpenLimitDown":
        gv.tsd.get_open_limit_and_lastdays('down')

    elif gv.command == "getSymbols":
        symbols = gv.tsd.get_all_stock_symbol()  # 会生成allsymbols.csv
        # for symbol in symbols:#传递参数太多，不适合outputStream传递，使用硬盘文件传递
        #     print("py to java:{}".format(symbol))
        # print(np.array(symbols))

    elif gv.command == "getStockNum":
        symbols = gv.tsd.get_all_stock_symbol()
        print("共有 {} 只股票".format(len(symbols)))

    elif gv.command == "getNewStocks":
        # 查询当前所有正常上市交易的股票列表 ts_code     symbol     name     area industry    list_date(上市日期)
        data = gv.tsd.api.query('stock_basic', exchange='', list_status='L',
                                fields='ts_code,symbol,name,area,industry,list_date')
        sortedData = data.sort_values(by="list_date", ascending=False)
        for index, row in sortedData[0:20].iterrows():
            print(row["list_date"], row["name"], row["area"], row["industry"], row["symbol"])

    elif gv.command == "getBottomOut":
        symbols, _ = gv.tsd.get_bottom_out(int(gv.symbol))
        print("{}天内触底反弹股票列表如下：".format(gv.symbol))
        print(symbols)

    elif gv.command == "debug":
        gv.tsd.download(gv.symbol, append=True)
        # tsd.download_daily(date.today())
        # gv.tsd.get_open_limit()
        # gv.tsd.get_bottom_out(10)
        # logging.debug("最后一个交易日：{}".format(tsd.get_last_working_day()))
        # logging.debug("查询股票{}今天的交易数据：".format(symbol, tsd.get_data_of_day(symbol)))
        # gv.logger.debug("目前上市的股票代码：\n{}".format(pd.Series(gv.tsd.get_all_stock_symbol())))
        # gv.logger.debug("最近的工作日列表:\n{}".format(pd.Series(gv.tsd.get_last_n_working_day(30))))
        # tsd.get_open_limit_of_n_trading_days(30, 'up', 'ascend')
        # gv.tsd.get_open_limit_of_n_trading_days(30, 'down', 'ascend')
        # gv.tsd.get_open_limit_and_lastdays(last_date=datetime.date.fromisoformat("2019-12-31"))
        # gv.tsd.recent_30_open_limit_down_to_file(days=30)

        # 模拟交易
        symbols = gv.tsd.get_all_stock_symbol()
        # db.test1()
        # Main.test1()

        # 神经网络预测
        # pad.test1()
        # pad.test2()
        # pad.test3()
        # pad.test4()
        # datafile = os.path.join(gv.dataDirectory, gv.symbol + '.csv')
        # pps.prediction1(datafile)

        # import prediction.pytorch_pred as ptp
        # ptp.start_mysql_service()

        import yangke.stock.prediction.pytorch_pred_stock as ptps

        ptps.lstm_stock_use_in_build_rnn_fit(gv.symbol)
        # ptps.lstm_stock_classify(gv.symbol)

        # start_mysql_service()

        start_scrapy_start(r"start_stock10jqka.py")
        # start_scrapy_spider(r"jqka_spider.py")  # 因为在start_stock10jqka.py中还初始化了数据库，因此只能从start_...开始执行爬虫

        # stocks = gv.tsd.download_all_stocks(exclude=['000029', '600145', '688086', '601696'])  # 排除掉两个停牌了很多年的傻逼股票
        # pred_df = ptps.prediction(stocks, 'fit')
        # pred_df.sort_values(by=['p_change'], inplace=True, ascending=False)
        # gv.logger.info("预测涨幅最大的5只股票为：\n{}".format(pred_df[:5]))

    else:
        gv.logger.error("Unknown command: {}".format(gv.command))
        sys.exit(0)
    end_time = datetime.datetime.now()
    print("执行用时：{}s".format((end_time - start_time)))


if __name__ == "__main__":
    start()
