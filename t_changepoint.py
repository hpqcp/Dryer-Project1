import utils.excel2redis as rds
import base.timeseries_process as ts
import chart.plot as cPlt
import base.data_preProcess as bsPre

import pandas as pd
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


def kmeans_building(x1, x2, types_num, types, colors, shapes):
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
    plt.legend()
    plt.show()
    return kmeans_model, x1_result, x2_result


def getDifferenceList(_df, _stdGCount, _stdMax):
    # #获取时间列
    # _series = pd.Series(df[0].values, index = df.index.values)
    # 获取数据是否连续
    # indexList=ts.check_ts_continuity(_series)
    # 定义使用的列
    useCol = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    df = _df
    df = DataFrame(df.values[:, useCol])
    # diffCol = [0,1,2,3,4,5,6]
    # 目标列Y
    yCol = 6
    # 时间频率
    freq = 6
    df = df[:int(len(df) / 2)]
    # df = df[35:49]
    # cPlt.singlePlot(df,_title=batchStr)
    cp = bsPre.compute_ChangePoint(df, _mode="last")
    print(cp)
    # ds = DataFrame({"data":df.values[:,1],"index":df.index})
    # clf = KMeans(n_clusters=3, random_state=10).fit(ds)
    # dt = clf.labels_
    # plt.plot(dt)
    # plt.show()
    #
    # # print(dt)
    # # df_count_type=dt.groupby('tag_col').apply(np.size)
    # exit()
    plt.figure(figsize=(8, 6))
    x1 = df.index  # x坐标列表
    x2 = df.values[:, 1]  # y坐标列表
    colors = ['b', 'g', 'r']  # 颜色列表，因为要分3类，所以该列表有3个元素
    shapes = ['o', 's', 'D']  # 点的形状列表，因为要分3类，所以该列表有3个元素
    labels = ['A', 'B', 'C']  # 画图的标签内容，A, B, C分别表示三个类的名称
    kmeans_model, x1_result, x2_result = kmeans_building(x1, x2, 3, labels, colors, shapes)  # 本例要分3类，所以传入一个3
    # print(kmeans_model)
    # print(x1_result)
    # print(x2_result)
    diff = [x2_result[i][-1] - x2_result[i][0] for i in range(0, len(x2_result), 1)]
    maxIndex = diff.index(max(diff))  # 最大值index
    DifferenceList_x1 = x1_result[maxIndex]
    DifferenceList_x2 = x2_result[maxIndex]
    DifferenceSeries = pd.Series(DifferenceList_x2, index=DifferenceList_x1)
    # center = True
    Difference_std = DifferenceSeries.rolling(_stdGCount).std()

    Difference_std_sort = Difference_std.sort_values(ascending=False)
    Difference_std_top = Difference_std_sort[Difference_std_sort.values > _stdMax]
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
    plt.scatter(result_series.index, result_series.values)
    plt.legend()
    plt.show()
    # cPlt.singlePlot(result_series.to_frame(name=None), _name="", _title="")
    return result_series


# 批次
batchStr = "b-YAR-19033102503-*"
# 获取批次数据
df = rds.getBatchData(batchStr, 1)
getDifferenceList(df, 8, 0.22)
