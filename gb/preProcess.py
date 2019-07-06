import base.webSocketHelp as ws
import chart.plot as plt
import numpy as np
import pandas as pd
import scipy.signal as sci
import matplotlib.pyplot as pyplot

#以拟合的方式读取HIS数据
#_tags 点名   _freq 频率
#type : Value , vVlalue
def loadHisDataByCyclic(_tags,_freq,_beginTimeStr,_endTimeStr,_type="vValue"):
    tagsStr = ""
    for i in range(0,len(_tags),1):
        if (i == len(_tags) - 1):
            tagsStr = tagsStr + _tags[i]
        else:
            tagsStr = tagsStr + _tags[i] + ","

    hisStr = tagsStr+"||"+_beginTimeStr+"||"+_endTimeStr+"||Cyclic||"+_freq
    df = ws.WebSocketHelp.WebSocketJson("ws://10.130.65.207:8181/HisWeb",hisStr)
    df2 = ws.WebSocketHelp.RowToColumn(df, 'TagName', _type, _indexName='DateTime', _havIndex=True)
    return df2



if __name__ == "__main__":
    # str = ["MES2RTDATA.U_Maker_11020030001.DC_SJCL","MES2RTDATA.U_Maker_11020030001.DC_BC",
    #        "MES2RTDATA.U_Maker_11020030001.DC_YXSD","MES2RTDATA.U_Maker_11020030001.DC_PH"]
    str = ["MES2RTDATA.U_Maker_11020030001.DC_BC","MES2RTDATA.U_Maker_11020030001.DC_DQBCJSSJ","MES2RTDATA.U_Maker_11020030001.DC_DQBCKSSJ"]
    freq = "3600000"
    a = loadHisDataByCyclic(str,freq,"2019-07-01 06:00:00","2019-07-02 06:00:00")
    print(a)