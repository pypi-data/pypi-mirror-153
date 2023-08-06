import datetime
# import locale
import io
import os
# import json
import sys
import time
from datetime import date
import logging
from dataset.tushareData import *
import common.fileOperate as fo

import numpy as np
import pandas as pd
import pandas_ta as ta
# import talib  # 下载不成功
import tensorflow as tf
import tushare as ts  # 股票数据下载


def append_MACD_to_stocks(directory: str, code: int):
    """
    读取本地的股票数据，计算以下股票指标并写入文件
    股票指标：\n
    ADX-Average Directional Indicator:平均趋向指标\n
    ADXR-:平均方向指数评估，配合ADX、DMI\n
    AR-BRAR_AR:人气指标\n
    ATR-Average True Ranger:均幅指标\n
    BOLL、BBANDs-Bollinger Bands:布林线指标。结合Trix判断更准确\n
    BR-BRAR_BR:意愿指标\n
    CCI-Commodity Channel Index:顺势指标\n
    CR-BRAR_CR: 该指标比较复杂，且各证券公司客户端数据不一致\n
    DMA-Different of Moving Average:平均差、平行线差指标。中短期\n
    DMA_AMA/DIFMA-10日DMA平均值\n
    DMI-Directional Movement Index:本身不对应任何值，它包括PDI、MDI、ADX和ADXR四个有值的指标\n
    MACD-Moving Average Convergence Divergence:移动平均聚散指标、平滑异同平均\n
    MATRIX-Moving Average of TRIX:通过stockStat['trix_9_sma']获得其值\n
    MAVR-Moving Average of VR:通过stockStat['vr_6_sma']获得其值\n
    MDI-DMI_MDI:DMI的子指标，即 -DI\n
    PDI-DMI_PDI:DMI的子指标，即 +DI\n
    ROC-:变动率指标\n
    RSI-Relative Strength Index:相对强弱指数、相对力度指数\n
    SMA-Simple Moving Average：简单移动平均线\n
    TR-True Ranger:均幅指标\n
    TRIX-Triple Exponentially Smoothed Average:三重指数平滑移动平均指标、三重指数平均线\n
    VR-Volumn Ratio:成交量变异率、成交量比率。中期\n
    WR-Williams Rate:威廉指标\n
    :param directory:
    :param code:
    :return:
    """
    file = os.path.join(directory, code + '.csv')
    df = pd.read_csv(file)

    df = cal_ARBR(df)
    # df['ATR'] = stockStat['atr']
    BOLL = ta.bbands(df['close'])  # df['boll']、df['boll_ub']、df['boll_lb']
    df = df.join(BOLL, how='right')
    cal_CCI(df, n=14)  # 已验证

    del BOLL
    cal_CR(df, n=26)  # 已验证

    # 弥补AR、BR的不足:https://wiki.mbalib.com/wiki/CR%E6%8C%87%E6%A0%87
    df['DMA'] = df['close'].rolling(10).mean() - df['close'].rolling(50).mean()  # stockStat['dma']  # 已验证，也称为DMA_DIF
    df['DMA_AMA'] = df['DMA'].rolling(10).mean()  # 已验证，也称为DMA_DIFMA
    cal_DMI(df)
    # ta.adx()

    # df['DX'] = stockStat['dx']
    cal_KDJ(df, 9)
    cal_MACD(df)  # pandas_ta的macd计算在某些情况下会报下标越界错误，这里自己编写

    cal_WR(df, 10, 6)  # 已验证

    df['ROC'] = ta.roc(df['close'])
    df['RSI'] = ta.rsi(df['close'])
    # df['OBV'] = ta.obv(close=df['close'], volume=df['volume'])
    df['OBV'] = talib.OBV(df['close'], df['volume'])

    # df['TR'] = stockStat['tr']
    df['TRIX'] = talib.TRIX(df['close'], timeperiod=14)
    df['MATRIX'] = talib.MA(df['TRIX'], 9, 0)

    cal_VR(df)  # stockStat['vr']

    # df.drop(['price_change', 'p_change', 'v_ma5', 'v_ma10', 'ma5', 'ma10', 'ma20',
    #          'v_ma20', 'high_delta', 'um', 'low_delta', 'dm', 'pdm', 'pdm_14_ema', 'pdm_14',
    #          'close_-1_s', 'tr', 'atr_14', 'mdm', 'mdm_14_ema', 'pdi_14', 'pdi',
    #          'mdm_14', 'mdi_14', 'mdi', 'dx_14', 'dx',
    #          'dx_6_ema', 'adx', 'adx_6_ema', 'adxr',
    #          'atr',  # 'middle', 'middle_14_sma', 'cci_14','cr', 'cr-ma1', 'cr-ma2', 'cr-ma3',
    #          'close_10_sma', 'close_50_sma', 'dma', 'wr_10', 'wr_6', 'change', 'vr'],
    #         axis=1, inplace=True)

    df.to_csv(file, index=False)


