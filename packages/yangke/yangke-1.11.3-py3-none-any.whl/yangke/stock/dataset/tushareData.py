# 使用tushare库获取股票数据
import datetime
import os
import time
from datetime import date
import logging  # 日志输出
import yangke.stock.globalVar as gv

import numpy as np
import pandas as pd
# import talib  # 下载不成功
import tushare as ts  # 股票数据下载
import json5
import yangke.common.config as config
from yangke.common.mysql import select_in_table, cursor2engine, dtype_dict, update_update_time_of_table
from threading import Thread
import traceback
import copy
from yangke.common.mysql import insert_item_to_mysql, insert_dataframe_to_mysql, start_mysql_service, \
    read_dataframe_from_mysql, get_update_time_of_table, has_table, create_table
from yangke.base import merge_two_dataframes


class StockData:
    """
    初始化tushare，填写token
    """

    def __init__(self, data_dir: str, code: str = None, day=date.today(), mysql_engine=None):
        super().__init__()
        self.api = ts.pro_api('67e4202fb31f321f28929afdbe11780241cd35eb662f6f1947f7e800')
        # --------------全局参数-----------------
        self.dataDir = data_dir
        self.code = code
        self.day = day
        self.encode = gv.encoding
        self.conn = mysql_engine
        if self.conn is None:  # 如果传入了非空的数据库连接，则使用mysql数据库存储股票数据，否则使用本地文件存储数据
            self.storage = "file"
        else:
            self.storage = "mysql"

    def __repr__(self):
        info = "dataDir={}, code={}, day={}, encoding={}".format(self.dataDir, self.code, self.day, self.encode)
        return info

    def setCode(self, code: str):
        self.code = code

    def setDay(self, day: datetime.date):
        self.day = day

    def get_name(self):
        # df = api.query('daily', ts_code='000001.SZ')
        # df.to_csv('000001.csv', columns=['trade_date', 'open', 'high', 'low', 'close', 'vol'])
        data = self.api.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')

        data_s = data[data['symbol'] == self.code]  # 选出‘symbol=600006'的那一行，成为1行n列的DataFrame数据

        name = data_s.iloc[0, 2]  # 选出第0行第2列，因为数据经过挑选只有一行，所以行号永远为0
        print("debug: name|" + name)
        return name

    def get_all_stock_symbol(self) -> list:
        """
        获得上海和深圳证券交易所目前上市的所有股票代码

        :return: 股票代码的列表
        """
        if self.storage == "file":
            symbol_file = os.path.join(self.dataDir, "allsymbols.json")
            if self.need_update(symbol_file):  # 如果需要更新
                inner_data = self.api.stock_basic(exchange='', list_status='L', fields='symbol')
                inner_data = inner_data.sort_values(by='symbol', ascending=True)
                inner_data.to_json(symbol_file)
                in_symbols = inner_data['symbol']  # 股票symbol的series，symbols[0]是第一只股票，symbols[-1]是最后一只股票
            else:
                in_symbols = pd.read_json(symbol_file, encoding=self.encode, dtype=str)['symbol']
            return list(in_symbols)
        else:
            update_time = get_update_time_of_table("symbols")
            if self.need_update(update_time):
                inner_data = self.api.stock_basic(exchange='', list_status='L', fields='symbol,name')
                inner_data: pd.DataFrame = inner_data.sort_values(by='symbol', ascending=True)
                inner_data.to_sql("symbols", con=self.conn, if_exists='replace', index=False)  # pd.to_sql会直接替换表
                in_symbols = inner_data['symbol']  # 股票symbol的series，symbols[0]是第一只股票，symbols[-1]是最后一只股票
                update_update_time_of_table("symbols")
            else:
                in_symbols = read_dataframe_from_mysql("symbols")['symbol']
            return list(in_symbols)

    @config.loggingTitleCall(title="查看触底反弹股")
    def get_bottom_out(self, in_recent_days: int = 10):  # 触底反弹股票，根据近30天内的数据进行判断
        """
        获得触底反弹股票

        :param in_recent_days:股票数据条数，即判断的时间周期
        :returns symbols 触底反弹股
                 symbols2 最后一天在增长的股票
        """
        df = self.download_daily(date.today())
        inner_symbols = []
        symbols_first = []
        # 首先获得满足如下3个条件的股票列表
        # 1. 当天开盘价小于收盘价，表明最后一天在增长
        # 2. 当天开盘价小于昨天收盘价，表明昨天到今天在下降，满足先降后生的特点，即触底反弹的特点
        # 3. 当天最高价等于收盘价，表明最后阶段没有出现下降的趋势
        for inner_index, inner_row in df.iterrows():
            if inner_row["open"] < inner_row["close"] and inner_row["open"] < inner_row["pre_close"] \
                    and inner_row["high"] == inner_row["close"]:
                # print(row['ts_code'])
                inner_symbols.append(inner_row['ts_code'])
                symbols_first.append(inner_row['ts_code'])
        gv.logger.debug("初筛触底反弹股列表:{}".format(symbols_first))
        gv.logger.debug("进一步检查初筛列表...")
        # 进一步删选选出来的股票，剔除其中最低价没有出现在最后一天的股票，只有最后一天是最低价，才能算是触底反弹
        for inner_symbol in symbols_first:
            df = self.download(inner_symbol, append=True)
            df = df.iloc[0 - in_recent_days:]  # 截取最后n天的数据
            lowest_price = df['low'].min()  # 获得30天内的最低价
            lowest_date = np.array(df['date'][df['low'] == lowest_price])[0]  # 获得30天内最低价对应的日期，这里返回的lowest_date为str类型

            if lowest_date == df.iloc[-1]['date']:
                pass
            else:
                inner_symbols.remove(inner_symbol)
        gv.logger.debug("触底反弹股列表:{}".format(inner_symbols))
        return inner_symbols, symbols_first

    def download_all_stocks(self, codes: list = None, num_works=64, exclude: list = None) -> list:
        """
        下载所有股票数据，如果传入的是列表，则只下载列表中股票代码对应的股票数据
        如果使用以下方法下载所有股票数据，则耗时巨大，实用性不强，本方法主要结合多线程进行下载。

        for stock_code in codes:
            self.download(stock_code)

        需要注意的是多线程并不会增加本地的处理速度，只是可以http并发请求数量，在高耗时的http连接上可以提高下载速度。

        测试该方法下载沪深所有股票数据需要7分钟左右。执行耗时与网速即硬件相关。

        如果本地数据是最新，则耗时大概10秒钟左右。

        :param codes: 股票代码列表
        :param num_works: 线程数
        :return: 存在有效数据的股票代码列表，由于有些股票连续停牌超过两年会导致没有数据，返回的股票列表会剔除这种股票
        """
        if codes is None:
            state = gv.RunState().load()
            if not self.need_update(state.last_update_time):
                return state.stocks
            codes_available = self.get_all_stock_symbol()
            gv.logger.debug("下载沪深所有股票数据，预计耗时10分钟左右（本地所有股票数据需要更新时）...")
        else:
            codes_available = codes
        if exclude is not None:
            codes_available = [code for code in codes_available if code not in exclude]

        # 将股票分成num_works份，传到每个线程进行下载
        num_codes = len(codes_available)
        num_works = min(num_codes / 10, num_works)  # 设计一个线程最少下载10个数据，最多num_works个线程
        num_works = int(num_works) + 1  # 小于10个股票，则单线程下载，这里不加1会导致10个以下股票数据需要下载时，需要0个线程
        interval = num_codes // num_works + 1
        codes_list_list = []
        for i in range(num_works):
            end = min((i + 1) * interval, num_codes)
            codes_list_list.append(copy.deepcopy(codes_available[i * interval:end]))
        if len(codes_list_list[
                   -1]) == 0:  # 极特殊情况下，(i+1)*interval==num_codes，导致列表最后一项为空，例如当num_codes=3780,num_works=64时
            num_works = num_works - 1
            codes_list_list.remove([])

        def _download_(codes_list):  # 这里的codes_list是codes深拷贝的索引
            config.holdLoggingLevel(logging.WARNING)
            for code in codes_list:
                df = self.download(code, append=True)
                if df is None:
                    codes_available.remove(code)  # 这里多线程都在操作codes，可能会有问题，目前没发现异常，暂未处理

            config.holdLoggingLevel()

        thread_list = []
        try:
            for i in range(num_works):
                t = Thread(target=_download_, args=(codes_list_list[i],))
                thread_list.append(t)
                t.start()
            # 在这里等待所有线程执行完毕
            for t in thread_list:
                t.join()

            codes_available.sort()  # 默认升序
        except:
            gv.logger.error("multi-process error!")
            traceback.print_exc()  # 打印系统错误提示
            import sys
            sys.exit(1)

        gv.logger.info("All stock data downloaded, finish")
        if codes is None:  # 如果下载了所有的股票，就记录最后更新时间
            state = gv.RunState(last_update_time=datetime.datetime.now(), stocks=codes_available)
            state.dump()  # 序列化后使用state=gv.RunState().load()可以加载回来
        return codes_available

    def download(self, code: str, append=True) -> pd.DataFrame:
        """
        下载或更新code对应的股票在近一年的数据，只能在交易时间之外进行。

        下载的股票数据列及其意义如下：

        date open high close low volume price_change p_change ma5 ...

        日期 开盘 最高 收盘 最低价 成交量 收盘价格变化 价格涨幅 滑动平均5 ...

        更新：下载股票数据时不会替换当前已经存在的数据，只是追加新数据

        :param code: 股票代码，可以带证交所后缀的股票代码：如601002.SH，也可以只是股票编号：601002
        :param append: 如果为True，则追加新数据到已有数据，而不是下载后替换已有数据
        :param to_mysql: 是否使用mysql数据库存储，如果为False，则存储为本地csv文件
        :return:
        """
        code = str(code)
        gv.logger.debug("准备下载股票数据，股票代码：" + code)
        if '.' in code:  # 如果传入的股票代码是类似于 000544.SZ 格式的，则去掉后面的 .SZ,只保留数字格式代码
            code = code[0:6]

        if self.storage == "mysql":
            update_time = get_update_time_of_table(f"basic{code}")
            if not self.need_update(update_time):
                gv.logger.debug("本地数据已是最新，使用本地股票数据（读取自mysql数据库）...")
                df = read_dataframe_from_mysql(f"basic{code}")
                return df
        else:
            if not os.path.exists(self.dataDir):
                os.mkdir(self.dataDir)
            inner_data_file = os.path.join(self.dataDir, code + '.csv')  # 数据存储时会覆盖，所以不用删除当前已存在的数据文件
            if not self.need_update(inner_data_file):  # 判断是否需要更新数据，无需更新则直接返回
                gv.logger.debug("本地数据已是最新，使用本地股票数据（%s）..." % inner_data_file)
                df = pd.read_csv(inner_data_file, encoding=self.encode)
                return df
        # 如果需要更新，则开始更新
        gv.logger.debug("本地数据需要更新，开始下载股票数据（%s）..." % code)
        success = False  # 标记是否成功下载
        try:
            df = ts.get_hist_data(code)  # ts.get_hist_data('600848',start='2015-01-05',end='2015-01-09')
            if df is None:  # 有时候下载失败，会导致df为None，如果出现这种情况，重复10次
                gv.logger.debug("下载股票数据{}失败，重试...".format(code))
                for i in range(10):
                    df: pd.DataFrame = ts.get_hist_data(code)
                    if df is not None:
                        success = True
                        gv.logger.debug("下载股票数据{}失败，重试...，成功！".format(code))
                        break
            else:
                success = True
        except:  # 当网络故障的时候，ts.get_hist_data(code)会报错
            gv.logger.error("获取股票{}失败，请检查网络".format(code))
            return None
        if not success:
            gv.logger.warning("经过10次尝试后，下载股票数据{}一直失败，没有数据"
                              "保存到本地！停牌超过两年或预上市股票也会产生该警告！".format(code))
            return None
        df.sort_index(inplace=True)  # 反序排列数据，这样让更新的数据位于文件最下方
        df.reset_index(inplace=True)
        df = df[['date', 'open', 'high', 'close',
                 'low', 'volume', 'price_change',
                 'p_change']]
        if append:  # 如果需要追加数据
            if self.storage == "mysql":
                # 建议使用df.to_sql()之前先创建表，因为df.to_sql()方法默认建的表数据类型及primary key都难以控制
                if not gv.mysql_engine.has_table(f"basic{code}"):  # 不存在就创建
                    create_table(table_name=f"basic{code}", columns={
                        'date': "date",
                        'open': "float",
                        "high": "float",
                        "close": "float",
                        "low": "float",
                        "volume": "float",
                        "price_change": "float",
                        "p_change": "float"
                    }, primary=[0])
                insert_dataframe_to_mysql(table_name=f"basic{code}",
                                          dataframe=df, ignore=True)
                # 手动更新mysql表的更新时间
                update_update_time_of_table(f"basic{code}")
                # 使用df.to_sql当df数据与现有表中有数据相同时，会报错。
                # df.to_sql(f"basic{code}", con=gv.mysql_engine, if_exists="append", index=False)
            else:
                # noinspection all
                if os.path.exists(inner_data_file):  # 如果本地存在
                    df_exists = pd.read_csv(inner_data_file, encoding=self.encode)  # 读取本地存在的数据
                    df, _ = merge_two_dataframes(df, df_exists)

        if self.storage == "mysql":
            # 存储到mysql数据库
            gv.logger.debug(f"股票数据存储在mysql数据库stocks > basic{code}表中")
            df = read_dataframe_from_mysql(f"basic{code}")
        else:
            df.to_csv(inner_data_file, index=False, encoding=self.encode, columns=['date', 'open', 'high', 'close',
                                                                                   'low', 'volume', 'price_change',
                                                                                   'p_change'])
            # 我们需要日期列的内容，因此需要重新读取一边csv文件
            gv.logger.debug("股票%s数据存储在%s" % (code, inner_data_file))
        return df

    def download_daily(self, day_datetime: datetime.date):
        """
        下载更新给定日期的所有股票数据

        :param day_datetime: 给定日期
        :return:
        """
        if self.is_holiday(day_datetime):
            day_datetime = self.get_working_day_before_day(day_datetime, 1)

        if day_datetime == date.today():  # 对于当天的股票数据，需要在16:00以后才会更新数据
            hour = time.strftime("%H")
            if int(hour) < 16:  # 更新时间：交易日每天15点～16点之间，所以需要16点以后调用保证正确性，16点以前调用获得的是上一个交易日的数据
                day_datetime = self.get_working_day_before_day(day_datetime, 1)
                gv.logger.debug("正常交易日，16:00之前当日数据尚未更新，使用上一个交易日的数据！")
            else:
                gv.logger.debug("正常交易日，使用本日数据！")
        else:
            gv.logger.debug("今天休市，使用上一个交易日的数据！")

        day_str = day_datetime.strftime("%Y%m%d")
        gv.logger.debug("准备交易日数据，日期：{}".format(day_datetime))
        # ------------创建“api_daily/日期.csv”用以保存数据-----------
        parent_path1 = os.path.join(self.dataDir, 'api_daily')
        if not os.path.exists(parent_path1):
            os.mkdir(parent_path1)
        data_file = os.path.join(parent_path1, day_str + '.csv')
        # ------------创建“api_daily/日期.csv”用以保存数据-----------
        if not self.need_update(data_file):
            df = pd.read_csv(data_file, encoding=self.encode)
            gv.logger.debug("检查本地数据：存在数据文件且无需更新，使用本地数据")
        else:
            df = self.api.daily(trade_date=day_str)  # 真正获得数据
            df.to_csv(data_file, encoding=self.encode, index=False)
            gv.logger.debug("检查本地数据：本地数据文件不存在或需要更新，下载交易日数据...")
        return df

    def get_data_of_day(self, code, day_datetime: date = date.today(), next_day: int = -1):
        """
        获得给定代码的股票在给定日期的开盘，收盘等等价格信息，如果给定的日期休市，默认返回其前一个工作日的数据。
        只能获得最近一年内的信息，更早的信息目前不支持

        :param code: 股票代码
        :param day_datetime: 日期datetime.date
        :param next_day: 如果给定日期股票停牌或不是交易日，是否获得其他天的股票数据，-1获得给定日期前一天，0返回空值，1返回给定日期后一天数据，如果为空，返回空值
        :return: DataFrame格式数据
        """
        df = self.download(code, True)  # 获得股票近一年的数据
        day_str = day_datetime.strftime("%Y-%m-%d")
        df = df.loc[df['date'] == day_str]  # 检索day_str对应的日期的股票数据
        if len(df) == 0:  # 即当天没有查到数据
            if next_day == 0:
                return df
            elif next_day == -1:
                day_datetime = self.get_working_day_before_day(day_datetime, 1)
                return self.get_data_of_day(code, day_datetime, -1)
            else:
                day_datetime = self.get_working_day_before_day(day_datetime, -1)  # 获得后一个工作日
                last_datetime = datetime.datetime.strptime(str(self.get_previous_working_day(includeTime=True)),
                                                           '%Y-%m-%d')  # 目前为止最后一个有数据的交易日
                if day_datetime >= last_datetime:  # 如果后一个工作日在今天(有数据的股票交易日)之前
                    return self.get_data_of_day(code, day_datetime, 1)  # 因为这里day_datetime必然是工作日，因此第三个参数
                    # 一般是不重要的，给了1是为了防止指定股票在当日停牌，这种情况极少见
                else:
                    gv.logger.error("指定日期{}的股票数据不存在，检查日期是否是未来的日期！".format(day_datetime))
                    # 这种情况目前不存在用例，将来在设计返回参数
        return df

    def get_last_n_working_day(self, n: int = 30, sort='ascend', last_date=date.today()) -> list:
        """
        获得最近n个交易日的日期列表；如果给定last_date，则获得last_date之前的n个交易日数据

        :param n:
        :param sort: 排序方式，'ascend'：从前到后，'descend'：从后到前；默认从前到后
        :param last_date: n个交易中最后一个日期
        :return: 返回长度为n的date列表,列表项为datetime.date类型数据
        """
        # <<<<<<<<<<<<<<<<<<<<<方法1-----------------------------------------
        dates = []
        day = self.get_previous_working_day(last_date, includeTime=True)  # 获得指定日期前的最后一个交易日
        while len(dates) < n:
            dates.append(day)
            day = self.get_working_day_before_day(day)
        # ---------------------方法1>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        if sort.lower() == 'ascend':
            dates = dates[::-1]  # 反序排列列表
        elif sort.lower() == 'descend':
            pass
        else:
            gv.logger.error("参数sort未识别，sort只能取值'ascend'和'descend'!")
        return dates

    def need_update(self, data_file: str or datetime.datetime):
        """
        检查数据文件是否需要更新；如果传入的是时间，则检查该时间之后是否有股票数据更新

        :param data_file:
        :return:
        """
        if isinstance(data_file, datetime.datetime):
            last_change_time = data_file
            last_change_date_str = last_change_time.strftime("%Y-%m-%d")
            print("最后更新于{}，".format(data_file))
        elif data_file is None:  # 如果文件为空
            return True
        elif os.path.exists(data_file):  # 如果文件存在，判断文件是否需要更新
            last_change_time = os.stat(data_file).st_mtime
            last_change_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(last_change_time))
            last_change_time = datetime.datetime.strptime(last_change_time_str, "%Y-%m-%d %H:%M:%S")
            last_change_date_str = last_change_time.strftime("%Y-%m-%d")
        else:  # 文件不存在，则需要更新
            return True

        now_time = datetime.datetime.now()  # 当前时间
        now_time_date_str = now_time.strftime("%Y-%m-%d")  # 用来和最后修改日期作比较

        if last_change_date_str == now_time_date_str:  # 如果是今天修改的
            if last_change_time.hour > 15:  # 最后修改日期是当天15点以后，则不用更新数据
                gv.logger.debug("数据文件{}已经最新，无需更新！".format(data_file))
                return False  # 无需更新数据
            else:
                if now_time.hour < 16:  # 如果今天修改过且今天还没到16:00，也无须更新
                    return False
                # 如果今天时holiday
                if self.is_holiday(date.today()):  # 如果今天时休息日，今天更新过也不用更新
                    gv.logger.debug("数据文件{}已经最新，无需更新！".format(data_file))
                    return False
                else:
                    return True
        else:
            last_working_day_str = str(self.get_previous_working_day(includeTime=True)) + ' 16:00:00'
            last_working_datetime = datetime.datetime.strptime(last_working_day_str, '%Y-%m-%d %H:%M:%S')
            if last_change_time > last_working_datetime:
                # 如果最后修改日期在上一个工作日15点之后
                gv.logger.debug("数据文件{}已经最新，无需更新！".format(data_file))
                return False  # 无需更新数据
            else:
                return True

    def get_open_limit(self, up_down='up', day_datetime: datetime.date = date.today()):
        """
        获得对应日期的开盘涨/跌停股
        如果对应日期休市，则查询昨天，以此类推，找最近一个交易日的数据

        :param up_down:
        :param day_datetime 日期
        :return 返回开盘跌停股的code列表
        """
        if up_down.lower() == 'up':
            title = "涨停"
        elif up_down.lower() == 'down':
            title = "跌停"
        else:
            gv.logger.debug("参数未识别，up_down只能取值'up'或'down'！")
        config.loggingTitle("查找开盘{}股({})".format(title, day_datetime), "start")
        open_limit = self._get_limit(up_down=up_down, day_datetime=day_datetime)
        gv.logger.debug("开盘{}股列表:{}".format(title, open_limit))
        config.loggingTitle("查找开盘{}股({})".format(title, day_datetime), "end")
        return open_limit

    def _get_limit(self, up_down: str = 'up', day_datetime: datetime.date = date.today()) -> list:
        """
        私有类，查询并获取指定日期的开盘涨停或跌停股，给外部接口函数get_open_limit_up/down调用，如果传入的日期是休息日，则获得
        传入日期上一个工作日的开盘涨停或跌停股。

        :param up_down: 涨停/跌停，可取值"up"和"down"
        :param day_datetime: 指定日期
        :return:
        """
        result = []
        if self.is_holiday(day_datetime):  # 如果今天是休息日
            day_datetime = self.get_working_day_before_day(day_datetime, 1)

        # ------------把day由"%Y-%m-%d"转为"%Y%m%d"格式-----------
        day_str = day_datetime.strftime("%Y%m%d")
        # ------------把day由"%Y-%m-%d"转为"%Y%m%d"格式-----------

        # ------------创建“api_daily/日期.csv”用以保存数据-----------
        parent_path1 = os.path.join(self.dataDir, 'api_daily')
        if not os.path.exists(parent_path1):
            os.mkdir(parent_path1)
        data_file = os.path.join(parent_path1, day_str + '.csv')
        # ------------创建“api_daily/日期.csv”用以保存数据-----------
        if os.path.exists(data_file):  # 因为data_file是以日期命名的，存在就不需要更新
            # 判断数据是否有变化
            df = pd.read_csv(data_file, encoding=self.encode)
        else:
            df = self.api.daily(trade_date=day_str)  # 真正获得数据
            df.to_csv(data_file, encoding=self.encode, index=False)
        df = np.array(df)
        for stock in df:  # 判断每一只股票
            # 开盘涨/跌停股票开盘/收盘/最高/最低价都是相同的
            if stock[2] == stock[3] == stock[4] == stock[5]:
                if up_down.lower() == "up":
                    if (stock[2] - stock[6]) / stock[6] > 0.09:
                        gv.logger.debug("开盘即涨停->代码:|%s|前一天股价:|%f|开盘价|%f" % (stock[0][0:6], stock[6], stock[2]))
                        result.append(stock[0][0:6])
                elif up_down.lower() == "down":
                    if (stock[6] - stock[2]) / stock[6] > 0.09 and stock[2] != 0:  # 排除停牌股票
                        gv.logger.debug("开盘即跌停->代码:|%s|前一天股价:|%f|开盘价|%f" % (stock[0][0:6], stock[6], stock[2]))
                        result.append(stock[0][0:6])
                else:
                    gv.logger.error("参数up_down未识别！")
        return result

    def is_working_time(self):
        """
        判断是否是交易时间
        """
        if not self.is_holiday():
            hour = datetime.datetime.hour
            if hour in range(9, 12):  # range(9,12)=[9,12)，即包含9，不包含12
                return True
            if hour in range(13, 15):
                return True
        return False

    def is_holiday(self, day_datetime: datetime.date = date.today()):
        """
        判断今天是不是休市，只适用于国内股市，不包括港股

        :param day_datetime: 给定日期的datetime类型
        :return: True 或 False
        """
        day_str = day_datetime.strftime("%Y%m%d")
        if (day_datetime.weekday() == 5) or (day_datetime.weekday() == 6):  # 周六和周日肯定是休市的
            return True
        date_str = day_str
        fetch = select_in_table(table_name='holiday',
                                condition_dict={"calendarDate": date_str},
                                result_col=['isOpen'])
        if fetch is None:
            gv.logger.debug("数据库中不存在假期数据表，请先初始化数据库！")

        if len(fetch) == 0:  # 未查找到相关记录
            year = day_datetime.year
            holiday_data: pd.DataFrame = self.api.query('trade_cal', start_date=f'{year}0101', end_date=f'{year}1231')
            holiday_data.rename(columns={"cal_date": "calendarDate", "is_open": "isOpen"}, inplace=True)
            holiday_data.drop(labels="exchange", axis=1, inplace=True)
            for date1, is_open in zip(holiday_data['calendarDate'], holiday_data['isOpen']):
                is_open = 'Y' if is_open == 1 else 'N'
                insert_item_to_mysql('holiday', [date1, is_open], ['calendarDate', 'isOpen'],
                                     replace=True, filter_warning=None)

            if holiday_data[holiday_data['calendarDate'] == date_str]['isOpen'].values[0] == 1:
                return False
            else:
                return True
        else:
            if fetch[0][0] == 'N':  # 不开市则为假日，返回True
                return True
            else:
                return False

    def get_previous_working_day(self, last_date=date.today(), includeTime=False) -> datetime.date:
        """
        获得指定日期的上一个交易日，如果不传入参数，则获得最近的一个交易日，包含今天。

        :param last_date: 指定的日期
        :param includeTime: 是否判断时间，如果includeTime=True，则会进一步判断今天的时间，如果时间在下午4:00之前，则不包括今天，因为当天的股票数据还没整理出来
        :return: 最近一个交易日日期
        """
        if last_date > date.today():
            gv.logger.warning("因为未来的股票数据不存在，不能获得将来日期的前一个工作日！")
        if self.is_holiday(last_date):
            one_day = datetime.timedelta(days=1)
            pre_day = last_date - one_day
            while self.is_holiday(pre_day):
                pre_day = pre_day - one_day
            return pre_day
        else:
            if includeTime and last_date == date.today():  # 需要判断时间，且last_date是今天
                dt = datetime.datetime.now()
                hour = dt.hour
                if hour < 16:  # 额外对时间进行判断
                    return self.get_working_day_before_day(date.today())
            return last_date

    def recent_30_open_limit_down_to_file(self, up_down='up', days=30):
        """
        获得最近30天内涨/跌停的所有股票的信息，并计算涨/跌停后两天的股价变化情况。
        剔除开始统计的第一天和最后一天的涨/跌停股票，因为它们仍在涨/跌停过程中，统计的持续涨跌天数不全。
        倒数第二天的股票信息中，停止涨/跌停后第二天的增幅数据为'OutOfRange'，因为第二天的增幅需要明天的数据，
        明天还未到来，因此没有明天的数据，无法计算。
        增幅显示为NaN，则表示股票存在停牌。
        该方法主要为连跌后股票的增幅变化提供依据。
        返回的'连涨/跌出现次数'：1 表示正常情况，出现了一次连续涨/跌；2 表示出现了一次或多次连续涨跌；-2 表示以停牌持续到
        统计天数末尾；-3 表示倒数第二天的股票，这些股票不存在'连涨/跌后增幅2'。

        :param up_down: 统计连续涨停还是连续跌停，可以取值'up'或'down'，这里的涨/跌停不包括ST股。
        :param days: 统计的天数
        :return: codes, lastDays 股票代码和连续跌停的天数
        """
        # 确保OpenLimit文件夹存在
        file = os.path.join(self.dataDir, "OpenLimit")
        if not os.path.exists(file):
            os.mkdir(file)
        file = os.path.join(file, "recent30Down.csv")

        if up_down.lower() == 'up':
            title = "涨"
        elif up_down.lower() == 'down':
            title = "跌"
        else:
            gv.logger.debug("参数未识别，up_down只能取值'up'或'down'！")

        # 拿到30天内每天的开盘涨/跌停股，以及对应的日期的列表
        limits, dates = self.get_open_limit_of_n_trading_days(days, up_down, sort='ascend')
        limits_set = []  # 将limit_downs中的每一个元素转化为集合
        for limit in limits:
            limits_set.append(set(limit))

        # <<<<<<<<<<<<<<<<<<<<<<首先删除数据不全的跌停股-----------------------------
        temp_set = limits_set[0]
        for i in range(1, len(limits_set)):
            """
            将temp_set和limits_set[i]的共有元素选出来，删除其他不共有的元素；因为如果一个元素在temp_set中，但
            不在limits_set[i]中，那么相对与limits_set[i]更靠内侧的日期的股票中再出现的temp_set中的元素就不属于数据
            不完整的股票了。举例如下：
            temp_set=['000001','000002']
            limits_set[0]=['000001','000002']
            limits_set[1]=['000001','000002','200002']
            limits_set[2]=['200003']
            limits_set[3]=['000001']
            limits_set[4]=['200005']
            则'000001'虽然在temp_set中，但是他在limits_set[3]中出现的时候，它的数据是全的。上一行是删除外侧日期
            即limits_set[0]和limits_set[1]中的'000001'，然后在limits_set[2]中没有'000001'，这是就要删除temp_set中的
            '000001'，下一行的工作就是删除temp_set中的'000001'
            """
            temp_set = limits_set[i] & temp_set
            # 从第一个集合里删除temp_set的元素，这里第一个集合指的是靠近最外边的日期的股票
            limits_set[i] = limits_set[i] - temp_set
            if len(temp_set) == 0:
                break
        # 删除另一侧的
        temp_set = limits_set[-1]
        for i in range(len(limits_set) - 2, 0, -1):
            temp_set = limits_set[i] & temp_set
            limits_set[i] = limits_set[i] - temp_set
            if len(temp_set) == 0:
                break
        # 删除边缘两天的所有股票，因为他们的持续天数都可能不全
        limits_set[0] = set()
        limits_set[-1] = set()
        # ----------------------首先删除数据不全的跌停股>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        # <<<<<<<<<<<<<<<<<<<<<<获得30天内所有出现过的开盘跌停股的集合-----------------
        codes = limits_set[0]  # 所有跌停股列表，为limit_downs_set所有元素的并集
        for i in range(1, len(limits_set)):
            codes = codes | limits_set[i]
        # ----------------------获得30天内所有出现过的开盘跌停股的集合>>>>>>>>>>>>>>>>>
        # 将limit_downs_set转换为列表，以方便进行索引
        limits = list(limits_set)
        # 将limits中每个元素转换为列表
        limits = [list(e) for e in limits]
        # 将codes转换为列表
        codes = list(codes)
        codes.sort(reverse=False)  # 随便排个序，不影响结果，只是为了方便每次调试时股票顺序一致好对比
        lastDays = []  # 每个涨/跌停股对应的持续天数
        increase_after1 = []  # 每个涨/跌停股停止涨/跌停后的第二天开盘价涨跌幅
        increase_after2 = []
        flags = []  # 标记当前股数据是否已经统计
        # -3表示倒数第二天的股票，这些股票的increase_after2不存在，因为涉及到了明天的数据，明天数据不存在，使得对应增幅无法计算
        # -2表示以跌停停牌，至今没有开牌
        # -1没统计，
        # 0正在统计/至今还处于跌停状态，
        # 1统计过一次，
        # 2开盘跌停在30天内出现一次以上

        for i in range(len(codes)):  # 数据齐全的所有股票代码
            lastDays.append(0)
            increase_after1.append(None)
            increase_after2.append(None)
            flags.append(-1)
        for i in range(len(codes)):  # 遍历所有需要统计的代码
            for j in range(len(limits)):  # 遍历所有日期的涨/跌停股
                if codes[i] in limits[j]:  # 首先查找包含codes[i]的日期，然后开始进入统计
                    if flags[i] == -1 or flags[i] == 0:
                        lastDays[i] = lastDays[i] + 1
                        flags[i] = 0
                    else:
                        flags[i] = flags[i] + 1
                else:
                    if flags[i] == 0:
                        flags[i] = 1
                        # 获得昨天和今天的股票数据，因为连续跌停时，停牌股概率大增，这里要考虑停牌影响
                        yesterday = self.get_data_of_day(codes[i], dates[j - 1], next_day=-1)
                        today = self.get_data_of_day(codes[i], dates[j], next_day=0)
                        if j < len(limits) - 1:
                            tomorrow = self.get_data_of_day(codes[i], dates[j + 1], next_day=0)
                        else:
                            tomorrow = []
                            outOfRange = True

                        if len(today) == 0:  # 因为dates中的日期都是工作日，如果查不到数据，则必然是股票停牌
                            flags[i] = -2
                        elif len(tomorrow) == 0:  # 停牌
                            open_yest = float(yesterday['close'])
                            open_today = float(today['close'])
                            increase_after1[i] = (open_today - open_yest) / open_yest
                            flags[i] = -2
                            if outOfRange:
                                increase_after2[i] = 'OutOfRange'
                                flags[i] = -3
                        else:
                            open_yest = float(yesterday['close'])
                            open_today = float(today['close'])
                            open_next = float(tomorrow['close'])
                            increase_after1[i] = (open_today - open_yest) / open_yest
                            increase_after2[i] = (open_next - open_today) / open_today
        # <<<<<<<<<<<<<<<<<<<<<<<获得具有完整跌停信息的股票的数据----------------------
        localData = {'股票代码': codes, '持续天数': lastDays, '连{}后增幅1'.format(title): increase_after1,
                     '连{}后增幅2'.format(title): increase_after2, '连{}出现次数'.format(title): flags}
        df = pd.DataFrame(localData)
        df.to_csv(file, encoding="utf8", index=False)
        gv.logger.debug("{}到{}日连续{}停股票统计：\n{}".format(dates[0], dates[-1], title, df))
        return df

    def get_open_limit_and_lastdays(self, up_down='up', days: int = 10, last_date=date.today()):
        """
        将最近一个工作日的开盘涨/跌停股及其持续涨/跌停天数写到文件"./OpenLimit/recentDown.csv"

        :param up_down:
        :param days: 统计的天数，这里设置为10，因为连续涨/跌停
        :param last_date: 如果指定last_date，则获得该日期时所有开盘涨/跌停股的信息
        :return: DataFrame 股票代码和连续跌停的天数
        """
        # 处理up_down参数
        if up_down.lower() == 'up':
            title = "Up"
            title1 = "涨停"
        elif up_down.lower() == 'down':
            title = "Down"
            title1 = "跌停"
        else:
            gv.logger.error("输入参数未识别，up_down只能取值'up'或'down'！")
        # 确保OpenLimit文件夹存在
        file = os.path.join(self.dataDir, "OpenLimit")
        if not os.path.exists(file):  # 确保文件夹存在
            os.mkdir(file)

        gv.logger.debug("获取{}的{}股代码及持续天数...".format(last_date, title1))
        config.holdLoggingLevel(logging.WARN)
        limits, dates = self.get_open_limit_of_n_trading_days(days, up_down, 'descend', last_date=last_date)
        config.holdLoggingLevel('end')
        file = os.path.join(file, "recent{}{}.csv".format(title, dates[0]))
        if os.path.exists(file):
            df = pd.read_csv(file, encoding=self.encode, dtype={'股票代码': str})
        else:
            today_codes = limits[0]
            codes = today_codes
            lastDays = []
            flag = []
            for _ in codes:  # 初始化最近一天的涨/跌停股，每一个股对应的持续天数初始化为1
                lastDays.append(1)
                flag.append(True)
            for i in range(1, days):  # 天数
                for j in range(len(codes)):  # 第一天涨/跌股的数量，逐个检查每个股
                    if (codes[j] in limits[i]) and flag[j]:  # 如果前一天的跌停股列表里仍有code，则code的持续天数+1
                        lastDays[j] = lastDays[j] + 1
                    else:  # 如果前一天的跌停股列表里没有code，则将code标记为False，其lastdays列表中对应的天数将不再改变
                        flag[j] = False
            data = {'股票代码': codes, '持续天数': lastDays}
            df = pd.DataFrame(data)
            df.to_csv(file, encoding=self.encode, index=False)
        gv.logger.debug("get_open_limit_and_lastdays()获得{}的{}股和持续天数：\n{}".format(last_date, title1, df))
        return df

    def get_open_limit_of_n_trading_days(self, days=30, up_down='up',
                                         sort='ascend', last_date=date.today()):
        """
        获得最近n个交易日的开盘涨/跌停股，包括今天（如果今天是交易日）；这里的涨/跌停不包括ST股。

        :param days: 统计的天数。
        :param up_down: 涨停还是跌停，取值：'up'或者'down'，默认是'up'。
        :param sort: 排序方式，'ascend'：从前到后，'descend'：从后到前；默认从前到后。
        :param last_date: 指定日期，如果不指定，则是最近的n个交易日，如果指定，则以指定日期为最后一个交易日。
        :return: limit_down_of_days和dates: [[],[],...[]]，列表中的每一个列表对应每一天的跌停股，result[0]是最近一个交易日的跌停股，如果今天是交易日，则result[0]就是今天。result[n]是第n个交易日前的跌停股，dates: 返回长度为n的date列表,列表为字符串，格式为"%Y-%m-%d"
        """
        if up_down.lower() == 'up':
            tmp = '涨停'
        elif up_down.lower() == 'down':
            tmp = '跌停'
        else:
            gv.logger.error("参数未识别，up_down只能取值'up'或'down'！")
        config.loggingTitle("获取最近{}个交易日的{}信息".format(days, tmp), 'start')
        date_times = self.get_last_n_working_day(days, sort, last_date=last_date)
        open_limit_list = []

        for day_datetime in date_times:
            gv.logger.debug("获取{}的开盘{}股...".format(day_datetime, tmp))
            config.holdLoggingLevel(logging.WARN)  # 临时将日志级别调高到警告，以取消局部的DEBUG日志输出
            limit = self.get_open_limit(up_down, day_datetime)
            open_limit_list.append(limit)
            config.holdLoggingLevel('end')  # 恢复日志输出级别
            gv.logger.debug("{}的开盘{}股有：{}".format(day_datetime, tmp, limit))

        config.loggingTitle("获取最近{}个交易日的{}信息".format(days, tmp), 'end')
        return open_limit_list, date_times

    def get_working_day_before_day(self, day_datetime: datetime.date = date.today(), day_num: int = 1) -> datetime.date:
        """
        获得指定日期的前一个交易日或后一个交易日，需要注意的是，该函数不对指定日期是否为工作日进行判断，
        因此，获得最近一个交易日，不能使用get_working_day_before_day(date.today(),1)
        :param day_datetime: datetime类型，默认为今天
        :param day_num: 可取正整数和-1，前day_num个交易日，取-1时,表示指定日期的后一个交易日，不可以取其他负值
        :return: date_datetime】,-----返回对应交易日的datetime类型数据
        """
        # day = day_datetime.strftime("%Y-%m-%d")
        if day_num < -1:
            gv.logger.error("day_num不能取-1以外的负值（{}）".format(day_num))
            return None
        if day_num == 1 or day_num == -1:
            one_day = datetime.timedelta(days=1)
            if day_num == -1:
                pre_day = day_datetime + one_day
            else:
                pre_day = day_datetime - one_day
            while self.is_holiday(pre_day):
                if day_num == -1:
                    pre_day = pre_day + one_day
                else:
                    pre_day = pre_day - one_day
            return pre_day
        else:  # day_num为大于1的整数
            day_datetime = self.get_working_day_before_day(day_datetime, 1)  # 计算上一个交易日
            return self.get_working_day_before_day(day_datetime, day_num - 1)  # 返回上一个交易日的上day_num-1个交易日

    @staticmethod
    def get_realtime_price(symbol):
        """
        获得股票实时价格
        只有实时价格需要实时获取，开盘、收盘等价格可能不需要实时更新，为了节省时间，顺便更新其他价格
        """
        data = ts.get_realtime_quotes(symbol)  # ts的实时行情接口在某些股票中会报错
        # ，因为某些股票的数据多了一个空数据，需要等待Tushare更新或者覆盖get_realtime_quotes中
        # 的相关参数，具体可以在get_realtime_quotes的下面代码之前，添加代码
        # df = pd.DataFrame(data_list, columns=ct.LIVE_DATA_COLS)
        # 添加的代码为：
        # if len(data_list[0])>33:
        #   data_list=data_list[0][:-1]
        name = str(data['name'][0])  # 这四条语句的执行是本地执行，且耗时很少
        open_price = float(data['open'])
        high = float(data['high'])
        low = float(data['low'])
        now_price = float(data['price'])
        return name, now_price, open_price, high, low
