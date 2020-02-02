from pandas import DataFrame
import numpy as np
import sshc.timeAlignment as ta

def retrieve_predict_data(_df,_index,_freq=1):

    diffList = [0, 58, 36, 35, 27]
    dfx = _df.loc[0:(_index+_freq-1),:]
    #显示 100个点 出口水分 预测/实际趋势
    #显示 全数据 出口水分 预测/实际趋势
    #显示 瞬时流量、加水量 趋势
    #显示预测指标 R2,mse,mae
    #显示操作提示

    df1 = _df.iloc[_index:(_index+_freq),[1,2,0]]
    df1.rename(columns={'0':'flow','1':'water','2':'moisture'},inplace=True)

    if _index < 58 :
        df1['predict'] = None
        return df1

    loc = _index - 58
    # diffList = [-27, 31, 13, 12, 0]
    df_diff = ta.time_align_transform(_df, diffList)

    # from sklearn.externals import joblib
    # model1 = joblib.load('c://md1.m')
    # ssx = joblib.load('c://md_ssx1.m')
    # ssy = joblib.load('c://md_ssy1.m')



    print


if __name__ == "__main__":
    import utils.excel2redis as rds

    keyStr = '2400-2019-11-03*'# + dateStr[i] + '*'
    df = rds.getBatchData(keyStr, 2)
    df1 = DataFrame(df.values[:, [3, 1, 9, 14, 16]])
    df2 = DataFrame(df1, dtype=np.float)
    rtl = retrieve_predict_data(df2,58,10)

    print






