import gb.baseAlgorithm as baseAlg
import gb.preProcess as pre
import pandas as pd
import numpy as np
import os
import datetime



#简要计算卷包机、提升机
#_threshold:临界值
def SimpleProductionalAlgorithm(_yieldsTag,_beginTime,_endTime,_threshold):
    ##3.获取产量数据
    tags3 = [_yieldsTag]
    freq = "6000"  # 6s
    hisData3 = pre.loadHisDataByCyclic(tags3, freq, _beginTime, _endTime, _type='Value')
    if (hisData3.empty):
        return True, ["-301", "GeneralProductionalAlgorithm", "数据为空！"]
    # ######曲烟数据存在NULL值，且为字符型，在此判断NULL比率，超过10%，则不进行后续计算     2019-7-26
    # nullCount = hisData3[hisData3.values[:, 1] == 'NULL'].shape[0]
    # if (nullCount / hisData3.shape[0] > 0.1):
    #     return True, ["-302", "GeneralProductionalAlgorithm", "NULL值过多！ NULL比率：" + str(nullCount / hisData3.shape[0])]
    # hisData3.replace('NULL', '0', inplace=True)  # 用 0 填充NULL
    # ###############################
    hisData3 = baseAlg.wavePorcess_fillBreakPoint(hisData3, _threshold / 4)
    peeks = baseAlg.findPeaksBySci(hisData3)
    if peeks.size < 1:
        return False, None
    # 4 .判断是否大于临界值的个数,如果小于1000，则认为未开机
    lessThresholdCount = hisData3[hisData3['Product'].values.astype(np.float) >= _threshold]
    if lessThresholdCount.empty | lessThresholdCount.shape[0] < 1000:
        return False, None

    # 5.
    pSec1 = baseAlg.wavePorcess_productionSection(hisData3, _threshold)
    pCompute1 = baseAlg.wavePorcess_productionCompute(pSec1)
    if pCompute1 is None:
        return False, None
    # productionTable = baseAlg.wavePorcess_shiftPH(hisData2, pCompute1)
    # productionTable1 = baseAlg.appenTotalRow(productionTable)
    return False, pCompute1





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
        noProductCount = noProductCount + 1
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
        noProductCount = noProductCount + 1
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

#
def dayProduction2Excel(_excelData,_strSet,_excelWriter,_startTime,_endTime,_path):
    jjHis = None
    xbHis = None
    tbHis = None
    setData = _excelData.iloc[_excelData['set'].values == _strSet,:]
    sTime = _startTime
    eTime = _endTime
    write = _excelWriter
    for i in range(0,setData.shape[0],1) :
        bcTag = setData['bc'].values[i]
        phTag = setData['ph'].values[i]
        clTag = setData['cl'].values[i]
        sdTag = setData['sd'].values[i]

        if setData['unit'].values[i] == '卷接' :
            threshold = 5000
            jjTitle = _strSet + ' ' + setData['unit'].values[i] + ' ' + sTime + ' - ' + eTime + ' 频率:6s' + '\n' + clTag
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
            threshold = 500
            xbTitle = _strSet + ' ' + setData['unit'].values[i] + ' ' + sTime + ' - ' + eTime + ' 频率:6s' + '\n' + clTag
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
            threshold = 100
            tbTitle = _strSet + ' ' + setData['unit'].values[i] + ' ' + sTime + ' - ' + eTime + ' 频率:6s' + '\n' + clTag
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
        pre.plot2Excel(jjHis, _path+"1.png", sheet1, 0, 14,_title=jjTitle)
    if xbHis is not None:
        pre.plot2Excel(xbHis, _path+"2.png", sheet1, 16, 14,_title=xbTitle)
    if tbHis is not None:
        pre.plot2Excel(tbHis, _path+"3.png", sheet1, 31, 14,_title=tbTitle)
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
    strDir = "d://jb//"

    # jbData = pd.read_excel(strDir+"hy.xlsx", sheet_name='Sheet1', header=0)
    # # setData = jbData.iloc[jbData['set'].values == '1#',:]
    # setData = jbData.drop_duplicates(['set'])
    # setData1 = setData.dropna(axis=0, how='any')
    # setData = setData1.reset_index(drop=True)
    # strDates = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19']
    # #strDates = [ '15','16','17','18','19','15', '16', '17', '18', '19']
    # # for j in range(0,len(strDates),1):
    # for j in range(2, setData.shape[0],1):
    #     setNo = setData['set'].values[j]
    #     # if not os.path.exists(strDir + strDates[j]) :
    #     if not os.path.exists(strDir + setNo):
    #         os.mkdir(strDir + setNo)
    #     # for i in range(1,2,1):#setData.shape[0],1):
    #     for i in range(1, len(strDates),1):
    #         sTime = "2019-07-" + strDates[i] + " 04:00:00"
    #         eTime = "2019-07-" + str(int(strDates[i]) + 1) + " 08:30:00"
    #         print('Begin process : '+str(datetime.datetime.now())+'    Set : '+setNo+'    Date : '+strDates[i])
    #         # setNo = setData['set'].values[i]
    #         write = pd.ExcelWriter(strDir+setNo+"//"+strDates[i]+".xlsx", engine='xlsxwriter')
    #         write = dayProduction2Excel(jbData,setNo,write,sTime,eTime)
    #         print('     Complete : '+str(datetime.datetime.now()))
    #     # write1 = dayProduction2Excel(jbData, '2#', write1, sTime, eTime)
    #         write.save()
    #         write.close()


    a = SimpleProductionalAlgorithm('XJYC.U_Packer_1500001070.DC_TYSSCL','2019-8-8 02:00:00','2019-8-9 2:35:00',50)


    print('')