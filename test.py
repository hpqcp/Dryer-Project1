import base.data_preProcess as bsPre
import  base.data_transform as bsTrans
import  chart.plot as cp
from pandas import DataFrame
import numpy as  np
import matplotlib.pyplot as pyplot
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics

rf = RandomForestRegressor()
# # 绘制数据集
path = "D://C线10批数据（20190315）.xlsx"
for i in range(0,9,1):
    df = bsPre.readExcel(path, i)
    useCol = [1,3,5,7,9,11,13,15,17]
    #df = DataFrame(bsTrans.diff(df.values[:,useCol]))
    df = DataFrame(df.values[:,useCol])
    diffCol = [0,1,2,3,4,5,6]
    yCol = 6
    freq = 6

    #画图
    # pyplot.plot(df.values[:,[6]])
    # pyplot.show()
    # exit()
    df = df[:]

    # print(df)

    # print(bsPre.computeIndex(df))
    df = df[800:int(len(df)/2)-1500]
    cp.singlePlot(df)
    rtn=bsPre.compute_ChangePoint(df,_mode="last")
    print(rtn)
    print(rtn[6]-rtn[0],rtn[8]-rtn[6])
exit()

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
cp.pairPlot(c,cName,[0,16])
cp.pairPlot(c,cName)

per20 = np.percentile(bsTrans.diff(df.values[:,[6]]),20)
per80 = np.percentile(bsTrans.diff(df.values[:,[6]]),80)
per50 = np.median(bsTrans.diff(df.values[:,[6]]))
print(bsTrans.trend(dfSplite.values[:,[0,1]]))

# diff1 = DataFrame(bsTrans.diff(df.values[:,[1,3,5,7,9,11,13,15]]))
# pyplot.plot(diff1.values[:,7])
#
# pyplot.show()