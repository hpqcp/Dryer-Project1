import pandas as pd
import numpy as np
from pandas import  DataFrame

#特征重要度排序
def feature_importances(_df):
    import sshc.modelPredict as mp
    xTrain = _df.values[:, 1:]
    yTrain = _df.values[:, 0]
    model, _, _ = mp.randomForest_model(xTrain, yTrain)
    fi = model.feature_importances_
    return fi



if __name__ == "__main__":
    import utils.excel2redis as rds

# #1.按天进行特征重要度排序
#     dateStr = ['03','04','05','06','07','08','09','10','11','12','14','15','16','17']
#     rtlList = list()
#     for i in range(0,len(dateStr),1):
#         keyStr = '2400-2019-11-'+dateStr[i]+'*'
#         df = rds.getBatchData(keyStr, 2)
#         # df1 = DataFrame(df.values[:, [3, 1, 6, 10, 11, 12, 13, 14, 17]])
#         df1 = DataFrame(df.values[:, [3,1,6,9,10,11,12,13,14,15,16]])
#         df2 = DataFrame(df1, dtype=np.float)
#         fi = feature_importances(df2)
#         rtlList.append(fi)
#     dfRtl = DataFrame(rtlList)

# #2.全数据重要度排序
#     keyStr = '2400-2019-11-*'
#     df = rds.getBatchData(keyStr, 2)
#     df1 = DataFrame(df.values[:, [3,1,6,9,10,11,12,13,14,15,16]])
#     df2 = DataFrame(df1, dtype=np.float)
#     fi = feature_importances(df2)

#3.对各特征变量的X1.。。Xn相对于Y的距离初步测算
    import sshc.timeAlignment as ta
    dateStr = ['03','04','05','06','07','08','09','10','11','12','14','15','16','17']
    listDF = list()
    for i in range(0,len(dateStr),1):
        df = rds.getBatchData('2400-2019-11-'+dateStr[i]+'*', 2)
        df1 = DataFrame(df.values[:, [3,1,6,9,10,11,12,13,14,15,16]])
        df2 = DataFrame(df1, dtype=np.float)
        listDF.append(df2)
    aList = list()
    for i in range(0,101,10):
        aList.append(i)
    ret = ta.multi_pre_align_train(listDF,aList)


    print