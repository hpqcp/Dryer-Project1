#
#
#

import redis as rds
from pandas import DataFrame

import edge_ai.data_source.excel as excel

'''
松散回潮redis数据操作类
'''
class sshc_redis():
    #将csv数据导入到redis
    def csv2Redis(_host, _db, _gourp, _path, _sheet, _keyCol, _valueCols):
        pool = rds.ConnectionPool(host=_host, decode_responses=True, db=_db)
        r = rds.Redis(connection_pool=pool, decode_responses=True, db=_db)
        path = _path
        group = _gourp
        xls = excel.excel_oprator()
        df = xls.readExcel(path, _sheet)
        cmdStr = "r.rpush(key"
        for i in range(0, len(_valueCols), 1):
            cmdStr = cmdStr + ",str(data[j][" + str(_valueCols[i]) + "])"
        cmdStr = cmdStr + ")"
        pipe = r.pipeline(transaction=True)
        data = df.values.tolist()
        lens = df.shape[0]
        for j in range(0, lens, 1):
            key = group + str(data[j][_keyCol])
            eval(cmdStr)
        pipe.execute()

    #从redis获取批次数据
    def getBatchData(_patten, _db,_host='127.0.0.1'):
        pool = rds.ConnectionPool(host=_host, decode_responses=True, db=_db)
        r = rds.Redis(connection_pool=pool, decode_responses=True, db=_db)
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
    # host = '127.0.0.1'
    # db = 2
    # group = '2400-'
    # path = 'E://工作文档//FangCloudV2//个人文件//9000其他//松散回潮项目//试验数据//2019年11月2400线回潮段数据.xlsx'
    # sheet = 0
    # keyCol = 0
    # valueCols = [0, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31]
    # for i in range(0, 37, 1):
    #     csv2Redis(host, db, group, path, i, keyCol, valueCols)
    print

