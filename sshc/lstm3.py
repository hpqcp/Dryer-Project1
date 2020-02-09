import pandas as pd
import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from sklearn.preprocessing import MinMaxScaler
from keras.callbacks import ReduceLROnPlateau
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

#
class timeSeries_self_model():
    tsData = None
    tsModel = None
    tsScaler = None
    __timesteps = None   #用前面几步用于预测
    __predict_steps = None  #预测后面几步


    def __init__(self, _tsData=None,_model=None):
        self.tsData = _tsData
        self.tsModel = _model

    def __create_dataset(self,dataset, timesteps=36, predict_steps=6):  # 构造数据集
        datax = []  # 构造x
        datay = []  # 构造y
        for each in range(len(dataset) - timesteps - predict_steps):
            x = dataset[each:each + timesteps, 0]
            y = dataset[each + timesteps:each + timesteps + predict_steps, 0]
            datax.append(x)
            datay.append(y)
        return datax, datay  # np.array(datax),np.array(datay)


    def __data_pre_process(self,_data,_timesteps,_predict_steps,_scaler=None):
        data = _data
        if _scaler == None:
            scaler = MinMaxScaler(feature_range=(0, 1))# 构造train and predict
            self.tsScaler = scaler
        else:
            scaler = _scaler
        data = scaler.fit_transform(data)
        train = data.copy()
        timesteps = _timesteps  # 构造x，为72个数据,表示每次用前72个数据作为一段
        predict_steps = _predict_steps  # 构造y，为12个数据，表示用后12个数据作为一段
        # length = 288  # 预测多步，预测288个数据，每次预测12个，想想要怎么构造预测才能满足288？
        trainx, trainy = self.__create_dataset(train, timesteps, predict_steps)
        trainx = np.array(trainx)
        trainy = np.array(trainy)
        # 变换
        trainx = np.reshape(trainx, (trainx.shape[0], timesteps, 1))  # 变换shape,以满足keras
        return trainx,trainy,scaler

    def fit(self,_timesteps,_predict_steps,_savePath=''):# lstm training
        reduce_lr = ReduceLROnPlateau(monitor='val_loss', patience=5, mode='auto')
        trainx, trainy, scaler = self.__data_pre_process(self.tsData,_timesteps,_predict_steps)
        model = Sequential()
        model.add(LSTM(128, input_shape=(_timesteps, 1), return_sequences=True))
        model.add(Dropout(0.5))
        model.add(LSTM(128, return_sequences=True))
        # model.add(Dropout(0.3))
        model.add(LSTM(64, return_sequences=False))
        # model.add(Dropout(0.2))
        model.add(Dense(_predict_steps))
        model.compile(loss="mean_squared_error", optimizer="adam",metrics=['mae', 'acc'])
        model.fit(trainx, trainy, epochs=400, batch_size=64,verbose=2,callbacks=[reduce_lr])
        if _savePath != '':
            model.save(_savePath)
        self.tsModel = model
        self.__timesteps = _timesteps
        self.__predict_steps = _predict_steps
        return model

    def predict_step(self,_testData=None,_timesteps=0, _scaler=None):
        model = self.tsModel
        if model == None:
            return None
        if _scaler == None:
            scaler1 = self.tsScaler
        else:
            scaler1 = _scaler
        datap = _testData
        lens = len(datap)
        if lens < _timesteps :
            return None
        testx = datap[-_timesteps:]
        testx = scaler1.transform(testx)
        testx = np.array([testx])
        testx = np.reshape(testx, (testx.shape[0], _timesteps, 1))  # 变换shape,以满足keras
        lstm_predict = model.predict(testx)
        lstm_predict = scaler1.inverse_transform(lstm_predict)
        return lstm_predict

    def predict_score(self,_testData=None,_timesteps=0,_scaler=None):
        datap = _testData
        lens = len(datap)
        if lens < _timesteps +1:
            return None
        YList = []
        PList = []
        for i in range(_timesteps,lens-1):
            testX = datap[(i - _timesteps):i]
            testY = datap[i+1]
            testP = self.predict_step(testX,_timesteps,_scaler)
            YList.extend(testY)
            PList.extend(testP)
        a = DataFrame(YList)
        b = DataFrame(PList)
        c = pd.concat([a,b],axis=1)
        r2 = r2_score(YList, PList)
        mse = mean_squared_error(YList, PList)
        mae = mean_absolute_error(YList, PList)
        import chart.plot as cplot
        cplot.pairPlot(c)
        print

    def predict_cycle(self,_testData=None,_timesteps=0,_scaler=None,_cycleStep = 20 , _greaterThan = None , _lessThan = None):
        datap = _testData
        lens = len(datap)
        if lens < _timesteps:
            return None
        # datap = datap[-_timesteps:]
        PList = []
        cycleNum = 0
        while(1==1):
            testX = datap[-_timesteps:]
            testP = self.predict_step(testX, _timesteps, _scaler)
            PList.extend(testP)
            datap = np.append(datap,[testP]).reshape(-1,1)
            if _greaterThan!=None :
                if float(testP)>=_greaterThan:
                    break
            else:
                if float(testP)<=_lessThan:
                    break
            cycleNum = cycleNum + 1
            if cycleNum >= _cycleStep:
                break
        return PList



    def predict(self,_testData=None,_timesteps=0, _predict_steps=0,_scaler=None):
        model = self.tsModel
        if model == None :
            return None
        if _scaler == None :
            scaler1 = self.tsScaler
        else:
            scaler1 = _scaler
        datap = _testData
        testx, testy, scaler = self.__data_pre_process(datap,_timesteps, _predict_steps,scaler1)

        length = len(datap)
        # 因为每次只能预测12个数据，但是我要预测288个数据，所以采用的就是循环预测的思路。每次预测的12个数据，添加到数据集中充当预测x，然后在预测新的12个y，再添加到预测x列表中，如此往复。最终预测出288个点。
        predict_xlist = []  # 添加预测x列表
        predict_y = []  # 添加预测y列表
        predict_xlist.extend(datap[datap.shape[0] - _timesteps:datap.shape[0],
                             0].tolist())  # 已经存在的最后timesteps个数据添加进列表，预测新值(比如已经有的数据从1,2,3到288。现在要预测后面的数据，所以将216到288的72个数据添加到列表中，预测新的值即288以后的数据）
        while len(predict_y) < length:
            predictx = np.array(predict_xlist[
                                -_timesteps:])  # 从最新的predict_xlist取出timesteps个数据，预测新的predict_steps个数据（因为每次预测的y会添加到predict_xlist列表中，为了预测将来的值，所以每次构造的x要取这个列表中最后的timesteps个数据词啊性）
            predictx = np.reshape(predictx, (1, _timesteps, 1))  # 变换格式，适应LSTM模型
            # print("predictx"),print(predictx),print(predictx.shape)
            # 预测新值
            lstm_predict = model.predict(predictx)
            # predict_list.append(train_predict)#新值y添加进列表，做x
            # 滚动预测
            # print("lstm_predict"),print(lstm_predict[0])
            predict_xlist.extend(lstm_predict[0])  # 将新预测出来的predict_steps个数据，加入predict_xlist列表，用于下次预测
            # invert
            lstm_predict = self.tsScaler.inverse_transform(lstm_predict)
            predict_y.extend(lstm_predict[0])  # 预测的结果y，每次预测的12个数据，添加进去，直到预测288个为止
            # print("xlist", predict_xlist, len(predict_xlist))
            # print(lstm_predict, len(lstm_predict))
            # print(predict_y, len(predict_y))
        # error
        y_ture = datap[:]
        a = DataFrame(y_ture, predict_y)
        train_score = np.sqrt(mean_squared_error(y_ture, predict_y[:length]))
        print("train score RMSE: %.2f" % train_score)
        y_predict = pd.DataFrame(predict_y, columns=["predict"])
        y_predict.to_csv("y_predict_LSTM.csv", index=False)
        # plot
        # plt.plot(y_ture,c="g")
        # plt.plot(predict_y, c="r")
        # plt.show()


