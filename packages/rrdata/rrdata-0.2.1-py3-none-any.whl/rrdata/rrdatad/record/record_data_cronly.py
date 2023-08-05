import time

from rrdata.common import engine
from rrdata.rrdatad.rrdataD_save_api import RrdataDSave
from rrdata.rrdatad.stock.fetch_stock_list import fetch_stock_list_tusharepro
from rrdata.rrdatad.stock import stock_zh_a_spot_em

def record_trade_cal_sse():
    from rrdata.rrdatad.trade_calender.get_trade_calendar_tspro import get_trade_calender_sse
    data = get_trade_calender_sse
    RrdataDSave('trade_cal_sse', engine(db_name="rrdata"))
    

def record_stock_list():
    data = fetch_stock_list_tusharepro
    RrdataDSave('stock_list', engine(db_name="rrdata"))


def record_stock_stock_spot_em():
    data = stock_zh_a_spot_em()
    data.sort_values(by="chg_pct", ascending=False,inplace=True)
    print(data)

    while 1:
        RrdataDSave('stock_spot').save(data)
        time.sleep(20)
        
def record_swl_list():
    pass




if __name__ == '__main__':
    record_trade_cal_sse()
    

