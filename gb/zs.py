import gb.preProcess as pre
import gb.baseAlgorithm as baseAL
import pandas as pd
import numpy as np
import os
import datetime

###获取制丝批次期间段
def zs_pcSecByPCH(_tags,_freq,_beginTime,_endTime):
    freq = _freq
    beginTime = _beginTime
    endTime = _endTime
    hisData = pre.loadHisDataByCyclic(_tags, freq, beginTime, endTime, _type='vValue')
    if hisData.empty:
        return None
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
    pchDF[['StartTime', 'EndTime']] = pchDF[['StartTime', 'EndTime']].apply(pd.to_datetime)
    pchDF['Interval'] = pchDF.apply(lambda x: (x['EndTime'] - x['StartTime']).total_seconds() / 60, axis=1)
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


def zs_pcSecByPCH(_tag,_freq,_pcSec,_delay):

    for i in range(0,_pcSec.shape[0],1):
        sTime = _pcSec.iloc[i,'StartTime']
        eTime = _pcSec.iloc[i, 'StartTime']
        hisData = pre.loadHisDataByCyclic(_tag, _freq, sTime, eTime, _type='Value')



if __name__ == "__main__":
    tags = ['XJYC.U_BladeFeedingA.GBH',	'XJYC.U_BladeFeedingA.PCH', 'XJYC.U_BladeFeedingA.PH']
    # tags = ['MES2RTDATA.U_BAL_11010150001.DC_TeamCode',	'MES2RTDATA.U_BAL_11010150001.DC_OrderNo',\
    #         'MES2RTDATA.U_Cutting_11010110002.DC_PCH',	'MES2RTDATA.U_Cutting_11010110002.DC_PH',	'MES2RTDATA.U_DRY_11010150002.IT_SBZT']

    llTag =
    freq = '60000'
    beginTime = '2019-8-8 02:00:00'
    endTime = '2019-8-9 02:00:00'
    a = zs_pcSecByPCH(tags,freq,beginTime,endTime)

    print('1')