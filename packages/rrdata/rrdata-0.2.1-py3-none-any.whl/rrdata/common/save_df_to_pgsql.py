from sqlalchemy import create_engine
import pandas as pd

import rrdata.rrdatad.index as index
from rrdata.utils.rqLogs import rq_util_log_info, rq_util_log_expection
from rrdata.utils.rqSetting import setting
from rrdata.common import engine


def save_df_to_pgsql(data, table_name, db_name='rrdata', if_exists='replace', index=False):
    rq_util_log_info(data)
    try:
        data.to_sql(table_name, con=engine(db_name=db_name), if_exists=if_exists, index=False)
        rq_util_log_info(f"Saved {len(data)} rows to Table:<{table_name}>/DB:<{db_name}>, finish !!!")
    except Exception  as e:
        rq_util_log_expection(e)
        

if  __name__ == '__main__':
    #data = index.sw_index_class_all()
    #save_df_to_pgsql(data,'swl_list')
    #data2 = index.sw_index_cons()
    #save_df_to_pgsql(data2, 'swl_cons')
    data3 = index.sw_index_spot(level="L2")
    save_df_to_pgsql(data3, 'swl_spot_L2') #,db_name='rrshare')