def cal_VR(df, n=26, m=6):
    # TH:=SUM(IF(CLOSE>REF(CLOSE,1),VOL,0),N);
    # TL:=SUM(IF(CLOSE<REF(CLOSE,1),VOL,0),N);
    # TQ:=SUM(IF(CLOSE=REF(CLOSE,1),VOL,0),N);
    # VR:100*(TH*2+TQ)/(TL*2+TQ);
    # MAVR:MA(VR,M);
    ref1 = pd.Series(np.where(df['close'] > df['close'].shift(1), df['volume'], 0))
    th = ref1.rolling(n).sum()
    ref2 = pd.Series(np.where(df['close'] < df['close'].shift(1), df['volume'], 0))
    tl = ref2.rolling(n).sum()
    ref3 = pd.Series(np.where(df['close'] == df['close'].shift(1), df['volume'], 0))
    tq = ref3.rolling(n).sum()
    vr = 100 * (th * 2 + tq) / (tl * 2 + tq)
    df['VR'] = np.array(vr)
    df['VR_MAVR'] = df['VR'].rolling(m).mean()
    return df


def cal_WR(df, n=10, n1=6):
    # WR1:100*(HHV(HIGH,N)-CLOSE)/(HHV(HIGH,N)-LLV(LOW,N));
    # WR2:100*(HHV(HIGH,N1)-CLOSE)/(HHV(HIGH,N1)-LLV(LOW,N1));
    temp = pd.DataFrame()
    temp['HHV'] = df['high'].rolling(n).max()
    temp['LLV'] = df['low'].rolling(n).min()
    df['WR_' + str(n)] = 100 * (temp['HHV'] - df['close']) / (temp['HHV'] - temp['LLV'])
    temp['HHV1'] = df['high'].rolling(n1).max()
    temp['LLV1'] = df['low'].rolling(n1).min()
    df['WR_' + str(n1)] = 100 * (temp['HHV1'] - df['close']) / (temp['HHV1'] - temp['LLV1'])
    return df


def cal_DMI(df, n1=14, n2=6):
    """
    本方法已验证，stockstats中DMI计算的四个参数全部错误
    :param df:
    :param n1:
    :param n2:
    :return:
    """
    '''
    MTR:=SUM(MAX(MAX(HIGH-LOW,ABS(HIGH-REF(CLOSE,1))),ABS(REF(CLOSE,1)-LOW)),N);
    HD :=HIGH-REF(HIGH,1);
    LD :=REF(LOW,1)-LOW;
    DMP:=SUM(IF(HD>0&&HD>LD,HD,0),N);
    DMM:=SUM(IF(LD>0&&LD>HD,LD,0),N);
    PDI: DMP*100/MTR;
    MDI: DMM*100/MTR;
    ADX: MA(ABS(MDI-PDI)/(MDI+PDI)*100,M);
    ADXR:(ADX+REF(ADX,M))/2;
    '''

    HD = df['high'] - df['high'].shift(1)
    LD = df['low'].shift(1) - df['low']

    T1 = df['high'] - df['low']
    T2 = abs(df['high'] - df['close'].shift(1))

    TEMP1 = np.where(T1 >= T2, T1, T2)
    TEMP2 = abs(df['low'] - df['close'].shift(1))
    TEMP = pd.Series(np.where(TEMP1 >= TEMP2, TEMP1, TEMP2))

    TR = TEMP.rolling(n1).sum()

    # df.iloc[(HD > 0) & (HD > LD), 'hd1'] = HD
    # df.iloc[(LD > 0) & (LD > HD), 'ld1'] = LD
    HD1 = pd.Series(np.where(((HD > 0) & (HD > LD)), HD, 0))
    LD1 = pd.Series(np.where(((LD > 0) & (LD > HD)), LD, 0))

    DMP = HD1.rolling(n1).sum()
    DMM = LD1.rolling(n1).sum()

    df['DMI_PDI'] = np.array(DMP / TR * 100)
    df['DMI_MDI'] = np.array(DMM / TR * 100)
    TEMP3 = abs(df['DMI_MDI'] - df['DMI_PDI']) / (df['DMI_MDI'] + df['DMI_PDI']) * 100
    df['DMI_ADX'] = np.array(TEMP3.rolling(n2).mean())
    df['DMI_ADXR'] = (df['DMI_ADX'] + df['DMI_ADX'].shift(n2)) / 2

    return df


