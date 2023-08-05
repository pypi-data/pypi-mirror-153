# see MyTT in github : mpquant/MyTT

# import modules
import pandas as pd
#from MyTT import *
from rrdata.utils.rqDate_trade import rq_util_get_pre_trade_date, rq_util_get_last_tradedate
from rrdata.rrdatac.rrdataD_read_api import RrdataD 
# get data -- df(price)

# indicator
def MA(S,N):
    return pd.Series(S).rolling(N).mean().values

df = RrdataD("stock_day_hfq").read(instruments="000792.SZ", \
    start_date=rq_util_get_pre_trade_date(rq_util_get_last_tradedate(), 120) )
#stock.get_price(code, count=120,frequency='1d')
CLOSE=df.close.values


MA5 = MA(CLOSE,5)
print(MA5)
