import gb.baseAlgorithm as baseAlg
import gb.preProcess as pre
import pandas as pd
import numpy as np


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
    shiftPhSec1 = baseAlg.shiftPhSec(hisData2,tags2)
    if (shiftPhSec1.shape[0]<= 1):
        noProduct[1] = 1  # 只有一条记录，可能本天未生产
        noProductCount = noProductCount + 1

    ##3.获取产量数据
    tags3 = [_yieldsTag]
    freq = "6000"  # 6s
    hisData3 = pre.loadHisDataByCyclic(tags3, freq, _beginTime, _endTime)
    if (hisData3.empty):
        return True,["-301","GeneralProductionalAlgorithm","数据为空！"]
    hisData3 = baseAlg.wavePorcess_fillBreakPoint(hisData3, _threshold/4)
    peeks = baseAlg.findPeaksBySci(hisData3)
    if peeks.size <= 0  :
        noProduct[2] = 1  #未找到拐点， 可能全天未开机
        noProductCount = noProductCount + 1
    #4.2个以上判断条件都为可能未开机，则表示当天未开机
    if noProductCount  >= 2 :
        return False,None

    #5.
    pSec1 = baseAlg.wavePorcess_productionSection(hisData3, _threshold)
    pCompute1 = baseAlg.wavePorcess_productionCompute(pSec1)
    productionTable = baseAlg.wavePorcess_shiftPH(hisData2, pCompute1)
    productionTable1 = baseAlg.appenTotalRow(productionTable)
    return False,productionTable1

#
def dayProduction2Excel(_excelData,_strSet,_excelWriter,_startTime,_endTime,):
    setData = _excelData.iloc[jbData['set'].values == _strSet,:]
    sTime = _startTime
    eTime = _endTime
    write = _excelWriter
    for i in range(0,setData.shape[0],1) :
        bcTag = setData['bc'].values[i]
        phTag = setData['ph'].values[i]
        clTag = setData['cl'].values[i]
        sdTag = setData['sd'].values[i]
        # a = setData['bc'].isna().where(True)
        # if  str(bcTag).isspace():
        #     jjProduction = pd.DataFrame(['数采点地址为空！'],columns=['描述'])
        #     xbProduction = jjProduction
        #     tbProduction = jjProduction
        #     jjHis,xbHis,tbHis = None,None,None
        #     break;
        if setData['unit'].values[i] == '卷接' :
            threshold = 5000
            res,jjProduction = GeneralProductionalAlgorithm(bcTag,phTag,clTag,sdTag,sTime,eTime,threshold)
            if res :
                jjProduction = pd.DataFrame(jjProduction)
                jjHis == None
            elif jjProduction is None :
                jjProduction = pd.DataFrame(['本日未开机！'],columns=['描述'])
                jjHis = pre.loadHisDataByCyclic([clTag], '6000', sTime, eTime)
            else:
                jjHis = pre.loadHisDataByCyclic([clTag], '6000', sTime, eTime)
        elif setData['unit'].values[i] == '小包' :
            threshold = 300
            res,xbProduction = GeneralProductionalAlgorithm(bcTag,phTag,clTag,sdTag,sTime,eTime,threshold)
            if res :
                xbProduction = pd.DataFrame(xbProduction)
                xbHis == None
            elif xbProduction is None :
                xbProduction = pd.DataFrame(['本日未开机！'],columns=['描述'])
                xbHis = pre.loadHisDataByCyclic([clTag], '6000', sTime, eTime)
            else:
                xbHis = pre.loadHisDataByCyclic([clTag], '6000', sTime, eTime)
        elif setData['unit'].values[i] == '条包' :
            threshold = 50
            res,tbProduction = GeneralProductionalAlgorithm(bcTag,phTag,clTag,sdTag,sTime,eTime,threshold)
            if res :
                tbProduction = pd.DataFrame(tbProduction)
                tbHis == None
            elif tbProduction is None :
                tbProduction = pd.DataFrame(['本日未开机！'],columns=['描述'])
                tbHis = pre.loadHisDataByCyclic([clTag], '6000', sTime, eTime)
            else:
                tbHis = pre.loadHisDataByCyclic([clTag], '6000', sTime, eTime)
    jjProduction.to_excel(write, sheet_name=_strSet)
    xbProduction.to_excel(write, startrow=15, sheet_name=_strSet)
    tbProduction.to_excel(write, startrow=30, sheet_name=_strSet)
    sheet1 = write.book.sheetnames[_strSet]
    if jjHis is not None :
        pre.plot2Excel(jjHis, "d://jb//1//1.png", sheet1, 0, 14)
    if xbHis is not None:
        pre.plot2Excel(xbHis, "d://jb//1//2.png", sheet1, 16, 14)
    if tbHis is not None:
        pre.plot2Excel(tbHis, "d://jb//1//3.png", sheet1, 31, 14)
    return write


