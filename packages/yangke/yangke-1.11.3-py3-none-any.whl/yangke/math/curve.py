import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate, scipy.optimize
import pandas as pd


def get_intersection_of_curve(x, y, func):
    x = np.array(x)
    y1 = np.array(y)
    y1, x = sort_an_array_by_another_array(y1, x)
    y2 = [func(x1) for x1 in x]

    interp1 = scipy.interpolate.InterpolatedUnivariateSpline(x, y1)
    interp2 = scipy.interpolate.InterpolatedUnivariateSpline(x, y2)

    def difference(x):
        return np.abs(interp1(x) - interp2(x))

    x_at_crossing = scipy.optimize.fsolve(difference, x0=3.0)

    return x_at_crossing, interp1(x_at_crossing)


def sort_an_array_by_another_array(sorted_array, by_array, ascending=True):
    """
    根据by_array的大小顺序，对两个数组都进行排序，返回两个数组排序后的结果

    :param sorted_array:
    :param by_array:
    :param ascending: 是否升序
    :return:
    """
    xy = pd.DataFrame([sorted_array, by_array])
    xy = xy.sort_values(by=1, axis=1, ascending=ascending)  # axis表示按行还是列排序，by表示指定排序的行号或列号，这里表示按行号为1的行排序
    return xy.iloc[0], xy.iloc[1]
