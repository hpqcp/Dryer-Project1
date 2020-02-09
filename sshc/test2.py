import pandas as pd
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
    import sshc.simulationRun.dataSource as ds
    import sshc.simulationRun.batchProcess as bp

# #1.按天进行特征重要度排序
#     # dateStr = [range(14)]
#     rtlList = list()
#     # for i in range(0,len(dateStr),1):
#     for i in range(0, 14, 1):
#         df = ds.sshc_datasource(no=i).sshc_df
#         batch1 = bp.batch(df)
#         wtDFList = batch1.retrive_wt_data(_flowCol=2,_moistureCol=1,_triggerFlow=0,_triggerMoisture=16,_delay=60)#(2,1,0,16,60)
#         for wtDF in wtDFList:
#             df1 = DataFrame(wtDF.values[:, [3, 1, 6, 8,10, 11,  14, 16]]) #删除特征12，13，15后重新进行重要度排序
#             df2 = DataFrame(df1, dtype=np.float)
#             fi = feature_importances(df2)
#             rtlList.append(fi)
#     dfRtl = DataFrame(rtlList)
#     print

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
#     allDF = DataFrame()
#     for i in range(0, 14, 1):
#         df = ds.sshc_datasource(no=i).sshc_df
#         batch1 = bp.batch(df)
#         wtDFList = batch1.retrive_wt_data(_flowCol=2,_moistureCol=1,_triggerFlow=0,_triggerMoisture=16,_delay=60)#(2,1,0,16,60)
#         for wtDF in wtDFList:
#             allDF = pd.concat([allDF,wtDF],axis=0)
#
#     allDF=allDF.iloc[:,[3,1,6,10,11]]
#     plt.figure(figsize=(16, 12))
#     sns.heatmap(allDF.corr(), annot=True, fmt=".2f")
#     plt.show()
#     print

# # 6.工艺流量、水分、实际加水量 预测 加水量设定
#     from matplotlib import pyplot as plt
#     import sshc.modelPredict as  mp
#     from sklearn.model_selection import train_test_split
#     from sklearn.preprocessing import StandardScaler
#     from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor, GradientBoostingRegressor
#     from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
#
#     allDF = DataFrame()
#     for i in range(0, 14, 1):
#         df = ds.sshc_datasource(no=i).sshc_df
#         batch1 = bp.batch(df)
#         wtDFList = batch1.retrive_wt_data(_flowCol=1,_moistureCol=3,_triggerFlow=0,_triggerMoisture=16,_delay=60)#(2,1,0,16,60)
#         wtDFList = batch1.headDFList
#         for wtDF in wtDFList:
#             allDF = pd.concat([allDF,wtDF],axis=0)
#     allDF=allDF.iloc[:,[3,9,6,16,15,8]]
#     df_x = allDF.values[:, 1:]
#     df_y = allDF.values[:, 0]
#
#     # df2 = ds.sshc_datasource(no=13).sshc_df
#     # batch2 = bp.batch(df2)
#     # wtDFList2 = batch2.retrive_wt_data(_flowCol=1, _moistureCol=3, _triggerFlow=0, _triggerMoisture=16,
#     #                                   _delay=60)  # (2,1,0,16,60)
#     # allDF2 = DataFrame()
#     # for wtDF2 in wtDFList2:
#     #     allDF2 = pd.concat([allDF2,wtDF2],axis=0)
#     #     allDF2 = allDF2.iloc[:, [3, 9, 6, 16, 15, 8]]
#     #     df_x1 = allDF2.values[:, 1:]
#     #     df_y1 = allDF2.values[:, 0]
#     #
#     # x_train , y_train = df_x , df_y
#     # x_test  ,  y_test = df_x1 , df_y1
#     # 随机采样20%作为测试 75%作为训练
#     x_train, x_test, y_train, y_test = train_test_split(df_x, df_y, test_size=0.05, random_state=33)
#     rf_model,ss_x,ss_y =mp.randomForest_model(x_train,y_train)
#     y_predict,df_p = mp.randomForest_predict_score(rf_model,ss_x,ss_y,x_test,y_test,_isPlot=True)
#     df_p.rename(columns={0: 'Y', 1: 'P'}, inplace=True)
#     df_p['S'] = df_p['Y'] - df_p['P']
#     fi = rf_model.feature_importances_
#     import chart.plot as myPlt
#     myPlt.singlePlot(df_p)
#     myPlt.pairPlot(df_p)
#     print

