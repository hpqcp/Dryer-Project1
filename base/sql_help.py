import pandas as pd
import pymssql
from sqlalchemy import create_engine


class SqlHelp:
    def __init__(self, host, port, user, password, db):
        self.host = host
        self.user = user
        self.pwd = password
        self.db = db
        self.port = port

    def GetEngine(self):
        connect_info = 'mssql+pymssql://{}:{}@{}:{}/{}'.format(self.user, self.pwd, self.host, self.port, self.db)  # 1
        # create_engine('mssql+pymssql://scott:tiger@hostname:port/dbname')
        engine = create_engine(connect_info)
        return engine


class Sql200:
    sql = None
    engine = None

    def GetEngine(self):
        sql = SqlHelp("10.130.65.200", "1433", "admin", "1qaz@WSX", "Cloud")
        return sql.GetEngine()

    def ExecQuery(self, sql):
        # create_engine('mssql+pymssql://scott:tiger@hostname:port/dbname')
        self.engine = self.GetEngine()
        df = pd.read_sql(sql=sql, con=self.engine)
        return df

    # 获取关键参数
    # _FactoryCode='1100'
    # _ZoneName='制丝'
    # _BrandName='云烟(紫)模组一'
    # _LineName='C线'
    # _StageName='切丝烘丝加香段'
    def GetImpParameter(self, _FactoryCode, _ZoneName, _BrandName, _LineName, _StageName, _parNameList):
        parName = "'" + "','".join(_parNameList) + "'"
        # parName = "'切叶丝含水率','叶丝增温增湿工艺流量','叶丝增温增湿蒸汽流量','薄板干燥热风温度','薄板干燥Ⅰ区筒壁温度','薄板干燥Ⅱ区筒壁温度','薄板干燥出料温度','薄板干燥出料含水率','叶丝冷却出料含水率'"
        ms = Sql200()
        df = ms.ExecQuery(
            "select ID,FactoryCode,FactoryName,ZoneCode,ZoneName,BrandCode,BrandName,LineID,LineName,StageID,StageName,ProcessID,ProcessName,ParameterID,ParameterName," +
            "GroupParameterTag,FactoryParameterTag,ZoneSort,LineSort,StageSort,ProcessSort,ParameterSort " +
            "from V_FactoryToParameterRelation " +
            "where 1 = 1 and GroupParameterTag is not null and FactoryParameterTag is not null " +
            "and FactoryCode = '" + _FactoryCode + "' and ZoneName = '" + _ZoneName + "' " +
            "and BrandName = '" + _BrandName + "' and LineName = '" + _LineName + "' and StageName = '" + _StageName + "' " +
            "and ParameterName in (" + parName + ") " +
            "order by ZoneSort,LineSort,StageSort,ProcessSort,ParameterSort")
        return df


    # 获取身份信息
    # _FactoryCode='1100'
    # _ZoneName='制丝'
    # _BrandName='云烟(紫)模组一'
    # _LineName='C线'
    # _StageName='切丝烘丝加香段'
    def GetIDInf(self, _FactoryCode, _ZoneName, _BrandName, _LineName, _StageName, _TypeNameList):
        # "0019de43-1a5c-4463-ac2a-ba64f1ff18a0"
        TypeName = "'" + "','".join(_TypeNameList) + "'"
        ms = Sql200()
        df = ms.ExecQuery(
            "select distinct * from V_StageRealTimePointBrand " +
            "where FactoryCode='" + _FactoryCode + "' and ZoneName='" + _ZoneName + "' and BrandName='" + _BrandName + "' " +
            "and LineName='" + _LineName + "' and StageName='" + _StageName + "' " +
            "and TypeName in (" + TypeName + ") " +
            "order by FactoryCode,Linesort,Stagesort")
        return df


if __name__ == "__main__":
    ms = Sql200()
    # df = ms.ExecQuery("SELECT * FROM B_Brand")
    # df = ms.GetImpParameter('1100', '制丝', '云烟(紫)模组一', 'C线', '切丝烘丝加香段', ['切叶丝含水率', '叶丝增温增湿工艺流量'])
    df = ms.GetIDInf('1100', '制丝', '云烟(紫)模组一', 'C线', '切丝烘丝加香段', ['牌号实时点', '批次号实时点'])
    print(df)
