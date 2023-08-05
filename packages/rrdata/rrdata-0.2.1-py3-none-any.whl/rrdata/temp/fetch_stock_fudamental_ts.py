#import tushare as ts 
#from tushare.stock.fundamental import get_stock_basics

from tushare.util.conns import  api,get_apis, close_apis
#df = get_stock_basics()
#df = ts.get_st_classified()
#df = ts.get_stock_basics("2022-05-27")

print(api())
#close_apis(api())

