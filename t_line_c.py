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

import matplotlib.pyplot as pyplot
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics

rf = RandomForestRegressor()
# 批次
batchStr = "t1zc0009*"
# 获取批次数据
df = rds.getBatchData(batchStr, 0)
# #获取时间列
# _series = pd.Series(df[0].values, index = df.index.values)
# 获取数据是否连续
# indexList=ts.check_ts_continuity(_series)
# 定义使用的列
useCol = [1, 5, 6, 7]  # , 10, 11, 12]
df = DataFrame(df.values[:, useCol])
diffCol = [0,1,2,3]
# 目标列Y
yCol = 3
# 时间频率
freq = 24

# df = df[35:49]
putTimes = [0,90,136,361,390,420]
df = bsTrans.data_alignment(df,putTimes)
cPlt.singlePlot(df, _title=batchStr)
df = df[1000:5000]#int(len(df) / 4)]
#原始
xa,xb,ya,yb = bsTrans.dataPartition(df.iloc[:,diffCol],yCol)
rf.fit(xa,ya)
p = rf.predict(xb)
print ("MSE:",metrics.mean_squared_error(yb, p))
# #移动平均
dfRoll = bsTrans.dataFrameRoll(df,freq,diffCol)
xa1,xb1,ya1,yb1 = bsTrans.dataPartition(dfRoll,yCol)
rf.fit(xa1,ya1)
p1 = rf.predict(xb1)
print ("MSE-roll:",metrics.mean_squared_error(yb1, p1))
#分段平均
dfSplite = DataFrame(bsTrans.splitMean(df.values[:,diffCol],freq))
xa2,xb2,ya2,yb2 = bsTrans.dataPartition(dfSplite,yCol)
rf.fit(xa2,ya2)
p2 = rf.predict(xb2)
print ("MSE-split:",metrics.mean_squared_error(yb2, p2))

d = DataFrame({"T":yb,"P":p})
d1= DataFrame({"T1":yb1,"P1":p1})
d2= DataFrame({"T2":yb2,"P2":p2})
c=[d,d1,d2]
cName = ["Origin","rollMean","splitMean"]
cPlt.pairPlot(c,cName,[0,16])
cPlt.pairPlot(c,cName)

per20 = np.percentile(bsTrans.diff(df.values[:,[3]]),20)
per80 = np.percentile(bsTrans.diff(df.values[:,[3]]),80)
per50 = np.median(bsTrans.diff(df.values[:,[3]]))
print(bsTrans.trend(dfSplite.values[:,[3]]))

# diff1 = DataFrame(bsTrans.diff(df.values[:,[1,3,5,7,9,11,13,15]]))
# pyplot.plot(diff1.values[:,7])
#
# pyplot.show()