if __name__ == "__main__":
    from pandas import DataFrame
    import sshc.simulationRun.dataSource as ds
    import sshc.simulationRun.batchProcess as bp
    from sklearn.externals import joblib

    # ds1 = ds.sshc_datasource(no=0).sshc_df
    # bp1 = bp.batch(df=ds1)
    # dfList = bp1.batch_splite_byTime(interval=24)
    # df = dfList[0]
    # # dateStr = ['03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '14', '15', '16', '17']
    # # keyStr = '2400-2019-11-12*'  # +dateStr[i]+'*'
    # # df = rds.getBatchData(keyStr, 2)
    # df1 = DataFrame(df.values[:, [9]])
    # df2 = DataFrame(df1, dtype=np.float)
    # dataset = df2.values[::-1]
    # dataset = dataset[-65:]
    # dataset = dataset.astype('float32')
    #
    #
    # ts = timeSeries_self_model(_tsData=dataset)
    # ts.fit(3,1,_savePath='c://lstm3.m')
    # scaler1 = ts.tsScaler
    # joblib.dump(scaler1,'c://lstm3-scaler.m')

    model1 = load_model('c://lstm3.m')
    ts1 = timeSeries_self_model(_model=model1)
    scaler1 = joblib.load('c://lstm3-scaler.m')
    # datap = ts1.predict_step(_testData=dataset[-13:-3],_timesteps=10,_scaler=scaler1)
    # ts1.predict_score(_testData=dataset,_timesteps=10,_scaler=scaler1)
    ds2 = ds.sshc_datasource(no=0).sshc_df
    bp2 = bp.batch(df=ds2)
    dfList = bp2.batch_splite_byTime(interval=24)
    df = dfList[0]
    df1 = DataFrame(df.values[:, [9]])
    df2 = DataFrame(df1, dtype=np.float)
    dataset = df2.values[::-1]
    dataset = dataset[:-8]
    dataset = dataset.astype('float32')
    ts1.predict_cycle(_testData=dataset,_timesteps=3,_scaler=scaler1,_cycleStep=100,_lessThan=0)

    print


