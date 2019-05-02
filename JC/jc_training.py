from pandas import DataFrame
import numpy as np
import base.data_preProcess as bsPre
import base.data_transform as bsTrans
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
from sklearn.externals import joblib
import warnings
warnings.filterwarnings("ignore")


path = "c://jc-t4.xls"
df = bsPre.readExcel(path, 1)
useCol = [6,7,8,9,10,11,12]
df = DataFrame(df.values[:,useCol])

xCols= [[0,1],[0,2],[0,3],[0,4],[0,5],[0,6], \
        [0,1,2],[0,1,3],[1,4],[0,5],[0,1,6], \
        [0,1,2,3],[1,2,4],[0,5],[0,1,2,6], \
        [0,1,2,3,4],[0,5],[0,1,2,3,6], \
        [0,5],[0,1,2,3,4,6], \
        [0,1,2,3,4,5,6]]
fileNames = ["01","02","03","04","05","06","12","13","14","15","16","23","24","25","26","34","35","36","45","46","56"]

i=0
for xCol in xCols:
    rf102 = RandomForestRegressor()
    xa, xb, ya, yb = bsTrans.dataPartition(df[xCol], df[xCol].shape[1] - 1,_partNum=1,_mode="seq")
    rf102.fit(xa, ya)
    fileName = "c://jc_model//jc_"+fileNames[i]+".m"
    joblib.dump(rf102, fileName)
    i=i+1