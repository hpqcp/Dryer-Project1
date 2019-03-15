from websocket import create_connection
from pandas.io.json import json_normalize
import pandas as pd
import json

class WebSocketHelp:
    @staticmethod
    def WebSocketJson(url,quary):
        ws = create_connection(url)
        ws.send(quary)
        result =  ws.recv()
        ws.close()
        data_list = json.loads(result)
        if (data_list["ResultState"] == 1):
            datajson = json.loads(data_list["Message"])
            data = [[d['TagName'], d['DateTime'], d['Value']] for d in datajson]
            df = pd.DataFrame(data, columns=['TagName', 'DateTime', 'Value'])
            return df
        else:
            return None     

if __name__ == "__main__":
    df = WebSocketHelp.WebSocketJson("ws://10.130.65.207:8181/HisWeb","MES2RTDATA.U_Enriche_11010030005.DC_PH||2018-01-01 00:00:00||2018-01-01 01:00:00||Cyclic||6000")
    print(df)
