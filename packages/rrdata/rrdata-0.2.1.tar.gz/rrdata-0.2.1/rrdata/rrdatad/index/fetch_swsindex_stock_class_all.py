from typing import List,Dict
import pandas as pd

from rrdata.rrdatac.rrdataD_read_api import RrdataD
from rrdata.utils.rqDate import rq_util_date_today
from rrdata.utils.rqDate_trade import trade_date_sse, rq_util_get_last_tradedate

from rrdata.rrdatad.rrdataD_save_api import RrdataDSave

from rrdata.rrdatad.stock.fetch_stock_basic_tspro import fetch_stock_basic_all_tspro, fetch_delist_stock
from rrdata.rrdatad.stock.fetch_stock_list import fetch_stock_list_tusharepro


def fetch_stock_class_cn_all():
    """ from swsindex.com table download SWI_2021 
        https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
    """
    path_file = u"/home/romep/rrdata/rrdata/rrdatad/index/swsindex/swsindex_all_stock_class_new.xlsx"
    df_all = pd.read_excel(path_file)
    col_old = ['交易所', '行业代码', '股票代码', '公司简称', '新版一级行业', '新版二级行业', '新版三级行业']
    col_new = ['exchange', 'industry_code','ts_code','name','name_L1','name_L2','name_L3']
    df_all.rename(columns={'交易所':'exchange',  '行业代码':'industry_code', '股票代码':'ts_code', '公司简称':'name', \
        '新版一级行业':'name_L1','新版二级行业':'name_L2', '新版三级行业':'name_L3'}, inplace=True)
    #df_cn = df_all[df_all['exchange'] == "A股"]
    df_A = df_all.query('exchange == ["A股"]')
    df_A = df_A.drop(labels=['exchange','industry_code', 'name'], axis=1) #,inplace=True)
    df_cn = df_A.copy()
    df_cn['name_L1'] = df_cn['name_L1'].apply(lambda x: x + "_L1")
    df_cn['name_L2'] = df_cn['name_L2'].apply(lambda x: x + "_L2")
    df_cn['name_L3'] =  df_cn['name_L3'].apply(lambda x: x + "_L3")
    #print(df_cn)
    df_stock_list = fetch_stock_list_tusharepro()[['ts_code','symbol','name']]
    df = pd.merge(df_stock_list, df_cn, how='left', on='ts_code').sort_values(by='ts_code')
    #df['trade_date'] = pd.to_datetime(df['trade_date'], format='%Y-%m-%d')
    delist_code = fetch_delist_stock(rq_util_get_last_tradedate())
    #print(delist_code)
    df=df[~df['symbol'].isin(delist_code)]
    return df


def fetch_swlindex_name(swl_level=None)-> pd.DataFrame:
    file =      u"/home/romep/rrdata/rrdata/rrdatad/index/swsindex/SwClassCode_2021.xlsx"
    df = pd.read_excel(file)
    print(df)
    df.rename(columns={'行业代码':'industry_code', '一级行业名称':'name_L1','二级行业名称':'name_L2', '三级行业名称':'name_L3'}, inplace=True)
    
    return df
                

def swl_index_to_name(index_symbol="", swl_level="", out_type=""):
    """index_symbol like 801020 not index_code 801020.SI
    swl_level= L1, L2, L3
        out_type =  dataframe, dict, list
    """
    swls = RrdataD('swl_list').read()
    if swl_level:
        swls = swls[swls['level'] == swl_level][['index_symbol','name_level']]
    else:
        swls =swls[['index_symbol','name_level']]
    #print(swls)
    if index_symbol:
        if isinstance(index_symbol,list):
            swl = swls[swls['index_symbol'].isin(index_symbol)]
            swl_d = dict(zip(swl.index_symbol,swl.name_level))
            if out_type==dict:
                return swl_d
            if out_type==list:
                return list(swl_d.values())
            return swl
        else:
            return swls[swls['index_symbol'] == index_symbol]['name_level'].values[0]
    else:
        if out_type == dict:
            return dict(zip(swls.index_symbol,swls.name_level))
        return swls



"""
 df = pd.merge(df_factor, df_p, how='left', on='code').sort_values(by = 'code')
    df['trade_date'] = pd.to_datetime(df['trade_date'], format='%Y-%m-%d')
    delist_code = fetch_delist_stock(trade_date)
    df=df[~df['code'].isin(delist_code)]
    save_df_to_pgsql(df, "swl_stock_class_all_2021_cn")
    print(df)

    print(df.columns)

    #table_name = 'stock_belong_swl'
"""

if __name__ == "__main__":
    #print(stock_code_to_name())
    df = fetch_stock_class_cn_all()
    #print(df)
    print(df[df.symbol== '000792'])
    print(swl_index_to_name().sort_values(by='index_symbol'))
    #print(fetch_swlindex_name("L2"))
    print(len(fetch_swlindex_name("L1")))
    print(len(fetch_swlindex_name("L2")))
    print(len(fetch_swlindex_name("L3")))
    #print(swl_index_to_name())
    
    
    #fetch_swlindex_name().to_csv('/mnt/g/data/rrdata/swl_class.csv', encoding='utf_8_sig')
    swl_class =  fetch_swlindex_name()
    swl_class_L2 = swl_class[['industry_code', 'name_L2']].dropna().drop_duplicates(subset="name_L2")
    swl_class_L3 = swl_class[['industry_code', 'name_L3']].dropna().drop_duplicates(subset="name_L3")
    print(swl_class_L2)
    swl_class_L2.to_csv('/mnt/g/data/rrdata/swl_class_L2.csv', encoding='utf_8_sig')
    



