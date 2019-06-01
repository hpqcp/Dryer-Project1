from base.sql_help import Sql200
from base.webSocketHelp import WebSocketHelp
from urllib.parse import urlencode
import pandas as pd
import time
import requests
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
webScortUrl = "ws://10.130.65.207:8181/HisWeb"
BASEURL = 'http://10.130.65.221:6666'

#ms = Sql200()
#impParDf = ms.GetImpParameterByLine(FactoryCode, ZoneName, BrandName, LineName)

impParDf = pd.DataFrame(pd.read_excel("C:\\LineBrandTag.xlsx"))

impParSeries = pd.Series(impParDf['ParameterName'].values, index=impParDf['GroupParameterTag'].values)
impParStr = ','.join(impParSeries.index.values)
AllStartTime = "2019-04-02 00:00:00"
AllEndTime = "2019-06-01 00:00:00"
# 时间向前向后推1小时
startTimeDt = datetime.datetime.strptime(AllStartTime, '%Y-%m-%d %H:%M:%S')
endTimeDt = datetime.datetime.strptime(AllEndTime, '%Y-%m-%d %H:%M:%S')
hoursDt = datetime.timedelta(days=1)

while(endTimeDt.__gt__(startTimeDt)):
   _endTimeDt = startTimeDt + hoursDt
   print(startTimeDt,_endTimeDt)
   for index, row in impParDf.iterrows():
       ParameterName = row['ParameterName']
       GroupParameterTag = row['GroupParameterTag']
       jsonStr = GroupParameterTag + "||" + startTimeDt.strftime("%Y-%m-%d %H:%M:%S") + "||" + _endTimeDt.strftime("%Y-%m-%d %H:%M:%S") + "||Cyclic||1000"
       StageBatchDf = WebSocketHelp.WebSocketJson(webScortUrl, jsonStr)
       StageBatchDf['DateTime'] = pd.to_datetime(StageBatchDf['DateTime'], format="%Y/%m/%d %H:%M:%S")
       resultNum = 100
       resultList = []
       i = 0
       str1 = ''
       for ImIndex, ImRow in StageBatchDf.iterrows():
           timeStamp = ImRow['DateTime'].value
           # timeStamp = timeStamp + 28800000000000
           str1 = str1 + 'ky_test_db,tag_name=' + ImRow['TagName'] + ' par_name=\"' + ParameterName + '\",value=' + str(
               ImRow['Value']) + ',vvalue=\"' + str(
               ImRow['vValue']) + '\" ' + str(timeStamp) + '\n'
           # ',par_name=' + ParameterName + ' ' \

           # +',par_name='+ImRow['ParName']
           # s = '''hsj1,tag_name=server04 value=123,vvalue=321 1558353606000000000'''
           i = i + 1
           if (i >= resultNum):
               resultList.append(str1)
               i = 0
               str1 = ''
       for resultStr in resultList:
           resp = requests.post(BASEURL + '/write', params={'db': 'test_db'}, data=resultStr.encode('utf-8'))
           # print(resp.status_code)
   print(startTimeDt, _endTimeDt,'ok')
   startTimeDt=_endTimeDt
# 时间向前向后推1小时
# startTimeDt = datetime.datetime.strptime(oStartTime, '%Y-%m-%d %H:%M:%S.%f')
# endTimeDt = datetime.datetime.strptime(oEndTime, '%Y-%m-%d %H:%M:%S.%f')
