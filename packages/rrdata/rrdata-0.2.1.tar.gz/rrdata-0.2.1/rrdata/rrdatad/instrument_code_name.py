""" read data from pqsql;
    code --> name from table stock_list;
    swl_index --> name_level  from table swl_list;
    stock code belong to swl_level, L1,L2,L3 from table stock_belong_swl:
"""

import pandas as pd

from rrdata.rrdatad.stock.fetch_stock_basic_tspro import fetch_stock_basic_all_tspro
from rrdata.rrdatac.rrdataD_read_api import RrdataD
from rrdata.common import engine

def stock_code_to_name(symbol=None, df=True):
    """ data get from local sql
        symbol --> 600519
        df=ture --> odataframe
        df=fasle --> dict 
    """
    stocks = fetch_stock_basic_all_tspro()[['symbol', 'name']]
    if symbol:
        if isinstance(symbol,str):
            symbol = [symbol]
        stock = stocks[stocks.symbol.isin(symbol)]
        if df:
            return stock
        return dict(zip(stock.symbol,stock.name))
    else:
        if df:
            return stocks
        return dict(zip(stocks.symbol,stocks.name))
        

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


def stock_code_belong_swl_name(symbol=None, swl_level=None): #TODO
    """ data get from local psql can select database--"rrshare"
        da change by client_pgsql("ttfactor") 
        swl_level --> L1 , L2, L3
        symbol--> 600519
        TODO
        #df=ture --> pd.dataframe
        #df=fasle --> dict 
    """
    stock_swls_all = RrdataD('stock_belong_swl', engine(db_name="rrshare")).read()
    #print(stock_swls_all.head())
    #print(stock_swls_all.columns)
    if swl_level:
        swl_level_name = f"swl_{swl_level}"
        stock_swls = stock_swls_all[['index_symbol', 'name',swl_level_name]]
        #print(stock_swls)
    else:
        swl_level_name = ['swl_L1', 'swl_L2', 'swl_L3']
        cols =  ['index_symbol','name'] + swl_level_name
        #print(cols)
        stock_swls = stock_swls_all[cols]
        print(stock_swls.head())
    if code:
        if isinstance(code,str):
            code = [code]
        stock_swl = stock_swls[stock_swls.code.isin(code)]
        return stock_swl
    else:
        return stock_swls
       

if __name__ == '__main__':
    
    print(stock_code_to_name('000831'))
    #print(stock_code_to_name(['000001','300674','000792']))
    #print(stock_code_to_name())
    print(swl_index_to_name('859811'))
    print(swl_index_to_name(['801010', '859822']))
    print(swl_index_to_name(swl_level='L2'))
    
    #print(stock_code_belong_swl_name(swl_level='L1'))
    #print(stock_code_belong_swl_name(code=["600519", "300146"]))
    #print(stock_code_belong_swl_name(code=['000001','600519'],swl_level='L3'))
    pass