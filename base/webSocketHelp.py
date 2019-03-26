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


if __name__ == "__main__":
    df = WebSocketHelp.WebSocketJson("ws://10.130.65.207:8181/HisWeb",
                                     "HZCF.U_Maker_11010011004.RD_QualifiedGoods||2019-03-26 12:00:00||2019-03-26 15:30:00||Full||6000")
    print()
    print(df)

