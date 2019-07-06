import gb.preProcess as pre


#获取班次开始结束时间
#_shiftTag 班次点,_beginShiftTag 班次开始点,_endShiftTag 班次结束点
def shiftTime(_shiftTag,_beginShiftTag,_endShiftTag,_beginTime,_endTime):
    tags = [_shiftTag,_beginShiftTag,_endShiftTag]
    freq = "3600000"   #1小时
    hisData = pre.loadHisDataByCyclic(tags, freq, _beginTime, _endTime)
    hisData1=hisData.drop_duplicates([_shiftTag, _beginShiftTag, _endShiftTag]) #去重
    # hisData1.columns["DateTime","Shfit","ShiftBegin","ShiftEnd"]
    hisData1.rename(columns={_shiftTag : 'Shfit', _beginShiftTag: 'ShiftBegin', _endShiftTag: 'ShiftEnd'}, inplace=True)
    order = ['DateTime', "Shfit","ShiftBegin","ShiftEnd"]
    hisData2 = hisData1[order]
    return hisData2










if __name__ == "__main__":
    # str = ["MES2RTDATA.U_Maker_11020030001.DC_SJCL","MES2RTDATA.U_Maker_11020030001.DC_BC",
    #        "MES2RTDATA.U_Maker_11020030001.DC_YXSD","MES2RTDATA.U_Maker_11020030001.DC_PH"]
    str1 ="MES2RTDATA.U_Maker_11020030001.DC_BC"
    str2 ="MES2RTDATA.U_Maker_11020030001.DC_DQBCKSSJ"
    str3 ="MES2RTDATA.U_Maker_11020030001.DC_DQBCJSSJ"
    a = shiftTime(str1,str2,str3,"2019-07-01 06:00:00","2019-07-02 06:00:00")
    print(a)