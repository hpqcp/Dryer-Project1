import scipy.signal as sci
import matplotlib.pyplot as pyplot
import gb.preProcess as pre
import gb.productionAlgorithm as pAlgorithm
import pandas as pd
import numpy as np
import gb.zs as zs

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

#获取制丝工艺段批次信息
#        _freq : 频率, int , 6000
#   _startTime : 开始时间, string   example: '2019-07-02 06:00:00'
#     _endTime : 时间, string
#        _tags : tag地址 , list  , example: ["工班号,"批次号","牌号","工艺流量"]
#       _delay : 前后扩展延时 , int , 1800 , 秒
def GetBatchInfoBySegment(_tags,_freq,_beginTime,_endTime,_delay):
    tags1 = _tags[0:3] #GBH PCH PH
    tags2 = _tags[3]   #GYLL
    pcInfo = zs.zs_pcSecByPCH(tags1,_freq,_beginTime,_endTime)
    if (pcInfo.empty):
        return [True,['0','GetBatchInfoBySegment','批次数据为空！']]
    b = zs.zs_pcSecByLL(tags2, _freq, pcInfo, _delay)
    return [False,b]

if __name__ == "__main__":
    # import datetime
    # print('Begin : ' + str(datetime.datetime.now()))
    # # tags=["MES2RTDATA.U_Maker_11020030010.DC_BC","MES2RTDATA.U_Maker_11020030010.DC_PH","MES2RTDATA.U_Maker_11020030010.DC_SJCL","MES2RTDATA.U_Maker_11020030010.DC_YXSD"]
    # tags = ['QJYC.U_Maker_1304_13020010003.DC_JT','QJYC.U_Maker_1304_13020010003.DC_PH','QJYC.U_Maker_1304_13020010003.DC_SJCL','QJYC.U_Maker_1304_13020010003.DC_SCSD']
    # sTime = "2019-07-02 04:00:00"
    # eTime ="2019-07-03 04:00:00"
    # res,p = GetUnitDayProduction('jj',sTime,eTime,tags)
    # hisData3 = pre.loadHisDataByCyclic([tags[2]], '60000', sTime, eTime)
    #
    # vector = hisData3.values[:, 1].astype(np.float)
    # indexes, values = sci.find_peaks(vector, height=7, distance=2.1)
    # pyplot.plot(range(0, len(vector), 1), vector, 'r-')
    # y = hisData3.values[indexes, 1].astype('float')
    # pyplot.scatter(indexes, y)
    # pyplot.title = '_title'
    # pyplot.show()
    #
    # print('   End : ' + str(datetime.datetime.now()))
    # print('a')

    #制丝
    #tags = ['XJYC.U_BladeFeedingA.GBH', 'XJYC.U_BladeFeedingA.PCH', 'XJYC.U_BladeFeedingA.PH','XJYC.U_BladeFeedingB.GYLL']
    # tags = ['MES2RTDATA.U_BAL_11010150001.DC_TeamCode',	 'MES2RTDATA.U_Cutting_11010110002.DC_PCH',	'MES2RTDATA.U_Cutting_11010110002.DC_PH','MES2RTDATA.U_BAL_11010150001.DC_LL']
    #昆烟A线回潮一加段
    tags = ['MES2RTDATA.U_BAL_11010010002.DC_TeamCode','MES2RTDATA.U_CON_11010010003.DC_PCH','MES2RTDATA.U_CON_11010010003.DC_PH','MES2RTDATA.U_BAL_11010010002.DC_LL']
    # tags = ['MES2RTDATA.U_BAL_11010140001.DC_TeamCode',	 'MES2RTDATA.U_DRY_11010140003.DC_PCH',	'MES2RTDATA.U_DRY_11010140003.DC_PH','MES2RTDATA.U_BAL_11010220001.DC_LL']
    freq = '60000'
    beginTime = '2019-8-9 06:00:00'
    endTime = '2019-8-10 06:00:00'
    b = GetBatchInfoBySegment(tags,freq,beginTime,endTime,1800)
    print(b)
