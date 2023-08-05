from sqlalchemy import create_engine
import pandas as pd
import tempfile

import rrdata.rrdatad.index as index
from rrdata.utils.rqLogs import rq_util_log_info, rq_util_log_expection
from rrdata.utils.rqSetting import setting
from rrdata.common import engine


def read_df_from_table(table_name, con=engine()):
    """read whole table all dataframe from eginee() """
    try:
        df = pd.read_sql(table_name, con)
        rq_util_log_info(f"Read dataframe: {len(df)} rows from Table:<{table_name}> from {con} \n{df}")
        return df
    except Exception as e:
        rq_util_log_expection(e)


def read_datas_from_table(sql_query, con=engine()):
    """sql_query= f'SELECT * FROM {table_name} WHERE trade_date BEETWIN start_date, end_date ' """
    try:
        df = pd.read_sql_query(sql_query, con)
        rq_util_log_info(f"Read dataframe: {len(df)} rows from Table from {con} \n{df}")
        return df
    except Exception as e:
        rq_util_log_expection(e)


def read_large_df_from_table(sql_query, con=engine()):
    """    pandas has a built-in chunksize parameter 
    that you can use to control this sort of thing
    """
    dfs = []
    for chunk in pd.read_sql_query(sql_query, con, chunksize=5000):
        dfs.append(chunk)
    df = pd.concat(dfs)
    rq_util_log_info(df())
    return df 


def read_sql_tmpfile(query, con=engine()):
    with tempfile.TemporaryFile() as tmpfile:
        copy_sql = "COPY ({query}) TO STDOUT WITH CSV {head}".format(
           query=query, head="HEADER"
        )
        connect = con.raw_connection()
        cur = connect.cursor()
        cur.copy_expert(copy_sql, tmpfile)
        tmpfile.seek(0)
        df = pd.read_csv(tmpfile)
        rq_util_log_info(df)
        return df


if __name__ == '__main__':
    #for t in ['swl_cons_L1','swl_cons_L2','swl_cons_L3']:
    #    read_df_from_table(t)

    #sql_query = 'SELECT * FROM swl_list'
    #read_large_df_from_table(sql_query)
    #read_sql_tmpfile(sql_query, engine)
    #read_df_from_table('stock_spot', con=engine(db_name="rrdata"))
    table_name = "stock_day_test"
    start_date = "2022-05-11"
    end_date = "2022-05-17"
    sql1 = f"""
        SELECT ts_code, trade_date, close, chg_pct 
        FROM {table_name}
        WHERE trade_date BETWEEN  '{start_date}' AND '{end_date}';
    """
    read_datas_from_table(sql1)
