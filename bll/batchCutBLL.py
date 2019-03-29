from base.sql_help import Sql200
from base.webSocketHelp import WebSocketHelp
import pandas as pd
import base.HisHelp as his
import datetime
from entity.HisBatchEntity import HisBatchEntity


# 行转列
def RowToColumn(_df, _groupName, _vColumns):
    dfFL = pd.DataFrame()
    for name, group in _df.groupby(_groupName):
        vDt = group.loc[:, _vColumns].reset_index(drop=True)
        coName = name
        vDt.name = coName
        dfFL = dfFL.join(vDt, how='outer')
    return dfFL


FactoryCode = '1100'
ZoneName = '制丝'
BrandName = '云烟(紫)模组一'
HLBrandName = '5.0'
LineName = 'C线'
StageName = '切丝烘丝加香段'
parNameList = ['切叶丝含水率', '叶丝增温增湿工艺流量', '叶丝增温增湿蒸汽流量', '薄板干燥热风温度', '薄板干燥Ⅰ区筒壁温度', '薄板干燥Ⅱ区筒壁温度', '薄板干燥出料温度', '薄板干燥出料含水率',
               '叶丝冷却出料含水率']
IdTypeNameList = ['牌号实时点', '批次号实时点']
webScortUrl = "ws://10.130.65.207:8181/HisWeb"
# 时间前后延长（分钟）
Delay = 10
ms = Sql200()
IdTypeDf = ms.GetIDInf(FactoryCode, ZoneName, BrandName, LineName, StageName, IdTypeNameList)
IdTypeSeries = pd.Series(IdTypeDf['TypeName'].values, index=IdTypeDf['GroupParameterTag'].values)
# 先按小时获取牌号批次号
IDTagName = ','.join(IdTypeSeries.index.values)
startTime = "2019-01-02 00:00:00"
endTime = "2019-01-04 00:00:00"
hisSType = "Cyclic"
frequency = "3600000"
df = WebSocketHelp.WebSocketJson(webScortUrl,
                                 IDTagName + "||" + startTime + "||" + endTime + "||" + hisSType + "||" + frequency)
# columns=df['TagName'].values, dtype=str
# df = df.astype({'TagName':'str','DateTime':'str','Value':'float', 'vValue':'float'})
# columns=['TagName', 'DateTime', 'Value', 'vValue']
dfFL = his.RowToColumn(df, 'TagName', 'vValue', _indexName='DateTime', _havIndex=True)
c = IdTypeSeries[dfFL.columns.values.tolist()].values
# dfFL.rename(columns=[c], inplace=True)
dfFL.columns = c
# 过滤其他牌号
dfFL = dfFL[dfFL['牌号实时点'] == HLBrandName]
# 批次开始结束时间（时间精确到分钟）
BatchCutDf = pd.DataFrame(columns=['PCH', 'PH', 'StartTime', 'EndTime'])
for name, group in dfFL.groupby('批次号实时点'):
    IdDfGLen = len(group)
    oStartTime = group.iloc[0, 0]
    oEndTime = group.iloc[-1, 0]
    # 时间向前向后推1小时
    startTimeDt = datetime.datetime.strptime(oStartTime, '%Y-%m-%d %H:%M:%S.%f')
    endTimeDt = datetime.datetime.strptime(oEndTime, '%Y-%m-%d %H:%M:%S.%f')
    hoursDt = datetime.timedelta(hours=1)
    startTimeDt = startTimeDt - hoursDt
    endTimeDt = endTimeDt + hoursDt
    oStartTime = startTimeDt.strftime("%Y-%m-%d %H:%M:%S")
    oEndTime = endTimeDt.strftime("%Y-%m-%d %H:%M:%S")
    # 按照分钟获取数据
    batchIdDf = WebSocketHelp.WebSocketJson(webScortUrl,
                                            IDTagName + "||" + oStartTime + "||" + oEndTime + "||Cyclic||60000")

    batchIdDf = his.RowToColumn(batchIdDf, 'TagName', 'vValue', _indexName='DateTime', _havIndex=True)
    c = IdTypeSeries[batchIdDf.columns.values.tolist()].values
    # dfFL.rename(columns=[c], inplace=True)
    batchIdDf.columns = c
    # 过滤获取这一批次这一牌号
    batchIdDf = batchIdDf[(batchIdDf['牌号实时点'] == HLBrandName) & (batchIdDf['批次号实时点'] == name)]
    b1 = batchIdDf.iloc[0, 1]
    b2 = batchIdDf.iloc[0, 2]
    b3 = batchIdDf.iloc[0, 0]
    b4 = batchIdDf.iloc[-1, 0]
    # 将批次号牌号开始结束时间添加到DF
    BatchCutDf = BatchCutDf.append([{'PCH': b1, 'PH': b2,
                                     'StartTime': b3, 'EndTime': b4}],
                                   ignore_index=True)

# 批次开始结束时间（时间精确到分钟）
print(BatchCutDf)

# 按时间牌号获取关键参数点
impParDf = ms.GetImpParameter(FactoryCode, ZoneName, BrandName, LineName, StageName, parNameList)
impParSeries = pd.Series(impParDf['ParameterName'].values, index=impParDf['GroupParameterTag'].values)
impParStr = ','.join(impParSeries.index.values)

# 按时间关键参数点获取数据
hisBatchList = []
for ImIndex, ImRow in BatchCutDf.iterrows():
    # 时间延长
    delta = datetime.timedelta(minutes=Delay)
    bStartTimeDt = datetime.datetime.strptime(ImRow['StartTime'], '%Y-%m-%d %H:%M:%S.%f')
    bEndTimeDt = datetime.datetime.strptime(ImRow['EndTime'], '%Y-%m-%d %H:%M:%S.%f')

    bStartTimeDt = bStartTimeDt - delta
    bEndTimeDt = bEndTimeDt + delta

    bStartTime = bStartTimeDt.strftime("%Y-%m-%d %H:%M:%S")
    bEndTime = bEndTimeDt.strftime("%Y-%m-%d %H:%M:%S")

    jsonStr = impParStr + "||" + bStartTime + "||" + bEndTime + "||Cyclic||1000"
    StageBatchDf = WebSocketHelp.WebSocketJson(webScortUrl, jsonStr)
    StageBatchDf = his.RowToColumn(StageBatchDf, 'TagName', 'Value', _indexName='DateTime', _havIndex=True)
    c = impParSeries[StageBatchDf.columns.values.tolist()].values
    # dfFL.rename(columns=[c], inplace=True)
    StageBatchDf.columns = c
    StageBatchDf = StageBatchDf[impParSeries.values]
    hisBatchEntity = HisBatchEntity(ImRow['PCH'], ImRow['PH'], ImRow['StartTime'], ImRow['EndTime'], StageBatchDf)
    hisBatchList.append(hisBatchEntity)
print(hisBatchList)
# 将异常批次数据存入redis
