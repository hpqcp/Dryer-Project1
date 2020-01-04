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
#
#
def

if __name__ == "__main__":

    import utils.excel2redis as rds
    df = rds.getBatchData('4000-2019-10-*', 1)
    df1 = DataFrame(df.values[:, [3, 1, 6, 10, 11, 12, 13, 14, 17]])
    df2 = DataFrame(df1,dtype=np.float)
    pointDiffList = [0,80,34,17,52,14,3,21,52]
    df3=time_align_transform(df2,pointDiffList)

    df_y = df3.values[:,0]
    df_x = df3.values[:,1:]
    feature_selection_sshc(df_x,df_y)
    print