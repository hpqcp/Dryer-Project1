import gb.preProcess as pre
import gb.baseAlgorithm as baseAL
import pandas as pd
import numpy as np
import datetime
import bll.batch_process as batchProcess


###获取制丝批次期间段
def zs_pcSecByPCH(_tags,_freq,_beginTime,_endTime):
    freq = _freq
    beginTime = _beginTime
    endTime = _endTime
    hisData = pre.loadHisDataByCyclic(_tags, freq, beginTime, endTime, _type='vValue')
    if hisData.empty:
        return None
    
    _tags.insert(0,'DateTime')
    hisData = hisData[_tags]

    hisData.columns = ['DateTime', 'Shift', 'PCH', 'PH']
    pch = list()
    for i in hisData.groupby('PCH'):
        index1 = i[1].index.tolist()
        sec1 = baseAL.continuousSegmentByIndex(index1)
        for j in range(0, len(sec1), 1):  # 处理批次混乱
            minIndex = sec1.iloc[j, 0]
            maxIndex = sec1.iloc[j, 1]
            count = sec1.iloc[j, 2]
            pch.append([i[0], minIndex, maxIndex, count, hisData.iloc[minIndex, 0], hisData.iloc[maxIndex, 0]])
    pchDF = pd.DataFrame(pch)
    pchDF.rename(columns={0: 'PCH', 1: 'StartIndex', 2: 'EndIndex', 3: 'Count', 4: 'StartTime', 5: 'EndTime'},
                 inplace=True)
    pchDF[['sTime','eTime']] =  pchDF[['StartTime', 'EndTime']].apply(pd.to_datetime)
    # pchDF[['StartTime', 'EndTime']] = pchDF[['StartTime', 'EndTime']].apply(pd.to_datetime)
    pchDF['Interval'] = pchDF.apply(lambda x: (x['eTime'] - x['sTime']).total_seconds() / 60, axis=1)
    pchDF = pchDF[['PCH', 'StartIndex', 'EndIndex', 'Count', 'StartTime', 'EndTime', 'Interval']]
    pchDF.sort_values(by=['StartIndex'], axis=0, ascending=True, inplace=True)
    # append ph bc
    nPH = list()
    nPHPer = list()
    nShift = list()
    nShiftPer = list()
    for i in range(0, pchDF.shape[0], 1):
        b1 = pchDF['StartIndex'].values[i].astype(np.int)
        e1 = pchDF['EndIndex'].values[i].astype(np.int)
        r = hisData.iloc[b1:e1, :]
        if r.empty:
            nPH.append(np.nan)
            nPHPer.append(np.nan)
            nShift.append(np.nan)
            nShiftPer.append(np.nan)
        else:
            phGroup = r.groupby('PH', as_index=False)['DateTime'].count()
            phGroup.sort_values(by=["DateTime"], ascending=False, inplace=True)
            maxPH = phGroup["DateTime"].values[0].astype(np.int)
            perPH = maxPH / (e1 - b1)
            shiftGroup = r.groupby('Shift', as_index=False)['DateTime'].count()
            shiftGroup.sort_values(by=["DateTime"], ascending=False, inplace=True)
            maxShift = shiftGroup["DateTime"].values[0].astype(np.int)
            perShift = maxShift / (e1 - b1)
            nPH.append(phGroup["PH"].values[0])
            nPHPer.append(perPH)
            nShift.append(shiftGroup["Shift"].values[0])
            nShiftPer.append(perShift)
    pchDF["PH"] = nPH
    pchDF["PhPer"] = nPHPer
    pchDF["Shift"] = nShift
    pchDF["ShiftPer"] = nShiftPer
    pchDF.reset_index(drop=True,inplace=True)
    return pchDF


def zs_pcSecByLL(_tag,_freq,_pcSec,_delay):
    import matplotlib.pyplot as pyplot

    sec1 = _pcSec
    sec1['Status'] = '0'
    sec1['BatchStart'] = '1900-01-01 00:00:00.000'
    sec1['BatchEnd'] = '1900-01-01 00:00:00.000'
    for i in range(0,_pcSec.shape[0],1):
        sTime = str(_pcSec['StartTime'].values[i])
        eTime = str(_pcSec['EndTime'].values[i])
        sTime = str(datetime.datetime.strptime(sTime,'%Y-%m-%d %H:%M:%S.%f')-datetime.timedelta(seconds=_delay))
        eTime = str(datetime.datetime.strptime(eTime,'%Y-%m-%d %H:%M:%S.%f')+datetime.timedelta(seconds=_delay))
        hisData = pre.loadHisDataByCyclic([_tag], '6000', sTime, eTime, _type='Value')
        vector = hisData.values[:, 1].astype(np.float)
        data1 = vector[:int(len(vector) / 2)]
        data2 = vector[len(data1):]
        #
        # pyplot.plot(range(0, len(vector), 1), vector, 'r-')
        # pyplot.show()
        #
        #通过标偏来判断是否有波形
        std = np.std(vector)
        if std <800 :  #以1000为临界值
            sec1['Status'].values[i] = '1'
        else:
            if np.std(data1) < 800 or np.std(data2) < 800 :
                sec1['Status'].values[i] = '2'
        if sec1['Status'].values[i] != '0' :
            continue
        df = pd.DataFrame(vector)
        batchPoint = batchProcess.check_batch_point(df)
        sIndex = int(batchPoint[0][0])
        eIndex = int(batchPoint[0][1])
        if sIndex >= 20 :
            sIndex = sIndex -20
        if len(vector) - eIndex >= 20 :
            eIndex = eIndex  + 20
        sec1['BatchStart'].values[i] = str(hisData.values[sIndex, 0])
        sec1['BatchEnd'].values[i] = str(hisData.values[eIndex, 0])

    sec1[['sTime', 'eTime']] = sec1[['BatchStart', 'BatchEnd']].apply(pd.to_datetime)
    # pchDF[['StartTime', 'EndTime']] = pchDF[['StartTime', 'EndTime']].apply(pd.to_datetime)
    sec1['Interval1'] = sec1.apply(lambda x: (x['eTime'] - x['sTime']).total_seconds() / 60, axis=1)
    return sec1

if __name__ == "__main__":
    tags = ['XJYC.U_BladeFeedingA.GBH','XJYC.U_BladeFeedingA.PCH', 'XJYC.U_BladeFeedingA.PH']
    llTag = 'XJYC.U_BladeFeedingB.GYLL'
    # tags = ['MES2RTDATA.U_BAL_11010150001.DC_TeamCode',	 'MES2RTDATA.U_Cutting_11010110002.DC_PCH',	'MES2RTDATA.U_Cutting_11010110002.DC_PH']
    # llTag = 'MES2RTDATA.U_BAL_11010150001.DC_LL'
    # tags = ['MES2RTDATA.U_BAL_11010140001.DC_TeamCode',	 'MES2RTDATA.U_DRY_11010140003.DC_PCH',	'MES2RTDATA.U_DRY_11010140003.DC_PH']
    # llTag = 'MES2RTDATA.U_BAL_11010220001.DC_LL'
    freq = '60000'
    beginTime = '2019-8-8 06:00:00'
    endTime = '2019-8-9 06:00:00'
    a = zs_pcSecByPCH(tags,freq,beginTime,endTime)
    b = zs_pcSecByLL(llTag,freq,a,1800)

    print('1')