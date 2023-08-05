import pandas as pd

import tushare as ts
from rrdata.rrdatad.stock.tusharepro import pro

startD = '20200101'

df_tradedate = pro.daily(trade_date='20220518')
print(df_tradedate)

df_hfq_adj_one = ts.pro_bar(ts_code='600519.SH', start_date=startD, adj='hfq', adjfactor=True).sort_values(by="trade_date", ascending=True)
print(df_hfq_adj_one)

df_adj_one = df_hfq_adj_one[['trade_date','ts_code','adj_factor']].sort_values(by="trade_date", ascending=True)

print(df_adj_one)