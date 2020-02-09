import numpy as np
import pandas as pd

class batch():
    __df = pd.DataFrame()
    spliteDFList = []
    wholeDFList = []
    wtDFList = []
    headDFList = [] #料头
    tailDFList = [] #料尾
    spliteLocList = []
    wholeLocList = []
    wtLocList = []


    def __init__(self, df=None):
        self.__df = df


    def batch_splite_byTime(self,interval = 1):#通过时间戳判断批次是否连续
        if self.__df.empty:
            return None
        timeSeries = pd.to_datetime(self.__df[0]).values
        sList = list()
        sLoc = 0
        eLoc = 0
        for i in range(1,len(timeSeries),1):
            itv = (timeSeries[i] - timeSeries[i-1]).astype('timedelta64[s]').astype(np.int)
            if (itv > interval):
                eLoc = i
                sList.append([sLoc,eLoc-1])
                sLoc = i
        eLoc = i
        sList.append([sLoc, eLoc])
        self.spliteLocList = sList
        self.spliteDFList = [self.__df.iloc[sList[i][0]:(sList[i][1]+1),:] for i in range(len(sList))]
        return self.spliteDFList

    def batch_whole(self,_flowCol=0,_triggerValue=0):#通过流量判断批次开始结束,流量大于或小于0进行判断
        dfList = self.spliteDFList
        retList = []
        locList=[]
        startIndex = 0
        for df in dfList:
            seriesFlow = df.values[:,_flowCol]
            data1 = seriesFlow[:int(len(seriesFlow) / 2)]
            data2 = seriesFlow[len(data1):]
            data2 = data2[::-1]  # 数据方向反转
            # 获取第一个大于触发值的Loc
            loc1 = np.where(data1 > _triggerValue)
            loc2 = np.where(data2 > _triggerValue)
            loc1 = loc1[0][0]
            loc2 = loc2[0][0]
            sLoc = loc1
            eLoc = len(seriesFlow) - loc2
            locList.append([startIndex + sLoc,startIndex + eLoc-1])
            retList.append(df.iloc[sLoc:eLoc,:])
            startIndex = startIndex + len(seriesFlow)
        self.wholeLocList = locList
        self.wholeDFList = retList
        return retList

    def batch_wt(self,_moistureCol,_triggerValue=0,_delay=0):#稳态截取，以水分到达临界值，并延时N个点
        dfList = self.wholeDFList
        locList = []
        retList = []
        startIndex = 0
        headList = [] #料头
        tailList = []  # 料尾
        for df in dfList:
            seriesMoisture = df.values[:,_moistureCol]
            data1 = seriesMoisture[:int(len(seriesMoisture) / 2)]
            data2 = seriesMoisture[len(data1):]
            data2 = data2[::-1]  # 数据方向反转
            # 获取第一个大于触发值的Loc
            loc1 = np.where(data1 > _triggerValue)
            loc2 = np.where(data2 > _triggerValue)
            loc1 = loc1[0][0] + _delay
            loc2 = loc2[0][0] + _delay
            sLoc = loc1
            eLoc = len(seriesMoisture) - loc2
            locList.append([startIndex + sLoc,startIndex + eLoc-1])
            retList.append(df.iloc[sLoc:eLoc,:])
            headList.append(df.iloc[0:sLoc,:])
            tailList.append(df.iloc[eLoc:, :])
            startIndex = startIndex + len(seriesMoisture)

        self.wtLocList = locList
        self.wtDFList = retList
        self.headDFList = headList
        self.tailDFList = tailList
        return retList

    def retrive_wt_data(self,_flowCol,_moistureCol,_triggerFlow=0,_triggerMoisture=0,_delay=0):
        bsList = self.batch_splite_byTime(interval=24)
        bwList = self.batch_whole(_flowCol,_triggerFlow)
        bwtList = self.batch_wt(_moistureCol=_moistureCol,_triggerValue= _triggerMoisture,_delay=_delay)
        return bwtList



if __name__ == "__main__":
    from sshc.simulationRun.dataSource import sshc_datasource
    for i in range(13,14):
        ds = sshc_datasource(no=i)
        df1 = ds.sshc_df
        batch1 = batch(df1)
        # rtList = b.batch_splite_byTime(interval=6)
        # ret = b.batch_whole(2,0)
        # mRet = b.batch_wt(1,16,60)
        ret = batch1.retrive_wt_data(1,3,0,16,60)
        h = batch1.headDFList
        t = batch1.tailDFList
        print
    print
