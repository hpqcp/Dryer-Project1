#稳态处理函数
##用于处理数据的稳态和非稳态
#
import pandas as pd
import numpy as np
from pandas import  DataFrame

if __name__ == "__main__":
    import utils.excel2redis as rds
    df = rds.getBatchData('4000-2019-10-09*', 1)
    df1 = DataFrame(df.values[:, [3, 1, 6, 10, 11, 12, 13, 14, 17]])
    df2 = DataFrame(df1, dtype=np.float)
    # pointDiffList = [0,80,34,17,52,14,3,21,52]
    # df3=time_align_transform(df2,pointDiffList)
    # df_y = df3.values[:,0]
    # df_x = df3.values[:,1:]

    from sklearn.cluster import KMeans
    import matplotlib.pyplot as plt

    X = df2.values[:,0].reshape(-1, 1)
    model = KMeans(n_clusters=2, random_state=9).fit(X)
    y_pred = model.predict(X)
    plt.scatter(range(0,len(X),1),X, c=y_pred)
    plt.show()
