from __future__ import absolute_import, division,\
    print_function, unicode_literals
import sys
import requests
import time
import json
import pandas as pd

quay_BASEURL = 'http://10.130.65.221:8086'
db = 'test_db'

def query(q, print_result=False):
    resp = requests.post(quay_BASEURL+'/query', params={'db': db, 'q': q})
    return resp.status_code, resp.content

def getDateBySql(q):
    data = query(q)
    if(data[0]==200):
        data_list = json.loads(data[1])
        columns =data_list['results'][0]['series'][0]['columns']
        values = data_list['results'][0]['series'][0]['values']
        df = pd.DataFrame(values, columns=columns)
        return df
    else:
        return None

if __name__ == '__main__':
    print()
    #df =getDateBySql('select * from hsj')
    #print(df)
    # timeArray = time.strptime('2019/5/20 12:00:06', "%Y/%m/%d %H:%M:%S")
    #
    # timeStamp = int(time.mktime(timeArray))
    # timeStamp=timeStamp+28800
    # print(timeStamp)
