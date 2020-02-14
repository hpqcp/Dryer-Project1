import datetime
import numpy as np
import pandas as pd
from pandas import DataFrame
import utils.excel2redis as rds

class sshc_datasource():
    # sshc_df = None

    def __init__(self, category='2400',no=0):
        self.sshc_df = self.__load_sshc_data(category,no)

    def __load_sshc_data(self,_category,_no):
        if _category=='2400':
            catStr = '2400-2019-11-'
            redisDB = 2
        dateStr = ['03','04','05','06','07','08','09','10','11','12','14','15','16','17']
        keyStr = catStr+dateStr[_no]+'*'
        df = rds.getBatchData(keyStr, redisDB)
        # df1 = DataFrame(df.values[:, [0, 3, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]])
        return df

    def retrive_data(self,location=0,step=-1):
        if self.sshc_df.empty:
            return None
        else:
            if step==-1:
                lens = self.sshc_df.shape[0]
                return self.sshc_df.values[location:lens, :]
            else:
                return self.sshc_df.values[location:(location+step),:]

if __name__ == "__main__":
    ds = sshc_datasource()
    df1 = ds.sshc_df
    for i in range(1):
        print(ds.retrive_data(location=i,step=-1))