if __name__ == "__main__":
    # str1 ="MES2RTDATA.U_Maker_11020030009.DC_BC"
    # str3 ="MES2RTDATA.U_Maker_11020030009.DC_SJCL"
    # str4 ="MES2RTDATA.U_Maker_11020030009.DC_YXSD"
    # str2 ="MES2RTDATA.U_Maker_11020030009.DC_PH"
    # a = GeneralProductionalAlgorithm(str1,str2,str3,str4,"2019-07-01 06:00:00","2019-07-02 06:00:00",5000)
    # print(a)

    # jbData = pd.read_excel("d://jb//jb.xlsx",sheet_name='ky',header=0)
    # # setData = jbData.iloc[jbData['set'].values == '1#',:]
    # sTime = "2019-07-01 06:00:00"
    # eTime = "2019-07-02 06:00:00"
    # # for i in range(0,setData.shape[0],1) :
    # #     bcTag = setData['bc'].values[i]
    # #     phTag = setData['ph'].values[i]
    # #     clTag = setData['cl'].values[i]
    # #     sdTag = setData['sd'].values[i]
    # #     if setData['unit'].values[i] == '卷接' :
    # #         threshold = 5000
    # #         jjProduction = GeneralProductionalAlgorithm(bcTag,phTag,clTag,sdTag,sTime,eTime,threshold)
    # #         jjHis = pre.loadHisDataByCyclic([clTag], '6000', sTime, eTime)
    # #
    # #     elif setData['unit'].values[i] == '小包' :
    # #         threshold = 300
    # #         xbProduction = GeneralProductionalAlgorithm(bcTag,phTag,clTag,sdTag,sTime,eTime,threshold)
    # #         xbHis = pre.loadHisDataByCyclic([clTag], '6000', sTime, eTime)
    # #     elif setData['unit'].values[i] == '条包' :
    # #         threshold = 50
    # #         tbProduction = GeneralProductionalAlgorithm(bcTag,phTag,clTag,sdTag,sTime,eTime,threshold)
    # #         tbHis = pre.loadHisDataByCyclic([clTag], '6000', sTime, eTime)
    #
    #
    # write = pd.ExcelWriter("d://jb//1.xlsx",engine='xlsxwriter')
    # write1 = dayProduction2Excel(jbData,'1#',write,sTime,eTime)
    # # jjProduction[1].to_excel(write, sheet_name="1#")
    # # xbProduction[1].to_excel(write, startrow=15, sheet_name="1#")
    # # tbProduction[1].to_excel(write, startrow=30, sheet_name="1#")
    # # sheet1 = write.book.sheetnames['1#']
    # # pre.plot2Excel(jjHis, "d://jb//1//1.png", sheet1, 0, 14)
    # # pre.plot2Excel(xbHis, "d://jb//1//2.png", sheet1, 16, 14)
    # # pre.plot2Excel(tbHis, "d://jb//1//3.png", sheet1, 31, 14)
    # # write.save()
    # #
    # # book = load_workbook(write.path)
    # # write.book = book
    # # sheet1 = book['1#']
    import datetime
    jbData = pd.read_excel("d://jb//jb.xlsx", sheet_name='ky', header=0)
    # setData = jbData.iloc[jbData['set'].values == '1#',:]
    sTime = "2019-07-02 06:00:00"
    eTime = "2019-07-03 06:00:00"

    setData = jbData.drop_duplicates(['set'])
    setData1 = setData.dropna(axis = 0 ,how='any')
    setData = setData1.reset_index(drop=True)
    for i in range(0,setData.shape[0],1):
        print('Begin process : '+str(i)+'   timestamp : '+str(datetime.datetime.now()))
        setNo = setData['set'].values[i]
        write = pd.ExcelWriter("d://jb//2//"+setNo+".xlsx", engine='xlsxwriter')
        write = dayProduction2Excel(jbData,setNo,write,sTime,eTime)
        print('Complete : ' + str(i)+'   timestamp : '+str(datetime.datetime.now()))
    # write1 = dayProduction2Excel(jbData, '2#', write1, sTime, eTime)
        write.save()
        write.close()

    print('')