"""
用来读取本地的股票数据
"""
import pandas as pd
import numpy as np
import yangke.stock.globalVar as gv
import torch.utils.data as tud
import os
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
# 类似于 pymysql中的游标
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import yangke.common.config as config
from yangke.common.mysql import start_mysql_service, mysql_available, has_table, \
    read_dataframe_from_mysql


class StockDataset(tud.Dataset):
    """
    构建pytorch的dataset
    """

    def __init__(self, stock_codes: list = None):
        """
        如果stock_codes为一个str，则生成该股票代码的数据集
        如果stock_codes为一个list，则生成该list中所有股票的数据集
        如果stock_codes为None，则默认生成所有有效股票的数据集

        :param stock_codes:
        """
        super(StockDataset, self).__init__()
        if stock_codes is None:
            stock_codes = gv.tsd.download_all_stocks()
        if isinstance(stock_codes, list):
            # 默认选择全部股票数据，如果传入stock_codes，则只加载该列表中的股票
            self.stock_codes = gv.tsd.download_all_stocks(stock_codes)  # 该方法会过滤数据不正常的股票
            # self.files = [os.path.join(gv.dataDirectory, code + ".csv") for code in self.stock_codes]
            current_total_length = 0
            self.index2code = []
            for code in stock_codes:
                result = get_data_days_list(code)
                if result is not None:
                    x, _ = result
                    self.index2code.append(
                        {'range': range[current_total_length, current_total_length + len(x)], 'code': code})
                    current_total_length = current_total_length + len(x)

            self.length = current_total_length
        else:
            self.stock_codes = str(stock_codes)
            result = get_data_days_list(self.stock_codes)
            if result is not None:
                x, y = result
            self.length = len(x)

    def __getitem__(self, index):
        if isinstance(self.stock_codes, list):
            code, pos = self.get_code_pos(index)
            result = get_data_days_list(code)
            x, y = result
        else:
            result = get_data_days_list(self.stock_codes)
            if result is not None:
                x, y = result
        return x[pos], y[pos]

    def __len__(self):
        # 返回整个数据集的长度
        return self.length

    def __repr__(self):
        if isinstance(self.stock_codes, list):
            return "包含以下股票的数据：{}".format(self.stock_codes)
        else:
            return "包含股票{}的数据".format(self.stock_codes)

    def get_code_pos(self, index):
        for i in range(len(self.index2code)):
            local_range = self.index2code[i]['range']
            bottom_index = next(iter(local_range))
            if index in local_range:
                pos = index - bottom_index
                code = self.index2code[i]['code']
                break
        return code, pos