# #读取数据
# data = pd.read_csv("./data/data_complete.csv")[['sump']]
# dataf = data.values[0:-288]
# def create_dataset(dataset, timesteps=36,predict_size=6):#构造数据集
#     datax=[]#构造x
#     datay=[]#构造y
#     for each in range(len(dataset)-timesteps - predict_steps):
#         x = dataset[each:each+timesteps,0]
#         y = dataset[each+timesteps:each+timesteps+predict_steps,0]
#         datax.append(x)
#         datay.append(y)
#     return datax, datay#np.array(datax),np.array(datay)
# #构造train and predict
# scaler = MinMaxScaler(feature_range=(0,1))
# dataf = scaler.fit_transform(dataf)
# train = dataf.copy()
# timesteps = 72#构造x，为72个数据,表示每次用前72个数据作为一段
# predict_steps = 12#构造y，为12个数据，表示用后12个数据作为一段
# length = 288#预测多步，预测288个数据，每次预测12个，想想要怎么构造预测才能满足288？
# trainx, trainy = create_dataset(train, timesteps, predict_steps)
# trainx = np.array(trainx)
# trainy = np.array(trainy)
#
# #变换
# trainx = np.reshape(trainx,(trainx.shape[0],timesteps,1))#变换shape,以满足keras
# #lstm training
# model = Sequential()
# model.add(LSTM(128,input_shape=(timesteps,1),return_sequences= True))
# model.add(Dropout(0.5))
# model.add(LSTM(128,return_sequences=True))
# #model.add(Dropout(0.3))
# model.add(LSTM(64,return_sequences=False))
# #model.add(Dropout(0.2))
# model.add(Dense(predict_steps))
# model.compile(loss="mean_squared_error",optimizer="adam")
# model.fit(trainx,trainy, epochs= 100, batch_size=512)
# #predict
# #因为每次只能预测12个数据，但是我要预测288个数据，所以采用的就是循环预测的思路。每次预测的12个数据，添加到数据集中充当预测x，然后在预测新的12个y，再添加到预测x列表中，如此往复。最终预测出288个点。
# predict_xlist = []#添加预测x列表
# predict_y = []#添加预测y列表
# predict_xlist.extend(dataf[dataf.shape[0]-timesteps:dataf.shape[0],0].tolist())#已经存在的最后timesteps个数据添加进列表，预测新值(比如已经有的数据从1,2,3到288。现在要预测后面的数据，所以将216到288的72个数据添加到列表中，预测新的值即288以后的数据）
# while len(predict_y) < length:
#     predictx = np.array(predict_xlist[-timesteps:])#从最新的predict_xlist取出timesteps个数据，预测新的predict_steps个数据（因为每次预测的y会添加到predict_xlist列表中，为了预测将来的值，所以每次构造的x要取这个列表中最后的timesteps个数据词啊性）
#     predictx = np.reshape(predictx,(1,timesteps,1))#变换格式，适应LSTM模型
#     #print("predictx"),print(predictx),print(predictx.shape)
#     #预测新值
#     lstm_predict = model.predict(predictx)
#     #predict_list.append(train_predict)#新值y添加进列表，做x
#     #滚动预测
#     #print("lstm_predict"),print(lstm_predict[0])
#     predict_xlist.extend(lstm_predict[0])#将新预测出来的predict_steps个数据，加入predict_xlist列表，用于下次预测
#     # invert
#     lstm_predict = scaler.inverse_transform(lstm_predict)
#     predict_y.extend(lstm_predict[0])#预测的结果y，每次预测的12个数据，添加进去，直到预测288个为止
#     #print("xlist", predict_xlist, len(predict_xlist))
#     #print(lstm_predict, len(lstm_predict))
#     #print(predict_y, len(predict_y))
# #error
#
# y_ture = np.array(data.values[-288:])
# train_score = np.sqrt(mean_squared_error(y_ture,predict_y))
# print("train score RMSE: %.2f"% train_score)
# y_predict = pd.DataFrame(predict_y,columns=["predict"])
# y_predict.to_csv("y_predict_LSTM.csv",index=False)
# #plot
# #plt.plot(y_ture,c="g")
# #plt.plot(predict_y, c="r")
# #plt.show()