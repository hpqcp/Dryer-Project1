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
    df = WebSocketHelp.WebSocketJson("ws://10.130.65.207:8181/HisWeb",
                                     "MES2RTDATA.U_DRY_11010160002.DC_PCH,MES2RTDATA.U_DRY_11010160002.DC_PH||2019-01-26 15:00:00||2019-01-26 17:30:00||Cyclic||360000")
    print()
    print(df)
    dfGroup = WebSocketHelp.DfGroup(df, 'TagName')
    print(dfGroup)