def get_data(stock_code, col_x=None, col_y=None, normalization=None) -> np.ndarray:
    """
    读取股票本地数据文件中指定columns的数据，返回ndarray格式，指定归一化方法可以进行归一化

    :param stock_code: 股票代码
    :param col_x: 需要读入的数据列
    :param col_y: 股票涨幅，如果传入的是列表，会把涨幅按列表分类，例[1, 5]，列表中的值应大于-10，小于10
    :param normalization: 是否需要归一化，默认不归一化处理，需要归一化处理时传入归一化方法，可取值'min-max'、'z-score'
    :return: x_values, y_values，分别表示输入数据和对应的标签值

    example:

        get_data('C:/stock/600006.csv', None, col_y=[1, 5])

        col_y=[1, 5]，
        则获得的标签中0代表股票涨幅小于1%，1代表涨幅位于[1, 5)，2代表涨幅处于[5,)

        col_y=[1]，则获得的标签中0代表股票涨幅小于1%，1表示股票涨幅大于等于1%。
    """
    gv.tsd.download(stock_code)  # 下载股票数据到本地，如果存在本地数据，则该语句相当于什么也不做
    # os.path.join(gv.dataDirectory, '{}.csv'.format(stock_code))
    # data = pd.read_csv(stock_code, encoding=gv.encoding)  # 相当于要让这句话常驻内存
    data = read_data_from_mysql_csv(stock_code, encoding=gv.encoding)  # 更新读取csv文件的方法，利用redis将数据驻留内存，多次调用加快速度
    if col_x is None:
        col_x = ['close']

    x = data[col_x].copy()  # 这里不加.copy()则报警告，因为修改x,y会修改data中对应的列值，pandas认为这可能是有问题的
    y = data['p_change'].copy()  # 股票涨幅位于区间[-10, 10]内；
    # =================================如果神经网络的输出是类别，这里把连续的y值按区间分类================================
    if isinstance(col_y, list):
        if len(col_y) == 0:
            gv.logger.warning("传入的col_y是一个空列表！")
        for i in col_y:
            if i < -10 or i > 10:
                gv.logger.warning("col_y的值超范围，涨跌幅限制在-0.1~0.1之间，传入的列表值达到{}".format(i))
                break
        # 按区间将标签分类，这里标签修改的顺序需要注意，
        # 修改后的标签的值不应落在区间[-10,10]内，所以标签0放在最后一个修改。
        y.loc[y > col_y[-1]] = len(col_y) * 100
        for i in range(len(col_y) - 1, 0, -1):
            condition_series = y[y > col_y[i - 1]][y < col_y[i]]  # 符合条件的行
            y[condition_series.index] = i * 100  # condition_series对应的行号的值设为i * 100
        y.loc[y < col_y[0]] = 0
        y = (y / 100).astype(int)
    # =================================如果神经网络的输出是类别，这里把连续的y值按区间分类================================
    if normalization == 'min-max':
        x = (x - x.min()) / (x.max() - x.min())  # df.min()默认是按行操作，即axis=0，将df形状的第一个数压缩为1
    elif normalization == 'z-score':
        x = (x - x.mean()) / x.std_range()  # 据说，pandas的std函数和numpy的std函数有差别，但是不影响神经网络训练结果

    return x.values, y.values  # 将DataFrame或Series转为ndarray


def get_data_stocks(stock_codes: list = None, col_x=None, col_y=None, normalization=None):
    """
    获取所有股票的数据

    从纯数据预测的角度来讲，所有股票的股价变化趋势都应是一样的

    :param stock_codes:
    :param col_x:
    :param col_y:
    :param normalization:
    :return:
    """
    stock_codes = gv.tsd.download_all_stocks(stock_codes)

    for stock_code in stock_codes:
        x, y = get_data(stock_code, col_x=None, col_y=None, normalization=None)


def get_data_days_list(stock_code, days=30, col_x=None, col_y=None, normalization=None, split=None,
                       need_pred=False):
    """
    构建神经网络训练数据集

    :param stock_code: 文件
    :param days: 根据过去days天的股票数据，预测接下来一天的涨幅
    :param col_x: x中的数据列
    :param col_y: 股票涨幅，如果传入的是列表，会把涨幅按列表分类，用于神经网络分类预测，例[1, 5]，列表中的值应大于-10，小于10
    :param normalization: 是否需要归一化，默认不归一化处理，需要归一化处理时传入归一化方法，可取值'min-max'、'z-score'
    :param split: split是None则不分割，split是(0,1)的小数，则分为两部分，如果split是长度为2的列表，如[0.7, 0.2]，则分为三部分
    :param need_pred: 是否返回需要预测的x数据
    :return: tuple(train_x, train_y, valid_x, valid_y, [...], pred_x)，数据类型是np.array
    """
    result_x, result_y = [], []
    x, y = get_data(stock_code, col_x=col_x, col_y=col_y, normalization=normalization)
    data_num = len(y)
    if data_num <= days + 100:
        gv.logger.error("文件{}中数据太少，不足以生成神经网络数据！data_num={}".format(stock_code, data_num))
        return None
    for i in range(data_num - days):  # 至少要有31天的数据，才能产生一个神经网络数据，即根据过去30天数据预测下一天的数据
        temp_x = []
        for j in range(days):
            temp_x.append(x[i + j])
        result_x.append(temp_x)
        result_y.append(y[i + days])
    # np.ndarray(x) 是以x为形状参数构建ndarray数组
    # np.array(x) 是以x为数据内容构建ndarray数组
    result = __split_dataset(np.array(result_x), np.array(result_y), split)

    if need_pred:
        pred_x = x[-days:]
        result = list(result)
        result.append(pred_x)
        result = tuple(result)
    return result


