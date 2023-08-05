import tushare as ts
import pandas as pd

from rrdata.utils.rqLogs import rq_util_log_info
from rrdata.rrdatad.stock import pro
#from rrdata.rrdatad.stock.fetch_stock_list import fetch_stock_list_tusharepro
from rrdata.common import save_df_to_pgsql


def save_stock_list_to_pgsql(table_name="stock_list"):
    stock_list_l= pro.stock_basic(exchange_id='', is_hs='',list_status='L' , fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')  
    #stock_list_D= pro.stock_basic(exchange_id='', is_hs='',list_status='D' , fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')  
    stock_list_P= pro.stock_basic(exchange_id='', is_hs='',list_status='P' , fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')          
    #stock_list=pd.concat([stock_list_l,stock_list_D],axis=0)
    stock_list=pd.concat([stock_list_l,stock_list_P],axis=0)
    #stock_list = stock_list_l
    stock_list['code']=stock_list['symbol']
    #rq_util_log_info(stock_list)
    try:
        save_df_to_pgsql(stock_list, table_name, db_name="rrdata")
        #print(len(stock_list))
    except Exception as e:        
        print(e)
    return stock_list

if __name__ == '__main__':
    print(save_stock_list_to_pgsql('stock_list_test'))
    from rrdata.rrdatac.rrdataD_read_api import RrdataD
    print(RrdataD('stock_list_test').read().columns)   