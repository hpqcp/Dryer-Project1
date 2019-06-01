import pandas as pd
from base.sql_help import Sql200
from base.webSocketHelp import WebSocketHelp
import datetime

# _df _groupName:以哪一列分组 _vColumns:以那一列作为数据 _indexName:以哪一列对齐（默认以索引对齐）_havIndex:是否显示对齐列
def RowToColumn(_df, _groupName, _vColumns, _indexName="index", _havIndex=False):
    dfFL = pd.DataFrame()
    i = 0
    for name, group in _df.groupby(_groupName):
        if ((_havIndex == True) & (i == 0)):
            inxDt = None
            if (_indexName == "index"):
                inxDt = pd.Series(group.index.values, index=group.index.values)
            else:
                inxDt = pd.Series(group.loc[:, _indexName].values, index=group.loc[:, _indexName].values)
            inxDt.name = _indexName
            dfFL = dfFL.join(inxDt, how='outer')
        vDt = None
        if (_indexName == "index"):
            vDt = group.loc[:, _vColumns].reset_index(drop=True)
        else:
            vDt = pd.Series(group.loc[:, _vColumns].values, index=group.loc[:, _indexName].values)
        coName = name
        vDt.name = coName
        dfFL = dfFL.join(vDt, how='outer')
        i = i + 1
    dfFL = dfFL.reset_index(drop=True)
    return dfFL

#获取牌号批次时间
# 时间前后延长（分钟）
def GetBatchCutDf(FactoryCode,ZoneName,BrandName,HLBrandName,LineName,StageName,Delay,startTime,endTime):
    IdTypeNameList = ['牌号实时点', '批次号实时点']
    webScortUrl = "ws://10.130.65.207:8181/HisWeb"
    ms = Sql200()
    #查询数据库
    #IdTypeDf = ms.GetIDInf(FactoryCode, ZoneName, BrandName, LineName, StageName, IdTypeNameList)
    IdTypeDf = pd.DataFrame(pd.read_excel("D:\\sql_data\\LineBrandSFTag.xlsx"))
    IdTypeDf = IdTypeDf[IdTypeDf['StageName']==StageName]
    IdTypeSeries = pd.Series(IdTypeDf['TypeName'].values, index=IdTypeDf['GroupParameterTag'].values)
    # 先按小时获取牌号批次号
    IDTagName = ','.join(IdTypeSeries.index.values)

    hisSType = "Cyclic"
    frequency = "3600000"  # 查询批次频率
    daraFrequency = "10000"  # 查询数据频率
    df = WebSocketHelp.WebSocketJson(webScortUrl,
                                     IDTagName + "||" + startTime + "||" + endTime + "||" + hisSType + "||" + frequency)
    # columns=df['TagName'].values, dtype=str
    # df = df.astype({'TagName':'str','DateTime':'str','Value':'float', 'vValue':'float'})
    # columns=['TagName', 'DateTime', 'Value', 'vValue']
    dfFL = RowToColumn(df, 'TagName', 'vValue', _indexName='DateTime', _havIndex=True)
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

        batchIdDf = RowToColumn(batchIdDf, 'TagName', 'vValue', _indexName='DateTime', _havIndex=True)
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
    return BatchCutDf
if __name__ == "__main__":
    FactoryCode = '1100'
    ZoneName = '制丝'
    BrandName = '云烟(紫)模组一'
    HLBrandName = '5.0'
    LineName = 'C线'
    StageName = '切丝烘丝加香段'
    startTime = "2019-04-02 00:00:00"  # 按时间段查询批次（开始时间）
    endTime = "2019-04-16 00:00:00"  # 按时间段查询批次（结束时间）
    Delay = 10 #时间范围延长（分钟）
    BatchCutDf = GetBatchCutDf(FactoryCode,ZoneName,BrandName,HLBrandName,LineName,StageName,Delay,startTime,endTime)
    print(BatchCutDf)