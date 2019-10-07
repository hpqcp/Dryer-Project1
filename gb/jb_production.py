#计算卷包机
#_threshold:临界值
def GeneralProductionalAlgorithm(_shiftTag,_phTag,_yieldsTag,_speedTag,_beginTime,_endTime,_threshold):
    #预定义变量
    noProduct = [0,0,0]   #是否全天未生产判断list,1未生产，0已生产；[0]通过制度排班进行判断；[1]通过运行速度判断
    noProductCount = 0

    # #1 . 获取排班信息
    # tags1 = [_shiftTag,_beginShiftTag,_endShiftTag]
    # freq = "60000"  # 1分钟
    # hisData = pre.loadHisDataByCyclic(tags1, freq, _beginTime, _endTime)
    # if (hisData.empty):
    #     return True,["-101","GeneralProductionalAlgorithm","数据为空！"]
    # if (hisData.shape[1]<4):
    #     return True, ["-102", "GeneralProductionalAlgorithm", "数据不完整，缺少列！列数："+str(hisData.shape[1])]
    # shiftSystemTime = baseAlg.shiftTime(tags1,hisData)   #获取制度时间
    # shiftData = shiftSystemTime.drop_duplicates('Shfit')  # 去重
    # if (shiftData.shape[0] <= 1):    #只有一条排班信息可估计为未生产
    #     noProduct[0]=1
    # else:
    #     noProduct[0]=0
    ##

    #1. 获取机器速度信息
    tags1 = [_speedTag]
    freq = "600000"  # 6分钟
    hisData1= pre.loadHisDataByCyclic(tags1, freq, _beginTime, _endTime)
    if (hisData1.empty):        return True,["-101","GeneralProductionalAlgorithm","数据为空！"]
    if (hisData1.shape[1]<2):        return True, ["-102", "GeneralProductionalAlgorithm", "数据不完整，缺少列！列数："+str(hisData1.shape[1])]

    nullCount = hisData1[hisData1.values[:,1] == 'NULL'].shape[0]
    if nullCount / hisData1.shape[0] > 0.1 :
        noProduct[0] = 1  # Null值过多
        #noProductCount = noProductCount + 1
    else:
        hisData1.replace('NULL','0',inplace=True)
        runSec = baseAlg.runHaltIntervalBySpeed(hisData1, _type='run')
        if (runSec is None):
            noProduct[0] = 1    #机器速度均为0 ， 表示全天未开机
            noProductCount = noProductCount + 1

    # #3.
    # hisData3 = hisData  #复用HIS1数据
    # shiftSec = baseAlg.shiftSection(hisData3)
    # if (shiftSec.shape[0]<= 1):     noProduct[2] = 1    #只有一条班次记录，有可能未生产，也有可能本机未作换班操作
    # else:   noProduct[2] = 0
    #
    #4.
    ##2. 获取牌号班次信息
    tags2=[_shiftTag,_phTag]
    freq = "6000"  # 6s
    hisData2 = pre.loadHisDataByCyclic(tags2, freq, _beginTime, _endTime)
    if (hisData2.empty):
        return True, ["-201", "GeneralProductionalAlgorithm", "数据为空！"]
    if (hisData2.shape[1] < 3):        return True, ["-202", "GeneralProductionalAlgorithm",
                                                     "数据不完整，缺少列！列数：" + str(hisData2.shape[1])]
    nullCount = hisData2[hisData2.values[:, [1,2]] == 'NULL'].shape[0]
    naCount = hisData2[hisData2.values[:, [1, 2]] == ''].shape[0]
    if nullCount / hisData2.shape[0] > 0.1 or naCount / hisData2.shape[0]:
        noProduct[0] = 1  # Null值过多
        # noProductCount = noProductCount + 1
    else:
        hisData2.replace('NULL', '0', inplace=True)
        shiftPhSec1 = baseAlg.shiftPhSec(hisData2,tags2)
        if (shiftPhSec1.shape[0]<= 1):
            noProduct[1] = 1  # 只有一条记录，可能本天未生产
            noProductCount = noProductCount + 1

    ##3.获取产量数据
    tags3 = [_yieldsTag]
    freq = "6000"  # 6s
    hisData3 = pre.loadHisDataByCyclic(tags3, freq, _beginTime, _endTime,_type='Value')
    if (hisData3.empty):
        return True,["-301","GeneralProductionalAlgorithm","数据为空！"]
    ######曲烟数据存在NULL值，且为字符型，在此判断NULL比率，超过10%，则不进行后续计算     2019-7-26
    nullCount = hisData3[hisData3.values[:,1] == 'NULL'].shape[0]
    if (nullCount / hisData3.shape[0] > 0.1) :
        return True, ["-302", "GeneralProductionalAlgorithm", "NULL值过多！ NULL比率：" + str(nullCount / hisData3.shape[0])]
    hisData3.replace('NULL', '0', inplace=True) #用 0 填充NULL
    ###############################
    hisData3 = baseAlg.wavePorcess_fillBreakPoint(hisData3, _threshold/4)
    peeks = baseAlg.findPeaksBySci(hisData3)
    if peeks.size <= 0  :
        noProduct[2] = 1  #未找到拐点， 可能全天未开机
        noProductCount = noProductCount + 1
    if peeks.size < 1:
        return False, None
    #4 .判断是否大于临界值的个数,如果小于1000，则认为未开机
    lessThresholdCount = hisData3[hisData3['Product'].values.astype(np.float) >= _threshold]
    if lessThresholdCount.empty | lessThresholdCount.shape[0] < 1000:
        return False, None
    #4.2个以上判断条件都为可能未开机，则表示当天未开机
    if noProductCount  >= 2  :
        return False, None

    #5.
    pSec1 = baseAlg.wavePorcess_productionSection(hisData3, _threshold)
    pCompute1 = baseAlg.wavePorcess_productionCompute(pSec1)
    if pCompute1 is None :
        return False, None
    productionTable = baseAlg.wavePorcess_shiftPH(hisData2, pCompute1)
    productionTable1 = baseAlg.appenTotalRow(productionTable)
    return False,productionTable1