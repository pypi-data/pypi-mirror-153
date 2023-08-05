from rrdata.utils.rqDate_trade import rq_util_get_last_tradedate, rq_util_get_trade_range, rq_util_get_pre_trade_date
from rrdata.common import read_rows_from_table
from rrdata.common import engine
from rrdata.common.read_data_from_table import read_one_row_from_table, read_one_row_from_table_check_tscode
from rrdata.utils.rqParameter import startDate

#startDate = "20210428"  #rq_util_get_pre_trade_date(rq_util_get_last_tradedate(), 255)
#print(startDate)

def get_wanted_record_tradedate(row="trade_date",table_name=None,start_date=startDate, con=engine(db_name='rrdata')):
    last_tradede = rq_util_get_last_tradedate()
    try:
        trade_date_pg = read_one_row_from_table(row, table_name)
    except:
        trade_date_pg =[]
    finally:
        trade_date_sql = trade_date_pg
    print(f"table_tradedate_sql : {trade_date_sql[:3]}---{trade_date_sql[-3:]}")
    trade_date = rq_util_get_trade_range(start_date, last_tradede)
    trade_date = list(map(lambda x: x.replace("-",""), trade_date))
    #print(f"trade_cal_date nums: {len(trade_date)} and last five: {trade_date[-5:]}")
    trade_date_diff = list(set(trade_date).difference(set(trade_date_sql)))
    #trade_date_diff = [x for x in trade_date if x not in trade_date_sql]
    trade_date_diff.sort()
    print(f"diff date:  {trade_date_diff}, {len(trade_date_diff)}")
    return trade_date_diff


def get_wanted_record_tradedate_check_tscode(ts_code="600519.SH",row="trade_date",table_name=None,start_date=startDate, con=engine(db_name='rrdata')):
    last_tradede = rq_util_get_last_tradedate()
    try:
        trade_date_pg = read_one_row_from_table_check_tscode(ts_code,row, table_name)
    except:
        trade_date_pg =[]
    finally:
        trade_date_sql = trade_date_pg
    #print(f"table_tradedate : {trade_date_sql}")
    trade_date =  rq_util_get_trade_range(start_date, last_tradede)
    trade_date = list(map(lambda x: x.replace("-",""), trade_date))
    #trade_date.sort()
    #print(f"trade_cal_date: {trade_date[-5:]}")
    trade_date_diff = list(set(trade_date).difference(set(trade_date_sql)))
    #trade_date_diff = [x for x in trade_date if x not in trade_date_sql]
    trade_date_diff.sort()
    print(f"diff date:  {trade_date_diff[:2]}  --  {trade_date_diff[-2:]}")
    return trade_date_diff


if __name__ == '__main__':
    read_one_row_from_table('trade_date','stock_day_test')
    #list_diff = get_wanted_record_tradedate(row="trade_date",table_name="stock_day_test")
    #print(len(list_diff))
    get_wanted_record_tradedate('trade_date','stock_day_hfq')
    get_wanted_record_tradedate_check_tscode('000002.SZ','trade_date','stock_day_bfq')

