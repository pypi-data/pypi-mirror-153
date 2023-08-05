import psycopg2
from sqlalchemy import create_engine

from rrdata.utils.rqLogs import rq_util_log_info
from rrdata.utils.rqSetting import setting

host = setting["IP_DATABASE_ALIYUN"]
passwd = setting["PGSQL_PASSWORD"]
database_str = f"postgres:{passwd}@{host}:5432"
database_dns = f"postgresql://postgres:{passwd}@{host}:5432"
#rq_util_log_info(database_dns)


def engine(driver="psycopg2", db_name="rrdata"):
    database_uri_str = f"{database_str}/{db_name}"
    if not driver:
        database_uri = f"postgresql://{database_uri_str}"
        #rq_util_log_info(database_uri)
        conn = create_engine(database_uri)
    elif driver == "psycopg2":
        conn = create_engine(f"postgresql+{driver}://{database_str}/{db_name}")
    return conn
   

if  __name__ == "__main__":
    rq_util_log_info(engine(db_name='rrdata'))
   
        