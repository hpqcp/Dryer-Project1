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

# 批次
batchStr = "t1zc0000*"
# 获取批次数据
df = rds.getBatchData(batchStr, 0)
df = DataFrame(df.values[:, [1,2,3,4,5,6,7,8,9]])

cPlt.singlePlot(df, _title=batchStr)