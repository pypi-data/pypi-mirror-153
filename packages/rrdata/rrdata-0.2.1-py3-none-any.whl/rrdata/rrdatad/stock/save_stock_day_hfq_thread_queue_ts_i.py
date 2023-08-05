# coding: utf-8
"""multi theard use threading.Thread and queue.Queue;
    pipline -- queue(q=queue.Queue);
    first q.put(id)  then queue.get()=id ;
    NUM_THREADS  decide by api speed limit(200/mins) and id totoals : lists // speed_per_mins
    every thead group num -- lists // NUM_TREADS
    开 NUM_TREADS 条线程， 每个线程有 NUM 项任务。
    API 速度限制： 60秒 - 200条请求的时间  --> time.sleeep(x) (if x > 0).
    TODO: hot to use many tspro_token auto change. get count of api bar_pro   
"""
import queue
import threading
import time

from rrdata.rrdatac.rrdataD_read_api import RrdataD
from rrdata.rrdatad.rrdataD_save_api import RrdataDSave
from rrdata.rrdatad.stock.fetch_stock_day import fetch_stock_list_tspro
from rrdata.utils.rqSetting import setting
from rrdata.utils.rqParameter import startDate

# daily: ts.pro_bar(ts_code=ts_code, asset="E", adj='hfq', start_date=startDate, end_date=None,adjfactor=True)
import tushare as ts1 
import tushare as ts2

try:
    token1 = setting['TSPRO_TOKEN']
    ts1.set_token(token1)
    pro1 = ts1.pro_api()
    #print('tushare token set ok , can use pro as api!')
except Exception as e:
    print(e)

try:
    token2 = setting['TSPRO_RBOBO']
    ts2.set_token(token2)
    pro2 = ts2.pro_api()
    #print('tushare token set ok , can use pro as api!')
except Exception as e:
    print(e)

q = queue.Queue()
workers = []
NUM_THREADS = 3


df = RrdataD('stock_list').read()
df = df.sort_values(by="symbol").head(450)
print(len(df))
stock_list = df.ts_code.values
#print(stock_list)

NUM = len(stock_list) // NUM_THREADS
print(NUM)


def get_stock_day_save_tosql(queue, table_name='stock_day_hfq_test'):
    id = queue.get()
    print(f"get id : -- {id}")
    try:
        ts = ts1 if (id % 2) == 0 else ts2
        data = ts.pro_bar(ts_code=stock_list[id], asset="E", adj='hfq', start_date=startDate, end_date=None,adjfactor=True)
        RrdataDSave(table_name,if_exists='append').save(data)
    except Exception as E:
        print(E)
    


def main():
    for i in range(NUM_THREADS + 1):
        for j in range(NUM):
            worker = threading.Thread(target=get_stock_day_save_tosql, args=(q,))
            worker.start()
            workers.append(worker)
            if (i * NUM + j) >= len(stock_list) :
                break
       
    for i in range(NUM_THREADS + 1):
        t1 = time.perf_counter()
        for j in range(NUM):
            id = i * NUM + j 
            q.put(id)
            #print(id)
            if (id + 2)  >  len(stock_list):
                break
            else:
                continue
        t = time.perf_counter() - t1
        print(t)
     
        if (t < 60): 
            time.sleep(60 - t)
        else:
            continue
      
    for w in workers:
        w.join()
        

if __name__ == "__main__":
    main()
   
    #print(RrdataD('stock_day_hfq_test').read(instruments='000792.SZ'))