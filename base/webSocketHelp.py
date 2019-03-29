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


if __name__ == "__main__":
    # df = WebSocketHelp.WebSocketJson("ws://10.130.65.207:8181/HisWeb",
    #                                  "MES2RTDATA.U_DRY_11010160002.DC_PH,MES2RTDATA.U_DRY_11010160002.DC_PCH,MES2RTDATA.U_BAL_11010160001.DC_OrderNo,MES2RTDATA.U_BAL_11010160001.DC_TeamCode,	MES2RTDATA.U_DRY_11010160002.DC_GYDZT||2019-01-02 6:00:00||2019-01-02 23:30:00||Cyclic||3600000")
    df = WebSocketHelp.WebSocketJson("ws://10.130.65.207:8181/HisWeb",
                                     "MES2RTDATA.U_DRY_11010160002.DC_CKWLSF||2019-01-02 17:00:00||2019-01-02 19:30:00||Cyclic||60000")
    df1 = WebSocketHelp.DfGroup(df, 'TagName')
    print(df1)
