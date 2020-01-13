#
#
#

import pandas as pd

#
#
#return: 训练后模型 ， 标准化对象X ， 标准化对象y
def randomForest_model(_xTrain,_yTrain):
    from sklearn.preprocessing import StandardScaler
    from sklearn.ensemble import RandomForestRegressor

    # 训练数据和测试数据进行标准化处理
    ss_x = StandardScaler()
    x_train = ss_x.fit_transform(_xTrain)
    # x_test = ss_x.transform(_xTest)
    ss_y = StandardScaler()
    y_train = ss_y.fit_transform(_yTrain.reshape(-1, 1))
    # y_test = ss_y.transform(_yTest.reshape(-1, 1))
    #生成模型
    rf_model = RandomForestRegressor(n_jobs=-1)
    rf_model.fit(x_train, y_train)
    return rf_model,ss_x,ss_y

#
#
#
def randomForest_predict_score(_model,_ssx,_ssy,_xTest,_yTest,_isPlot=False):
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
    import chart.plot as plt

    # rfr,ss_x,ss_y = randomForest_model(_xTrain,_yTrain)
    xTest1 = _ssx.transform(_xTest)
    y_predict = _model.predict(xTest1)
    df_p = pd.DataFrame(_ssy.inverse_transform(y_predict))  # 将标准化后的数据转换为原始数据。
    # df_t = pd.DataFrame(_ssy.inverse_transform(_yTest))  # 将标准化后的数据转换为原始数据。
    df_t = pd.DataFrame(_yTest)
    df = pd.concat([df_t, df_p], axis=1)
    if _isPlot:
        plt.pairPlot(df)
    r2 = r2_score(df.values[:, 0], df.values[:, 1])
    mse = mean_squared_error(df.values[:, 0], df.values[:, 1])
    mae = mean_absolute_error(df.values[:, 0], df.values[:, 1])
    return {'R2':r2,'MSE':mse,'MAE':mae},df

#
#
#
def model_save(_model=None,_path=None):
    from sklearn.externals import joblib
    if _model==None or _path == None :
        raise Exception('模型或保存路径为空！')
    try:
        joblib.dump(_model,_path)
    except:
        raise Exception('模型保存错误！')
    else:
        return


#parm : 1.
#return : 1.得分数组 2.评价得分
def cross_score(_x,_y,_n):
    from sklearn import metrics
    from sklearn.preprocessing import StandardScaler
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import KFold
    from sklearn.model_selection import cross_val_score

    # 训练数据和测试数据进行标准化处理
    ss_x = StandardScaler()
    x1 = ss_x.fit_transform(_x)
    ss_y = StandardScaler()
    y1 = ss_y.fit_transform(_y.reshape(-1, 1))
    randomForest_model = RandomForestRegressor()
    kf = KFold(n_splits=_n, shuffle=True)
    score_ndarray = cross_val_score(randomForest_model, x1, y1, cv=kf)
    return score_ndarray,score_ndarray.mean()





#
#
#
def feature_selection_sshc(_x,_y):
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.feature_selection import SelectFromModel
    from sklearn.preprocessing import StandardScaler

    #训练数据和测试数据进行标准化处理
    ss_x = StandardScaler()
    x1 = ss_x.fit_transform(_x)
    ss_y = StandardScaler()
    y1 = ss_y.fit_transform(_y.reshape(-1, 1))
    clf = RandomForestRegressor()
    clf = clf.fit(x1, y1)
    return clf.feature_importances_  # 显示每一个特征的重要性指标，越大说明越重要，可以看出，第三第四两个特征比较重要


#


#
#
#
def searchCV(_x,_y,_testSize=0.25):
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import r2_score,mean_squared_error,mean_absolute_error
    import chart.plot as plt

    # 随机采样25%作为测试 75%作为训练
    # x_train, x_test, y_train, y_test = train_test_split(df_x, df_y, test_size=_testSize, random_state=33)
    # randomForest_predict(x_train,y_train,x_test,y_test)
#
#
#
if __name__ == "__main__":
    __spec__ = None
    import utils.excel2redis as rds
    import sshc.timeAlignment as timeAlign
    import numpy as np

    df = rds.getBatchData('4000-2019-10-08*', 1)
    df1 = pd.DataFrame(df.values[:, [3, 1, 6, 10, 11, 12, 13, 14, 17]])
    df2 = pd.DataFrame(df1,dtype=np.float)
    pointDiffList = [0,80,34,17,52,14,3,21,52]
    df3=timeAlign.time_align_transform(df2,pointDiffList)
    df_y = df3.values[:,0]
    df_x = df3.values[:,1:]
    #
    # model , StandardScaler_x,StandardScaler_y = randomForest_model(df_x,df_y)
    # model_save(model,'c://model1.m')
    # model_save(StandardScaler_x, 'c://ssx1.m')
    # model_save(StandardScaler_y, 'c://ssy1.m')
    from sklearn.externals import joblib
    model = joblib.load('c://model1.m')
    ssx = joblib.load('c://ssx1.m')
    ssy = joblib.load('c://ssy1.m')
    scores = randomForest_predict_score(model,ssx,ssy, df_x, df_y, _isPlot=True)
    # fi = model.feature_importances_




    # feature_selection_sshc(df_x,df_y)
    #scores,mean_score = cross_score(df_x,df_y,10)
    #searchCV(df_x,df_y,_testSize=0.2)

    # import chart.plot as plt
    # plt.pairPlot(DataFrame(df_y))

    # df_train_x = df3.values[200:1500,1:]
    # df_train_y = df3.values[200:1500, 0]
    # df_test_x = df3.values[200:399,1:]
    # df_test_y = df3.values[200:399, 0]
    # randomForest_predict(df_train_x,df_train_y,df_test_x,df_test_y)


    # time_align_fit(df1,[0,10,20,30,40,50,60,70,80,90,100])
    print
