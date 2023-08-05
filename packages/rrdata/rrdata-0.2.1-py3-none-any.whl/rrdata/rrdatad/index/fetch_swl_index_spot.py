# coding: utf-8
from turtle import clear
import requests
import json
import time
import pandas as pd

SWL1_INDEX = ('801010','801030','801040','801050','801080','801110','801120','801130','801140','801150','801160','801170','801180','801200','801210', \
              '801230','801710','801720','801730','801740','801750','801760','801770','801780','801790','801880','801890','801950','801960','801970','801980')

SWL2_INDEX = ('801012','801014','801015','801016','801017','801018','801032','801033','801034','801036','801037','801038','801039','801043','801044', \
            '801045','801051','801053','801054','801055','801056','801072','801074','801076','801077','801078','801081','801082','801083','801084','801085','801086', \
            '801092','801093','801095','801096','801101','801102','801103','801104','801111','801112','801113','801114','801115','801116','801124','801125','801126', \
            '801127','801128','801129','801131','801132','801133','801141','801142','801143','801145','801151','801152','801153','801154','801155','801156','801161', \
            '801163','801178','801179','801181','801183','801191','801193','801194','801202','801203','801204','801206','801218','801219','801223','801231','801711', \
            '801712','801713','801721','801722','801723','801724','801726','801731','801733','801735','801736','801737','801738','801741','801742','801743','801744', \
            '801745','801764','801765','801766','801767','801769','801782','801783','801784','801785','801881','801951','801952','801962','801963','801971','801972', \
            '801981','801982','801991','801992','801993','801994','801995')

# sw-url
sw_url = "http://www.swsindex.com/handler.aspx"

# sw-payload
swl_payload = {
    "tablename": "swzs",
    "key": "L1",
    "p": "1",
    "where": "",
    "orderby": "",
    "fieldlist": "L1,L2,L3,L4,L5,L6,L7,L8,L11",
    "pagecount": "28",
    "timed": "",
}

# sw-headers
sw_headers = {
    'Accept': 'application/json, text/javascript, */*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Content-Type': 'application/x-www-form-urlencoded',
    'DNT': '1',
    'Host': 'www.swsindex.com',
    'Origin': 'http://www.swsindex.com',
    'Pragma': 'no-cache',
    'Referer': 'http://www.swsindex.com/idx0120.aspx?columnid=8832',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}


def sw_index_spot(level="L1") -> pd.DataFrame:
    """
    申万一，二级行业-实时行情数据
    http://www.swsindex.com/idx0120.aspx?columnId=8833
    :return: 申万一，二级行业-实时行情数据
    :rtype: pandas.DataFrame
    """
    result = []
    if level == 'L1':
        N = 3
        N_pages = 32
        SWL_INDEX = SWL1_INDEX
    elif level == 'L2':
        N= 8
        N_pages = 134
        SWL_INDEX = SWL2_INDEX
    else:
        print("No the sw index level !")
    for i in range(1,N):
        payload = swl_payload
        payload.update({"p": i})
        payload.update({"pagecount": f"{N_pages}"})
        payload.update({"timed": int(time.time() * 1000)})
        payload.update({"where": f"L1 in{SWL_INDEX}"})
        r = requests.post(url=sw_url, headers=sw_headers, data=payload)
        data = r.content.decode()
        data = data.replace("'", '"')
        data = json.loads(data)
        result.extend(data["root"])
    temp_df = pd.DataFrame(result)
    temp_df["L2"] = temp_df["L2"].str.strip()
    temp_df.columns = ["index_code", "index_name", "pre_close", "open", "amount", "high", "low", "close", "volume"]
    temp_df["pre_close"] = pd.to_numeric(temp_df["pre_close"])
    temp_df["open"] = pd.to_numeric(temp_df["open"])
    temp_df["high"] = pd.to_numeric(temp_df["high"])
    temp_df["low"] = pd.to_numeric(temp_df["low"])
    temp_df["amount"] = pd.to_numeric(temp_df["amount"])
    temp_df["close"] = pd.to_numeric(temp_df["close"])
    temp_df["volume"] = pd.to_numeric(temp_df["volume"])
    temp_df['change_pct'] = 100 * (temp_df['close'] / temp_df['pre_close'] -1 )
    temp_df = temp_df.sort_values(by='change_pct', ascending=False)
    return temp_df.round(2)


if __name__ == '__main__':
    #print(sw_index_spot(level="L1"))
    import datetime
    import time
    """
    while 1:
        print('swl_L2_spot: \n')
        print(sw_index_spot(level="L2"))
        
        print(datetime.datetime.now())
        time.sleep(20)
    """
    
    print(sw_index_spot(level="L1"))
    
    print(sw_index_spot(level="L2"))
    
    sw_index_spot(level="L2").to_csv('/mnt/g/data/rrdata/sw_L2_spot.csv', encoding='utf_8_sig')