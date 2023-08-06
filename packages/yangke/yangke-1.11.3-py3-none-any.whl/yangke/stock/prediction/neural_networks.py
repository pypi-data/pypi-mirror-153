
def set_LSTM_x_y(data_local):
    data_local = data_local.tolist()
    size = len(data_local)
    x = []  # x包含data_local个数据
    y = []
    local_kind = ["跌", "涨幅位于区间[0, 1%]", "涨幅位于区间[1%, 2%]",
                  "涨幅位于区间[2%, 3%]", "涨幅位于区间[3%, 4%]",
                  "涨幅位于区间[4%, 5%]", "涨幅位于区间[5%, 6%]", "涨幅位于区间[6%, 7%]",
                  "涨幅位于区间[7%, 8%]", "涨幅位于区间[8%, 10%"]
    for i in range(size - 60):
        x_temp = []
        for j in range(60, 0, -1):
            x_temp.append(data_local[i + 60 - j])
        x.append(x_temp)
        inc = data_local[i + 60][0] - data_local[i + 59][0]
        y_temp = inc / data_local[i + 59][0]
        if y_temp < 0:
            y.append(0)
        elif y_temp < 0.01:
            y.append(1)
        elif y_temp < 0.02:
            y.append(2)
        elif y_temp < 0.03:
            y.append(3)
        elif y_temp < 0.04:
            y.append(4)
        elif y_temp < 0.05:
            y.append(5)
        elif y_temp < 0.06:
            y.append(6)
        elif y_temp < 0.07:
            y.append(7)
        elif y_temp < 0.08:
            y.append(8)
        else:
            y.append(9)
    # x比y多一个数据
    x_temp = []
    for j in range(60, 0, -1):
        x_temp.append(data_local[size - j])

    x.append(x_temp)
    return x, y, local_kind


def normalization(x):
    x = np.array(x)
    mean = np.mean(x, axis=0)
    std = np.std_range(x, axis=0)
    normalized_x = (x - mean) / std
    return normalized_x


def prediction_by_1MACD(df):
    """
    MACD_DIFF、MACD_DEA、MACD;中长期指标

    :return label: 0-无预测意见，1-买入信号，-1-卖出信号
    """
    label = 0
    diff = np.array(df['MACD_DIFF'])
    dea = np.array(df['MACD_DEA'])
    macd = np.array(df['MACD'])
    if diff[-1] > 0 & dea[-1] > 0:
        if (diff[-1] - dea[-1]) > (diff[-2] - dea[-2]) > (diff[-3] - dea[-3]) > (diff[-4] - dea[-4]):
            label = 1 + label
    if (diff[-1] - dea[-1]) < (diff[-2] - dea[-2]) < (diff[-3] - dea[-3]):
        label = label - 1
    return label


def prediction_by_2DMI(df):
    """
    中长期指标
    :param df:
    :return:
    """
    pass


def prediction_by_3DMA(df):
    """
    中短期指标
    :param df:
    :return:
    """
    pass


def prediction_by_4TRIX(df):
    """
    长期指标
    :param df:
    :return:
    """
    TRIX = df['TRIX']
    MATRIX = df['MATRIX']
    result = 0
    if (TRIX[-1] - MATRIX[-1]) > 0 > (TRIX[-2] - MATRIX[-2]):  # 认为TRIX线向上突破TRMA线 金叉
        result = 1
    elif (TRIX[-1] - MATRIX[-1]) < 0 < (TRIX[-2] - MATRIX[-2]):  # 认为TRIX线在高位向下突破TRMA线 死叉
        result = -1
    return result


def prediction_by_5BRAR(df):
    pass


def prediction_by_6VR(df):
    """
    中期指标
    :param df:
    :return:
    """
    pass


def prediction_by_7OBV(df):
    pass


def prediction_by_8EMV(df):
    pass


def prediction_by_9WVAD(df):
    """
    长期指标
    WVAD、ADX、PDI、MDI
    :param df:
    :return:
    """
    pass


def prediction_by_10RSI(df):
    pass


def prediction_by_11WR(df):
    """
    短期指标
    :param df:
    :return:
    """
    pass


def prediction_by_12KDJ(df):
    """
    中短期指标
    :param df:
    :return:
    """
    pass


def prediction_by_13CCI(df):
    """
    短期暴涨暴跌行情研判指标
    :param df:
    :return:
    """
    pass


def prediction_by_14ROC(df):
    """
    短期指标
    :param df:
    :return:
    """
    pass


def prediction_by_15BOLL(df):
    """
    中长期指标
    :param df:
    :return:
    """
    pass


def prediction_by_16BIAS(df):
    pass


def prediction_by_17PSY(df):
    """
    短期指标
    :param df:
    :return:
    """
    pass
