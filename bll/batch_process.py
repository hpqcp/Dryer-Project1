###
###
### 


import pandas as pd
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


#
#
#
def check_batch_point(_df, _groupRatio=0.1, _GroupTop=5):
    # 将df分为前后两半
    firstDf = _df[:int(_df.shape[0] / 2)]
    lastDf = _df[firstDf.shape[0]:].reset_index(drop=True)
    # 处理前半部分数据
    lsFirst = getDifferenceList_Top(firstDf, _stdGPro=_groupRatio, _stdTop=_GroupTop, _mode="up", _isPlot=True)
    lsLast = getDifferenceList_Top(lastDf, _stdGPro=_groupRatio, _stdTop=_GroupTop, _mode="down", _isPlot=True)
    print(lsFirst)
    print(lsLast)


# 按照移动极差topN 获取范围
# _df 批次数据  ， _stdGPro 分组比率 ，  _stdTop 极差topN
# _mode = up 上升波形（料头）  ， down 下降波形（料尾）
# _isPlot 是否绘图
def getDifferenceList_Top(_df, _stdGPro, _stdTop, _mode="up", _isPlot=False):
    df = _df
    x1 = df.index  # x坐标列表
    result_list = []
    if (_isPlot == True):
        plt.figure(figsize=(8, 6))

    for i in range(0, df.shape[1], 1):
        x2 = df.values[:, i]  # y坐标列表
        colors = ['b', 'g', 'r']  # 颜色列表，因为要分3类，所以该列表有3个元素
        shapes = ['o', 's', 'D']  # 点的形状列表，因为要分3类，所以该列表有3个元素
        labels = ['A', 'B', 'C']  # 画图的标签内容，A, B, C分别表示三个类的名称
        kmeans_model, x1_result, x2_result = kmeans_building(x1, x2, 3, labels, colors, shapes,
                                                             _isPlot)  # 本例要分3类，所以传入一个3
        diff = []
        if (_mode == "up"):
            diff = [x2_result[i][-1] - min(x2_result[i]) for i in range(0, len(x2_result), 1)]
        else:
            diff = [x2_result[i][0] - min(x2_result[i]) for i in range(0, len(x2_result), 1)]
        maxIndex = diff.index(max(diff))  # 最大值index
        DifferenceList_x1 = x1_result[maxIndex]
        DifferenceList_x2 = x2_result[maxIndex]
        DifferenceSeries = pd.Series(DifferenceList_x2, index=DifferenceList_x1)
        _stdGCount = int(len(DifferenceSeries) * _stdGPro)
        Difference_max = DifferenceSeries.rolling(_stdGCount).max()
        Difference_min = DifferenceSeries.rolling(_stdGCount).min()
        Difference_std = Difference_max.sub(Difference_min)
        Difference_std_sort = Difference_std.sort_values(ascending=False)
        Difference_std_top = Difference_std_sort[0: _stdTop]
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

        result_series = DifferenceSeries[(DifferenceSeries.index.values >= all_list[0]) & (
                DifferenceSeries.index.values <= all_list[-1])]
        result_list.append(result_series)
        if (_isPlot == True):
            plt.scatter(result_series.index, result_series.values)
            plt.legend()
            plt.show()
    return result_list


# 获取最后一个最小值或第一最大值
def getHeadOrTail(_series, _type):
    if (_type == "Last"):
        minV = min(_series.values)
        min_series = _series[_series.values == minV]
        return [min_series.values[-1], min_series.index.values[-1]]
    elif (_type == "First"):
        maxV = max(_series.values)
        max_series = _series[_series.values == maxV]
        return [max_series.values[0], max_series.index.values[0]]


def kmeans_building(x1, x2, types_num, types, colors, shapes, _isPlot=False):
    X = np.array(list(zip(x1, x2))).reshape(len(x1), 2)
    # KMeans(algorithm='auto', copy_x=True, init='k-means++', max_iter=300,n_clusters=3, n_init=10, n_jobs=None, precompute_distances='auto',random_state=None, tol=0.0001, verbose=0)
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
        if (_isPlot == True):
            plt.scatter(x1[i], x2[i], c=colors[l], marker=shapes[l])
    if (_isPlot == True):
        for i in range(len(list(kmeans_model.cluster_centers_))):  # 画聚类中心点
            plt.scatter(list(list(kmeans_model.cluster_centers_)[i])[0],
                        list(list(kmeans_model.cluster_centers_)[i])[1],
                        c=colors[i], marker=shapes[i], label=types[i])
        plt.legend()
        plt.show()
    return kmeans_model, x1_result, x2_result


if __name__ == "__main__":
    import utils.excel2redis as rds
    from pandas import DataFrame
    import chart.plot as cPlt

    batchStr = "t1zc0000*"
    # 获取批次数据
    df = rds.getBatchData(batchStr, 0)
    useCol = [1, 2, 3, 4, 5, 6, 7, 8, 9]  # , 10, 11, 12]
    # df = DataFrame(df.values[:, useCol])
    df = df[useCol]
    df = df[:]  # int(len(df) / 4)]
    # df = df[35:49]
    # cPlt.singlePlot(df, _title=batchStr)
    check_batch_point(df)
