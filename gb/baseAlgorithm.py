import gb.preProcess as pre
import numpy as np
import pandas as pd
import scipy.signal as sci
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
    hisData1.rename(columns={_tags[0] : 'Shfit', _tags[1]: 'ShiftBegin', _tags[2]: 'ShiftEnd'}, inplace=True)
    order = ['DateTime', "Shfit","ShiftBegin","ShiftEnd"]
    hisData2 = hisData1[order]#调整顺序
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


#
def findPeaksBySci(_hisData):
    vector = _hisData.values[:, 1].astype(np.float)
    indexes, values = sci.find_peaks(vector, height=7, distance=2.1)
    #
    print('Peaks are: %s' % (indexes))
    pyplot.figure()
    pyplot.plot(range(0, len(vector), 1), vector, 'r-')
    y = _hisData.values[indexes, 1].astype('float')
    pyplot.scatter(indexes, y)
    pyplot.show()
    #
    return indexes


#找出每个班次的开始结束区间
#_lsShift : 传入班次List
def shiftSection(_lsShifts):
    ls1 = _lsShifts
    r1 = _lsShifts[0]
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
    return df





if __name__ == "__main__":
    # str1 ="MES2RTDATA.U_Maker_11020030001.DC_BC"
    # str2 ="MES2RTDATA.U_Maker_11020030001.DC_DQBCKSSJ"
    # str3 ="MES2RTDATA.U_Maker_11020030001.DC_DQBCJSSJ"
    # a = shiftTime(str1,str2,str3,"2019-07-02 00:00:00","2019-07-03 06:00:00")
    # print(a)

    freq = "60000"  # 1分钟
    hisData = pre.loadHisDataByCyclic(["MES2RTDATA.U_Maker_11020030001.DC_YXSD"], freq, "2019-07-06 06:00:00","2019-07-07 06:00:00")
    a = runHaltIntervalBySpeed(hisData,_type='run')
    print(a)

    # freq = "60000"  # 1min
    # for i in range(1,10,1):
    #     tags = ['MES2RTDATA.U_Packer_1102003000'+str(i)+'.DC_TBSJCL']
    #     hisData = pre.loadHisDataByCyclic(tags, freq, '2019-07-4 6:00:00','2019-07-5 6:00:00')
    #     findPeaksBySci(hisData)

    # freq = "60000"  # 1min
    # #str1 = "MES2RTDATA.U_Maker_11020030001.DC_BC"
    # tags=[str1]
    # hisData = pre.loadHisDataByCyclic(tags, freq, '2019-07-2 00:00:00', '2019-07-3 6:00:00')
    # a = shiftSection(hisData.values[:,1])
    # b= list(a.values[:,[1,2]].astype(np.int))
    # print (hisData.values[b,0])
    # print(a)
    #
    # tags = ['MES2RTDATA.U_Packer_11020030001.DC_SJCL']
    # hisData1 = pre.loadHisDataByCyclic(tags, freq, '2019-07-4 6:00:00','2019-07-5 6:00:00')
    # b = findPeaksBySci(hisData1)
    # print(hisData1.values[b,0])