def cal_ARBR(df: pd.DataFrame, n: int = 26) -> pd.DataFrame:
    stock = pd.DataFrame()
    stock['HO'] = df['high'] - df['open']
    stock['OL'] = df['open'] - df['low']
    stock['HCY'] = df['high'] - df['close'].shift(1)
    # 百度百科等介绍的指标计算没有取非负值的步骤,百度百科关于很多指标的计算公式都有问题
    stock['HCY'] = np.where(stock['HCY'] < 0, 0, stock['HCY'])  # 将stock['HCY']列小于0的数替换为0，即取非负值
    stock['CYL'] = df['close'].shift(1) - df['low']
    stock['CYL'] = np.where(stock['CYL'] < 0, 0, stock['CYL'])  # 将stock['CYL']列小于0的数替换为0
    df['ARBR_AR'] = stock['HO'].rolling(26).sum() / stock['OL'].rolling(26).sum() * 100  # 已验证
    df['ARBR_BR'] = stock['HCY'].rolling(26).sum() / stock['CYL'].rolling(26).sum() * 100  # 已验证
    return df


def cal_CCI(df, n=14):
    """
    计算CCI指标，已验证。
    pandas_ta的cci指标计算结果错误，stockstats的cci指标有警告，另外，
    百度百科里的cci指标计算公式错误，主要是close和TYP弄混了，其次
    # MD = (MA - TYP).abs().rolling(n).mean()计算的MD是不对的，因为MA不应参与rolling,
    而应该与当前MD的索引一致
    :param df:
    :param n:
    :return:
    """
    # TYP: = (HIGH + LOW + CLOSE) / 3;
    # CCI: (TYP - MA(TYP, N)) / (0.015 * AVEDEV(TYP, N));
    TYP = (df['high'] + df['low'] + df['close']) / 3
    MA = TYP.rolling(n).mean()
    cci = []
    for i in range(len(MA)):
        ma = MA.iloc[i]
        if i < n - 1:
            cci.append(np.NaN)
            continue
        else:
            sum = 0
            for j in range(n):
                sum = abs(TYP.iloc[i - j] - ma) + sum
            md = sum / n
        cci.append((TYP.iloc[i] - ma) / (0.015 * md))

    df['CCI'] = cci

    return df


def cal_CR(df, n=26):
    """
    结果已验证，stockstats的cr计算结果错误
    MID:=REF(HIGH+LOW,1)/2;
    CR:SUM(MAX(0,HIGH-MID),N)/SUM(MAX(0,MID-LOW),N)*100;
    MA1:REF(MA(CR,M1),M1/2.5+1);
    MA2:REF(MA(CR,M2),M2/2.5+1);
    MA3:REF(MA(CR,M3),M3/2.5+1);
    MA4:REF(MA(CR,M4),M4/2.5+1);
    :param df:
    :param n:
    :return:
    """
    MID = ((df['high'] + df['low']) / 2).shift(1)
    P1 = df['high'] - MID
    P1 = np.where(P1 < 0, 0, P1)  # 将stock['HCY']列小于0的数替换为0，即取非负值
    P1 = pd.Series(P1)
    P2 = MID - df['low']
    P2 = np.where(P2 < 0, 0, P2)
    P2 = pd.Series(P2)
    CR = P1.rolling(n).sum() / P2.rolling(n).sum() * 100  # 直接使用df['CR'] = CR，结果df['CR']没有数据，全是空值
    df['CR'] = np.array(CR)
    return df


def cal_MACD(df, fast_ma=12, slow_ma=26, ma=9):
    """
    已验证
    中长期投资者首选参考指标，该指标具有滞后性，当行情迅速大幅涨跌时，不适用。\n

    :param df: original dataframe, index = 'date',
                columns ='open','high','close','low','volume','amount'
    :param fast_ma: fast period
    :param slow_ma: slow period
    :param ma: moving average
    :return: DateFrame
    """
    df['MACD_DIFF'] = df['close'].ewm(adjust=False, alpha=2 / (fast_ma + 1), ignore_na=True).mean() - \
                      df['close'].ewm(adjust=False, alpha=2 / (slow_ma + 1), ignore_na=True).mean()
    df['MACD_DEA'] = df['MACD_DIFF'].ewm(adjust=False, alpha=2 / (ma + 1), ignore_na=True).mean()
    df['MACD'] = 2 * (df['MACD_DIFF'] - df['MACD_DEA'])
    return df


def cal_KDJ(df, n=9, ksgn='close'):
    """
    【输入】
        df, pd.dataframe格式数据源
        n，时间长度
        ksgn，列名，一般是：close收盘价
    【输出】    
        df, pd.dataframe格式数据源,
        增加了一栏：_{n}，输出数据
    """
    lowList = df['low'].rolling(n).min()
    lowList.fillna(value=df['low'].expanding().min(), inplace=True)
    highList = df['high'].rolling(n).max()
    highList.fillna(value=df['high'].expanding().max(), inplace=True)
    rsv = (df[ksgn] - lowList) / (highList - lowList) * 100

    df['KDJ_K'] = rsv.ewm(com=2).mean()  # 指数平滑移动平均线
    df['KDJ_D'] = df['KDJ_K'].ewm(com=2).mean()  # Exponentially Weighted Moving-Average

    df['KDJ_J'] = 3.0 * df['KDJ_K'] - 2.0 * df['KDJ_D']
    return df
