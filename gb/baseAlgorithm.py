import gb.preProcess as pre
import numpy as np
import pandas as pd
import scipy.signal as sci
import datetime
import matplotlib.pyplot as pyplot


#获取班次开始结束时间
#_shiftTag 班次点,_beginShiftTag 班次开始点,_endShiftTag 班次结束点
def shiftTime(_tags,_hisData):
    # tags = [_shiftTag,_beginShiftTag,_endShiftTag]
    # freq = "3600000"   #1小时
    # hisData = pre.loadHisDataByCyclic(tags, freq, _beginTime, _endTime)
    hisData = _hisData
    hisData1=hisData.drop_duplicates(_tags) #去重
    #列重命名
    hisData1.rename(columns={_tags[0] : 'Shift', _tags[1]: 'ShiftBegin', _tags[2]: 'ShiftEnd'}, inplace=True)
    order = ['DateTime', "Shift","ShiftBegin","ShiftEnd"]
    hisData2 = hisData1[order]#调整顺序
    return hisData2

#牌号班次分段
def shiftPhSec(_hisData,_tags):
    hisData = _hisData
    hisData1 = hisData.drop_duplicates(_tags)  # 去重
    # 列重命名
    hisData1.rename(columns={_tags[0]: 'Shift', _tags[1]: 'PH'}, inplace=True)
    order = ['DateTime', "Shift", "PH"]
    hisData2 = hisData1[order]  # 调整顺序
    return hisData2

#利用机器速度计算停机区间
#_type : run , halt
def runHaltIntervalBySpeed(_hisData,_type='run'):
    #tags = [_speedTag]
    #freq = "60000"  # 1分钟
    #hisData = pre.loadHisDataByCyclic(tags, freq, _beginTime, _endTime)
    hisData = _hisData
    tagName = hisData.columns[1]
    hisData.rename(columns={tagName: 'Speed'}, inplace=True)
    if (_type=='run'):   his1 = hisData[hisData.iloc[:,1].astype(float) > 0]  # 开机
    else:  his1 = hisData[hisData.iloc[:,1].astype(float) <= 0]  # 停机
    if (his1.empty): return None
    lsSec1 = continuousSegmentByIndex(his1.index)    #开机时段
    return  lsSec1

#通过索引获取连续段
def continuousSegmentByIndex(_index):
    index1 = _index
    ls1 =list()
    g1 = index1[0]
    for i in range(0,len(index1) - 1,1):
        g2 = index1[i]
        if (g2 + 1 == index1[i+1]):
            continue
        else:
            g3 = index1[i]
            ls1.append([g1,g3,g3-g1+1])
            g1 = index1[i+1]
    ls1.append([g1,index1[-1],index1[-1] - g1 + 1])
    df = pd.DataFrame(ls1)
    df.rename(columns={0: 'BeginIndex', 1: 'EndIndex', 2: 'Count'}, inplace=True)
    return  df

####
def findPeaksBySci(_hisData):
    vector = _hisData.values[:, 1].astype(np.float)
    indexes, values = sci.find_peaks(vector, height=7, distance=2.1)
    # #
    # print('Peaks are: %s' % (indexes))
    # pyplot.figure(1)
    # pyplot.plot(range(0, len(vector), 1), vector, 'r-')
    # y = _hisData.values[indexes, 1].astype('float')
    # pyplot.scatter(indexes, y)
    # pyplot.title = _title
    # pyplot.show()
    # #
    return indexes

#找出每个班次的开始结束区间
#_lsShift : 传入班次List
def shiftSection(_hisData):
    lsShift = _hisData.values[:,1]
    ls1 = lsShift
    r1  = lsShift[0]
    loc=0
    ls2=list()
    for i in range(0,len(ls1) - 1,1):
        if (r1 == ls1[i+1]):
            continue
        else:
            ls2.append([r1,loc,i])
            r1 = ls1[i+1]
            loc = i+1
    ls2.append([r1,loc,len(ls1) - 1])
    df = pd.DataFrame(ls2)
    df.rename(columns={0: 'Shfit', 1: 'ShiftBegin', 2: 'ShiftEnd'}, inplace=True)
    df['BeginTime'] = _hisData.values[df.values[:,1].astype(np.int),0]
    df['EndTime'] = _hisData.values[df.values[:, 2].astype(np.int), 0]
    return df




