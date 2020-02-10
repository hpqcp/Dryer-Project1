import datetime
import numpy as np
import pandas as pd
from pandas import DataFrame
import sshc.simulationRun.dataSource as ds
import sshc.simulationRun.batchProcess as bp

class batch_sim_run():
    sshc_df = None
    batch_df_list = []
    batch_Num = 0

    def __init__(self, _category='2400',_no=0):
        ds1 = ds.sshc_datasource(no=_no)
        self.sshc_df = ds1.sshc_df
        bp1 = bp.batch(self.sshc_df)
        self.batch_df_list = bp1.batch_splite_byTime(interval=24)#流量列为第1列，超过24秒不连续就判定为不为同一批
        self.batch_Num = len(self.batch_df_list)

    def retrive_data_step(self,_batchNo=0,_startLoc=0,_step=1):
        if _batchNo >= self.batch_Num :
            return DataFrame()
        df1 = self.batch_df_list[_batchNo]
        dfLen = df1.shape[0]
        if _startLoc+_step >= dfLen:
            df2 = df1.iloc[_startLoc:]
        else:
            df2 = df1.iloc[_startLoc:(_startLoc+_step)]
        return df2


class batch_running_process():
    dfALL = DataFrame()
    dfList = []
    dfLast = DataFrame()
    importCount = 0
    lastLoc = 0

    def __init__(self):
        self.lastLoc=0

    def import_running_data(self,_df=None):
        if _df.empty:
            return  None
        self.dfList.append(_df)
        self.dfALL = pd.concat([self.dfALL,_df],axis=0)
        self.dfLast = _df
        self.importCount = self.importCount + 1


        self.lastLoc = self.lastLoc + _df.shape[0]
        return 1



    def __find_trigger_index(self, _series, _triggervalue=0, _than='>'):
        if _than == '>':
            loc1 = np.where(_series > _triggervalue)
        else:
            loc1 = np.where(_series < _triggervalue)
        return loc1




if __name__ == "__main__":
    bsr1 = batch_sim_run(_no=0)
    df = bsr1.batch_df_list[0]
    dfL = len(df)
    n = 0
    brp1 = batch_running_process()
    while(True):
        df1 = bsr1.retrive_data_step(0,n,1000)
        if df1.empty :
            break
        brp1.import_running_data(df1)
        loc1 = brp1.get_all(df1.values[:,9],0,'>')
        n = n + 1000




    print