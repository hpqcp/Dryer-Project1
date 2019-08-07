import numpy as np
import pandas as pd
import os
import datetime
import gb.productionAlgorithm as pAlgorithm
import gb.preProcess as pre


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
    for j in range(0, setData.shape[0], 1):
        setNo = setData['set'].values[j]
        print(
            'Begin process : ' + str(datetime.datetime.now()) + '    Set : ' + setNo + '    Date : ' + productDate)
        write = pd.ExcelWriter(_dir + productDate + "//" + setNo + ".xlsx", engine='xlsxwriter')
        write = pAlgorithm.dayProduction2Excel(jbData, setNo, write, sTime, eTime,_dir)
        print('     Complete : ' + str(datetime.datetime.now()))
        write.save()
        write.close()


#
def excel2Plot(_dir,_excelName,_sheetName,_startTime,_endTime,_strSet,_isSave=False):

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

#
def zsExcel2Plot(_tagName,_startTime,_endTime,_strSet,_isSave=False,_imgPath=''):

    import  matplotlib.pylab as pyplot
    import scipy.signal as sci
    from matplotlib.font_manager import FontProperties

    sTime = _startTime
    eTime = _endTime
    clTag = _tagName
    hisData = pre.loadHisDataByCyclic([clTag], '600000', sTime, eTime,_type='Value')

    vector = hisData.values[:, 1].astype(np.float)
    indexes, values = sci.find_peaks(vector, height=7, distance=2.1)
    pyplot.plot(range(0, len(vector), 1), vector, 'r-')
    y = hisData.values[indexes, 1].astype('float')
    pyplot.scatter(indexes, y)
    font_set = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=10)
    title = _strSet + ' ' + sTime + ' - '+eTime+' 频率:24H' +'\n'+ clTag
    pyplot.title(title,fontproperties=font_set)
    if _isSave :
        imgPath = _imgPath + _strSet +'.png'
        pyplot.savefig(imgPath)
    # pyplot.show()
    pyplot.close()


def multivValue2Excel(_taglist,_tagNames,_startTime,_endTime,_path):
    sTime = _startTime
    eTime = _endTime
    hisData = pre.loadHisDataByCyclic(_taglist, '86400000', sTime, eTime, _type='vValue')
    hisData.columes = _tagNames

    write = pd.ExcelWriter(_path, engine='xlsxwriter')
    hisData.to_excel(write)

if __name__ == "__main__":
    dir = "d://jb//zs//"
    excelStr = 'kyzs.xlsx'
    sheetName = 'Sheet1'
    sTime = '2019-8-1 06:00:00'
    eTime = '2019-8-3 06:00:00'

    # excelName = dir + excelStr
    # jbData = pd.read_excel(excelName, sheet_name=sheetName, header=0)
    # setData = jbData.drop_duplicates(['set'])
    # setData1 = setData.dropna(axis=0, how='any')
    # setData2 = setData1.reset_index(drop=True)
    # for i in range(0,setData2.shape[0],1) :
    #     strSet = setData['set'].values[i]
    #     excel2Plot(dir, excelStr, sheetName, sTime, eTime,strSet,_isSave=True)

    # DayProductionByExcelFactory(dir,excelStr,sheetName,sTime,eTime)

    # excelName = dir + excelStr
    # jbData = pd.read_excel(excelName, sheet_name=sheetName, header=0)
    # jbData1 = jbData.set_index('单元').stack().reset_index()
    #
    # for i in range(0,jbData1.shape[0],1) :
    #     strSet = jbData1.values[i,0] +'-'+jbData1.values[i,1]
    #     tagStr =  jbData1.values[i,2]
    #     zsExcel2Plot(tagStr, sTime, eTime,strSet,_isSave=True,_imgPath=dir)

    excelName = dir + excelStr
    jbData = pd.read_excel(excelName, sheet_name='Sheet2', header=0)
    jbData1 = jbData.set_index('单元').stack().reset_index()
    tags = list(jbData1.values[:,2])
    names = list(jbData1.values[:,0]+'-'+jbData1.values[:,1])
    multivValue2Excel([tags[0]],names,sTime, eTime,dir+'vValue.xlsx')
    print('1')