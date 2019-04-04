from base.sql_help import Sql200
from base.webSocketHelp import WebSocketHelp
import pandas as pd
import base.HisHelp as his
import datetime
import bll.batch_process as batPro
from entity.HisBatchEntity import HisBatchEntity

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
startTime = "2019-01-02 00:00:00"  # 按时间段查询批次（开始时间）
endTime = "2019-01-02 10:00:00"  # 按时间段查询批次（结束时间）
hisSType = "Cyclic"
frequency = "3600000"  # 查询批次频率
daraFrequency = "10000"  # 查询数据频率
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

    batchIdDf = WebSocketHelp.WebSocketJson(webScortUrl,
                                            IDTagName + "||" + oStartTime + "||" + oEndTime + "||Cyclic||" + daraFrequency)

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

    jsonStr = impParStr + "||" + bStartTime + "||" + bEndTime + "||Cyclic||10000"
    StageBatchDf = WebSocketHelp.WebSocketJson(webScortUrl, jsonStr)
    StageBatchDf = his.RowToColumn(StageBatchDf, 'TagName', 'Value', _indexName='DateTime', _havIndex=True)
    c = impParSeries[StageBatchDf.columns.values.tolist()].values
    # dfFL.rename(columns=[c], inplace=True)
    StageBatchDf.columns = c
    StageBatchDf = StageBatchDf[impParSeries.values]
    hisBatchEntity = HisBatchEntity(ImRow['PCH'], ImRow['PH'], ImRow['StartTime'], ImRow['EndTime'], StageBatchDf)
    hisBatchList.append(hisBatchEntity)

# standardDf = pd.DataFrame({
#     '切叶丝含水率': {'down': 20, 'up': 21},
#     '薄板干燥出料含水率': {'down': 13, 'up': 15},
#     '叶丝冷却出料含水率': {'down': 12.3, 'up': 13.3},
# })
# 工艺标准
standardDf = pd.DataFrame({
    1: {'down': 20, 'up': 21},
    7: {'down': 13, 'up': 15},
    9: {'down': 12.3, 'up': 13.3},
})
abnBatchParList = []#异常数据批次
for _hisBatchEntity in hisBatchList:
    hisDf = _hisBatchEntity.HisDf
    hisDf = hisDf.astype('float64')#转换格式
    useCol = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    hisDf.columns = useCol
    point = batPro.check_batch_point(hisDf)  # 获取批次开始结束点
    c = 1
    # 按列进行遍历
    for column, colSeries in hisDf.iteritems():#column:列名(参数点),colSeries:数据
        # 判断该参数点是否有标准
        if column in standardDf.columns:
            up = standardDf.loc['up', column]
            down = standardDf.loc['down', column]
            p1 = point[c][0]
            p2 = point[c][1]
            wtDF = colSeries.values[p1:p2]  # serieas
            # 错误1：索引有负数,错误2：料尾索引小于料头索引
            wt = batPro.batch_Steadystate_r1(wtDF)  # 批次截取方法
            # print(wt,len(wtDF),len(df))
            wtSeries = colSeries[p1 + wt[0]:p1 + wt[1]]
            # cPlt.singlePlot(df[p1 + wt[0]:p1 + wt[1]], _title=batchStr)
            abnSeries = wtSeries[wtSeries > up & wtSeries < down]  # 过滤获取异常数据
            if len(abnSeries) > 0:  # 如果存在超出标准的数据
                # 毫厘牌号|毫厘牌号批次号|开始时间|结束时间|参数点
                abnBatchParList.append(
                    _hisBatchEntity.PH + "|" + _hisBatchEntity.PCH + "|" + hisBatchEntity.StartTime + "|" + hisBatchEntity.EndTime + "|" + column)

        c = c + 1
print(abnBatchParList)
