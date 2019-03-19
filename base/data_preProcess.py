import numpy as np
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
from functools import reduce


'''
读取EXCEL
_path,路径，_sheetNum第几个Sheet , _colName选择列
Return : DataFrame
'''
def readExcel(_path,_sheetNum,_colNum=[]):
    if len(_colNum) <= 0 :
        dfData = pd.read_excel(_path, sheet_name=_sheetNum)
    else:
        dfData = pd.read_excel(_path,sheet_name=_sheetNum ,usecols=_colNum)
    return dfData

'''
计算统计指标
_path,路径，_sheetNum第几个Sheet , _colName选择列
Return : DataFrame
'''
def computeIndex(_df):
    count = _df.count()
    max = _df.max()
    min = _df.min()
    mean = _df.mean()
    std = _df.std()
    dfRtn = DataFrame({'Count':count,'Max':max,'Min':min,'Mean':mean,'Std':std})
    return dfRtn

'''判断是否有空值，True 有空值 ， False 无空值
'''
def isContainMissValue(_df):
    for i in _df.isnull().any():
        if i :
            return True
    return False

'''
空值处理
'''
def FillMissValue(_df):
    return 0

'''
'''
def compute_ChangePoint(_series,_mode="first"):
    minList = computeIndex(_series).values[:,2]
    if _mode == "first" :
        minIndexList =  [_series[_series[i] == minList[i]].index.values[0] for i in range(0, _series.shape[1], 1)][:]
    else:
        minIndexList = [_series[_series[i] == minList[i]].index.values[-1] for i in range(0, _series.shape[1], 1)][:]
    # minIndexList = _series[_series[0] == minList[0]].index.values[-1]
    return  minIndexList
    # return  _series
    # return [_series[_series[i]>minList[2]][i]  for i in range(1, len(_series) - 1, 1)][:]
    # print(minList[0])
    # return _series[_series[0]>minList[0] and _series[0].index ][0]

'''
'''
def wave_peakTrough(_series):
    minList = computeIndex(_series).values[:, 2]
    min1 = [_series[_series[i] == minList[i]].index.values[1] for i in range(0, _series.shape[1], 1)][:]
    min2 = [_series[_series[i] == minList[i]].index.values[-1] for i in range(0, _series.shape[1], 1)][:]
    #从最小点往前


    max1 = [_series[_series[i] ==max(_series[i])].index.values[-1] for i in range(0, _series.shape[1], 1)][:]
    max2 = [_series[_series[i] == max(_series[i])].index.values[0] for i in range(0, _series.shape[1], 1)][:]


    # _series[_series[i] == ]
    # print(max0,max1)
    return minIndex



