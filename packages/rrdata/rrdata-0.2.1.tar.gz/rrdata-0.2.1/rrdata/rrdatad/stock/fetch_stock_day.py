import time
import pandas as pd
from typing import Optional, List,Dict, Tuple

import tushare as ts
from rrdata.rrdatad.stock.tusharepro import pro
from rrdata.utils.rqDate import  rq_util_date_int2str
from rrdata.utils.rqDate_trade import rq_util_get_last_tradedate, rq_util_get_last_day,rq_util_get_pre_trade_date,rq_util_get_trade_range
from rrdata.rrdatad.stock.fetch_stock_list import fetch_stock_code_em
from rrdata.utils.rqCode import rq_util_str_tounitecode
from rrdata.utils.rqLogs import rq_util_log_debug, rq_util_log_info, rq_util_log_expection
from rrdata.utils.rqDate import rq_util_date_str2int
from rrdata.common import save_df_to_pgsql, read_df_from_table,read_data_from_table, engine
from rrdata.common.get_update_tradedate import get_wanted_record_tradedate, get_wanted_record_tradedate_check_tscode

from rrdata.common.read_data_from_table import read_one_row_from_table, read_one_row_from_table_check_tscode
from rrdata.rrdatac.rrdataD_read_api import RrdataD
from rrdata.utils.rqParameter import startDate


#startDate = "2021-04-28"
last_tradedate = rq_util_get_last_tradedate().replace("-","")
#startDate = rq_util_get_pre_trade_date(rq_util_get_last_tradedate(),255).replace("-","")
print(last_tradedate, startDate)


def fetch_stock_list_tspro()-> pd.DataFrame:
    stock_list_l= pro.stock_basic(exchange_id='', is_hs='',list_status='L' , fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')  
    #stock_list_D= pro.stock_basic(exchange_id='', is_hs='',list_status='D' , fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')  
    stock_list_P= pro.stock_basic(exchange_id='', is_hs='',list_status='P' , fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')          
    #stock_list=pd.concat([stock_list_l,stock_list_D],axis=0)
    stock_list=pd.concat([stock_list_l,stock_list_P],axis=0)
    #stock_list = stock_list_l
    stock_list['code']=stock_list['symbol']
    #rq_util_log_info(stock_list)
    return stock_list


def fetch_stock_daily_hfq_one_tspro(ts_code='600519.SH',asset="E", adj='hfq', start_date=startDate, end_date=None,adjfactor=True):
    return ts.pro_bar(ts_code=ts_code, asset=asset,adj=adj, start_date=start_date, end_date=end_date, adjfactor=adjfactor) 


def fetch_stock_daily_adjfactor_one(symbol="600519", period="daily",start_date=startDate, end_date="20321231", adj="hfq", adjfactor=True):
    """  from tushare pro ts.pro_bar(adj="hfq', adjfactor=True)"""
    ts_code = rq_util_str_tounitecode(symbol)
    df_hfq_adj_one = ts.pro_bar(ts_code=ts_code, start_date=startDate, adj=adj, adjfactor=adjfactor)
    return df_hfq_adj_one[['trade_date','ts_code','adj_factor']]
    

def fetch_stock_day_bfq_from_tspro(ts_code=None,trade_date=rq_util_get_last_tradedate().replace("-",""),start_date=None,end_date=None):   
    trade_date = trade_date.replace('-', '') #兼容设置以防日期格式为2001-10-20格式
    for _ in range(3):
        try:
            if trade_date:
                df = pro.daily(ts_code=ts_code, trade_date=trade_date)
            else:
                df = pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        except:
            time.sleep(1)
        else:
            return df

if  __name__ == "__main__":
    #print(fetch_stock_daily_hfq_one_tspro('600060.SH'))
    #print(fetch_stock_daily_adjfactor_one())
    #print(fetch_stock_day_bfq_from_tspro(trade_date="20220518"))
           
    #print(read_df_from_table("stock_day"))
    t1 = time.perf_counter()
    print(fetch_stock_list_tspro())
    print(fetch_stock_daily_hfq_one_tspro('600519.SH'))
    t2 = time.perf_counter()
    t = t2 - t1
    print(f"times:  --- {t}")
    
    pass


