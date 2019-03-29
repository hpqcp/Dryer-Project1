import pandas as pd


def RowToColumn(_df, _groupName, _vColumns, _indexName="index", _havIndex=False):
    dfFL = pd.DataFrame()
    i = 0
    for name, group in _df.groupby(_groupName):
        if ((_havIndex == True) & (i == 0)):
            inxDt = None
            if (_indexName == "index"):
                inxDt = pd.Series(group.index.values, index=group.index.values)
            else:
                inxDt = pd.Series(group.loc[:, _indexName].values, index=group.loc[:, _indexName].values)
            inxDt.name = _indexName
            dfFL = dfFL.join(inxDt, how='outer')
        vDt = None
        if (_indexName == "index"):
            vDt = group.loc[:, _vColumns].reset_index(drop=True)
        else:
            vDt = pd.Series(group.loc[:, _vColumns].values, index=group.loc[:, _indexName].values)
        coName = name
        vDt.name = coName
        dfFL = dfFL.join(vDt, how='outer')
        i = i + 1
    dfFL = dfFL.reset_index(drop=True)
    return dfFL