#计算生产时段
#_threshold 临界值
def wavePorcess_productionSection(_hisData,_threshold):
    hisData1= _hisData
    tagName = hisData1.columns[1]
    hisData1.rename(columns={tagName: 'Speed'}, inplace=True)
    values1 = hisData1.loc[hisData1['Speed'].astype(np.float) <= _threshold]  #获取小于临界的值
    if values1.empty  :     df2 = None
    else :  df2 = continuousSegmentByIndex(values1.index)
    values3 = hisData1.loc[hisData1['Speed'].astype(np.float) > _threshold]   #获取大于临界的值
    if values3.empty :      df3 = None
    else :  df3 =  continuousSegmentByIndex(values3.index)
    df1 = df2.append(df3)  #合并
    df1.sort_values(by = ['BeginIndex'],ascending = True,inplace=True)  #正排序
    df1.reset_index(drop=True,inplace=True)
    #
    hisData2 = hisData1.sort_index(axis=0, ascending=False).reset_index(drop=True)
    #计算指标
    df1['StartTime'] = hisData1.iloc[df1.iloc[:,0].astype(np.int),0].reset_index(drop=True)
    df1['EndTime'] = hisData1.iloc[df1.iloc[:, 1].astype(np.int), 0].reset_index(drop=True)
    minValue = [hisData1.iloc[df1.iloc[i, 0].astype(np.int) : df1.iloc[i, 1].astype(np.int)+1 , 1].astype(np.float).min() for i in range(0,df1.shape[0],1)]
    minIndex = [np.argmin(hisData1.iloc[df1.iloc[i, 0].astype(np.int) : df1.iloc[i, 1].astype(np.int)+1 , 1].astype(np.float)) for i in range(0,df1.shape[0],1)]
    maxValue = [hisData1.iloc[df1.iloc[i, 0].astype(np.int): df1.iloc[i, 1].astype(np.int)+1, 1].astype(np.float).max()  for i in range(0, df1.shape[0], 1)]
    maxIndex = [np.argmax(hisData1.iloc[df1.iloc[i, 0].astype(np.int): df1.iloc[i, 1].astype(np.int)+1, 1].astype(np.float)) for i in range(0, df1.shape[0], 1)]
    his2Len = hisData2.shape[0]
    maxIndex2 = list(reversed([his2Len - 1 - np.argmax(hisData2.iloc[his2Len - df1.iloc[i, 1].astype(np.int) - 1: his2Len - df1.iloc[i, 0].astype(np.int), 1].astype(np.float)) for i in range( -1,-df1.shape[0] - 1, -1)]))
    minIndex2 = list(reversed([his2Len - 1 - np.argmin(
        hisData2.iloc[his2Len - df1.iloc[i, 1].astype(np.int) - 1: his2Len - df1.iloc[i, 0].astype(np.int), 1].astype(
            np.float)) for i in range(-1, -df1.shape[0] - 1, -1)]))

    df1['MinValue'] = minValue
    df1['MinLoc1'] = minIndex
    df1['MinLoc2'] = minIndex2
    df1['MinTime1'] = hisData1.values[minIndex, 0]
    df1['MinTime2'] = hisData1.values[minIndex2, 0]
    df1['MaxValue'] = maxValue
    df1['MaxLoc1'] = maxIndex
    df1['MaxLoc2'] = maxIndex2
    df1['MaxTime1'] = hisData1.values[maxIndex, 0]
    df1['MaxTime2'] = hisData1.values[maxIndex2, 0]
    df1['MeanSpeed'] = df1.apply(lambda x: x['MaxValue'] / x['Count'], axis=1)
    df1['Type'] = df1.apply(lambda x: x['MaxValue'] <= _threshold, axis=1)   #类型，True:小于临界  ； False:大于临界

    return df1

