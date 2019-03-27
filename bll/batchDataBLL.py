from base.sql_help import Sql200
import datetime
from base.webSocketHelp import WebSocketHelp
from entity.hisEntity import HisEntity
import pandas as pd


class BatchDataBLL:

    # 通过批次 关键参数点 时间获取数据
    # bll.GetHisData("KY_MES_2018_5_24","WT",10,"Cyclic",6)
    def GetHisData(self, BatchByGroup, TimeType, Delay, SelectType, PL):
        PL = PL * 1000
        # 通过批次号获取批次信息
        BatchDf = self.GetBatchByGroupCode(BatchByGroup)
        # print(BatchDf)
        BatchID = BatchDf['BatchID'][0]
        # print(BatchID)
        # 通过批次信息获取关键参数点
        ImDf = self.GetImpParameter()
        # 数据时间
        ColDf = self.GetCollectionData(BatchID)
        DfList = []
        # 通过参数点，时间，属性获取his数据
        for ImIndex, ImRow in ImDf.iterrows():
            for ColIndex, ColRow in ColDf.iterrows():
                if ((ImRow["LineID"] == ColRow["LineID"]) &
                        (ImRow["StageID"] == ColRow["StageID"]) &
                        (ImRow["ProcessID"] == ColRow["ProcessID"]) &
                        (ImRow["ParameterID"] == ColRow["ParameterID"])):
                    TimeDf = self.GetBatchTime(ColRow["ParameterComputerID"])
                    MesLotStartTime = "";
                    MesLotEndTime = "";
                    TotalSampleStartTime = "";
                    TotalSampleEndTime = "";
                    for TimeIndex, TimeRow in TimeDf.iterrows():
                        IndexID = TimeRow['IndexID']
                        if (IndexID == "MesLotStartTime"):
                            MesLotStartTime = TimeRow["IndexValue"]
                        if (IndexID == "MesLotEndTime"):
                            MesLotEndTime = TimeRow["IndexValue"]
                        if (IndexID == "TotalSampleStartTime"):
                            TotalSampleStartTime = TimeRow["IndexValue"]
                        if (IndexID == "TotalSampleEndTime"):
                            TotalSampleEndTime = TimeRow["IndexValue"]
                    startTime = "";
                    endTime = "";
                    if (TimeType != "WT"):
                        startTime = MesLotStartTime;
                        endTime = MesLotEndTime;
                    else:
                        startTime = TotalSampleStartTime;
                        endTime = TotalSampleEndTime;
                    # 时间延长
                    delta = datetime.timedelta(seconds=Delay)

                    startTimeDt = datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S')
                    endTimeDt = datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S')

                    startTimeDt = startTimeDt - delta
                    endTimeDt = endTimeDt + delta

                    startTime = startTimeDt.strftime("%Y-%m-%d %H:%M:%S")
                    endTime = endTimeDt.strftime("%Y-%m-%d %H:%M:%S")

                    jsonStr = ImRow[
                                  "GroupParameterTag"] + "||" + startTime + "||" + endTime + "||" + SelectType + "||" + str(
                        PL);

                    hisDf = WebSocketHelp.WebSocketJson("ws://10.130.65.207:8181/HisWeb", jsonStr)

                    if (hisDf is not None):
                        if (len(hisDf) > 0):
                            HisEy = HisEntity(ImRow["LineName"], ImRow["StageName"], ImRow["ProcessName"],
                                              ImRow["ParameterName"], hisDf)
                            DfList.append(HisEy)
        # 数据整理
        # print(DfList)
        AllDf = None
        columnList = []
        maxCountList = []
        zidian = {}
        for _Df in DfList:
            columnList.append(_Df.ParameterName + "时间")
            columnList.append(_Df.ParameterName)
            maxCountList.append(len(_Df.HisDf))
            zidian.update({_Df.ParameterName + "时间": ""})
            zidian.update({_Df.ParameterName: ""})

        maxCount = max(maxCountList)
        AllDf = pd.DataFrame(columns=columnList)
        add_data = pd.Series(zidian)
        for i in range(maxCount):
            AllDf = AllDf.append(add_data, ignore_index=True)

        m = 0
        for _Df in DfList:
            j = 0
            for _index, row in _Df.HisDf.iterrows():
                AllDf.loc[j, _Df.ParameterName + "时间"] = row["DateTime"]
                AllDf.loc[j, _Df.ParameterName] = row["Value"]
                j = j + 1
        print(AllDf)
        return AllDf

    # 通过集团批次号 时间类型 延时时间s 查询方式 频率s 获取数据（时间对齐）
    def GetHisDataAlign(self, BatchByGroup, TimeType, DelayStart, DelayEnd, SelectType, PL):
        PL = PL * 1000
        # 通过批次号获取批次信息
        BatchDf = self.GetBatchByGroupCode(BatchByGroup)
        # print(BatchDf)
        BatchID = BatchDf['BatchID'][0]
        # print(BatchID)
        # 通过批次信息获取关键参数点
        ImDf = self.GetImpParameter()
        # 数据时间
        ColDf = self.GetCollectionData(BatchID)
        DfList = []

        StartTimeList = []
        EndTimeList = []

        # 通过参数点，时间，属性获取his数据
        for ImIndex, ImRow in ImDf.iterrows():
            for ColIndex, ColRow in ColDf.iterrows():
                if ((ImRow["LineID"] == ColRow["LineID"]) &
                        (ImRow["StageID"] == ColRow["StageID"]) &
                        (ImRow["ProcessID"] == ColRow["ProcessID"]) &
                        (ImRow["ParameterID"] == ColRow["ParameterID"])):
                    TimeDf = self.GetBatchTime(ColRow["ParameterComputerID"])
                    MesLotStartTime = "";
                    MesLotEndTime = "";
                    TotalSampleStartTime = "";
                    TotalSampleEndTime = "";
                    for TimeIndex, TimeRow in TimeDf.iterrows():
                        IndexID = TimeRow['IndexID']
                        if (IndexID == "MesLotStartTime"):
                            MesLotStartTime = TimeRow["IndexValue"]
                        if (IndexID == "MesLotEndTime"):
                            MesLotEndTime = TimeRow["IndexValue"]
                        if (IndexID == "TotalSampleStartTime"):
                            TotalSampleStartTime = TimeRow["IndexValue"]
                        if (IndexID == "TotalSampleEndTime"):
                            TotalSampleEndTime = TimeRow["IndexValue"]
                    startTime = "";
                    endTime = "";
                    if (TimeType != "WT"):
                        startTime = MesLotStartTime;
                        endTime = MesLotEndTime;
                    else:
                        startTime = TotalSampleStartTime;
                        endTime = TotalSampleEndTime;
                    # 时间延长
                    deltaStar = datetime.timedelta(seconds=DelayStart)
                    deltaEnd = datetime.timedelta(seconds=DelayEnd)

                    startTimeDt = datetime.datetime.strptime(startTime, '%Y-%m-%d %H:%M:%S')
                    endTimeDt = datetime.datetime.strptime(endTime, '%Y-%m-%d %H:%M:%S')

                    startTimeDt = startTimeDt - deltaStar
                    endTimeDt = endTimeDt + deltaEnd

                    StartTimeList.append(startTimeDt)
                    EndTimeList.append(endTimeDt)
                    startTime = startTimeDt.strftime("%Y-%m-%d %H:%M:%S")
                    endTime = endTimeDt.strftime("%Y-%m-%d %H:%M:%S")

                    HisEy = HisEntity(ImRow["LineName"], ImRow["StageName"], ImRow["ProcessName"],
                                      ImRow["ParameterName"], None)
                    HisEy.TagName = ImRow["GroupParameterTag"]
                    DfList.append(HisEy)

        # 最小开始时间（首参数开始时间）
        MinTime = min(StartTimeList)
        # 最大结束时间
        MaxTime = max(EndTimeList)

        startMinTime = MinTime.strftime("%Y-%m-%d %H:%M:%S")
        endMaxTime = MaxTime.strftime("%Y-%m-%d %H:%M:%S")
        tagNameStr = ",".join([x.TagName for x in DfList])
        jsonStr = tagNameStr + "||" + startMinTime + "||" + endMaxTime + "||" + SelectType + "||" + str(PL);

        hisDf = WebSocketHelp.WebSocketJson("ws://10.130.65.207:8181/HisWeb", jsonStr)

        hisGroupDf = hisDf.groupby(['TagName'])
        for _hisEy in DfList:
            for name, group in hisGroupDf:
                if (_hisEy.TagName == name):
                    _hisEy.HisDf = group

        # 数据整理
        AllDf = pd.DataFrame()
        for _hisEy in DfList:
            # _hisDataTime = _hisEy.HisDf["DateTime"]
            # _hisValue = _hisEy.HisDf["Value"]
            _hisDataTime = _hisEy.HisDf.pop('DateTime').tolist()
            _hisValue = _hisEy.HisDf.pop('Value').tolist()

            AllDf[_hisEy.ParameterName + "时间"] = _hisDataTime
            AllDf[_hisEy.ParameterName] = _hisValue
        # print(DfList)
        AllDf.to_excel(BatchByGroup + ".xlsx")
        print(AllDf)
        return AllDf

    # 通过集团批次号获取批次信息
    def GetBatchByGroupCode(self, GroupBatchCode):
        ms = Sql200()
        df = ms.ExecQuery(
            "select * from V_SilkBatch where 1=1 and CraftType='006cfd06-c513-4f7c-a9b5-80e3218bff02' and GroupBatchCode='" + GroupBatchCode + "'")
        return df

    # 获取关键参数
    def GetImpParameter(self):
        parName = "'切叶丝含水率','叶丝增温增湿工艺流量','叶丝增温增湿蒸汽流量','薄板干燥热风温度','薄板干燥Ⅰ区筒壁温度','薄板干燥Ⅱ区筒壁温度','薄板干燥出料温度','薄板干燥出料含水率','叶丝冷却出料含水率'"
        ms = Sql200()
        df = ms.ExecQuery(
            "select ID,FactoryCode,FactoryName,ZoneCode,ZoneName,BrandCode,BrandName,LineID,LineName,StageID,StageName,ProcessID,ProcessName,ParameterID,ParameterName," +
            "GroupParameterTag,FactoryParameterTag,ZoneSort,LineSort,StageSort,ProcessSort,ParameterSort " +
            "from V_FactoryToParameterRelation " +
            "where 1 = 1 and GroupParameterTag is not null and FactoryParameterTag is not null " +
            "and FactoryCode = '1100' and ZoneName = '制丝' " +
            "and BrandName = '云烟(紫)模组一' and LineName = 'C线' and StageName = '切丝烘丝加香段' " +
            "and ParameterName in (" + parName + ") " +
            "order by ZoneSort,LineSort,StageSort,ProcessSort,ParameterSort")
        return df

    # 获取参数点计算信息
    def GetCollectionData(self, BatchID):
        # "0019de43-1a5c-4463-ac2a-ba64f1ff18a0"
        ms = Sql200()
        df = ms.ExecQuery("SELECT a.* FROM V_ParameterCollectionDataInfoReal a " +
                          "inner join T_SilkBatchSample b on a.BatchID= b.BatchID and a.BatchSampleID= b.BatchSampleID " +
                          "WHERE 1=1 and a.BatchID= '" + BatchID + "' and b.BackCol2=0")
        return df

    # 获取参数点计算信息
    def GetBatchTime(self, ParameterComputerID):
        # "0019de43-1a5c-4463-ac2a-ba64f1ff18a0"
        ms = Sql200()
        df = ms.ExecQuery(
            "SELECT a.IndexComputerID, a.IndexValue, a.IndexID, a.ParameterComputerID, c.IndexName 'IndexName', c.Countnumber, c.Sort, c.FormulaCode " +
            "FROM T_SilkIndexComputer a " +
            "LEFT JOIN T_SilkParameterComputer b ON a.ParameterComputerID= b.ParameterComputerID " +
            "left JOIN B_FactoryJudgeFunctionDetail c ON c.IndexCode= a.IndexID AND c.FunctionID= b.FunctionID " +
            "WHERE 1=1 and IndexID in ('MesLotStartTime','TotalSampleStartTime','TotalSampleEndTime','MesLotEndTime') " +
            "and b.ParameterComputerID='" + ParameterComputerID + "' " +
            "AND c.FunctionID IS NOT NULL ORDER BY c.Sort asc,c.IsIndex DESC")
        return df

if __name__ == "__main__":
    bll = BatchDataBLL()
    # df = bll.GetCollectionData("0019de43-1a5c-4463-ac2a-ba64f1ff18a0")
    # print(df)
    # bll.GetHisData("KY_MES_2018_5_24","WT",10,"Cyclic",6)

    bll.GetHisDataAlign("KY_MES_2018_5_43", "YX", 900, 900, "Cyclic", 1)
