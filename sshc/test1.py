import utils.excel2redis as rds
from pandas import DataFrame
import numpy as np
import pandas as pd


def multiPlot():
    df = rds.getBatchData('4000-2019-10-07*', 1)
    df1 = DataFrame(df.values[:, [0, 1, 2, 3, 4]])
    df1[0] = pd.to_datetime(df1[0])
    df1[1] = df1[1].astype('float64')
    df1[2] = df1[2].astype('float64')
    df1[3] = df1[3].astype('float64')
    df1[4] = df1[4].astype('float64')

    import chart.plot as cplt
    cplt.singlePlot(df1)
    return

    import matplotlib.pyplot as pyplot
    fig, ax1 = pyplot.subplots()
    pyplot.ylim(0, 4200)
    ax2 = ax1.twinx()  # 做镜像处理
    pyplot.ylim(0, 4200)
    ax3 = ax1.twinx()
    ax4 = ax1.twinx()
    ax1.plot(df1[0], df1[1], 'g-')
    ax2.plot(df1[0], df1[2], 'y--')
    ax3.plot(df1[0], df1[3], 'r--')
    ax4.plot(df1[0], df1[4], 'b--')
    pyplot.show()
    print('1')

#各参数时间对齐算法
def time_align(_date,_align):
    from sklearn.preprocessing import StandardScaler
    df = rds.getBatchData('4000-' + _date + '*', 1)
    df1 = DataFrame(df.values[:, [3, 18]])
    for x in range(0, df1.shape[1], 1):
        df1[x] = df1[x].astype('float64')
    df2 = df1[1].shift(_align)
    df2=pd.concat([df1[0],df2],axis=1)
    df2=df2.dropna(axis=0,how='any')
    df_x = df2.values[:, 1]
    df_y = df2.values[:, 0]

    from sklearn.model_selection import KFold
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, GradientBoostingRegressor
    from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

    # 随机采样25%作为测试 75%作为训练
    x_train, x_test, y_train, y_test = train_test_split(df_x, df_y, test_size=0.25, random_state=33)
    # 3 训练数据和测试数据进行标准化处理
    ss_x = StandardScaler()
    x_train = ss_x.fit_transform(x_train.reshape(-1,1))
    x_test = ss_x.transform(x_test.reshape(-1,1))
    ss_y = StandardScaler()
    y_train = ss_y.fit_transform(y_train.reshape(-1, 1))
    y_test = ss_y.transform(y_test.reshape(-1, 1))
    # 4 三种集成回归模型进行训练和预测
    # 随机森林回归
    rfr = RandomForestRegressor()
    # 训练
    rfr.fit(x_train, y_train)
    # 预测 保存预测结果
    rfr_y_predict = rfr.predict(x_test)
    # # 极端随机森林回归
    # etr = ExtraTreesRegressor()
    # etr.fit(x_train, y_train)
    # etr_y_predict = rfr.predict(x_test)
    # # 梯度提升回归
    # gbr = GradientBoostingRegressor()
    # gbr.fit(x_train, y_train)
    # gbr_y_predict = rfr.predict(x_test)
    # 5 模型评估
    # print("随机森林回归的默认评估值为:", rfr.score(x_test, y_test))
    # print("随机森林回归的R_squared值为:", r2_score(y_test, rfr_y_predict))
    # print("随机森林回归的均方误差为:", mean_squared_error(ss_y.inverse_transform(y_test),ss_y.inverse_transform(rfr_y_predict)))
    # print("随机森林回归的平均绝对误差为:", mean_absolute_error(ss_y.inverse_transform(y_test),ss_y.inverse_transform(rfr_y_predict)))
    # # 极端随机森林回归模型评估
    # print("极端随机森林回归的默认评估值为:", etr.score(x_test, y_test))
    # print("极端随机森林回归的R_squared值为:", r2_score(y_test, gbr_y_predict))
    # print("极端随机森林回归的均方误差为:", mean_squared_error(ss_y.inverse_transform(y_test),ss_y.inverse_transform(gbr_y_predict)))
    # print("极端随机森林回归的平均绝对误差为:", mean_absolute_error(ss_y.inverse_transform(y_test),ss_y.inverse_transform(gbr_y_predict)))
    # # 梯度提升回归模型评估
    # print("梯度提升回归回归的默认评估值为:", gbr.score(x_test, y_test))
    # print("梯度提升回归回归的R_squared值为:", r2_score(y_test, etr_y_predict))
    # print("梯度提升回归回归的均方误差为:", mean_squared_error(ss_y.inverse_transform(y_test),ss_y.inverse_transform(etr_y_predict)))
    # print("梯度提升回归回归的平均绝对误差为:", mean_absolute_error(ss_y.inverse_transform(y_test),ss_y.inverse_transform(etr_y_predict)))
    return rfr.score(x_test, y_test)


