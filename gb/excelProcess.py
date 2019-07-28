import numpy as np
import pandas as pd
import os
import datetime
import gb.productionAlgorithm as pAlgorithm


def DayProductionByExcelFactory(_dir,_excelName,_sheetName,_startTime,_endTime) :
    excelName = _dir + _excelName
    jbData = pd.read_excel(excelName, sheet_name=_sheetName, header=0)
    setData = jbData.drop_duplicates(['set'])
    setData1 = setData.dropna(axis=0, how='any')
    setData = setData1.reset_index(drop=True)
    productDate = str(datetime.datetime.strptime(_startTime,'%Y-%m-%d %H:%M:%S').date())
    sTime = _startTime
    eTime = _endTime
    if not os.path.exists(_dir+productDate):
        os.mkdir(_dir+productDate)
    for j in range(12, setData.shape[0], 1):
        setNo = setData['set'].values[j]
        print(
            'Begin process : ' + str(datetime.datetime.now()) + '    Set : ' + setNo + '    Date : ' + productDate)
        write = pd.ExcelWriter(_dir + productDate + "//" + setNo + ".xlsx", engine='xlsxwriter')
        write = pAlgorithm.dayProduction2Excel(jbData, setNo, write, sTime, eTime)
        print('     Complete : ' + str(datetime.datetime.now()))
        write.save()
        write.close()


#
def excel2Plot(_dir,_excelName,_sheetName,_startTime,_endTime,_strSet):
    import gb.preProcess as pre
    import  matplotlib.pylab as pyplot
    import scipy.signal as sci

    excelName = _dir + _excelName
    jbData = pd.read_excel(excelName, sheet_name=_sheetName, header=0)
    # setData = jbData.drop_duplicates(['set'])
    # setData1 = setData.dropna(axis=0, how='any')
    # setData = setData1.reset_index(drop=True)
    # productDate = str(datetime.datetime.strptime(_startTime, '%Y-%m-%d %H:%M:%S').date())
    sTime = _startTime
    eTime = _endTime
    setData = jbData.iloc[jbData['set'].values == _strSet, :]
    for i in range(0,setData.shape[0],1) :
        clTag = setData['cl'].values[i]
        hisData = pre.loadHisDataByCyclic([clTag], '6000', sTime, eTime)
        hisData.replace('NULL', '0', inplace=True)
        vector = hisData.values[:, 1].astype(np.float)
        indexes, values = sci.find_peaks(vector, height=7, distance=2.1)
        pyplot.plot(range(0, len(vector), 1), vector, 'r-')
        y = hisData.values[indexes, 1].astype('float')
        pyplot.scatter(indexes, y)
        pyplot.title = '_title'
        pyplot.show()

if __name__ == "__main__":
    dir = "d://jb//"
    excelStr = 'ky.xlsx'
    sheetName = 'ky'
    sTime = '2019-7-23 05:00:00'
    eTime = '2019-7-24 05:00:00'
    strSet = '13#'
    DayProductionByExcelFactory(dir,excelStr,sheetName,sTime,eTime)
    #excel2Plot(dir, excelStr, sheetName, sTime, eTime,strSet)
    print(str(date2.date()))