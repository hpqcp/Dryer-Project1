import utils.excel2redis as rds
import base.timeseries_process as ts
import chart.plot as cPlt
import base.data_preProcess as bsPre
import base.data_transform as bsTrans

import pandas as pd
import numpy as np
from pandas import DataFrame
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

import matplotlib.pyplot as pyplot
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics

# 定义使用的列
useCol = [1, 5, 6, 7, 8,9]  # , 10, 11, 12]
# df = DataFrame(df.values[:, useCol])
diffCol = [0, 1, 2, 3, 4,5]
# 目标列Y
yCol = 5
# 时间频率
freq = 6
# 延时
putTimes = [0, 90, 136, 361, 378, 420]



def MergeBatch(_batchList,_db):
    dfAll = DataFrame()
    for _li in _batchList:
        batchStr = _li
        # 获取批次数据
        df = rds.getBatchData(batchStr, _db)
        # #获取时间列
        # _series = pd.Series(df[0].values, index = df.index.values)
        # 获取数据是否连续
        # indexList=ts.check_ts_continuity(_series)
        df = DataFrame(df.values[:, useCol])
        df = bsTrans.data_alignment(df, putTimes)
        df = df[:]
        dfAll = dfAll.append(df)
        # print(dfAll.shape[0])
    dfAll = dfAll.reset_index(drop=True)
    return dfAll


batchList = ["t1zc0000*", "t1zc0001*", "t1zc0002*", "t1zc0003*", "t1zc0004*","t1zc0005*" ,"t1zc0006*","t1zc0007*","t1zc0008*","t1zc0009*"]
allDf = MergeBatch(batchList,0)


rf = RandomForestRegressor()

df = allDf
batchStr = ""
# # 批次
# batchStr = "t1zc0000*"
# # 获取批次数据
# df = rds.getBatchData(batchStr, 0)
#
# # #获取时间列
# # _series = pd.Series(df[0].values, index = df.index.values)
# # 获取数据是否连续
# # indexList=ts.check_ts_continuity(_series)

# # df = df[35:49]
# putTimes = [0, 90, 136, 361, 390, 420]
# df = bsTrans.data_alignment(df, putTimes)

cPlt.singlePlot(df, _title=batchStr)
df = df[:]  # int(len(df) / 4)]
# 原始
# xa, xb, ya, yb = bsTrans.dataPartition(df.iloc[:, diffCol], yCol)
xa = df.iloc[:, [0,1,2,3,4]]
ya = df.iloc[:,5]
df1 = rds.getBatchData("t1zc0000*", 0)
df1 = DataFrame(df1.values[:, useCol])
df1 = bsTrans.data_alignment(df1, putTimes)
df1 = df1[:]
xb = df1.iloc[:, [0,1,2,3,4]]
yb = df1.iloc[:,5]


rf.fit(xa, ya)
p = rf.predict(xb)
print("MSE:", metrics.mean_squared_error(yb, p))

# #移动平均
dfRoll = bsTrans.dataFrameRoll(df, freq, diffCol)
# xa1, xb1, ya1, yb1 = bsTrans.dataPartition(dfRoll, yCol)
xa1 = dfRoll.iloc[:, [0,1,2,3,4]]
ya1 = dfRoll.iloc[:,5]
dfRoll_pre = bsTrans.dataFrameRoll(df1, freq, diffCol)
xb1 = dfRoll_pre.iloc[:, [0,1,2,3,4]]
yb1 = dfRoll_pre.iloc[:,5]
rf.fit(xa1, ya1)
p1 = rf.predict(xb1)
print("MSE-roll:", metrics.mean_squared_error(yb1, p1))

# 分段平均
dfSplite = DataFrame(bsTrans.splitMean(df.values[:, diffCol], freq))
xa2, xb2, ya2, yb2 = bsTrans.dataPartition(dfSplite, yCol)
rf.fit(xa2, ya2)
p2 = rf.predict(xb2)
print("MSE-split:", metrics.mean_squared_error(yb2, p2))

d = DataFrame({"T": yb, "P": p})
d1 = DataFrame({"T1": yb1, "P1": p1})
d2 = DataFrame({"T2": yb2, "P2": p2})
c = [d, d1, d2]
cName = ["Origin", "rollMean", "splitMean"]
cPlt.pairPlot(c, cName, [12, 16])
cPlt.pairPlot(c, cName)



# per20 = np.percentile(bsTrans.diff(df.values[:,[3]]),20)
# per80 = np.percentile(bsTrans.diff(df.values[:,[3]]),80)
# per50 = np.median(bsTrans.diff(df.values[:,[3]]))
# print(bsTrans.trend(dfSplite.values[:,[3]]))


# diff1 = DataFrame(bsTrans.diff(df.values[:,[1,3,5,7,9,11,13,15]]))
# pyplot.plot(diff1.values[:,7])
#
# pyplot.show()
