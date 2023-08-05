# coding:utf-8
import asyncio
import asyncpg
import psycopg2
from rrdata.utils.config_setting import setting


host = setting['IP_DATABASE_ALIYUN']
db_name = setting["DATABASE"]
passwd = setting["PGSQL_PASSWORD"]
uri = f'postgresql://postgres:{passwd}@{host}:5432/{db_name}'

# connect client
def rq_util_sql_postgres_setting(uri=uri):
    # 使用uri代替ip,port的连接方式
    # 这样可以对postgresql进行加密:
    # uri=postgresql://user:passwor@ip:port/daatbase
    client = psycopg2.connect(uri)
    #print(client)
    return client


if __name__ == '__main__':
    # test client
    print(rq_util_sql_postgres_setting())

