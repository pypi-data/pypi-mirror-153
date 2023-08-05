
from typing import List
import pandas as pd

from rrdata.rrdatad.stock.tusharepro import pro
from rrdata.rrdatad.stock.stock_hist_em import  code_id_map_em
from rrdata.utils.rqCode import rq_util_str_tounitecode

def fetch_stock_list_tusharepro()-> pd.DataFrame:    
    stock_list_l= pro.stock_basic(exchange_id='', is_hs='',list_status='L' , fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')  
    stock_list_D= pro.stock_basic(exchange_id='', is_hs='',list_status='D' , fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')  
    stock_list_P= pro.stock_basic(exchange_id='', is_hs='',list_status='P' , fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs')          
    stock_list=pd.concat([stock_list_l,stock_list_D],axis=0)
    stock_list=pd.concat([stock_list,stock_list_P],axis=0)
    return stock_list


def fetch_stock_code_em(ts_code=False) -> List: #TODO
    """  get stock list from em out -- dict"""
    dicts =code_id_map_em()
    #df = pd.DataFrame.from_dict(dicts,orient='index')
    lists = list(dicts.keys())
    #print(type(lists))
    lists = list(map(lambda x: rq_util_str_tounitecode(x), lists)) if ts_code else lists
    return lists


if __name__ == '__main__':
    print(fetch_stock_list_tusharepro())
   
