import time
import pandas as pd


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


def fetch_stock_daily_hfq_one_tspro(ts_code='600519.SH',asset="E", adj='hfq', start_date=None, end_date=None,adjfactor=True):
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


def save_stock_day_hfq_to_pgsql(stock_list=None,start_date=startDate,table_name='stock_day_hfq'):
    """two factor: ts_coe /trade_date
       TODO suspased to fillna by trade_date / ipo date < startDate / 
    """
    #lists = read_df_from_table('stock_list').symbol.values if None else stock_list
    lists = fetch_stock_list_tspro().ts_code.to_list()
    print(f" stock_list nums: {len(lists)}") # \n {lists[:10]}")
        
    t1 = time.time()
    # check stock_dat_hfq trade_date_sql for update #TODO check for stock_list every one just chang start_date_one to for and change get_wanted...
    start_date_one_list = get_wanted_record_tradedate(row="trade_date",start_date=start_date,table_name=table_name)
    
    if  start_date_one_list:
        start_date_one =  rq_util_date_int2str(max(list(map(lambda x: rq_util_date_str2int(x), start_date_one_list)))) 
        print(start_date_one)
   
        for ts_code in lists:
            try:
                print(ts_code)
                #start_date_one_list = get_wanted_record_tradedate_check_tscode(ts_code,"trade_date",table_name)
                #start_date_one = max(list(map(lambda x: rq_util_date_str2int(x), start_date_one_list))) if  start_date_one_list else last_tradedate
                #print(start_date_one)
                #start_date_one = rq_util_date_int2str(start_date_one)
                data = ts.pro_bar(ts_code=ts_code, start_date=start_date_one, adj='hfq', adjfactor=True)
                save_df_to_pgsql(data,table_name,if_exists='append')
            except Exception as e:
                rq_util_log_expection(e)
    
    else:
        #if start_date_one == last_tradedate:
        print("data is new, do not need update!")
 
    t2 = time.time()
    print(f"times: {t2 - t1}")


def save_stock_day_bfq_to_pgsql(start_date=startDate, table_name="stock_day_bfq"):
    end_date = rq_util_get_last_tradedate()
    try:
        trade_data_pg = RrdataD(table_name).read(fields=['trade_date']).trade_date.to_list() 
    except: 
        #第一次运行
        trade_data_pg = []
    finally:
        trade_date_sql = trade_data_pg
    print(f"sql_trade_date nums:{len(trade_date_sql)}, like :{trade_date_sql[-1:]}")  # read trade_adte from stock_day_bfq 
    trade_date = list(map(lambda x: x.replace("-",""), rq_util_get_trade_range(start_date, end_date)))  # TODO
    print(len(trade_date))
    trade_date2=list(set(trade_date).difference(set(trade_date_sql)))  #差集 trade_date in / not in trade_date_sql
    # trade_date2 = [x for x in trade_date if x not in trade_date_sql]
    trade_date2.sort()
    print(f" -- diff  want to add trade_date : {trade_date2}")
    
    if len(trade_date2)==0:
        print('Stock day is up to date and does not need to be updated')
    for i in trade_date2:
        #print(i)
        try:
            t=time.time()        
            df=fetch_stock_day_bfq_from_tspro(trade_date=i.replace("-",""))  
            #print(df)
            save_df_to_pgsql(df, f'{table_name}',if_exists='append')
            t1=time.time()   
            print(f"save {i} stock day bfq to table: <{table_name}> success,take '+str(round(t1-t,2))+' S")        
        except Exception as e:
            print(e)


def fetch_stock_day_adj_change(trade_date=rq_util_get_last_tradedate().replace("-","")): #TODO
    """for one stock ---ts_code
    last_preclose = df.pre_close.values[-1]
    before_close = df.shift().close.values[-1]
    if last_preclose != before_clode:
        update adjfactor
    else:
        fill with new adjfactor
    """
    df_last = fetch_stock_day_bfq_from_tspro(trade_date=trade_date)
    pass

def caculate_one_stock_ma_rt_oh_volchg_from_stockhfq(ts_code='000792.SZ'):
    df = RrdataD('stock_day_hfq').read(instruments=ts_code)
    print(df)
    df['ma_5'] = df.pct_chg.sum()
    print(df)
    
    pass


if  __name__ == "__main__":
    #print(fetch_stock_daily_hfq_one_tspro('600060.SH'))
    #print(fetch_stock_daily_adjfactor_one())
    #print(fetch_stock_day_bfq_from_tspro(trade_date="20220518"))
    #save_stock_day_bfq_to_pgsql() 
           
    #df = RrdataD('stock_day_hfq').read(instruments='600519.SH')
    #print(df)
    
    #save_stock_day_bfq_to_pgsql()
  
    #df = RrdataD('stock_day_bfq').read(instruments=['000792.SZ'])
    #print(df)
    #df = RrdataD('stock_list',engine(driver="", db_name="rrshare")).read(instruments=['000792.SZ'])
    #print(df)
    #print(read_df_from_table("stock_day"))
    t1 = time.perf_counter()
    df = RrdataD('stock_day_hfq',engine(driver="", db_name="rrddata")).read(start_date=last_tradedate)
    print(df)
    #caculate_one_stock_ma_rt_oh_volchg_from_stockhfq()
    save_stock_day_bfq_to_pgsql() 
    #save_stock_day_hfq_to_pgsql()
    save_stock_day_hfq_to_pgsql()
    t2 = time.perf_counter()
    t = t2 - t1
    print(f"times:  --- {t}")
    
    pass