def __split_dataset(x, y, split=None):
    """
    将数据按split分为训练集、测试集和验证集。
    split是None则不分割，split是(0,1)之间的小数，则分为两部分，如果split是长度为2的列表，如[0.7, 0.2]，则分为三部分

    :param x: 数据集x，传入的是列表，则返回的tuple中对应的类型也是列表，传入的是np.array，则返回的tuple中对应的类型也是np.array
    :param y: 数据集y
    :param split: 分割数据集的大小
    :return: (x_train, y_train, x_test, y_test, x_valid, y_valid)
    """
    if split is None:
        result = (x, y)
    if isinstance(split, float):
        split = int(len(y) * split)
        x_train, y_train = x[:split], y[:split]
        x_test, y_test = x[split:], y[split:]
        result = (x_train, y_train, x_test, y_test)
    elif isinstance(split, list) and isinstance(split[0], float) and isinstance(split[1], float):
        split0 = int(len(y) * split[0])
        split1 = int(len(y) * (split[0] + split[1]))
        x_train, y_train = x[:split0], y[:split0]
        x_test, y_test = x[split0:split1], y[split0:split1]
        x_valid, y_valid = x[split1:], y[split1:]
        result = (x_train, y_train, x_test, y_test, x_valid, y_valid)
    return result


def get_data_days_generator(stock_code, days=30, col_x=None, col_y=None, split=0.7, normalization=None,
                            need_pred=False):
    """
    作用同get_data_days_list()，只是返回的是generator，目前有问题

    :param stock_code: 文件
    :param days: 根据过去days天的股票数据，预测接下来一天的涨幅
    :param col_x: x中的数据列
    :param col_y: 股票涨幅，如果传入的是列表，会把涨幅按列表分类，用于神经网络分类预测，例[1, 5]，列表中的值应大于-10，小于10
    :param split: split是None则不分割，split是(0,1)的小数，则分为两部分，如果split是长度为2的列表，如[0.7, 0.2]，则分为三部分
    :param normalization: 是否需要归一化，默认不归一化处理，需要归一化处理时传入归一化方法，可取值'min-max'、'z-score'
    :param need_pred: 是否返回需要预测的x数据
    """
    x, y = get_data_days_list(stock_code, days, col_x, col_y, normalization)

    result = __split_dataset(x, y, split)
    x_train, y_train, x_test, y_test = result

    def generator():
        for i in range(len(y)):
            yield x[i], y[i]

    def generator_train():
        for i in range(len(y_train)):
            yield x_train[i], y_train[i]

    def generator_test():
        for i in range(len(y_test)):
            yield x_test[i], y_test[i]

    if need_pred:  # 是否需要返回最后一个需要预测的x数据
        pred_x = x[-days:]
    return generator, generator_train, generator_test, pred_x


def read_data_from_mysql_csv(stock_code, encoding=gv.encoding):
    """
    读取股票基本数据，从mysql数据库或本地读取股票数据

    :param stock_code:
    :param encoding:
    :return:
    """

    # 首先检测mysql服务是否在运行
    # encoding: utf-8

    data = None
    if gv.storage == "mysql":  # 尝试从mysql数据库读取
        if has_table(table_name=f"basic{stock_code}"):
            data = read_dataframe_from_mysql(f"basic{stock_code}")
            if data is not None:
                return data
    else:
        # 如果本地没有mysql服务，就使用简单的csv文件读取
        file = os.path.join(gv.dataDirectory, '{}.csv'.format(stock_code))
        data = pd.read_csv(file, encoding=gv.encoding)
        return data
