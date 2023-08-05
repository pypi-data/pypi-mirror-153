
import json
import tushare as ts 

from rrdata.utils.config_setting import setting

try:
    token = setting['TSPRO_TOKEN']
    ts.set_token(token)
    pro = ts.pro_api()
    #print('tushare token set ok , can use pro as api!')
except Exception as e:
    print(e)
    


