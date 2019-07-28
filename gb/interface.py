import scipy.signal as sci
import matplotlib.pyplot as pyplot
import gb.preProcess as pre
import gb.productionAlgorithm as pAlgorithm
import pandas as pd
import numpy as np

#获取卷包单元（卷接、小包、条包、提升机等）日产量信息
#        _type : 单元类型, string , 'jj' : 卷接 ,'xb' :小包 , 'tb' : 条包
#   _startTime : 开始时间, string   example: '2019-07-02 06:00:00'
#     _endTime : 时间, string
#        _tags : tag地址 , list  , example: ["MES2RTDATA.U_Maker_11020030010.DC_BC","MES2RTDATA.U_Maker_11020030010.DC_PH","MES2RTDATA.U_Maker_11020030010.DC_SJCL","MES2RTDATA.U_Maker_11020030010.DC_YXSD"]
def GetUnitDayProduction(_type , _startTime , _endTime , _tags):
    #1 . 判断参数_type
    if _type == 'jj' :
        threshold = 5000     #临界值，根据单元类型不同，赋予不同数值
    elif _type == 'xb'   :
        threshold = 500
    elif _type == 'tb'   :
        threshold = 80
    else :
        return True,['-101','GetUnitDayProduction','参数_type没有传入已知的类型！']
    #2 . 准备
    bcTag = _tags[0]    #班次tag
    phTag = _tags[1]    #牌号tag
    clTag = _tags[2]    #产量tag
    sdTag = _tags[3]    #速度tag
    #3 . 调用GeneralProductionalAlgorithm计算产量信息
    sTime = _startTime
    eTime = _endTime
    res, Production = pAlgorithm.GeneralProductionalAlgorithm(bcTag, phTag, clTag, sdTag, sTime, eTime, threshold)
    if Production is None:
        return True,['0','GetUnitDayProduction','本日未开机！']
    else:
        return res , Production




if __name__ == "__main__":
    import datetime
    print('Begin : ' + str(datetime.datetime.now()))
    # tags=["MES2RTDATA.U_Maker_11020030010.DC_BC","MES2RTDATA.U_Maker_11020030010.DC_PH","MES2RTDATA.U_Maker_11020030010.DC_SJCL","MES2RTDATA.U_Maker_11020030010.DC_YXSD"]
    tags = ['QJYC.U_Maker_1304_13020010003.DC_JT','QJYC.U_Maker_1304_13020010003.DC_PH','QJYC.U_Maker_1304_13020010003.DC_SJCL','QJYC.U_Maker_1304_13020010003.DC_SCSD']
    sTime = "2019-07-02 04:00:00"
    eTime ="2019-07-03 04:00:00"
    res,p = GetUnitDayProduction('jj',sTime,eTime,tags)
    hisData3 = pre.loadHisDataByCyclic([tags[2]], '60000', sTime, eTime)

    vector = hisData3.values[:, 1].astype(np.float)
    indexes, values = sci.find_peaks(vector, height=7, distance=2.1)
    pyplot.plot(range(0, len(vector), 1), vector, 'r-')
    y = hisData3.values[indexes, 1].astype('float')
    pyplot.scatter(indexes, y)
    pyplot.title = '_title'
    pyplot.show()

    print('   End : ' + str(datetime.datetime.now()))
    print('a')