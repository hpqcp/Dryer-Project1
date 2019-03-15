from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.utils import plot_model
import numpy as np
import pandas as pd
import matplotlib.pyplot as pyplot
from pandas import DataFrame

import base.data_preProcess as bsPre
import  base.data_transform as bsTrans
import  chart.plot as cp



# # 绘制数据集
path = "D://延时对齐.xls"
df = bsPre.readExcel(path, 1)
useCol = [1,3,5,7,9,11,15]
df = DataFrame(df.values[:,useCol])
diffCol = [4,5,6]
yCol = 2
freq = 30
#原始
xa,xb,ya,yb = bsTrans.dataPartition(df.iloc[:,diffCol],yCol)

model = Sequential()

model.add(Dense(input_dim=2,output_dim=1))
model.add(Activation('relu'))
model.add(Dense(units=1))
model.add(Activation('softmax'))

model.compile(loss='mse',
              optimizer='sgd',
              metrics=['accuracy'])


model.fit(xa,ya , epochs=5, batch_size=32)
loss_and_metrics = model.evaluate(xb, yb, batch_size=32)
print(loss_and_metrics)

p = model.predict(xb)
print(yb,p)
# d = DataFrame({"T":yb,"P":p})
# # c=[d]
# cName = ["Origin"]
# # cp.multiPlot(c,cName,[-1,1])
# cp.multiPlot(c,cName)