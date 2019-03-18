import numpy as np
import pandas as pd
from pandas import DataFrame

'''
分段平均函数
'''
def splitMean(_series,_n):
    return [sum(_series[i:i + _n])/_n for i in range(0, len(_series), _n)][:-1]


'''dataframe移动(平均、中位数、最大、最小)
'''
def dataFrameRoll(_df,_freq,_colNum=[]):
    colSize = _df.shape[1]
    rowSize = _df.shape[0]
    if len(_colNum) <= 0 :
        _colNum = range(0,colSize - 1,1)
    dfRtn = DataFrame()
    for i in _colNum:
        x1 = pd.Series(_df.values[:, i]).rolling(_freq).mean()
        dfRtn[_df.columns[i]]  = x1
    return dfRtn[_freq:]


'''自动划分训练集、测试集
'''
def dataPartition(_df,_predictColNum,_partNum = 0.8,_mode="seq"):
    if _partNum > 1 or _partNum<=0 :
        return -1,-1,-1,-1
    rowSize = _df.shape[0]
    colSize = _df.shape[1]
    if rowSize <=1 :
        return -2,-2,-2,-2
    fisrtNum = int(rowSize * _partNum)
    valuesTest = _df.values[:,_predictColNum]
    valuesLearn = _df.values[:,[j for j in range(0,colSize-1,1) if j != _predictColNum]]
    return valuesLearn[:fisrtNum] , valuesLearn[fisrtNum :] ,valuesTest[:fisrtNum], valuesTest[fisrtNum :]

'''生成数差（即后一个值减前一个值）
'''
def diff(_series):
    return [_series[i+1] - _series[i]  for i in range(1, len(_series)-1, 1)][:]

'''生成数差（即后一个值减前一个值）
'''
def trend(_series):
     return [2 if _series[i]<0 else 1  for i in range(0, len(_series)-1, 1)][:]

'''数据对齐
'''
def  data_alignment(_df,_putTimes):
    dfLen = _df.shape[1]
    putLen = len(_putTimes)
    maxPut = max(_putTimes)

    rtnDF = DataFrame()
    for i in range(0,dfLen,1):
        dt = _df.values[_putTimes[i]:_putTimes[i] - maxPut,i]
        rtnDF = rtnDF.append(pd.Series(dt),ignore_index=True)

    return rtnDF