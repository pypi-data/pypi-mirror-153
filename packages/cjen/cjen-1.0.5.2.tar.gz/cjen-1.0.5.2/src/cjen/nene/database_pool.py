import pymysql
from dbutils.pooled_db import PooledDB
from pymysql.cursors import Cursor


class DatabasePool(object):
    __pools = {}

    @classmethod
    def cursor(cls, host: str, user: str, pwd: str, database: str, port: int = 3306) -> Cursor:
        session_name = f'{host}{user}{pwd}{port}{database}'
        if not cls.__pools.get(session_name):
            cls.__pools[session_name] = PooledDB(
                creator=pymysql,
                maxconnections=5,
                mincached=1,
                maxcached=0,
                blocking=True,
                host=host,
                port=port,
                user=user,
                password=pwd,
                database=database,
                charset='utf8mb4',
            )
        return cls.__pools.get(session_name).connection().cursor()
