from base.sql_help import Sql200
from base.webSocketHelp import WebSocketHelp
import pandas as pd

FactoryCode = '1100'
ZoneName = '制丝'
BrandName = '云烟(紫)模组一'
LineName = 'C线'
StageName = '切丝烘丝加香段'
parNameList = ['切叶丝含水率', '叶丝增温增湿工艺流量', '叶丝增温增湿蒸汽流量', '薄板干燥热风温度', '薄板干燥Ⅰ区筒壁温度', '薄板干燥Ⅱ区筒壁温度', '薄板干燥出料温度', '薄板干燥出料含水率',
               '叶丝冷却出料含水率']
IdTypeNameList = ['牌号实时点', '批次号实时点']
webScortUrl = "ws://10.130.65.207:8181/HisWeb"
ms = Sql200()
IdTypeDf = ms.GetIDInf(FactoryCode, ZoneName, BrandName, LineName, StageName, IdTypeNameList)
IdTypeSeries = pd.Series(IdTypeDf['TypeName'].values, index=IdTypeDf['GroupParameterTag'].values)
# 按时间段获取牌号批次号
IDTagName = ','.join(IdTypeSeries.index.values)
startTime = "2019-01-01 00:00:00"
endTime = "2019-01-01 23:59:59"
hisSType = "Cyclic"
frequency = "3600000"


df = WebSocketHelp.WebSocketJson(webScortUrl,
                                 IDTagName + "||" + startTime + "||" + endTime + "||" + hisSType + "||" + frequency)

dfFL = pd.DataFrame()
for name, group in df.groupby('TagName'):
    dfFL[IdTypeSeries[name]] = group.pop('vValue').tolist()

# 按时间牌号获取关键参数点

# 按时间关键参数点获取数据

# 将异常批次数据存入redis
print()
