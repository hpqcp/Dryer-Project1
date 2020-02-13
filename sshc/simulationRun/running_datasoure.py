import datetime
import numpy as np
import pandas as pd
from pandas import DataFrame
import sshc.simulationRun.dataSource as ds
import sshc.simulationRun.batchProcess as bp
import sshc.modelPredict as mp
import sshc.timeAlignment as ta
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

class batch_sim_run():
    sshc_df = None
    batch_df_list = []
    batch_Num = 0

    def __init__(self, _category: object = '2400', _no: object = 0) -> object:
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
            df2 = df1.iloc[_startLoc:(_startLoc+_step),:]
        return df2

class batch_running_process():
    dfALL = DataFrame()
    dfList = []
    dfLast = DataFrame()
    importCount = 0
    lastLoc = 0
    moisturePointIndex = -1
    waterPointIndex = -1
    diff_list = []
    waterModel = None
    waterScalerXModel = None
    waterScalerYModel = None
    realYlist = []
    predictYList = []

    def __init__(self):
        self.lastLoc=0
        self.load_model('c:\\')

    def load_model(self,_path):
        model1 = mp.model_load(_path+'allX.m')
        ssxModel1 = mp.model_load(_path + 'allX-ss_x.m')
        ssyModel1 = mp.model_load(_path + 'allX-ss_y.m')

        self.waterModel = model1
        self.waterScalerXModel = ssxModel1
        self.waterScalerYModel = ssyModel1
        return

    def import_running_data(self,_df=None):
        if _df.empty:
            return  None
        self.dfList.append(_df)
        self.dfALL = pd.concat([self.dfALL,_df],axis=0)
        self.dfLast = _df
        self.importCount = self.importCount + 1
        #find moisture and water begin point,than compute diff_list
        if self.moisturePointIndex == -1 or self.waterPointIndex == -1 :
            self.get_key_timepoints()
            if self.moisturePointIndex > -1 and self.waterPointIndex > -1 :
                self.diff_list = self.__generate_timediff_list(_moistureValue=self.moisturePointIndex,_waterValue=self.waterPointIndex)
        #step predict
        df_p = DataFrame(self.dfALL.values[:,[3, 9, 6, 16, 15, 8]])
        scores,pVlues = self.__running_predict(df_p,self.waterModel,self.waterScalerXModel,self.waterScalerYModel,_newRowNum = _df.shape[0])
        # print(scores)
        self.lastLoc = self.lastLoc + _df.shape[0]
        return

    def get_key_timepoints(self):
        moistureTrigger = 1
        waterSetTrigger = 0.1
        moistureList = self.__find_trigger_index(self.dfALL.values[:,3],_triggervalue=moistureTrigger)
        if not(moistureList is None) :
            self.moisturePointIndex = moistureList[0][0]
        waterList = self.__find_trigger_index(self.dfALL.values[:, 9], _triggervalue=waterSetTrigger)
        if  not(waterList is None) :
            self.waterPointIndex = waterList[0][0]
        return

    def __generate_timediff_list(self,_moistureValue=0,_waterValue=0):
        diff1 = _moistureValue - _waterValue
        list1 = [0,diff1,diff1,diff1-4,diff1-13,diff1-10]
        return list1

    def __find_trigger_index(self, _series, _triggervalue=0, _than='>',_isReverse=False):
        if _isReverse :
            data = _series[::-1]
        else:
            data = _series
        if _than == '>':
            loc1 = np.argwhere(_series > _triggervalue)
        else:
            loc1 = np.argwhere(_series < _triggervalue)
        if len(loc1) == 0 :
            return None
        return loc1


    def __running_predict(self,_df=None,_model=None,_scalerX=None,_scalerY=None,_newRowNum = 0):
        model = self.waterModel
        scalerx = self.waterScalerXModel
        scalery = self.waterScalerYModel
        testY = _df.values[:,0]
        testX = _df.values[:,1:]
        pValues = self.__predict(model,testX,scalerx,scalery)
        self.realYlist.extend(testY[-_newRowNum:])
        self.predictYList.extend(pValues[-_newRowNum:])
        # print(str(len(testY)))
        # print(str(len(self.realYlist)))

        df_t = pd.DataFrame(pValues)
        df = DataFrame([testY, pValues]).T
        r2 = r2_score(df.values[:, 0], df.values[:, 1])
        mse = mean_squared_error(df.values[:, 0], df.values[:, 1])
        mae = mean_absolute_error(df.values[:, 0], df.values[:, 1])
        return {'R2': r2, 'MSE': mse, 'MAE': mae}, pValues

        return pValues

    def __predict(self,_model,_x,_scalerX,_scalerY):
        xTest1 = _scalerX.transform(_x)
        y_predict = _model.predict(xTest1)
        df_p = _scalerY.inverse_transform(y_predict) # 将标准化后的数据转换为原始数据。
        return df_p


if __name__ == "__main__":
    bsr1 = batch_sim_run(_no=0)
    df = bsr1.batch_df_list[1]
    dfL = len(df)
    n = 0
    step = 10
    brp1 = batch_running_process()
    while(True):
        df1 = bsr1.retrive_data_step(0,n,step)
        if df1.empty :
            break
        brp1.import_running_data(df1)
        # loc1 = brp1.get_all(df1.values[:,9],0,'>')
        a = DataFrame([brp1.realYlist, brp1.predictYList]).T

        n = n + step
    # df1 = bsr1.retrive_data_step(0, n, 3000)
    # brp1.import_running_data(df1)
    # diffList = brp1.diff_list
    #
    # bp1 = bp.batch(df1)
    # dfWT = bp1.retrive_wt_data(1,3,0,16,60)
    # # df1=dfWT[0]
    # # df2 = DataFrame(df1.values[:,[3,9,6,16,8,15]])
    # df3 = ta.time_align_transform(df1,diffList)
    #
    # score,sMean = mp.cross_score(df3.values[:,1:],df3.values[:,0].reshape(-1,1),10)

    print