#计算产量等指标
def wavePorcess_productionCompute(_productionSection):
    data1 = _productionSection
    isLast = False
    if(data1['Type'].values[0]==False):
        data1.drop(index=[0],inplace=True)
        data1.reset_index(drop=True,inplace=True)
    len = data1.shape[0]

    if (len % 2) == 0:
        range1 = range(0, len, 2)
        range2 = range(1,len+1,2)
    else:
        range1 = range(0, len - 1, 2)
        range2 = range(1, len - 1 , 2)
        isLast = True
    df1 = pd.DataFrame()

    df1['StartIndex'] = data1['MinLoc2'].values[range1].astype(np.int)
    df1['EndIndex'] = data1['MaxLoc1'].values[range2].astype(np.int)
    # if isLast :
    #     df1['StartIndex'].append(data1['MinLoc2'].values[range1].astype(np.int))
    #     df1['EndIndex'].append(data1['MaxLoc1'].values[range1].astype(np.int))

    df1['Count'] = df1.apply(lambda x: x['EndIndex'] - x['StartIndex'], axis=1)
    df1['StartTime'] = data1['MinTime2'].values[range1].astype(np.datetime64)
    df1['EndTime'] = data1['MaxTime1'].values[range2].astype(np.datetime64)
    df1['Interval'] = df1.apply(lambda x: (x['EndTime'] - x['StartTime']).total_seconds()/60 , axis=1)
    df1['Product'] = data1['MaxValue'].values[range2]
    df1['MeanSpeed'] = df1.apply(lambda x: x['Product'] / x['Count'], axis=1)
    return  df1

#填充断点
#_threshold : 临界值 ，默认值0
def wavePorcess_fillBreakPoint(_hisData,_threshold = 0):
    hisData1 = _hisData
    tagName = hisData1.columns[1]
    hisData1.rename(columns={tagName: 'Product'}, inplace=True)
    values1 = hisData1.loc[hisData1['Product'].astype(np.float) <= _threshold]  # 获取0的值
    if values1.empty :  return hisData1
    df1 = continuousSegmentByIndex(values1.index)
    if df1.shape[0] <= 0: return hisData1
    for i in range(0,df1.shape[0],1):
        loc1 = df1['BeginIndex'].values[i].astype(np.int)
        loc2 = df1['EndIndex'].values[i].astype(np.int)
        if  loc1 == 0 :    continue
        if  loc2 >=  hisData1.shape[0] - 1 :     continue
        product1 = float(hisData1['Product'].values[loc1 - 1])
        product2 = float(hisData1['Product'].values[loc2 + 1])
        v0 = (product2 - product1) / 2
        fill0 = [(product1 + (i + 1) * v0) for i in range(0, loc2 - loc1+1, 1)]
        v = (product2 - product1) / (loc2 - loc1 + 1)
        fill1 = [(product1 + (i+1) * v)  for i in range(0,loc2 - loc1 + 1 , 1)]
        if  product1 <= product2 :
            if loc2 - loc1 == 0 :
                hisData1['Product'].ix[loc1] = fill0[0]
            else :
                hisData1['Product'].ix[loc1:loc2] = fill1
    return hisData1

#
def wavePorcess_shiftPH(_shiftPhHisData,_productionSec):
    hisData1 = _shiftPhHisData
    productionSec1 = _productionSec
    # 列重命名
    hisData1.rename(columns={hisData1.columns[1]: 'Shift', hisData1.columns[2]: 'PH'}, inplace=True)
    order = ['DateTime', "Shift", "PH"]
    hisData2 = hisData1[order]  # 调整顺序
    nPH = list()
    nPHPer = list()
    nShift = list()
    nShiftPer = list()
    for i in range(0,_productionSec.shape[0],1):
        b1 = _productionSec['StartIndex'].values[i].astype(np.int)
        e1 = _productionSec['EndIndex'].values[i].astype(np.int)
        r = hisData2.iloc[b1:e1,:]
        shiftGroup = r.groupby('Shift', as_index=False)['DateTime'].count()
        shiftGroup.sort_values(by = ["DateTime"],ascending = False,inplace = True)
        maxShift = shiftGroup["DateTime"].values[0].astype(np.int)
        perShift = maxShift / (e1 - b1)
        phGroup = r.groupby('PH', as_index=False)['DateTime'].count()
        phGroup.sort_values(by=["DateTime"], ascending=False, inplace=True)
        maxPH = phGroup["DateTime"].values[0].astype(np.int)
        perPH = maxPH / (e1 - b1)
        nPH.append(phGroup["PH"].values[0])
        nPHPer.append(perPH)
        nShift.append(shiftGroup["Shift"].values[0])
        nShiftPer.append(perShift)
    productionSec1["PH"] = nPH
    productionSec1["PhPer"] = nPHPer
    productionSec1["Shift"] = nShift
    productionSec1["ShiftPer"] = nShiftPer
    return productionSec1

