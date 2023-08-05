from typing import List
import pandas as pd

from rrdata.utils.rqTusharepro import pro
from rrdata.utils.rqDate_trade import rq_util_get_last_tradedate
from rrdata.utils.rqCode import rq_util_str_tounitecode


def fetch_stock_basic_all_tspro()-> pd.DataFrame:    
    stock_list_l= pro.stock_basic(exchange_id='', is_hs='',list_status='L' , fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')  
    stock_list_D= pro.stock_basic(exchange_id='', is_hs='',list_status='D' , fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')  
    stock_list_P= pro.stock_basic(exchange_id='', is_hs='',list_status='P' , fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')          
    stock_list=pd.concat([stock_list_l,stock_list_D],axis=0)
    stock_list=pd.concat([stock_list,stock_list_P],axis=0)
    return stock_list



def fetch_delist_stock(trade_date=None) -> List:
    df_P = pro.stock_basic(exchange='',list_status='P',fields='ts_code,symbol,name,list_status,delist_date,list_date')
    df_D = pro.stock_basic(exchange='',list_status='D',fields='ts_code,symbol,name,list_status,delist_date,list_date')
    df_DP = pd.concat([df_P, df_D], axis=0)
    df_DP['code'] = df_DP['ts_code'].apply(lambda x: x[0:6])
    if not trade_date:
        trade_date = rq_util_get_last_tradedate().replace('-','')
    df_DD = df_DP[df_DP['delist_date'] <= trade_date]
    df_DD_code = list(df_DD['code'].values)
    return df_DD_code


def fetch_stock_list(trade_date=None,ts_code=True) -> List:
    df_L= pro.stock_basic(exchange_id='', is_hs='',list_status='L') # , fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')  
    #stock_list_P= pro.stock_basic(exchange_id='', is_hs='',list_status='P' , fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')          
    #stock_list=pd.concat([stock_list_l,stock_list_P],axis=0)
    if ts_code:
        return list(df_L['ts_code'].values)
    else:
        df_L['code'] = df_L['ts_code'].apply(lambda x: x[0:6])
        print(f"stock list nums: {len(df_L)}")
        return list(df_L['code'].values)


if __name__ == "__main__":
    print(fetch_delist_stock())
    print(fetch_stock_basic_all_tspro())
    print(len(fetch_stock_list()))


