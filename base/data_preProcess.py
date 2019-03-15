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