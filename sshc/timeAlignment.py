#
#
#

from pandas import DataFrame
import numpy as np
import pandas as pd




#
#传入源dataframe，输出对齐后df，有NA值的行都drop
#_df : dataframe , 源数据df,要求全部列均为float型
#_pointDifferList , list , 每一列参照第一列需要平移的量（int）,不需要平移输入0;大小为_df 相同
def time_align_transform(_df,_pointDifferList):
    df1 = [_df[x].shift(_pointDifferList[x]) for x in range(0,len(_pointDifferList),1)]
    df2 = DataFrame(df1).T
    df3=df2.dropna(axis=0,how='any')
    return df3

#
#
#
def time_align_fit(_df,_pointDifferList):
    import itertools
    lens = len(_pointDifferList)
    ll =list()
    for item in itertools.product([0,1,2],repeat=3):
        ll.append(list(item))
    for i in range(0,len(ll),1):
        a = ll[i]
        df1 = time_align_transform(_df, ll[i])
        df_y = df1.values[:, 0]
        df_x = df1.values[:, 1:]


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
    a = clf.feature_importances_  # 显示每一个特征的重要性指标，越大说明越重要，可以看出，第三第四两个特征比较重要
    model = SelectFromModel(clf, prefit=True)
    X_new = model.transform(x1)

#
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
def searchCV(_x,_y,_testSize=0.25):
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import r2_score,mean_squared_error,mean_absolute_error
    import chart.plot as plt

    # 随机采样25%作为测试 75%作为训练
    x_train, x_test, y_train, y_test = train_test_split(df_x, df_y, test_size=_testSize, random_state=33)
    randomForest_predict(x_train,y_train,x_test,y_test)

#
#
#
def randomForest_predict(_xTrain,_yTrain,_xTest,_yTest):
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
    import chart.plot as plt

    # 随机采样25%作为测试 75%作为训练
    x_train = _xTrain
    x_test = _xTest
    y_train = _yTrain
    y_test = _yTest
    # 3 训练数据和测试数据进行标准化处理
    ss_x = StandardScaler()
    x_train = ss_x.fit_transform(x_train)
    x_test = ss_x.transform(x_test)
    ss_y = StandardScaler()
    y_train = ss_y.fit_transform(y_train.reshape(-1, 1))
    y_test = ss_y.transform(y_test.reshape(-1, 1))
    rfr = RandomForestRegressor()
    rfr.fit(x_train, y_train)
    y_predict = rfr.predict(x_test)
    df_p = DataFrame(ss_y.inverse_transform(y_predict))  # 将标准化后的数据转换为原始数据。
    df_t = DataFrame(ss_y.inverse_transform(y_test))  # 将标准化后的数据转换为原始数据。
    df = pd.concat([df_t, df_p], axis=1)
    plt.pairPlot(df)
    print('R2:' + str(r2_score(df.values[:, 0], df.values[:, 1])))
    print('MSE:' + str(mean_squared_error(df.values[:, 0], df.values[:, 1])))
    print('MAE:' + str(mean_absolute_error(df.values[:, 0], df.values[:, 1])))
    print



if __name__ == "__main__":

    import utils.excel2redis as rds
    df = rds.getBatchData('4000-2019-10-09*', 1)
    df1 = DataFrame(df.values[:, [3, 1, 6, 10, 11, 12, 13, 14, 17]])
    df2 = DataFrame(df1,dtype=np.float)
    pointDiffList = [0,80,34,17,52,14,3,21,52]
    df3=time_align_transform(df2,pointDiffList)
    df_y = df3.values[:,0]
    df_x = df3.values[:,1:]
    # feature_selection_sshc(df_x,df_y)
    # scores,mean_score = cross_score(df_x,df_y,10)
    #searchCV(df_x,df_y,_testSize=0.2)

    # import chart.plot as plt
    # plt.pairPlot(DataFrame(df_y))

    # df_train_x = df3.values[200:1500,1:]
    # df_train_y = df3.values[200:1500, 0]
    # df_test_x = df3.values[200:399,1:]
    # df_test_y = df3.values[200:399, 0]
    # randomForest_predict(df_train_x,df_train_y,df_test_x,df_test_y)

    ll =list()
    import itertools
    for item in itertools.product([0,1,2,1],repeat=4):
        ll.append(list(item))
    # l = list(itertools.permutations([0,1,2],3))
    # a = itertools.permutations([1,2,3,4],4)
    print