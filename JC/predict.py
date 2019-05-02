from pandas import DataFrame
import numpy as np
import base.data_preProcess as bsPre
import base.data_transform as bsTrans
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
import warnings
warnings.filterwarnings("ignore")

def rf(df):
    rf102 = RandomForestRegressor()
    mse = list()
    r2 = list()
    for i in range(0, 100, 1):
        xa, xb, ya, yb = bsTrans.dataPartition(df, df.shape[1] - 1, _mode="random")
        rf102.fit(xa, ya)
        p = rf102.predict(xb)
        mse.append(metrics.mean_squared_error(yb, p))
        r2.append(metrics.r2_score(yb, p))
        # print("MSE-:"+str(i), metrics.mean_squared_error(yb, p),metrics.r2_score(yb, p))
    mse1 = np.median(mse)
    mse2 = np.mean(mse)
    r21 = np.median(r2)
    r22 = np.mean(r2)
    return  mse1,mse2,r21,r22



path = "c://jc-t4.xls"
df = bsPre.readExcel(path, 1)
useCol = [6,7,8,9,10,11,12]
df = DataFrame(df.values[:,useCol])



# xCols = [[0,6],[1,6],[2,6],[3,6],[4,6],[5,6],[0,1,6],[0,2,6],[0,3,6],[0,4,6],[0,5,6],[1,2,6],[1,3,6],[1,4,6],[1,5,6], \
#          [2,3,6],[2,4,6],[2,5,6],[3,4,6],[3,5,6],[4,5,6],[0,1,2,6],[0,1,3,6],[0,1,4,6],[0,1,5,6],[0,2,3,6],\
#          [0,2,4,6],[0,2,5,6],[0,3,4,6],[0,3,5,6],[0,4,5,6],[1,2,3,6],[1,2,4,6],[1,2,5,6],[1,3,4,6],[1,3,5,6],[1,4,5,6],[2,3,4,6],[2,3,5,6],[2,4,5,6], \
#          [3,4,5,6],[0,1,2,3,6],[0,1,2,4,6],[0,1,2,5,6],[0,1,3,4,6],[0,1,3,5,6],[0,1,4,5,6],[0,2,3,4,6],[0,2,3,5,6],[0,2,4,5,6],[0,3,4,5,6], \
#          [1,2,3,4,6],[1,2,3,5,6],[1,2,4,5,6],[1,3,4,5,6],[2,3,4,5,6], [0,1,2,3,4,5,6]]
xCols= [[1,2,3,4,6]]
yCol = 1

# for xCol in xCols:
#     print(rf(df[xCol]))

rf102 = RandomForestRegressor()
xa, xb, ya, yb = bsTrans.dataPartition(df, df.shape[1] - 1, _mode="random")
rf102.fit(xa, ya)
p = rf102.predict(xb)
print("MSE-R2:", metrics.mean_squared_error(yb, p),metrics.r2_score(yb, p))
d = DataFrame({"Y":yb,"P":p})
#d1 = DataFrame(r2)
# d2 = DataFrame({"T2": yb2, "P2": p2})
c = [d]
cName = ["Origin"]#, "rollMean"]#, "splitMean"]
import chart.plot as cPlt
cPlt.pairPlot(c, cName)


# print(1)