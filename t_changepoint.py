import utils.excel2redis as rds
import base.timeseries_process as ts
import chart.plot as cPlt
import base.data_preProcess as bsPre

import pandas as pd
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


def kmeans_building(x1, x2, types_num, types, colors, shapes, _isPlot=False):
    X = np.array(list(zip(x1, x2))).reshape(len(x1), 2)
    kmeans_model = KMeans(n_clusters=types_num).fit(X)  # 设置聚类数n_clusters的值为types_num
    # 整理分类好的原始数据, 并画出聚类图
    x1_result = [];
    x2_result = []
    for i in range(types_num):
        temp = [];
        temp1 = []
        x1_result.append(temp)
        x2_result.append(temp1)
    for i, l in enumerate(kmeans_model.labels_):  # 画聚类点
        x1_result[l].append(x1[i])
        x2_result[l].append(x2[i])
        plt.scatter(x1[i], x2[i], c=colors[l], marker=shapes[l])
    for i in range(len(list(kmeans_model.cluster_centers_))):  # 画聚类中心点
        plt.scatter(list(list(kmeans_model.cluster_centers_)[i])[0], list(list(kmeans_model.cluster_centers_)[i])[1],
                    c=colors[i], marker=shapes[i], label=types[i])
    if (_isPlot == True):
        plt.legend()
        plt.show()
    return kmeans_model, x1_result, x2_result


# 按照移动极差大于固定值获取范围
def getDifferenceList(_df, _stdGCount, _stdMax, _isPlot=False):
    df = _df
    plt.figure(figsize=(8, 6))
    x1 = df.index  # x坐标列表
    result_list = []
    for i in range(0, df.shape[1], 1):
        x2 = df.values[:, i]  # y坐标列表
        colors = ['b', 'g', 'r']  # 颜色列表，因为要分3类，所以该列表有3个元素
        shapes = ['o', 's', 'D']  # 点的形状列表，因为要分3类，所以该列表有3个元素
        labels = ['A', 'B', 'C']  # 画图的标签内容，A, B, C分别表示三个类的名称
        kmeans_model, x1_result, x2_result = kmeans_building(x1, x2, 3, labels, colors, shapes,
                                                             _isPlot)  # 本例要分3类，所以传入一个3
        diff = [abs(x2_result[i][-1] - x2_result[i][0]) for i in range(0, len(x2_result), 1)]
        maxIndex = diff.index(max(diff))  # 最大值index
        DifferenceList_x1 = x1_result[maxIndex]
        DifferenceList_x2 = x2_result[maxIndex]
        DifferenceSeries = pd.Series(DifferenceList_x2, index=DifferenceList_x1)
        # center = True
        # 移动标准差
        # Difference_std = DifferenceSeries.rolling(_stdGCount).std()
        # 移动极差
        Difference_max = DifferenceSeries.rolling(_stdGCount).max()
        Difference_min = DifferenceSeries.rolling(_stdGCount).min()
        Difference_std = Difference_max.sub(Difference_min)

        # _stdMax = (DifferenceSeries.max() - DifferenceSeries.min()) * 0.07

        Difference_std_sort = Difference_std.sort_values(ascending=False)
        Difference_std_top = Difference_std_sort[Difference_std_sort.values > _stdMax]
        if (len(Difference_std_top) == 0):
            Difference_std_top = Difference_std_sort
        Difference_std_topIndex = Difference_std_top.index
        Difference_std_topIndex = Difference_std_topIndex.sort_values()

        # rolling_series_list = []
        # for index in Difference_std_topIndex:
        #     rolling_series = DifferenceSeries[
        #         (DifferenceSeries.index.values > index - _stdGCount) & (DifferenceSeries.index.values <= index)]
        #     rolling_series_list.append(rolling_series)
        #
        # all_list = []
        # [all_list.extend(_list) for _list in [rol.index.values for rol in rolling_series_list]]
        #
        # all_list = list(set(all_list))
        # all_list.sort()
        # result_series = DifferenceSeries[
        #     (DifferenceSeries.index.values >= all_list[0]) & (DifferenceSeries.index.values <= all_list[-1])]

        result_series = DifferenceSeries[(DifferenceSeries.index.values >= Difference_std_topIndex[0]) & (
                DifferenceSeries.index.values <= Difference_std_topIndex[-1])]
        result_list.append(result_series)
        if (_isPlot == True):
            plt.scatter(result_series.index, result_series.values)
            plt.legend()
            plt.show()
        # cPlt.singlePlot(result_series.to_frame(name=None), _name="", _title="")
    return result_list


