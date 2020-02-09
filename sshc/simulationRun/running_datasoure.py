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


if __name__ == "__main__":
    bRun1 = batch_sim_run(_no=0)
    df = bRun1.batch_df_list[0]
    dfL = len(df)
    n = 0
    while(True):
        df1 = bRun1.retrive_data_step(0,n,1000)
        if df1.empty :
            break
        n = n + 1000




    print