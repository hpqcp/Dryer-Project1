#######################################
##     用于工艺参数之间距离估算     ##
######################################
import bll.batch_process as batchProcess

#
def compute_batch_point(_df):
    batchPoint = batchProcess.check_batch_point(_df)
    print(batchPoint)
    return 0

if __name__ == "__main__":
    import utils.excel2redis as rds
    from pandas import DataFrame
    import chart.plot as cPlt

    batchStr = "t1zc0000*"
    # 获取批次数据
    df = rds.getBatchData(batchStr, 0)
    useCol = [1, 2, 3, 4, 5, 6, 7, 8, 9]  # , 10, 11, 12]
    # df = DataFrame(df.values[:, useCol])
    df = df[useCol]
    df = df[:]  # int(len(df) / 4)]
    bp = compute_batch_point(df)


    # # df = df[35:49]
    # #cPlt.singlePlot(df, _title=batchStr)
    # point = check_batch_point(df)#获取批次开始结束点
    # parmNo = 3
    # p1 = point[parmNo][0]
    # p2 = point[parmNo][1]
    # wtDF = df.values[p1:p2,0]   #serieas
    # wt = batch_Steadystate_r1(wtDF)#批次截取方法
    # # print(wt,len(wtDF),len(df))
    # #cPlt.singlePlot(df[p1+wt[0]:p1+wt[1]], _title=batchStr)
    # cPlt.zsParmPlot(df.values[:,parmNo],_vline=[p1,p2,p1+wt[0],p1+wt[1]])
    #
    # print(len(df[p1+wt[0]:p1+wt[1]]))