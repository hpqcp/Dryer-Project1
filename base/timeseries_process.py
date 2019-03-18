import utils.excel2redis as res
import pandas as pd
import datetime


def check_ts_continuity(_series):
    _series = pd.to_datetime(_series)
    list = []
    for i in range(1, len(_series), 1):
        if (_series[i] - _series[i - 1] != datetime.timedelta(seconds=15)):
            list.append(_series.index.values[i])

    # ser = [_series.index.values[_series[i] - _series[i - 1] != datetime.timedelta(
    #     seconds=15)] for i in range(1, len(_series), 1)]
    return list

df = res.getBatchData("b-YAR-19033103103*", 2)
_series = pd.Series(df[0].values, index=df.index.values)
list =check_ts_continuity(_series)

print()
