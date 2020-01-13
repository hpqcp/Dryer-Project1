#数据预处理模块
#1、截取稳态
#




#截取数据稳态（简易方式）
#主要针对流量和水分
#采用经典截取法：即料头到达工艺下限往后推3分钟，料尾低于工艺下限往前推三分钟
def cut_steady_state_simple(_series,_lsl,_delay):
    return

if __name__ == "__main__":
    import utils.excel2redis as rds
    from pandas import DataFrame
    import chart.plot as cPlt
    import bll.batch_process as bp
    import numpy as np

    # batchStr = "t1zc0002*"
    # 获取批次数据
    df = rds.getBatchData('4000-2019-10-09*', 1)
    df1 = DataFrame(df.values[:, [3]])
    df2 = DataFrame(df1, dtype=np.float)
    # df = df[35:49]
    #cPlt.singlePlot(df, _title=batchStr)
    point = bp.check_batch_point(df2)#获取批次开始结束点
    parmNo = 3
    p1 = point[parmNo][0]
    p2 = point[parmNo][1]
    wtDF = df.values[p1:p2,0]   #serieas
    wt = bp.batch_Steadystate_r1(wtDF)#批次截取方法
    # print(wt,len(wtDF),len(df))
    #cPlt.singlePlot(df[p1+wt[0]:p1+wt[1]], _title=batchStr)
    cPlt.zsParmPlot(df.values[:,parmNo],_vline=[p1,p2,p1+wt[0],p1+wt[1]])

    print(len(df[p1+wt[0]:p1+wt[1]]))