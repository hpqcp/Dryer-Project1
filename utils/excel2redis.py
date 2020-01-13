import redis as redis
from pandas import DataFrame
import pandas as pd
import base.data_preProcess as bsPre
import datetime





def csv2Redis(_host,_db,_gourp,_path,_sheet,_keyCol,_valueCols):
    pool = redis.ConnectionPool(host=_host, decode_responses=True, db=_db)
    r = redis.Redis(connection_pool=pool, decode_responses=True, db=_db)
    path = _path
    group = _gourp
    df = bsPre.readExcel(path, _sheet)
    cmdStr = "r.rpush(key"
    for i in range(0, len(_valueCols), 1):
        cmdStr = cmdStr + ",str(data[j][" + str(_valueCols[i]) + "])"
    cmdStr = cmdStr + ")"
    pipe = r.pipeline(transaction=True)
    data = df.values.tolist()
    lens = df.shape[0]
    for j in range(0,lens, 1):
        key = group + str(data[j][_keyCol])
        eval(cmdStr)
    pipe.execute()

def getBatchData(_patten, _db):
    pool = redis.ConnectionPool(host='127.0.0.1', decode_responses=True, db=_db)
    r = redis.Redis(connection_pool=pool, decode_responses=True, db=_db)
    key1 = r.keys(pattern=_patten)  # "t1zc0000*")
    dt = DataFrame([r.lrange(key1[i], 0, -1) for i in range(1, len(key1), 1)][:])
    dt1 = dt.sort_values(0)
    dt2 = dt1.reset_index(drop=True)
    for i in range(1, dt2.shape[1], 1):
        dt2[[i]] = dt2[[i]].astype('float')
    # print(dt.dtypes)
    r.connection_pool.disconnect()
    return dt2

if __name__ == "__main__":
    host = '127.0.0.1'
    db = 2
    group = '2400-'
    path = 'E://工作文档//FangCloudV2//个人文件//9000其他//松散回潮项目//试验数据//2019年11月2400线回潮段数据.xlsx'
    sheet = 0
    keyCol = 0
    valueCols = [0,1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31]
    for i in range(0,37,1):
        csv2Redis(host,db,group,path,i,keyCol,valueCols)


    # df = getBatchData('4000-2019-10-07*', 1)
    # df1 = DataFrame(df.values[:,[0,1,2,3]])
    # df1[0]=pd.to_datetime(df1[0])
    # df1[1]=df1[1].astype('float64')
    # df1[2] = df1[2].astype('float64')
    # df1[3] = df1[3].astype('float64')
    # import chart.plot as pl
    # # pl.singlePlot(df1)
    # import matplotlib.pyplot as pyplot
    # fig, ax1 = pyplot.subplots()
    # pyplot.ylim(0, 4200)
    # ax2 = ax1.twinx()  # 做镜像处理
    # pyplot.ylim(0, 4200)
    # ax3 = ax1.twinx()
    # ax1.plot(df1[0],df1[1], 'g-')
    # ax2.plot(df1[0],df1[2], 'b--')
    # ax3.plot(df1[0],df1[3], 'r--')
    # pyplot.show()
    print('1')

def fromCsv():
    pool = redis.ConnectionPool(host='127.0.0.1', decode_responses=True, db=1)
    r = redis.Redis(connection_pool=pool, decode_responses=True, db=1)
    path = "d://hsj时间格式.xlsx"
    group = "b"  # t test data
    factoryID = "9"  # 1Ky 2 hy 3qy
    deptID = "z"  # z zs j jb c cx
    lineID = "a"  # line C
    # batch = "0001"
    # secID = 3 # 3 yslq 4 hs 5 yslq
    df = bsPre.readExcel(path, 0)
    # df = df[2853:]
    # df = df.reset_index(drop=True)
    # print(df.values[0,:])
    for j in range(0, df.shape[0], 1):
        data = df.values[j, :].tolist()
        key = group + "-" + str(data[1]) + "-" + str(data[0]) + "-" + str(data[2])
        r.rpush(key, data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11],
                data[12], data[13], data[14])





def getBatchDataDelay(_patten, startDelay, endDelay, _db):
    # 获取批次数据
    df1 = getBatchData(_patten, _db)
    # 获取开始结束时间
    startTime = df1.values[0, 0]
    endTime = df1.values[-1, 0]
    # 获取所有数据
    df2 = getBatchData("b*", _db)
    # 截取时间段之间的数据
    startdf = df2[df2[0].isin({startTime})]
    enddf = df2[df2[0].isin({endTime})]

    startIndex = startdf.index.values[0]
    endIndex = enddf.index.values[0]

    startIndex = startIndex - startDelay
    endIndex = endIndex + endDelay
    if (startIndex < 0):
        startIndex = 0
    if (endIndex > len(df2) - 1):
        endIndex = len(df2) - 1
    df2 = df2[(df2.index.values>=startIndex)&(df2.index.values<=endIndex)]
    df2 = df2.reset_index(drop=True)
    return df2
