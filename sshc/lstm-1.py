import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = ""

import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import pandas as pd
from pandas import DataFrame
import os
from keras.models import Sequential, load_model
from sklearn.preprocessing import MinMaxScaler
import utils.excel2redis as rds
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

def create_dataset(dataset, look_back,predict_step=1):
#这里的look_back与timestep相同
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back-1-predict_step):
        a = dataset[i:(i+look_back)]
        dataX.append(a)
        b=dataset[(i + look_back):(i + look_back + predict_step)]
        dataY.append(b)
    return np.array(dataX),np.array(dataY)

#逐点预测
def pointwise_predict():
    model = load_model('c://lstm1.m')


    return


if __name__ == '__main__':
    dateStr = ['03','04','05','06','07','08','09','10','11','12','14','15','16','17']
    keyStr = '2400-2019-11-*'#+dateStr[i]+'*'
    df = rds.getBatchData(keyStr, 2)
    df1 = DataFrame(df.values[:, [3]])
    df2 = DataFrame(df1, dtype=np.float)
    # dataframe = pd.read_csv('./international-airline-passengers.csv', usecols=[1], engine='python', skipfooter=3)
    dataset = df2.values
    # 将整型变为float
    dataset = dataset.astype('float32')
    #归一化 在下一步会讲解
    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset = scaler.fit_transform(dataset)

    train_size = int(len(dataset) * 0.7)
    trainlist = dataset[:train_size]
    testlist = dataset[train_size:]

    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset = scaler.fit_transform(dataset)


    #训练数据太少 look_back并不能过大
    look_back = 10
    trainX,trainY  = create_dataset(trainlist,look_back,predict_step=10)
    testX,testY = create_dataset(testlist,look_back,predict_step=10)

    trainX = np.reshape(trainX, (trainX.shape[0], trainX.shape[1], 1))
    testX = np.reshape(testX, (testX.shape[0], testX.shape[1] ,1 ))
    trainY = np.reshape(trainY, (trainY.shape[0], trainY.shape[1], 1))
    testY = np.reshape(testY, (testY.shape[0], testY.shape[1], 1))

    # create and fit the LSTM network
    model = Sequential()
    model.add(LSTM(3, input_shape=(None,1),return_sequences=True))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam',metrics=['mae', 'acc'])
    model.fit(trainX, trainY, epochs=100, batch_size=1024, verbose=2)
    # model.save('c://lstm1.m')
    # make predictions

    #model = load_model(os.path.join("DATA","Test" + ".h5"))
    trainPredict = model.predict(trainX)
    testPredict = model.predict(testX)




    #反归一化
    trainPredict = scaler.inverse_transform(trainPredict)
    trainY = scaler.inverse_transform(trainY)
    testPredict = scaler.inverse_transform(testPredict)
    testY = scaler.inverse_transform(testY)

    r2 = r2_score(testY, testPredict)
    mse = mean_squared_error(testY, testPredict)
    mae = mean_absolute_error(testY, testPredict)

    r2_all = r2_score(trainY, trainPredict)
    mse_all = mean_squared_error(trainY, trainPredict)
    mae_all = mean_absolute_error(trainY, trainPredict)

    plt.plot(trainY)
    plt.plot(trainPredict[1:])
    plt.show()
    plt.plot(testY)
    plt.plot(testPredict[1:])
    plt.show()