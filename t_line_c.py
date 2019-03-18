import utils.excel2redis as rds
import base.timeseries_process as ts
import chart.plot as cPlt
import base.data_preProcess as bsPre
import  base.data_transform as bsTrans

import pandas as pd
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans



# 批次
batchStr = "t1zc0009*"
# 获取批次数据
df = rds.getBatchData(batchStr, 0)
# #获取时间列
# _series = pd.Series(df[0].values, index = df.index.values)
# 获取数据是否连续
# indexList=ts.check_ts_continuity(_series)
# 定义使用的列
useCol = [1, 5, 6, 7, 8, 9]  # , 10, 11, 12]
df = DataFrame(df.values[:, useCol])
# diffCol = [0,1,2,3,4,5]
# 目标列Y
yCol = 6
# 时间频率
freq = 6
df = df[:]#int(len(df) / 4)]
# df = df[35:49]
putTimes = [0,90,136,361,390,420]
df = bsTrans.data_alignment(df,putTimes)
cPlt.singlePlot(df, _title=batchStr)
exit()