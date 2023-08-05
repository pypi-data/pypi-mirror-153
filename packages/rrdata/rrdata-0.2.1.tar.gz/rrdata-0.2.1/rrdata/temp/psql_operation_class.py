#!/usr/bin/python
import  psycopg2

from rrdata.utils.config_postgresql import get_config_ini
from rrdata.utils.rqLogs import rq_util_log_info, rq_util_log_expection

db_name_rrdata = "pgsql_rrdata"

class PgsqlClass(object):

    def __init__(self,
            db_name=db_name_rrdata
            ):
        self.db_name=db_name
        self.params =get_config_ini(section=db_name)


    def create_tables(self, sql):
        """ create tables in the PostgreSQL database"""
        conn = None
        try:
            # read the connection parameters
            #params = get_config_ini(section=self.db_name)
            # connect to the PostgreSQL server
            with psycopg2.connect(**self.params) as conn:
                rq_util_log_info(conn)
                cur = conn.cursor()
                # create table one by one
                cur.execute(sql)
                # close communication with the PostgreSQL database server
                cur.close()
                # commit the changes
                conn.commit()
                rq_util_log_info(f"create table use cli: {sql}")
        except (Exception, psycopg2.DatabaseError) as error:
            rq_util_log_expection(error)


    def insert_one(self,sql_one,table_name):
        pass


    def insert_lists(self, sql_lists,table_name):
        pass


    def update(self):
        pass


    def fetchone(self):
        pass


    def fetchall(self, table_name='cities'):
        conn = None
        try:
            with psycopg2.connect(**self.params) as conn:
                cur = conn.cousor()
                cur.execute("""
                
                """)
                cur.close()
                cur.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            rq_util_log_expection(error)

    

if  __name__ == '__main__':
    psql = PgsqlClass()
    sql="""
        DROP TABLE IF EXISTS cities;
        CREATE TABLE IF NOT EXISTS cities (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            population INT NOT NULL
        )
        """
    psql.create_tables(sql)
