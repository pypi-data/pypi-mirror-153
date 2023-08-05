# -*- coding: utf-8 -*-
from operator import index
import time
import pandas as pd
import psycopg2
from sqlalchemy import create_engine, engine_from_config
#import logging

from rrdata.utils.rqSingleton import  ConSqlDb
from rrdata.utils.rqLogs import (rq_util_log_debug, rq_util_log_expection,
                                             rq_util_log_info)
from rrdata.utils.rqDate_trade import (rq_util_get_trade_range, rq_util_get_last_tradedate, 
                        rq_util_get_pre_trade_date, setting)


password_pgsql = setting['PGSQL_PASSWORD']
host_db_ip = setting['IP_DATABASE_ALIYUN']
port_psql = 5432

class PgsqlOperation(object):
    """
    user/password: postgres
    host_default='127.0.0.1'
    host_database_server='39.108.68.163'
    port_default=5432
    execute:
    CREATE DATABASE db_name;
    DROP DATABASE [ IF EXISTS ] db_name;
    CREATE TABLE table_name(
   column1 datatype,
   column2 datatype,
   .....
   columnN datatype,
   PRIMARY KEY( 一个或多个列 )
);
    DROP TABLE table_name;
    PostgreSQL 模式（SCHEMA）:允许多个用户使用一个数据库并且不会互相干扰。
    CREATE SCHEMA myschema.mytable (
...
);
    create table myschema.table_name()
    DROP SCHEMA myschema;
    https://www.runoob.com/postgresql/postgresql-insert-into.html

use sqlalchemy:

from sqlalchemy import create_engine
engine = create_engine("postgresql+psycopg2://scott:tiger@host/dbname")
    
https://docs.sqlalchemy.org/en/14/dialects/postgresql.html
To set using per-connection execution options:

with engine.connect() as conn:
    conn = conn.execution_options(
        isolation_level="REPEATABLE READ"
    )
    with conn.begin():
        # ... work with transaction
    """

def create_psqlDB(db_name=None):
        try:
            conn = psycopg2.connect(user='postgres',
                                    database='postgres',
                                    password=password_pgsql,
                                    host=host_db_ip, 
                                    port=port_psql)
            #print(conn)
            psql = f'''CREATE DATABASE {db_name}'''
            #OWNER {self.user};
            #        GRANT ALL PRIVILEGES ON DATABASE {db_name}  to {self.user};
            #        '''
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute(psql)
            #conn.commit()
            print(f'database {db_name} created successfully use by user postgres')
            #cursor.close()
            conn.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print('Error while create PostgresSQL database', error)

class PgsqlClass(ConSqlDb):
    """ postgresql operation:
        first connect database uri from config.json;
        execute database 
    """  

    def __init__(self):
        self.user =  'postgres'
        self.password = password_pgsql
        self.host = host_db_ip
        self.port = 5432
        # self.engine = create_engine(f'postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}')


    def client_pgsql(self, db_name):
        client = psycopg2.connect(user='postgres',
                                    database=db_name,
                                    password=self.password,
                                    host=self.host, 
                                    port=self.port)
        #client = create_engine(f'postgres+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{db_name}')
        return client


    def create_table(self, db_name, table_name, tsql):
        try:
            conn = self.client_pgsql(db_name=db_name)
            cursor = conn.cursor()
            conn.autocommit = True
            cursor.execute(f"DROP TABLE if EXISTS {table_name}")
            cursor.execute(tsql)
            print(f'{table_name} created  successfully on database {db_name}')
            conn.close()
        except Exception as e:
            print(e)


    def insert_to_psql(self, df,db_name, table_name, if_exists='append'):
        try:
            engine = self.client_pgsql(db_name)
            df.to_sql(name=table_name, con=engine, index=False, if_exists=if_exists)
            print(f'write to database:{db_name} table:{table_name} ok !')
        except Exception as e:
            print(e)


    def save_df_to_pgsql(self, df, table_name, db_name, if_exists='replace'):
        engine = self.client_pgsql(db_name)
        df.to_sql(table_name,client=engine,index=False,if_exists=if_exists)


    def read_psql(self, db_name, table_name):
        engine = self.client_pgsql(db_name=db_name)
        return pd.read_sql_table(table_name,engine)



