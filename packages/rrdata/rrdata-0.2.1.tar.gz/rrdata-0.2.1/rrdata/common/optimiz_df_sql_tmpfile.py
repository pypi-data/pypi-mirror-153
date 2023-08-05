#!/usr/bin/python
import pandas
import tempfile
from sqlalchemy import create_engine

#from rrdata.utils.rqSql import rq_util_sql_postgres_setting
from rrdata.utils.rqSetting import setting
from rrdata.utils.client_postgsql import get_config_ini
from rrdata.utils.rqLogs import rq_util_log_info


engine = get_config_ini(section='pgsql_rrdata')
print(engine)

database_uri = setting['POSTGRESQL']
rq_util_log_info(database_uri)
engine = create_engine(database_uri)
rq_util_log_info(engine)


def read_sql_tmpfile(query, db_engine):
    """ db_engine must create_engine("postgresql://host/dbname")
    """
    with tempfile.TemporaryFile() as tmpfile:
        copy_sql = "COPY ({query}) TO STDOUT WITH CSV {head}".format(
           query=query, head="HEADER"
        )
        conn = db_engine.raw_connection()
        cur = conn.cursor()
        cur.copy_expert(copy_sql, tmpfile)
        tmpfile.seek(0)
        df = pandas.read_csv(tmpfile)
        return df

if  __name__ == '__main__':
    query = """ SELECT * FROM swl_list
  
    """
    df = read_sql_tmpfile(query,engine)
    print(df)