# 按照移动极差大于总极差百分比获取范围
def getDifferenceList_aut(_df, _stdGCount, _per, _isPlot=False):
    df = _df
    plt.figure(figsize=(8, 6))
    x1 = df.index  # x坐标列表
    result_list = []
    for i in range(0, df.shape[1], 1):
        x2 = df.values[:, i]  # y坐标列表
        colors = ['b', 'g', 'r']  # 颜色列表，因为要分3类，所以该列表有3个元素
        shapes = ['o', 's', 'D']  # 点的形状列表，因为要分3类，所以该列表有3个元素
        labels = ['A', 'B', 'C']  # 画图的标签内容，A, B, C分别表示三个类的名称
        kmeans_model, x1_result, x2_result = kmeans_building(x1, x2, 3, labels, colors, shapes,
                                                             _isPlot)  # 本例要分3类，所以传入一个3
        diff = [abs(x2_result[i][-1] - x2_result[i][0]) for i in range(0, len(x2_result), 1)]
        maxIndex = diff.index(max(diff))  # 最大值index
        DifferenceList_x1 = x1_result[maxIndex]
        DifferenceList_x2 = x2_result[maxIndex]
        DifferenceSeries = pd.Series(DifferenceList_x2, index=DifferenceList_x1)
        # center = True
        # 移动标准差
        # Difference_std = DifferenceSeries.rolling(_stdGCount).std()
        # 移动极差
        Difference_max = DifferenceSeries.rolling(_stdGCount).max()
        Difference_min = DifferenceSeries.rolling(_stdGCount).min()
        Difference_std = Difference_max.sub(Difference_min)

        _stdMax = (DifferenceSeries.max() - DifferenceSeries.min()) * _per

        Difference_std_sort = Difference_std.sort_values(ascending=False)
        Difference_std_top = Difference_std_sort[Difference_std_sort.values > _stdMax]
        if (len(Difference_std_top) == 0):
            Difference_std_top = Difference_std_sort
        Difference_std_topIndex = Difference_std_top.index
        Difference_std_topIndex = Difference_std_topIndex.sort_values()

        # rolling_series_list = []
        # for index in Difference_std_topIndex:
        #     rolling_series = DifferenceSeries[
        #         (DifferenceSeries.index.values > index - _stdGCount) & (DifferenceSeries.index.values <= index)]
        #     rolling_series_list.append(rolling_series)
        #
        # all_list = []
        # [all_list.extend(_list) for _list in [rol.index.values for rol in rolling_series_list]]
        #
        # all_list = list(set(all_list))
        # all_list.sort()
        # result_series = DifferenceSeries[
        #     (DifferenceSeries.index.values >= all_list[0]) & (DifferenceSeries.index.values <= all_list[-1])]

        result_series = DifferenceSeries[(DifferenceSeries.index.values >= Difference_std_topIndex[0]) & (
                DifferenceSeries.index.values <= Difference_std_topIndex[-1])]
        result_list.append(result_series)
        if (_isPlot == True):
            plt.scatter(result_series.index, result_series.values)
            plt.legend()
            plt.show()
        # cPlt.singlePlot(result_series.to_frame(name=None), _name="", _title="")
    return result_list


