

import pandas as pd
from pandas import DataFrame


class excel_oprator():
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