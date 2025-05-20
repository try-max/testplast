import pymysql
# 数据库连接配置信息

from dbutils.pooled_db import PooledDB

from app.conf.dbConfig import getMysqlSetting

config = getMysqlSetting()


class DbConnectionPool:
    def __init__(self):
        self.pool = PooledDB(
            creator=pymysql,
            maxconnections=20,
            mincached=2,
            maxcached=5,
            blocking=True,
            setsession=[],
            ping=0,
            **config
        )

    def create_conn(self):
        """获取连接和游标"""
        conn = self.pool.connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        return conn, cursor

    def close_conn(self, conn, cursor):
        """归还连接和关闭游标"""
        if cursor:
            cursor.close()
        if conn:
            conn.close()  # 关键：归还到连接池

# 全局连接池实例
dbconnectionpool = DbConnectionPool()
