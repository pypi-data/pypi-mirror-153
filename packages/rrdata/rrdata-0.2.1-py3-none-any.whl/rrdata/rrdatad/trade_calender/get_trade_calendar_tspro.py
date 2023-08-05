import tushare as ts
import pandas

from rrdata.utils.rqSetting import setting


def get_trade_calender_sse() -> pandas.DataFrame:
    token =  setting['TSPRO_TOKEN']
    pro = ts.pro_api(token=token)
    return pro.trade_cal(exchange='SSE', start_date='20050101', end_date='20251231')


if __name__ == '__main__':
    trade_date_sse = get_trade_calender_sse()
    print(trade_date_sse)