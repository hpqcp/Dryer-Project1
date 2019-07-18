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

#以拟合的方式读取HIS数据
#_tags 点名   _freq 频率
#type : Value , vVlalue
def loadHisDataByFull(_tags,_freq,_beginTimeStr,_endTimeStr,_type="vValue"):
    tagsStr = ""
    for i in range(0,len(_tags),1):
        if (i == len(_tags) - 1):
            tagsStr = tagsStr + _tags[i]
        else:
            tagsStr = tagsStr + _tags[i] + ","

    hisStr = tagsStr+"||"+_beginTimeStr+"||"+_endTimeStr+"||Full||"+_freq
    df = ws.WebSocketHelp.WebSocketJson("ws://10.130.65.207:8181/HisWeb",hisStr)
    df2 = ws.WebSocketHelp.RowToColumn(df, 'TagName', _type, _indexName='DateTime', _havIndex=True)
    return df2


def plot2Excel(_hisData,_imgPath,_sheet,_x,_y):
    vector = _hisData.values[:, 1].astype(np.float)
    indexes, values = sci.find_peaks(vector, height=7, distance=2.1)
    pyplot.plot(range(0, len(vector), 1), vector, 'r-')
    y = _hisData.values[indexes, 1].astype('float')
    pyplot.scatter(indexes, y)
    pyplot.title = '_title'
    pyplot.savefig(_imgPath)
    pyplot.show()
    # writer = pd.ExcelWriter('savepicture.xlsx', engine='xlsxwriter')
    # sheet = _write.book.add_worksheet('test')
    _sheet.insert_image(_x, _y, _imgPath, {'x_scale': 0.6, 'y_scale': 0.6})
    return 0

if __name__ == "__main__":
    # str = ["MES2RTDATA.U_Maker_11020030001.DC_SJCL","MES2RTDATA.U_Maker_11020030001.DC_BC",
    #        "MES2RTDATA.U_Maker_11020030001.DC_YXSD","MES2RTDATA.U_Maker_11020030001.DC_PH"]
    # str = ["MES2RTDATA.U_Maker_11020030001.DC_BC","MES2RTDATA.U_Maker_11020030001.DC_DQBCJSSJ","MES2RTDATA.U_Maker_11020030001.DC_DQBCKSSJ"]
    str = ["MES2RTDATA.U_Maker_11020030001.DC_SJCL"]
    freq = "6000"
    a = loadHisDataByCyclic(str,freq,"2019-07-01 06:00:00","2019-07-02 06:00:00")
    plot2Excel(a)
    print(a)