# 按照移动极差topN 获取范围
# df 批次数据 _stdGCount 移动极差样本数 _stdTop 极差topN
def getDifferenceList_Top(_df, _stdGCount, _stdTop, _isPlot=False):
    df = _df
    plt.figure(figsize=(8, 6))
    x1 = df.index  # x坐标列表
    result_list = []

    for i in range(0, df.shape[1], 1):
        x2 = df.values[:, i]  # y坐标列表
        colors = ['b', 'g', 'r']  # 颜色列表，因为要分3类，所以该列表有3个元素
        shapes = ['o', 's', 'D']  # 点的形状列表，因为要分3类，所以该列表有3个元素
        labels = ['A', 'B', 'C']  # 画图的标签内容，A, B, C分别表示三个类的名称
        kmeans_model, x1_result, x2_result = kmeans_building(x1, x2, 3, labels, colors, shapes,
                                                             _isPlot)  # 本例要分3类，所以传入一个3
        diff = [abs(x2_result[i][-1] - x2_result[i][0]) for i in range(0, len(x2_result), 1)]
        maxIndex = diff.index(max(diff))  # 最大值index
        DifferenceList_x1 = x1_result[maxIndex]
        DifferenceList_x2 = x2_result[maxIndex]
        DifferenceSeries = pd.Series(DifferenceList_x2, index=DifferenceList_x1)
        # center = True
        # 移动标准差
        # Difference_std = DifferenceSeries.rolling(_stdGCount).std()
        # 移动极差
        Difference_max = DifferenceSeries.rolling(_stdGCount).max()
        Difference_min = DifferenceSeries.rolling(_stdGCount).min()
        Difference_std = Difference_max.sub(Difference_min)

        Difference_std_sort = Difference_std.sort_values(ascending=False)
        Difference_std_top = Difference_std_sort[0: _stdTop]

        # top_index = []
        # top_value = []
        # i_stdTop = 0
        # for i, t in Difference_std_top.to_frame(name=None).iteritems:
        #     if (i_stdTop < _stdTop):
        #         top_index.append(i)
        #         top_value.append(t)
        # Difference_std_top.pd.Series(top_value, index=top_index)

        if (len(Difference_std_top) == 0):
            Difference_std_top = Difference_std_sort

        Difference_std_topIndex = Difference_std_top.index
        Difference_std_topIndex = Difference_std_topIndex.sort_values()

        rolling_series_list = []
        for index in Difference_std_topIndex:
            rolling_series = DifferenceSeries[
                (DifferenceSeries.index.values > index - _stdGCount) & (DifferenceSeries.index.values <= index)]
            rolling_series_list.append(rolling_series)

        all_list = []
        [all_list.extend(_list) for _list in [rol.index.values for rol in rolling_series_list]]

        all_list = list(set(all_list))
        all_list.sort()

        # result_series = DifferenceSeries[
        #     (DifferenceSeries.index.values >= all_list[0]) & (DifferenceSeries.index.values <= all_list[-1])]

        result_series = DifferenceSeries[(DifferenceSeries.index.values >= all_list[0]) & (
                DifferenceSeries.index.values <= all_list[-1])]
        result_list.append(result_series)
        if (_isPlot == True):
            plt.scatter(result_series.index, result_series.values)
            plt.legend()
            plt.show()
        # cPlt.singlePlot(result_series.to_frame(name=None), _name="", _title="")
        vi = getHeadOrTail(result_series, "Last")
        print(vi)
    return result_list


# 获取最后一个最小值或第一最大值
def getHeadOrTail(_series, _type):
    if (_type == "Last"):
        minV = min(_series.values)
        min_series = _series[_series.values == minV]
        return [min_series.values[-1], min_series.index.values[-1]]
        print()
    elif (_type == "First"):
        maxV = max(_series.values)
        max_series = _series[_series.values == maxV]
        return [max_series.values[0], max_series.index.values[0]]


# 批次
batchStr = "b-YAR-19033103203-*"
# 获取批次数据
df = rds.getBatchData(batchStr, 1)
# #获取时间列
# _series = pd.Series(df[0].values, index = df.index.values)
# 获取数据是否连续
# indexList=ts.check_ts_continuity(_series)
# 定义使用的列
useCol = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
df = DataFrame(df.values[:, useCol])
# diffCol = [0,1,2,3,4,5,6]
# 目标列Y
yCol = 6
# 时间频率
freq = 6
df = df[:int(len(df) / 2)]
# df = df[35:49]
cPlt.singlePlot(df,_title=batchStr)
# cp = bsPre.compute_ChangePoint(df, _mode="last")
# print(cp)
# df 批次数据 _stdGCount 移动极差样本数 _stdTop 极差topN
# cp1 = getDifferenceList_Top(df, 5, 21)
# cp1 = getDifferenceList(df, 5,1)
dt = DataFrame(df[[1]])
cp1 = getDifferenceList_Top(df, 10, 3, _isPlot=False)
# print(cp1)