def feature_selection_sshc(_date):
    from sklearn.preprocessing import StandardScaler

    df = rds.getBatchData('4000-'+_date+'*', 1)
    # df1 = DataFrame(df.values[:, [3, 1, 4, 6, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18]])
    df1 = DataFrame(df.values[:, [3, 1, 6, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18]])
    # names = ['ck_sf', 'rk_ll', 'ck_wd', 'rf_wd', 'hf_wd', 'jsl', 'zq_ll', 'zss_ll', 'zqqy_wd', 'zqqy_yl', 'zpzq_yl',
    #          'sy_yl', \
    #          'yskq_yl', 'zsszq_yl']
    for x in range(0, 12, 1):
        df1[x] = df1[x].astype('float64')
    # df1.columns = names

    # 数据标准化
    df2 = StandardScaler().fit_transform(df1)

    # 区间缩放，返回值为缩放到[0, 1]区间的数据
    from sklearn.preprocessing import MinMaxScaler
    df3 = MinMaxScaler().fit_transform(df1)

    # 归一化，返回值为归一化后的数据
    from sklearn.preprocessing import Normalizer
    df4 = Normalizer().fit_transform(df1)

    # 方差选择法，返回值为特征选择后的数据
    # 参数threshold为方差的阈值
    from sklearn.feature_selection import VarianceThreshold
    df5 = pd.DataFrame(df4)
    df_f1 = VarianceThreshold(threshold=0.01).fit_transform(df5)
    df_var = np.var(df4, axis=0)  # 计算各列方差

    # 相关系数法
    from sklearn.feature_selection import SelectKBest
    from scipy.stats import pearsonr
    # 选择K个最好的特征，返回选择特征后的数据
    # 第一个参数为计算评估特征是否好的函数，该函数输入特征矩阵和目标向量，输出二元组（评分，P值）的数组，数组第i项为第i个特征的评分和P值。在此定义为计算相关系数
    # 参数k为选择的特征个数
    # SelectKBest(lambda X, Y: np.array(map(lambda x: pearsonr(x, Y), X.T)).T, k=2).fit_transform(df4[:,1:], df4[:,0])

    df_x = df4[:, 1:]
    df_y = df1.values[:, 0]
    # 卡方检验
    from sklearn.feature_selection import SelectKBest
    from sklearn.feature_selection import chi2
    # 选择K个最好的特征，返回选择特征后的数据
    # SelectKBest(chi2, k=2).fit_transform(df_x, df_y)

    # RFE递归特征消除法
    from sklearn.feature_selection import RFE
    from sklearn.linear_model import LogisticRegression
    # 递归特征消除法，返回特征选择后的数据
    # 参数estimator为基模型
    # 参数n_features_to_select为选择的特征个数

    # from sklearn.datasets import load_iris
    # iris = load_iris()
    # a=iris.data
    # b=iris.target

    # from sklearn.utils import shuffle
    # X_shuffle, y_shuffle = shuffle(df_x, df_y.astype('int'))
    # df_ref = RFE(estimator=LogisticRegression(), n_features_to_select=4).fit_transform(df_x, df_y)

    from sklearn.ensemble import RandomForestRegressor
    from sklearn.feature_selection import SelectFromModel

    X, y = df_x, df_y
    # X.shape
    # (150, 4)
    clf = RandomForestRegressor()
    clf = clf.fit(X, y)
    a = clf.feature_importances_  # 显示每一个特征的重要性指标，越大说明越重要，可以看出，第三第四两个特征比较重要
    # [ 0.04505659  0.01056346  0.45428591  0.49009404]
    model = SelectFromModel(clf, prefit=True)
    X_new = model.transform(X)
    # X_new.shape
    # (150, 2)
    return a
    # print(a)


if __name__ == "__main__":
    # multiPlot()
    # exit()

    ###
    dates = ['2019-10-07','2019-10-08','2019-10-09','2019-10-10','2019-10-11','2019-10-12',\
                '2019-10-13','2019-10-14','2019-10-15','2019-10-16','2019-10-17']
    # result = DataFrame()
    # for i in range(0,len(dates),1):
    #     a = DataFrame(feature_selection_sshc(dates[i]))
    #     result=pd.concat([result,a],axis=1)
    # print('a')

    ####
    #aligns=[range(0, 100,10)]
    scores = []
    result = DataFrame()
    for j in range(0,len(dates),1):
        for i in range(70,90,1):
            res = time_align(dates[0],i)
            # print(str(i)+":"+str(res))
            scores.append(res)
        s = DataFrame(scores)
        result = pd.concat([result, s], axis=1)
        scores.clear()
    print('a')






