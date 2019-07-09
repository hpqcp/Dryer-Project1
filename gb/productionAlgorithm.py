import gb.baseAlgorithm as baseAlg
import gb.preProcess as pre


#计算卷包机
def GeneralProductionalAlgorithm(_shiftTag,_yields,_speed,_beginShiftTag,_endShiftTag,_beginTime,_endTime):
    #预定义变量
    noProduct = [0,0,0]   #是否全天未生产判断list,1未生产，0已生产；[0]通过制度排班进行判断；[1]通过运行速度判断

    #1 . 获取排班信息
    tags1 = [_shiftTag,_beginShiftTag,_endShiftTag]
    freq = "60000"  # 1分钟
    hisData = pre.loadHisDataByCyclic(tags1, freq, _beginTime, _endTime)
    if (hisData.empty):
        return True,["-101","GeneralProductionalAlgorithm","数据为空！"]
    if (hisData.shape[1]<4):
        return True, ["-102", "GeneralProductionalAlgorithm", "数据不完整，缺少列！列数："+str(hisData.shape[1])]
    shiftSystemTime = baseAlg.shiftTime(tags1,hisData)   #获取制度时间
    shiftData = shiftSystemTime.drop_duplicates('Shfit')  # 去重
    if (shiftData.shape[0] <= 1):    #只有一条排班信息可估计为未生产
        noProduct[0]=1
    else:
        noProduct[0]=0

    # #2. 获取机器速度信息
    # tags2 = [_speed]
    # freq = "60000"  # 1分钟
    # hisData2= pre.loadHisDataByCyclic(tags2, freq, _beginTime, _endTime)
    # if (hisData2.empty):        return True,["-201","GeneralProductionalAlgorithm","数据为空！"]
    # if (hisData2.shape[1]<2):        return True, ["-202", "GeneralProductionalAlgorithm", "数据不完整，缺少列！列数："+str(hisData2.shape[1])]
    # runSec = baseAlg.runHaltIntervalBySpeed(hisData2, _type='run')
    # if (runSec is None):    noProduct[1] = 1    #机器速度均为0 ， 表示全天未开机

    #3.
    hisData3 = hisData  #复用HIS1数据
    shiftSec = baseAlg.shiftSection(hisData3)
    if (shiftSec.shape[0]<= 1):     noProduct[2] = 1    #只有一条班次记录，有可能未生产，也有可能本机未作换班操作
    else:   noProduct[2] = 0

    #4.
    tags4 = [_yields]
    freq = "60000"  # 6s    # #3.

    hisData4 = pre.loadHisDataByCyclic(tags4, freq, _beginTime, _endTime)
    b = baseAlg.findPeaksBySci(hisData4)
    print(hisData4.values[b,0])


    return 0


if __name__ == "__main__":
    str1 ="MES2RTDATA.U_Maker_11020030001.DC_BC"
    str2 ="MES2RTDATA.U_Maker_11020030001.DC_SJCL"
    str3 ="MES2RTDATA.U_Maker_11020030001.DC_YXSD"
    str4 ="MES2RTDATA.U_Maker_11020030001.DC_DQBCKSSJ"
    str5 ="MES2RTDATA.U_Maker_11020030001.DC_DQBCJSSJ"
    a = GeneralProductionalAlgorithm(str1,str2,str3,str4,str5,"2019-07-01 06:00:00","2019-07-02 06:00:00")
    # print(a)