import pandas as pd

def RowToColumn(_df, _groupName, _vColumns):
    dfFL = pd.DataFrame()
    for name, group in _df.groupby(_groupName):
        vDt = group.loc[:, _vColumns].reset_index(drop=True)
        coName = name
        vDt.name = coName
        dfFL = dfFL.join(vDt, how='outer')
        
    return dfFL