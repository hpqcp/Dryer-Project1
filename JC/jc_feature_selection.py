from pandas import DataFrame
import numpy as np
import base.data_preProcess as bsPre
import base.data_transform as bsTrans
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
from sklearn.externals import joblib
from sklearn.feature_selection import RFE

import warnings
warnings.filterwarnings("ignore")


path = "c://jc-t4.xls"
df = bsPre.readExcel(path, 1)
useCol = [6,7,8,9,10,11,12]
df = DataFrame(df.values[:,useCol])
xCol= [0,1,2,3,4,5,6]

xa, xb, ya, yb = bsTrans.dataPartition(df[xCol], df[xCol].shape[1] - 1,_partNum=1,_mode="seq")
# model = RandomForestRegressor()
# # create the RFE model and select 3 attributes
# rfe = RFE(model, 1)
# rfe = rfe.fit(xa, ya)
# # summarize the selection of the attributes
# print(rfe.support_)
# print(rfe.ranking_)

from sklearn.feature_selection import SelectFromModel
rf = RandomForestRegressor()
rfc = rf.fit(xa,ya)
model  = SelectFromModel(rfc,prefit=True)
x =model.transform(xa)
print (x.shape)