#7.滚动预测
    import sshc.modelPredict as  mp

    allDF = DataFrame()
    for i in range(0, 14, 1):
        df = ds.sshc_datasource(no=i).sshc_df
        # batch2 = bp.batch(df)
        wtDFList = [df]#batch2.retrive_wt_data(_flowCol=1, _moistureCol=3, _triggerFlow=0, _triggerMoisture=16,_delay=60)
        for wtDF in wtDFList:
            allDF = pd.concat([allDF, wtDF], axis=0)
    allDF = allDF.iloc[:, [3, 9, 6, 16, 15, 8]]
    df_x = allDF.values[:, 1:]
    df_y = allDF.values[:, 0]

    df1 = ds.sshc_datasource(no=0).sshc_df
    batch1 = bp.batch(df1)
    wtDFList = batch1.retrive_wt_data(_flowCol=1, _moistureCol=3, _triggerFlow=0, _triggerMoisture=16,
                                      _delay=60)  # (2,1,0,16,60)
    rf_model, ss_x, ss_y = mp.randomForest_model(df_x, df_y)
    mp.model_save(rf_model,'c://allX.m')
    mp.model_save(ss_x, 'c://allX-ss_x.m')
    mp.model_save(ss_y, 'c://allX-ss_y.m')
    headDF1 = batch1.headDFList[0]
    for i in range(1,wtDFList[0].shape[0],20):
        testDF = wtDFList[0].iloc[:i,:]#pd.concat([headDF1,wtDFList[0].iloc[:i,:]],axis=0)
        testDF = testDF.iloc[:, [3, 9, 6, 16, 15, 8]]
        df_x1 = testDF.values[:, 1:]
        df_y1 = testDF.values[:, 0]
        scores, df_p = mp.randomForest_predict_score(rf_model, ss_x, ss_y, df_x1, df_y1, _isPlot=True)
        print(str(i))
        print(scores)


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

# #7.工艺流量与加水量设定值关系
#     import sshc.timeAlignment as ta
#     import sshc.modelPredict as modelPredict
#     import sshc.timeAlignment as ta
#     import base.data_transform as dt
#     dateStr = ['03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '14', '15', '16', '17']
#
#     # df = rds.getBatchData('2400-2019-11-*', 2)
#     # df1 = DataFrame(df.values[:, [3,1,9,14,16]])
#     # df2 = DataFrame(df1, dtype=np.float)
#     # df3 = ta.time_align_transform(df2,[0,58,36,35,27])
#
#     scoreList=list()
#     for i in range(0, len(dateStr), 1):
#         keyStr = '2400-2019-11-'+dateStr[i]+'*'
#         dfy = rds.getBatchData(keyStr, 2)
#         dfy1 = DataFrame(dfy.values[:, [3, 1, 9, 14, 16]])
#         dfy2 = DataFrame(dfy1, dtype=np.float)
#         dfy3 = ta.time_align_transform(dfy2, [0, 58, 36, 35, 27])
#     # a = dt.dataFrameRoll(df3, 10)
#     # _, scores = modelPredict.cross_score(df3.values[:, 1:], df3.values[:, 0], 5)
#
#     # model1,ssx,ssy = modelPredict.randomForest_model(df3.values[:, 1:], df3.values[:, 0])
#     # modelPredict.model_save(model1,'c://md1.m')
#     # modelPredict.model_save(ssx, 'c://md_ssx1.m')
#     # modelPredict.model_save(ssy, 'c://md_ssy1.m')
#
#         from sklearn.externals import joblib
#         model1 = joblib.load('c://md1.m')
#         ssx = joblib.load('c://md_ssx1.m')
#         ssy = joblib.load('c://md_ssy1.m')
#         score ,dfRes = modelPredict.randomForest_predict_score(model1,ssx,ssy,dfy3.values[:, 1:], dfy3.values[:, 0],_isPlot=True)
#         scoreList.append(score)
#
#     print
#
#
#     print