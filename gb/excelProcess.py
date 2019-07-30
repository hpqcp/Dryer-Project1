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
    for j in range(5, setData.shape[0], 1):
        setNo = setData['set'].values[j]
        print(
            'Begin process : ' + str(datetime.datetime.now()) + '    Set : ' + setNo + '    Date : ' + productDate)
        write = pd.ExcelWriter(_dir + productDate + "//" + setNo + ".xlsx", engine='xlsxwriter')
        write = pAlgorithm.dayProduction2Excel(jbData, setNo, write, sTime, eTime)
        print('     Complete : ' + str(datetime.datetime.now()))
        write.save()
        write.close()


#
def excel2Plot(_dir,_excelName,_sheetName,_startTime,_endTime,_strSet,_isSave=False):
    import gb.preProcess as pre
    import  matplotlib.pylab as pyplot
    import scipy.signal as sci
    from matplotlib.font_manager import FontProperties

    excelName = _dir + _excelName
    jbData = pd.read_excel(excelName, sheet_name=_sheetName, header=0)
    sTime = _startTime
    eTime = _endTime
    setData = jbData.iloc[jbData['set'].values == _strSet, :]
    setData = setData.dropna(axis=0, how='any')
    for i in range(0,setData.shape[0],1) :
        clTag = setData['cl'].values[i]
        strUnit = setData['unit'].values[i]
        hisData = pre.loadHisDataByCyclic([clTag], '86400000', sTime, eTime,_type='Value')
        hisData.replace('NULL', '0', inplace=True)
        vector = hisData.values[:, 1].astype(np.float)
        indexes, values = sci.find_peaks(vector, height=7, distance=2.1)
        pyplot.plot(range(0, len(vector), 1), vector, 'r-')
        y = hisData.values[indexes, 1].astype('float')
        pyplot.scatter(indexes, y)
        font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=10)
        title = _strSet  + ' '+ strUnit+ ' ' + sTime + ' - '+eTime+' 频率:24H' +'\n'+ clTag
        pyplot.title(title,fontproperties=font_set)
        if _isSave :
            imgPath = _dir + _strSet  + '-'+ strUnit+'.png'
            pyplot.savefig(imgPath)
        pyplot.show()

if __name__ == "__main__":
    dir = "d://jb//hz//"
    excelStr = 'hz.xlsx'
    sheetName = 'hz'
    sTime = '2019-7-2 05:00:00'
    eTime = '2019-7-3 05:00:00'

    # excelName = dir + excelStr
    # jbData = pd.read_excel(excelName, sheet_name=sheetName, header=0)
    # setData = jbData.drop_duplicates(['set'])
    # setData1 = setData.dropna(axis=0, how='any')
    # setData2 = setData1.reset_index(drop=True)
    # for i in range(0,setData2.shape[0],1) :
    #
    #     strSet = setData['set'].values[i]
    #     excel2Plot(dir, excelStr, sheetName, sTime, eTime,strSet,_isSave=True)

    DayProductionByExcelFactory(dir,excelStr,sheetName,sTime,eTime)
    print('1')