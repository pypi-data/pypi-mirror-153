# coding: utf-8
import pandas as pd
import numpy as np
import time
import datetime
import tushare as ts
import easyquotation as eq
import warnings
warnings.filterwarnings("ignore")

from rrdata.utils.rqLogs import (rq_util_log_debug, rq_util_log_expection,
                                     rq_util_log_info)
from rrdata.utils.rqCode import (rq_util_code_tosrccode, rq_util_code_tostr)
from rrdata.utils.rqDate import rq_util_date_str2int,rq_util_date_int2str,rq_util_date_today
from rrdata.utils.rqDate_trade import ( trade_date_sse,
                            rq_util_get_last_tradedate,rq_util_get_trade_range)
from rrdata.rrdatad.stock.fetch_stock_basic_tspro import fetch_delist_stock, fetch_stock_list
from  rrdata.rrdatad.stock.tusharepro import pro

PERIODS=[5,20,60,120,250]


def fetch_stock_spot_from_easyquotation(src='sina'):
    """if today is trade date trade_date = today
        else trade_date = last trade_date
        time: 9:30-11:31 , 13:00-15:03
        easyquotation as eq with stick_list
    """
    
    trade_date = rq_util_date_today() if rq_util_date_today().strftime('%Y-%m-%d') \
        in trade_date_sse else  rq_util_get_last_tradedate()
    trade_date = str(trade_date).replace('-','')
    quotation = eq.use(src)
    secs_eq = list(map(lambda x: x[0:6], fetch_stock_list()))
    price_all = quotation.stocks(secs_eq)
    df_p = pd.DataFrame(price_all).T.reset_index()
    df_p = df_p[['index','name', 'close','now','open','high','low','turnover','volume','date','time']]
    df_p = df_p.loc[df_p['volume'] > 0]
    df_p['pct_chg'] = (100*(df_p['now']/df_p['close'] - 1)).map(lambda x:round(x,2))
    df_p['avg'] = df_p['volume']/df_p['turnover']
    df_p = df_p.rename(columns={'index':'code','close':'pre_close', 'now':'close','turnover':'vol','volume':'amount'})
    df_p = df_p.sort_values(by='code')
    for i in ['vol', 'amount']:
        df_p[i] = (df_p[i]/100.00).apply(lambda x: round(float(x), 2))
    df_p.fillna({'pct_chg':0,'vol':0,'amount':0}, inplace=True)
    return df_p


if __name__ == "__main__":
    print(fetch_realtime_price_stock_day())
  