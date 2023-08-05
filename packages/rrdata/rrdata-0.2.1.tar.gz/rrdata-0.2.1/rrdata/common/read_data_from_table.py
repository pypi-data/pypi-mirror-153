import pandas as pd

from rrdata.common.engine_pgsql import engine
from rrdata.utils.rqLogs import rq_util_log_info, rq_util_log_expection


def read_rows_from_table(sql_query, con=engine()) -> pd.DataFrame:
    """sql_query= f'SELECT row  FROM {table_name} WHERE trade_date BEETWIN start_date, end_date ' """
    try:
        df = pd.read_sql_query(sql_query, con)
        rq_util_log_info(f"Read dataframe: {len(df)} rows from Table from {con} \n{df}")
        return df
    except Exception as e:
        rq_util_log_expection(e)
        
        
def read_one_row_from_table(row="trade_date",table_name=None, con=engine()) -> pd.Series:
    """sql_query= f'SELECT row  FROM {table_name} WHERE trade_date BEETWIN start_date, end_date ' """
    try:
        sql_query = f"SELECT DISTINCT {row} FROM {table_name};"
        cols = pd.read_sql_query(sql_query, con)[f'{row}'].to_list()
        #cols = list(map(lambda x: x.replace("-",""), cols))
        cols.sort()
        rq_util_log_info(f"Read column: {len(cols)} rows from table <{table_name}> on {con}")
        return cols
    except Exception as e:
        rq_util_log_expection(e)
    
        
def read_one_row_from_table_check_tscode(ts_code="600519.SH", row="trade_date",table_name=None, con=engine()) -> pd.Series:
    try:
        try:
            sql_query = str(f"SELECT DISTINCT {row} FROM {table_name} WHERE ts_code = '{ts_code}';");
            #print(sql_query)
            cols = pd.read_sql_query(sql_query, con)[f'{row}'].to_list()
            #cols = list(map(lambda x: x.replace("-",""), cols))
            cols.sort()
            rq_util_log_info(f"Read column: {len(cols)} rows from table <{table_name}> on {con}")
            #return cols
        except:
            cols = []
        finally:
            #print(cols)
            return cols            
    except Exception as e:
        rq_util_log_expection(e)


if __name__ == "__main__":
    
    read_one_row_from_table_check_tscode(ts_code="000002.SZ",row="trade_date",table_name="stock_day_hfq", con=engine())
    read_one_row_from_table(row="trade_date",table_name="stock_day_bfq", con=engine())
    