def client_pgsql(database='rrdata'):
    try:
        client = create_engine(f'postgresql+psycopg2://postgres:{password_pgsql}@{host_db_ip}:{port_psql}/{database}')
        return client
    except Exception as e:
        print(e)     


def save_data_to_postgresql(data,table_name,db_name,if_exists='replace'):
    client = client_pgsql(database=db_name)
    data.to_sql(table_name=table_name,client=client,index=False,if_exists=if_exists)
    

def load_data_from_postgresql(mes='',client=client_pgsql("rrdata")):
    res=pd.read_sql(mes,client)
    return res


def read_data_from_pg(table_name='', client=client_pgsql("rrdata")):
    ''' load all data of table_name
    '''
    res = pd.read_sql_table(table_name, client)
    return res


def read_table_from_pg(table_name='',period=1, client=None):
    '''only select trade_date, can't select columns
        default out lasttradedate data
        period -->int >= 1
    '''
    try: 
        start_date = rq_util_get_pre_trade_date(rq_util_get_last_tradedate(), period-1)
        logging.info(start_date)
        sql = ''.join(['SELECT * FROM ', f'{table_name}', f" WHERE trade_date >= date_trunc('day', timestamp '"+start_date+"') order by trade_date ASC;"])
        logging.info(sql)
        res = pd.read_sql(sql,client)
        logging.info(f'\n {res}')
        return res
    except Exception as e:
        logging.info(e)


def read_sql_from_pg(start_date=None,data=None,table_name=None,client=client_pgsql()):
    '''can select columns and trade_date
    '''
    sql = ''.join(['SELECT ', data, ' FROM ', f'{table_name}', f" WHERE trade_date >= date_trunc('day', timestamp '"+start_date+"') order by trade_date ASC;"])
    #sql= 'select ' + data + ' from ' +table_name+" where trade_date >= date_trunc('day',timestamp '"+start_date+"') order by trade_date ASC;"
    try:
        t=time.time()
        res=pd.read_sql(sql,client)
        t1=time.time()
        tt = t1-t
        logging.info(f'read  data from {table_name} ,take {tt}')
        return res
    except Exception as e:
        logging.error(e)


def read_unique_data_from_pg(cols='*',table_name='',period=1, client=client_pgsql()):
    ''' select trade_date and columns( * is all), data GROUP BY trade_date and _ts_code --> duplicates 
    '''
    try: 
        start_date = rq_util_get_pre_trade_date(rq_util_get_last_tradedate(), period-1)
        logging.info(start_date)
        sql = f"""
        SELECT {cols} 
        FROM  {table_name}
        GROUP BY trade_date, ts_code 
        """        
        logging.info(sql)
        res = pd.read_sql(sql,client)
        logging.info(f'\n {res}')
        return res
    except Exception as e:
        logging.info(e)


if __name__ == '__main__':
    import os
    #create_psqlDB("rralpha")

    psql = PgsqlClass()
    #psql.create_table('rrdata','swl_list', '')
   
    
    """
    path = '/home/rome/rrdata/rrdata/sql'
    file_n = 'stock_day.sql'
    file_path = os.path.join(path, file_n)
    print(file_path)
    with open(file_path, 'r') as f:
        tsql = f.read()
    print(tsql)
    psql.create_table('rrdata','stock_day',tsql)
    """
    #psql2 = PgsqlClass()
    #print(id(psql), id(psql2))
    #psql.client_pgsql(db_name='rrdata')
    
    #print(read_data_from_pg('swl_list'))

    #print(read_table_from_pg(table_name='swl_day',client=client_pgsql('rrdata')))
    
