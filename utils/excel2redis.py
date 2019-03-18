import redis as redis
from pandas import DataFrame
import base.data_preProcess as bsPre
import datetime

# pool = redis.ConnectionPool(host='127.0.0.1')
# r = redis.Redis(connection_pool=pool)

# path = "z://C线10批数据（20190315）.xlsx"
# group = "t"  # t test data
# factoryID="1" # 1Ky 2 hy 3qy
# deptID = "z" # z zs j jb c cx
# lineID = "c" # line C
# batch = "0001"
# #secID = 3 # 3 yslq 4 hs 5 yslq
# for i in range(0,10,1):
#     df = bsPre.readExcel(path, i)
#     # print(df.values[0,:])
#     for j in range(0,df.shape[0],1):
#         data = df.values[j,[0,1,3,5,7,9,11,13,15,17]].tolist()
#         key = group+factoryID+deptID+lineID+"000"+str(i)+data[0]
#         r.rpush(key,data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9])
# exit()


def fromCsv():
    pool = redis.ConnectionPool(host='127.0.0.1', decode_responses=True, db=1)
    r = redis.Redis(connection_pool=pool, decode_responses=True, db=1)
    path = "d://hsj1.xlsx"
    group = "b"  # t test data
    factoryID = "9"  # 1Ky 2 hy 3qy
    deptID = "z"  # z zs j jb c cx
    lineID = "a"  # line C
    # batch = "0001"
    # secID = 3 # 3 yslq 4 hs 5 yslq
    df = bsPre.readExcel(path, 0)
    df = df[2853:]
    df = df.reset_index(drop=True)
    # print(df.values[0,:])
    for j in range(0, df.shape[0], 1):
        data = df.values[j, :].tolist()
        key = group +"-" + str(data[1]) +"-" +str(data[0]) +"-" + str(data[2])
        r.rpush(key, data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11],
                data[12], data[13], data[14])


def getBatchData(_patten):
    pool = redis.ConnectionPool(host='127.0.0.1', decode_responses=True)
    r = redis.Redis(connection_pool=pool, decode_responses=True)
    key1 = r.keys(pattern=_patten)  # "t1zc0000*")
    dt = DataFrame([r.lrange(key1[i], 0, -1) for i in range(1, len(key1), 1)][:])
    dt1 = dt.sort_values(0)
    dt2 = dt1.reset_index(drop=True)
    for i in range(1, dt2.shape[1], 1):
        dt2[[i]] = dt2[[i]].astype('float')
    # print(dt.dtypes)
    r.connection_pool.disconnect()
    return dt2


fromCsv()
