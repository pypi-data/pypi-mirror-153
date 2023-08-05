from rrdata.rrdatac.rrdataD_read_api import RrdataD
from rrdata.utils import rq_util_get_last_tradedate, rq_util_get_pre_trade_date


count = 5
last_tradedate = rq_util_get_last_tradedate()
start_date = rq_util_get_pre_trade_date(last_tradedate, count)

#print(RrdataD("adj_factor").read(instruments="000792.SZ,600519.SH,000002.SZ,000001.SZ",\
#      start_date='2022-05-17',end_date=rq_util_get_last_tradedate()))
#print(RrdataD("adj_factor").read(start_date='2022-05-16'))
print(RrdataD("stock_day_hfq").read(start_date=last_tradedate,fields="trade_date,ts_code,adj_factor"))