#增加汇总行
def appenTotalRow(_df):
    df1 = _df
    sumCount = df1['Count'].values.sum()
    sumInterval = df1['Interval'].values.sum()
    sumProduct = df1['Product'].values.sum()
    sumMeanSpeed = sumProduct / sumInterval
    newRow = pd.DataFrame({'StartIndex':np.nan,'EndIndex':np.nan,
                        'Count':sumCount ,
                        'StartTime':np.datetime64('NaT'),'EndTime':np.datetime64('NaT'),
                        'Interval': sumInterval,
                        'Product': sumProduct,'MeanSpeed':sumMeanSpeed,'PH':np.nan,
                        'PhPer': np.nan,  'Shift': np.nan, 'ShiftPer': np.nan},index=[0])


    df1 = df1.append(newRow,ignore_index=True)
    return df1



if __name__ == "__main__":
    # freq = "60000"  # 1分钟
    # str1 ="MES2RTDATA.U_Maker_11020030001.DC_BC"
    # str2 ="MES2RTDATA.U_Maker_11020030001.DC_DQBCKSSJ"
    # str3 ="MES2RTDATA.U_Maker_11020030001.DC_DQBCJSSJ"
    # #str4 ="MES2RTDATA.U_Maker_11020030001.DC_PH"
    # tags = [str1,str2,str3]
    # hisData = pre.loadHisDataByCyclic(tags, freq, "2019-07-02 06:00:00","2019-07-03 06:00:00")
    # a = shiftTime(tags,hisData)
    # print(a)

    # freq = "60000"  # 1分钟
    # tags = ["MES2RTDATA.U_Maker_11020030001.DC_BC","MES2RTDATA.U_Maker_11020030001.DC_PH"]
    # hisData = pre.loadHisDataByCyclic(tags, freq, "2019-07-01 06:00:00","2019-07-02 06:00:00")
    # a = shiftPhSec(hisData,tags)
    # print(a)


    # freq = "60000"  # 1分钟
    # hisData = pre.loadHisDataByCyclic(["MES2RTDATA.U_Maker_11020030001.DC_YXSD"], freq, "2019-07-01 06:00:00","2019-07-02 06:00:00")
    # a = runHaltIntervalBySpeed(hisData,_type='run')
    # import datetime
    # d = hisData.values[:,0].shape[0]
    # pyplot.hist(hisData.values[:,1].astype(np.float),d)
    # pyplot.show()
    # print(a)

    # freq = "60000"  # 1min
    # for i in range(1,10,1):
    #     tags = ['MES2RTDATA.U_Packer_1102003000'+str(i)+'.DC_TBSJCL']
    #     hisData = pre.loadHisDataByCyclic(tags, freq, '2019-07-4 6:00:00','2019-07-5 6:00:00')
    #     findPeaksBySci(hisData)

    # freq = "60000"  # 1min
    # str1 = "MES2RTDATA.U_Maker_11020030011.DC_PH"
    # tags=[str1]
    # hisData = pre.loadHisDataByCyclic(tags, freq, '2019-06-15 06:00:00', '2019-06-16 6:00:00')
    # a = shiftSection(hisData)
    # b= list(a.values[:,[1,2]].astype(np.int))
    # print (hisData.values[b,0])
    # print(a)
    #
    # from sklearn.preprocessing import Imputer



    # freq = "60000"  # 1min
    # for i in range(16,17,1):
    #     tags = ['MES2RTDATA.U_Packer_110200300'+str(i)+'.DC_SJCL']
    #     hisData1 = pre.loadHisDataByFull(tags, freq, '2019-06-24 6:00:00','2019-06-25 6:00:00')
    #     hisData1.rename(columns={tags[0] : 'cl'}, inplace=True)
    #     hisData1.loc[hisData1['cl'].astype(np.int) <= 10000,'cl'] = np.nan
    #     imr = Imputer(missing_values='NaN', strategy='mean', axis=0)  # 均值填充缺失值
    #     imr = imr.fit(hisData1.drop('DateTime', 1))
    #     imputed_data = imr.transform(hisData1.drop('DateTime',1).values)
    #     pyplot.plot(range(0, len(imputed_data), 1), imputed_data, 'r-')
    #     pyplot.show()
    #     b = findPeaksBySci(hisData1)
    #     print(hisData1.values[b,0])

    # freq = "6000"  # 1min
    # # tags = ['MES2RTDATA.U_Packer_11020030001.DC_SJCL']DC_TBSJCL
    # tags = ['MES2RTDATA.U_Maker_11020030002.DC_SJCL']
    # hisData1 = pre.loadHisDataByCyclic(tags, freq, '2019-07-1 6:00:00', '2019-07-2 6:00:00')
    # # hisData1.rename(columns={tags[0]: 'cl'}, inplace=True)
    # # b = findPeaksBySci(hisData1)
    # d = findPeaksBySci(hisData1)
    # a = wavePorcess_productionSection(hisData1,20000)
    # b = wavePorcess_productionCompute(a)
    # writer = pd.ExcelWriter('c://aa.xls')
    # b.to_excel(writer,sheet_name='Sheet1')

    # tags = ['MES2RTDATA.U_Packer_11020030002.DC_SJCL']
    # hisData1 = pre.loadHisDataByCyclic(tags, freq, '2019-07-1 6:00:00', '2019-07-2 6:00:00')
    # a1 = wavePorcess_productionSection(hisData1, 1000)
    # b1 = wavePorcess_productionCompute(a1)
    # # b1.to_excel(writer, sheet_name='Sheet2',)
    # d = findPeaksBySci(hisData1)
    #
    # tags = ['MES2RTDATA.U_Packer_11020030002.DC_TBSJCL']
    # hisData1 = pre.loadHisDataByCyclic(tags, freq, '2019-07-1 6:00:00', '2019-07-2 6:00:00')
    # a2 = wavePorcess_productionSection(hisData1, 100)
    # b2 = wavePorcess_productionCompute(a2)
    # b2.to_excel(writer, sheet_name='Sheet3')
    # d = findPeaksBySci(hisData1)
    #
    # writer.save()

    # freq = "6000"
    # # tags = ['MES2RTDATA.U_Maker_11020030002.DC_SJCL']
    # for i in range(9,10,1):
    #     tags= ['MES2RTDATA.U_Maker_1102003000'+str(i)+'.DC_SJCL']
    #     hisData1 = pre.loadHisDataByCyclic(tags, freq, '2019-07-1 6:00:00', '2019-07-2 6:00:00')
    #     f = findPeaksBySci(hisData1,str(i))
    #     hisData2 = wavePorcess_fillBreakPoint(hisData1,500)
    #     f1 = findPeaksBySci(hisData2,str(i)+"A")
    #     a1 = wavePorcess_productionSection(hisData2, 5000)
    #     b1 = wavePorcess_productionCompute(a1)
    # #
    #     tags = ['MES2RTDATA.U_Maker_1102003000'+str(i)+'.DC_BC', 'MES2RTDATA.U_Maker_1102003000'+str(i)+'.DC_PH']
    #     # tags = ['HHMES.U_Maker_12020030001.SC_DBGZBC','HHMES.U_Maker_12020030001.SC_DQPHDM']
    #     hisData3 = pre.loadHisDataByCyclic(tags, freq, '2019-07-2 6:00:00', '2019-07-3 6:00:00')
    #     c1 = wavePorcess_shiftPH(hisData3, b1)
    #     print('a')
    # # d = findPeaksBySci(hisData2)
    # #
    # # print("")

    freq = "3600000"
    tags = ['MES2RTDATA.U_BAL_11010060001.DC_TeamCode','MES2RTDATA.U_BAL_11010060001.DC_OrderNo','MES2RTDATA.U_CON_11010060002.DC_PCH'
            'MES2RTDATA.U_CON_11010060002.DC_PH','MES2RTDATA.U_CON_11010060002.IT_SBZT']
    hisData1 = pre.loadHisDataByCyclic(tags, freq, '2019-07-1 6:00:00', '2019-07-10 6:00:00')
    print('')