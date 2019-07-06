from websocket import create_connection
from pandas.io.json import json_normalize
import pandas as pd
import json


class WebSocketHelp:
    @staticmethod
    def WebSocketJson(url, quary):
        ws = create_connection(url)
        ws.send(quary)
        result = ws.recv()
        ws.close()
        data_list = json.loads(result)
        if (data_list["ResultState"] == 1):
            datajson = json.loads(data_list["Message"])
            data = [[d['TagName'], d['DateTime'], d['Value'], d['vValue']] for d in datajson]
            df = pd.DataFrame(data, columns=['TagName', 'DateTime', 'Value', 'vValue'])
            return df
        else:
            return None

    @staticmethod
    def DfGroup(_df, _groupC):
        df = pd.DataFrame()
        for name, group in _df.groupby(_groupC):
            df = df.append(group)
        df = df.reset_index(drop=True)
        return df

    @staticmethod
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

if __name__ == "__main__":
    df = WebSocketHelp.WebSocketJson("ws://10.130.65.207:8181/HisWeb",
                                     "MES2RTDATA.U_Maker_11020030001.DC_JTH,MES2RTDATA.U_Maker_11020030001.DC_PH,MES2RTDATA.U_Maker_11020030001.DC_BC,"
                                     "MES2RTDATA.U_Maker_11020030001.DC_YXSD,MES2RTDATA.U_Maker_11020030001.DC_LLCL,MES2RTDATA.U_Maker_11020030001.DC_SJCL,"
                                     "MES2RTDATA.U_Maker_11020030001.DC_ZCL,MES2RTDATA.U_Maker_11020030001.DC_FPL,MES2RTDATA.U_Maker_11020030001.DC_LYL,"
                                     "MES2RTDATA.U_Maker_11020030001.DC_XL,MES2RTDATA.U_Maker_11020030001.DC_TJCS,MES2RTDATA.U_Maker_11020030001.DC_DQBCJSSJ,"
                                     "MES2RTDATA.U_Maker_11020030001.DC_DQBCKSSJ"
                                     "||2019-07-5 6:30:00||2019-07-5 10:30:00||Cyclic||600000")
    df2 = WebSocketHelp.RowToColumn(df, 'TagName', 'vValue', _indexName='DateTime', _havIndex=True)
    print(df2)
    print()
    # dfGroup = WebSocketHelp.DfGroup(df, 'TagName')
    # print(dfGroup)



