import pandas as pd
import numpy as np
from pandas import  DataFrame
import sys
sys.path.append("..")


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
#     # for i in range(0,len(dateStr),1):
#     for i in range(0, len(dateStr), 1):
#         keyStr = '2400-2019-11-'+dateStr[i]+'*'
#         df = rds.getBatchData(keyStr, 2)
#         # df1 = DataFrame(df.values[:, [3, 1, 6, 10, 11, 12, 13, 14, 17]])
#         # df1 = DataFrame(df.values[:, [3,1,6,9,10,11,12,13,14,15,16]])
#         df1 = DataFrame(df.values[:, [3, 1, 6, 8,10, 11,  14, 16]]) #删除特征12，13，15后重新进行重要度排序
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

# #3.对按不同天数据，各特征变量的X1.。。Xn相对于Y的距离初步测算
#     import sshc.timeAlignment as ta
#     dateStr = ['03','04','05','06','07','08','09','10','11','12','14','15','16','17']
#     listDF = list()
#     for i in range(0,len(dateStr),1):
#         df = rds.getBatchData('2400-2019-11-'+dateStr[i]+'*', 2)
#         df1 = DataFrame(df.values[:, [3,1,6,9,10,11,12,13,14,15,16]])
#         df2 = DataFrame(df1, dtype=np.float)
#         listDF.append(df2)
#     aList = list()
#     for i in range(0,101,1):
#         aList.append(i)
#     ret = ta.multi_pre_align_train(listDF,aList)
#     ret.to_csv('/home/preat1.csv')

# # 4.11月全数据数据，各特征变量的X1.。。Xn相对于Y的距离初步测算
#     import sshc.timeAlignment as ta
#     dateStr = ['03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '14', '15', '16', '17']
#     listDF = list()
#     df = rds.getBatchData('2400-2019-11-*', 2)
#     df1 = DataFrame(df.values[:, [3, 1, 6, 9, 10, 11, 12, 13, 14, 15, 16]])
#     df2 = DataFrame(df1, dtype=np.float)
#     listDF.append(df2)
#     aList = list()
#     for i in range(0, 101, 1):
#         aList.append(i)
#     ret = ta.multi_pre_align_train(listDF, aList)
#     ret.to_csv('/home/preat_all.csv')

#临时 1.
    # csvData = pd.read_csv('c://preat1.csv')
    # # dg = csvData.groupby('round')
    # # df = DataFrame()
    # # for key in dg.groups:
    # #     data_p = dg.get_group(key)
    # #     # df = pd.concat([df,data_p],axis=1)
    # #     a = pd.pivot_table(data_p,values=['shifts','score'], columns='x')
    # #     print
    # a = csvData.loc[ (csvData['x'] == 1) & (csvData['score'] > 0)]

# # 5.各特征相关性分析
#     import seaborn as sns
#     from matplotlib import pyplot as plt
#
#     dateStr = ['03','04','05','06','07','08','09','10','11','12','14','15','16','17']
#     rtlList = list()
#     # for i in range(0,len(dateStr),1):
#     for i in range(0, len(dateStr), 1):
#         keyStr = '2400-2019-11-'+dateStr[i]+'*'
#         # keyStr = '2400-2019-11-*'
#         df = rds.getBatchData(keyStr, 2)
#         df1 = DataFrame(df.values[:, [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]])
#         df2 = DataFrame(df1, dtype=np.float)
#         plt.figure(figsize=(16, 12))
#         sns.heatmap(df2.corr(), annot=True, fmt=".2f")
#         plt.show()

# #6.工艺流量与加水量设定值关系
#     import sshc.timeAlignment as ta
#     dateStr = ['03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '14', '15', '16', '17']
#     listDF = list()
#     df = rds.getBatchData('2400-2019-11-03*', 2)
#     df1 = DataFrame(df.values[:, [3,1,2,4,5,6,7,8,9,10,11,12,13,14,15,16]])
#     df2 = DataFrame(df1, dtype=np.float)
#     listDF.append(df2)
#     aList = list()
#     for i in range(0, 101, 1):
#         aList.append(i)
#     ret = ta.multi_pre_align_train(listDF, aList,_topNum=5)
#     ret.to_csv('/home/pre-1103.csv')
#     print

#7.工艺流量与加水量设定值关系
    import sshc.timeAlignment as ta
    import sshc.modelPredict as modelPredict
    import sshc.timeAlignment as ta
    import base.data_transform as dt
    dateStr = ['03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '14', '15', '16', '17']

    # df = rds.getBatchData('2400-2019-11-*', 2)
    # df1 = DataFrame(df.values[:, [3,1,9,14,16]])
    # df2 = DataFrame(df1, dtype=np.float)
    # df3 = ta.time_align_transform(df2,[0,58,36,35,27])

    scoreList=list()
    for i in range(0, len(dateStr), 1):
        keyStr = '2400-2019-11-'+dateStr[i]+'*'
        dfy = rds.getBatchData(keyStr, 2)
        dfy1 = DataFrame(dfy.values[:, [3, 1, 9, 14, 16]])
        dfy2 = DataFrame(dfy1, dtype=np.float)
        dfy3 = ta.time_align_transform(dfy2, [0, 58, 36, 35, 27])
    # a = dt.dataFrameRoll(df3, 10)
    # _, scores = modelPredict.cross_score(df3.values[:, 1:], df3.values[:, 0], 5)

    # model1,ssx,ssy = modelPredict.randomForest_model(df3.values[:, 1:], df3.values[:, 0])
    # modelPredict.model_save(model1,'c://md1.m')
    # modelPredict.model_save(ssx, 'c://md_ssx1.m')
    # modelPredict.model_save(ssy, 'c://md_ssy1.m')

        from sklearn.externals import joblib
        model1 = joblib.load('c://md1.m')
        ssx = joblib.load('c://md_ssx1.m')
        ssy = joblib.load('c://md_ssy1.m')
        score ,dfRes = modelPredict.randomForest_predict_score(model1,ssx,ssy,dfy3.values[:, 1:], dfy3.values[:, 0],_isPlot=True)
        scoreList.append(score)

    print


    print