# import gb.preProcess as pre
import gb.productionAlgorithm as pAlgorithm
import pandas as pd

#获取卷包单元（卷接、小包、条包、提升机等）日产量信息
#   _type : 单元类型 string , 'jj' : 卷接 ,'xb' :小包 , 'tb' : 条包
def GetUnitDayProduction(_type , _startTime , _endTime , _tags):
    #1 . 判断参数_type
    if _type == 'jj' :
        threshold = 5000     #临界值，根据单元类型不同，赋予不同数值
    elif _type == 'xb'   :
        threshold = 300
    elif _type == 'tb'   :
        threshold = 50
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
    tags=["MES2RTDATA.U_Maker_11020030010.DC_BC","MES2RTDATA.U_Maker_11020030010.DC_PH","MES2RTDATA.U_Maker_11020030010.DC_SJCL","MES2RTDATA.U_Maker_11020030010.DC_YXSD"]
    sTime = "2019-07-02 06:00:00"
    eTime ="2019-07-03 06:00:00"
    res,p = GetUnitDayProduction('jj',sTime,eTime,tags)
    print('   End : ' + str(datetime.datetime.now()))
    print(p)