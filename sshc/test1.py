import utils.excel2redis as rds
from pandas import DataFrame
import numpy as np
import pandas as pd


def multiPlot():
    df = rds.getBatchData('4000-2019-10-09*', 1)
    df1 = DataFrame(df.values[:, [0, 1, 2, 3, 4]])
    df1[0] = pd.to_datetime(df1[0])
    df1[1] = df1[1].astype('float64')
    df1[2] = df1[2].astype('float64')
    df1[3] = df1[3].astype('float64')
    df1[4] = df1[4].astype('float64')

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



if __name__ == "__main__":
    from sklearn.preprocessing import StandardScaler

    df = rds.getBatchData('4000-2019-10-09*', 1)
    df1 = DataFrame(df.values[:, [3,4,1,6,8,10]])
    df1[0] = df1[0].astype('float64')
    df1[1] = df1[1].astype('float64')
    df1[2] = df1[2].astype('float64')
    df1[3] = df1[3].astype('float64')
    df1[4] = df1[4].astype('float64')
    df1[5] = df1[5].astype('float64')
    # 数据标准化
    df2 = StandardScaler().fit_transform(df1)

    # 区间缩放，返回值为缩放到[0, 1]区间的数据
    from sklearn.preprocessing import MinMaxScaler
    df3=MinMaxScaler().fit_transform(df1)

    # 归一化，返回值为归一化后的数据
    from sklearn.preprocessing import Normalizer
    df4=Normalizer().fit_transform(df1)


    # 方差选择法，返回值为特征选择后的数据
    # 参数threshold为方差的阈值
    from sklearn.feature_selection import VarianceThreshold
    df5 = pd.DataFrame(df4)
    df_f1 = VarianceThreshold(threshold=0.01).fit_transform(df5)
    df_var = np.var(df4,axis=0) #计算各列方差

    #相关系数法
    from sklearn.feature_selection import SelectKBest
    from scipy.stats import pearsonr
    # 选择K个最好的特征，返回选择特征后的数据
    # 第一个参数为计算评估特征是否好的函数，该函数输入特征矩阵和目标向量，输出二元组（评分，P值）的数组，数组第i项为第i个特征的评分和P值。在此定义为计算相关系数
    # 参数k为选择的特征个数
    #SelectKBest(lambda X, Y: np.array(map(lambda x: pearsonr(x, Y), X.T)).T, k=2).fit_transform(df4[:,1:], df4[:,0])

    df_x = df4[:,1:]
    df_y = df1.values[:,0]
    #卡方检验
    from sklearn.feature_selection import SelectKBest
    from sklearn.feature_selection import chi2
    # 选择K个最好的特征，返回选择特征后的数据
    # SelectKBest(chi2, k=2).fit_transform(df_x, df_y)

    #RFE递归特征消除法
    from sklearn.feature_selection import RFE
    from sklearn.linear_model import LogisticRegression
    # 递归特征消除法，返回特征选择后的数据
    # 参数estimator为基模型
    # 参数n_features_to_select为选择的特征个数

    # from sklearn.datasets import load_iris
    # iris = load_iris()
    # a=iris.data
    # b=iris.target

    from sklearn.utils import shuffle
    X_shuffle, y_shuffle = shuffle(df_x, df_y.astype('int'))
    df_ref = RFE(estimator=LogisticRegression(), n_features_to_select=4).fit_transform(df_x, df_y)


    print('OK!')






