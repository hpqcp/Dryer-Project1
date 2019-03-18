import pandas as pd
import pymssql
from sqlalchemy import create_engine


class SqlHelp:
    def __init__(self,host,port,user,password,db):
        self.host = host
        self.user = user
        self.pwd = password
        self.db = db
        self.port =port

    def GetEngine(self):
        connect_info = 'mssql+pymssql://{}:{}@{}:{}/{}'.format(self.user,self.pwd,self.host,self.port,self.db)  #1
        # create_engine('mssql+pymssql://scott:tiger@hostname:port/dbname')
        engine = create_engine(connect_info)
        return engine

class Sql200:
    sql = None
    engine = None
    def GetEngine(self):
        sql = SqlHelp("10.130.65.200","1433","admin","1qaz@WSX","Cloud")
        return sql.GetEngine()

    def ExecQuery(self,sql):
        # create_engine('mssql+pymssql://scott:tiger@hostname:port/dbname')
        self.engine = self.GetEngine()
        df = pd.read_sql(sql=sql, con=self.engine)
        return df