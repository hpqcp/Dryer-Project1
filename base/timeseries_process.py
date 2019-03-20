import pandas as pd
import datetime
import utils.excel2redis as rds


# 获取时间列不连续的索引
def check_ts_continuity(_series):
    _series = pd.to_datetime(_series)
    list = []
    for i in range(1, len(_series), 1):
        if (_series[i] - _series[i - 1] != datetime.timedelta(seconds=15)):
            list.append(_series.index.values[i])

    # ser = [_series.index.values[_series[i] - _series[i - 1] != datetime.timedelta(
    #     seconds=15)] for i in range(1, len(_series), 1)]
    return list


# df = res.getBatchData("b-YAR-19033103103*", 1)
# _series = pd.Series(df[0].values, index=df.index.values)
# list =check_ts_continuity(_series)
#
# print(list)

# 判断延时后和延时前是否是“同一批次”
def isSameBatch(_df, _delayDf):
    # 获取开始结束时间
    startTime = _df.values[0, 0]
    endTime = _df.values[-1, 0]

    startdf = _delayDf[_delayDf[0].isin({startTime})]
    enddf = _delayDf[_delayDf[0].isin({endTime})]

    startIndex = startdf.index.values[0]
    endIndex = enddf.index.values[0]

    outStarDf = _delayDf[_delayDf.index.values <= startIndex]
    outEndDf = _delayDf[_delayDf.index.values >= endIndex]

    outStarDf = outStarDf.reset_index(drop=True)
    outEndDf = outEndDf.reset_index(drop=True)

    startSeries = pd.Series(outStarDf[0].values, index=outStarDf.index.values)
    endSeries = pd.Series(outEndDf[0].values, index=outEndDf.index.values)

    startflag = True
    endflag = True
    if (len(startSeries) > 1):
        startList = check_ts_continuity(startSeries)
        if (len(startList) > 0):
            startflag = False

    if (len(endSeries) > 1):
        endList = check_ts_continuity(endSeries)
        if (len(endList) > 0):
            endflag = False

    return [startflag, endflag]

str = "b-YAR-19033102403-*"
df = rds.getBatchData(str, 1)
df2 = rds.getBatchDataDelay(str, 15, 0, 1)
print(isSameBatch(df, df2))
