#
#
#

from pandas import DataFrame
import numpy as np
import pandas as pd


#
#
#
def multi_pre_align_train(_dfList=[],_pointList=[],_topNum=3):

    dfAll = DataFrame()
    for i in range(0,len(_dfList),1):
        retDF = pre_align_train(_dfList[i],_pointList,_topNum)
        retDF['round'] = i
        dfAll=pd.concat([dfAll,retDF],axis=0)
    return dfAll



#
#对时间对齐进行预训练
##思路是x1,x2,x3.....分别与y进行一对一进行交叉验证，找到每一组得分最高TOPn点
#
def pre_align_train(_df,_pointList,_topNum=3):
    from multiprocessing import Pool
    import multiprocessing as mp
    import datetime
    starttime = datetime.datetime.now()
    cores = mp.cpu_count()
    cList = list()
    for j in range(1,_df.shape[1],1):
        for i in _pointList:
            cList.append([0,j,i,_df.values[:,[0,j]]])
    #
    pool = Pool(cores-1)
    res = pool.map(rf_model,cList)
    pool.close()
    endtime = datetime.datetime.now()
    df_res = DataFrame(res)
    print ((endtime - starttime).seconds)
    df_res.columns = ['x','shifts','score'] #x,偏移量，得分
    df_res.sort_values(['x','score'],ascending=[1,0],inplace=True)
    grouped = df_res.groupby(['x']).head(_topNum)
    return grouped

#
#_df,_xLoc,_yLoc,_pointNum
#
def rf_model(_parmList):
    import sshc.modelPredict as modelPredict
    _yLoc = _parmList[0]
    _xLoc = _parmList[1]
    _pointNum = _parmList[2]
    df_target =  DataFrame(_parmList[3])
    df_target = DataFrame(df_target.values)
    df_a = time_align_transform(df_target,[0,_pointNum])
    _, scores = modelPredict.cross_score(df_a.values[:,1].reshape(-1,1), df_a.values[:,0], 5)
    return [_xLoc,_pointNum,scores]

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
def time_align_fit(_df,_pointList):
    #通过预训练得到每一参数TopN个优值
    # dfPreTrainTopN = pre_align_train()
    dfPreTrainTopN = pd.read_csv('c://1.csv')
    allList = list()
    for df_sub in dfPreTrainTopN.groupby(['x']):
        lens = df_sub[1].shape[0]
        list1=list()
        for j in range(0,lens,1):
            list1.append(df_sub[1].values[j,2])
        allList.append(list1)
    trainList = list()
    from itertools import product   #使用itertools中的product,实现笛卡尔乘积
    for item in  product(*allList):
        trainList.append([list(item),_df.values])
    dff = DataFrame(trainList)
    from multiprocessing import Pool
    import multiprocessing as mp
    import datetime
    starttime = datetime.datetime.now()
    cores = mp.cpu_count()
    # pool = Pool(cores - 1)
    # res = pool.map(rf_model, trainList)
    for i in range(0,len(trainList),1):
        res = rf_model_1(trainList[i])
    endtime = datetime.datetime.now()
    df_res = DataFrame(res)

    return


#
#_df,_xLoc,_yLoc,_pointNum
#
def rf_model_1(_parmList):
    import sshc.modelPredict as modelPredict
    shiftList = _parmList[0]
    df = _parmList[1]
    df_a = time_align_transform(df,shiftList)
    _, scores = modelPredict.cross_score(df_a.values[:,0], df_a.values[:,1], 5)
    return [_xLoc,_pointNum,scores]
#
#
#
def read_sshc_data(_keyStr):
    __spec__ = None
    import utils.excel2redis as rds
    df = rds.getBatchData(_keyStr, 1)
    df1 = DataFrame(df.values[:, [3, 1, 6, 10, 11, 12, 13, 14, 17]])
    df2 = DataFrame(df1, dtype=np.float)
    return df2



if __name__ == "__main__":
    # __spec__ = None
    # import utils.excel2redis as rds
    #
    # df = rds.getBatchData('4000-2019-10-07*', 1)
    # df1 = DataFrame(df.values[:, [3, 1, 6, 10, 11, 12, 13, 14, 17]])
    # df2 = DataFrame(df1, dtype=np.float)
    # pointDiffList = [0,80,34,17,52,14,3,21,52]
    # df3=time_align_transform(df2,pointDiffList)
    # df_y = df3.values[:,0]
    # df_x = df3.values[:,1:]

    dateStr = ['07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22']
    listDF = list()
    for i in range(0,len(dateStr),1):
        data = read_sshc_data('4000-2019-10-'+dateStr[i]+'*')
        listDF.append(data)

    aList = list()
    for i in range(0,101,10):
        aList.append(i)
    ret = multi_pre_align_train(listDF,aList)


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


    # time_align_fit(df1,[0,10,20,30,40,50,60,70,80,90,100])
    print