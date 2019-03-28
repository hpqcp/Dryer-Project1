import pandas as pd

def RowToColumn(_df, _groupName, _vColumns,_indexName="index"):
    dfFL = pd.DataFrame()
    for name, group in _df.groupby(_groupName):
        vDt =None
        if(_indexName=="index"):
            vDt = group.loc[:, _vColumns].reset_index(drop=True)
        else:
            vDt = pd.Series(group.loc[:, _vColumns].values, index=group.loc[:, _indexName].values)
        coName = name
        vDt.name = coName
        dfFL = dfFL.join(vDt, how='outer')

    return dfFL