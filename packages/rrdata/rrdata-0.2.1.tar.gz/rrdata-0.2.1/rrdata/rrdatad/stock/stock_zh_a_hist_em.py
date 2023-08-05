#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Date: 2022/2/2 23:26
Desc: 东方财富网-行情首页-沪深京 A 股 
    spot / hist days/ min 
    hist daily default : ajust:"qfq"

columns_new1 = [
            "no",
            "code",
            "name",
            "close",
            "chg_pct",
            "change",
            "vol",
            "amount",
            "amplitude",
            "high",
            "low",
            "open",
            "pre_close",
            "vol_chg",
            "turnover",
            "pe",
            "pb",
        ]
"""
import requests
import pandas as pd


def stock_zh_a_spot_em() -> pd.DataFrame:
    """
    东方财富网-沪深京 A 股-实时行情
    http://quote.eastmoney.com/center/gridlist.html#hs_a_board
    :return: 实时行情
    :rtype: pandas.DataFrame
    """
    url = "http://82.push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": "1",
        "pz": "5000",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fid": "f3",
        "fs": "m:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23,m:0 t:81 s:2048",
        "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152",
        "_": "1623833739532",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    if not data_json["data"]["diff"]:
        return pd.DataFrame()
    temp_df = pd.DataFrame(data_json["data"]["diff"])
    temp_df.columns = [
        "_",
        "最新价",
        "涨跌幅",
        "涨跌额",
        "成交量",
        "成交额",
        "振幅",
        "换手率",
        "市盈率-动态",
        "量比",
        "_",
        "代码",
        "_",
        "名称",
        "最高",
        "最低",
        "今开",
        "昨收",
        "_",
        "_",
        "_",
        "市净率",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
    ]
    temp_df.reset_index(inplace=True)
    temp_df["index"] = temp_df.index + 1
    temp_df.rename(columns={"index": "序号"}, inplace=True)
    temp_df = temp_df[
        [
            "序号",
            "代码",
            "名称",
            "最新价",
            "涨跌幅",
            "涨跌额",
            "成交量",
            "成交额",
            "振幅",
            "最高",
            "最低",
            "今开",
            "昨收",
            "量比",
            "换手率",
            "市盈率-动态",
            "市净率",
        ]
    ]
    temp_df.columns = [
            "no",
            "code",
            "name",
            "close",
            "chg_pct",
            "change",
            "vol",
            "amount",
            "amplitude",
            "high",
            "low",
            "open",
            "pre_close",
            "vol_chg",
            "turnover",
            "pe",
            "pb",
        ]
    
    temp_df["close"] = pd.to_numeric(temp_df["close"], errors="coerce")
    temp_df["chg_pct"] = pd.to_numeric(temp_df["chg_pct"], errors="coerce")
    temp_df["change"] = pd.to_numeric(temp_df["change"], errors="coerce")
    temp_df["vol"] = pd.to_numeric(temp_df["vol"], errors="coerce")
    temp_df["amount"] = pd.to_numeric(temp_df["amount"], errors="coerce")
    temp_df["amplitude"] = pd.to_numeric(temp_df["amplitude"], errors="coerce")
    temp_df["high"] = pd.to_numeric(temp_df["high"], errors="coerce")
    temp_df["low"] = pd.to_numeric(temp_df["low"], errors="coerce")
    temp_df["open"] = pd.to_numeric(temp_df["open"], errors="coerce")
    temp_df["pre_close"] = pd.to_numeric(temp_df["pre_close"], errors="coerce")
    temp_df["vol_chg"] = pd.to_numeric(temp_df["vol_chg"], errors="coerce")
    temp_df["turnover"] = pd.to_numeric(temp_df["turnover"], errors="coerce")
    temp_df["pe"] = pd.to_numeric(temp_df["pe"], errors="coerce")
    temp_df["pb"] = pd.to_numeric(temp_df["pb"], errors="coerce")
    return temp_df


def code_id_map_em() -> dict:
    """
    东方财富-股票和市场代码
    http://quote.eastmoney.com/center/gridlist.html#hs_a_board
    :return: 股票和市场代码
    :rtype: dict
    """
    url = "http://80.push2.eastmoney.com/api/qt/clist/get"
    params = {
        "pn": "1",
        "pz": "5000",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fid": "f3",
        "fs": "m:1 t:2,m:1 t:23",
        "fields": "f12",
        "_": "1623833739532",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    if not data_json["data"]["diff"]:
        return dict()
    temp_df = pd.DataFrame(data_json["data"]["diff"])
    temp_df["market_id"] = 1
    temp_df.columns = ["sh_code", "sh_id"]
    code_id_dict = dict(zip(temp_df["sh_code"], temp_df["sh_id"]))
    params = {
        "pn": "1",
        "pz": "5000",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fid": "f3",
        "fs": "m:0 t:6,m:0 t:80",
        "fields": "f12",
        "_": "1623833739532",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    if not data_json["data"]["diff"]:
        return dict()
    temp_df_sz = pd.DataFrame(data_json["data"]["diff"])
    temp_df_sz["sz_id"] = 0
    code_id_dict.update(dict(zip(temp_df_sz["f12"], temp_df_sz["sz_id"])))
    params = {
        "pn": "1",
        "pz": "5000",
        "po": "1",
        "np": "1",
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": "2",
        "invt": "2",
        "fid": "f3",
        "fs": "m:0 t:81 s:2048",
        "fields": "f12",
        "_": "1623833739532",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    if not data_json["data"]["diff"]:
        return dict()
    temp_df_sz = pd.DataFrame(data_json["data"]["diff"])
    temp_df_sz["bj_id"] = 0
    code_id_dict.update(dict(zip(temp_df_sz["f12"], temp_df_sz["bj_id"])))
    return code_id_dict


def stock_zh_a_hist_em(
        symbol: str = "600519",
        period: str = "daily",
        start_date: str = "20050101",
        end_date: str = "22220101",
        adjust: str = "qfq",
) -> pd.DataFrame:
    """
    东方财富网-行情首页-沪深京 A 股-每日行情
    http://quote.eastmoney.com/concept/sh603777.html?from=classic
    :param symbol: 股票代码
    :type symbol: str
    :param period: choice of {'daily', 'weekly', 'monthly'}
    :type period: str
    :param start_date: 开始日期
    :type start_date: str
    :param end_date: 结束日期
    :type end_date: str
    :param adjust: choice of {"qfq": "前复权", "hfq": "后复权", "": "不复权"}
    :type adjust: str
    :return: 每日行情
    :rtype: pandas.DataFrame
    """
    code_id_dict = code_id_map_em()
    adjust_dict = {"qfq": "1", "hfq": "2", "": "0"}
    period_dict = {'daily': '101', 'weekly': '102', 'monthly': '103'}
    url = "http://push2his.eastmoney.com/api/qt/stock/kline/get"
    params = {
        "fields1": "f1,f2,f3,f4,f5,f6",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f116",
        "ut": "7eea3edcaed734bea9cbfc24409ed989",
        "klt": period_dict[period],
        "fqt": adjust_dict[adjust],
        "secid": f"{code_id_dict[symbol]}.{symbol}",
        "beg": "0",
        "end": "20500000",
        "_": "1623766962675",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]["klines"]])
    temp_df.columns = [
        "日期",
        "开盘",
        "收盘",
        "最高",
        "最低",
        "成交量",
        "成交额",
        "振幅",
        "涨跌幅",
        "涨跌额",
        "换手率",
    ]
    temp_df.index = pd.to_datetime(temp_df["日期"])
    temp_df = temp_df[start_date:end_date]
    temp_df.reset_index(inplace=True, drop=True)
    
    temp_df['开盘'] = pd.to_numeric(temp_df['开盘'])
    temp_df['收盘'] = pd.to_numeric(temp_df['收盘'])
    temp_df['最高'] = pd.to_numeric(temp_df['最高'])
    temp_df['最低'] = pd.to_numeric(temp_df['最低'])
    temp_df['成交量'] = pd.to_numeric(temp_df['成交量'])
    temp_df['成交额'] = pd.to_numeric(temp_df['成交额'])
    temp_df['振幅'] = pd.to_numeric(temp_df['振幅'])
    temp_df['涨跌幅'] = pd.to_numeric(temp_df['涨跌幅'])
    temp_df['涨跌额'] = pd.to_numeric(temp_df['涨跌额'])
    temp_df['换手率'] = pd.to_numeric(temp_df['换手率'])
    
    temp_df.columns = [
        
        "trade_date",
        "open",
        "close",
        "high",
        "low",
        "vol",
        "amount",
        "amplitude",
        "chg_pct",
        "change",
        "turnover",       
    ]
    temp_df['symbol'] = symbol
    temp_df = temp_df[['symbol',
        "trade_date",
        "open",
        "close",
        "high",
        "low",
        "vol",
        "amount",
        "amplitude",
        "chg_pct",
        "change",
        "turnover"  ]]
    
    return temp_df


def stock_zh_a_hist_min_em(
        symbol: str = "000001",
        start_date: str = "1979-09-01 09:32:00",
        end_date: str = "2222-01-01 09:32:00",
        period: str = '5',
        adjust: str = '',
) -> pd.DataFrame:
    """
    东方财富网-行情首页-沪深京 A 股-每日分时行情
    http://quote.eastmoney.com/concept/sh603777.html?from=classic
    :param symbol: 股票代码
    :type symbol: str
    :param start_date: 开始日期
    :type start_date: str
    :param end_date: 结束日期
    :type end_date: str
    :param period: choice of {'1', '5', '15', '30', '60'}
    :type period: str
    :param adjust: choice of {'', 'qfq', 'hfq'}
    :type adjust: str
    :return: 每日分时行情
    :rtype: pandas.DataFrame
    """
    code_id_dict = code_id_map_em()
    adjust_map = {
        '': '0',
        'qfq': '1',
        'hfq': '2',
    }
    if period == '1':
        url = 'https://push2his.eastmoney.com/api/qt/stock/trends2/get'
        params = {
            "fields1": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58",
            "ut": "7eea3edcaed734bea9cbfc24409ed989",
            "ndays": "5",
            "iscr": "0",
            "secid": f"{code_id_dict[symbol]}.{symbol}",
            "_": "1623766962675",
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]["trends"]])
        temp_df.columns = [
            "时间",
            "开盘",
            "收盘",
            "最高",
            "最低",
            "成交量",
            "成交额",
            "最新价",
        ]
        temp_df.index = pd.to_datetime(temp_df["时间"])
        temp_df = temp_df[start_date:end_date]
        temp_df.reset_index(drop=True, inplace=True)
        temp_df["开盘"] = pd.to_numeric(temp_df["开盘"])
        temp_df["收盘"] = pd.to_numeric(temp_df["收盘"])
        temp_df["最高"] = pd.to_numeric(temp_df["最高"])
        temp_df["最低"] = pd.to_numeric(temp_df["最低"])
        temp_df["成交量"] = pd.to_numeric(temp_df["成交量"])
        temp_df["成交额"] = pd.to_numeric(temp_df["成交额"])
        temp_df["最新价"] = pd.to_numeric(temp_df["最新价"])
        temp_df['时间'] = pd.to_datetime(temp_df['时间']).astype(str)

        temp_df.columns = [
        "time",
        "open",
        "close",
        "high",
        "low",
        "vol",
        "amount",
        "last"
        ]
        return temp_df
    else:
        url = 'http://push2his.eastmoney.com/api/qt/stock/kline/get'
        params = {
            'fields1': 'f1,f2,f3,f4,f5,f6',
            'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
            'ut': '7eea3edcaed734bea9cbfc24409ed989',
            'klt': period,
            'fqt': adjust_map[adjust],
            'secid': f"{code_id_dict[symbol]}.{symbol}",
            'beg': '0',
            'end': '20500000',
            '_': '1630930917857',
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]["klines"]])
        temp_df.columns = [
            "时间",
            "开盘",
            "收盘",
            "最高",
            "最低",
            "成交量",
            "成交额",
            "振幅",
            "涨跌幅",
            "涨跌额",
            "换手率",
        ]
        temp_df.index = pd.to_datetime(temp_df["时间"])
        temp_df = temp_df[start_date:end_date]
        temp_df.reset_index(drop=True, inplace=True)
        temp_df["开盘"] = pd.to_numeric(temp_df["开盘"])
        temp_df["收盘"] = pd.to_numeric(temp_df["收盘"])
        temp_df["最高"] = pd.to_numeric(temp_df["最高"])
        temp_df["最低"] = pd.to_numeric(temp_df["最低"])
        temp_df["成交量"] = pd.to_numeric(temp_df["成交量"])
        temp_df["成交额"] = pd.to_numeric(temp_df["成交额"])
        temp_df["振幅"] = pd.to_numeric(temp_df["振幅"])
        temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"])
        temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"])
        temp_df["换手率"] = pd.to_numeric(temp_df["换手率"])
        temp_df['时间'] = pd.to_datetime(temp_df['时间']).astype(str)
        temp_df = temp_df[[
            "时间",
            "开盘",
            "收盘",
            "最高",
            "最低",
            "涨跌幅",
            "涨跌额",
            "成交量",
            "成交额",
            "振幅",
            "换手率",
        ]]
        temp_df.columns = [
        "time",
        "open",
        "close",
        "high",
        "low",
        "chg_pct",
        "change",
        "vol",
        "amount",
        "amplitude",
        "turnover",
        ]
        return temp_df


def stock_zh_a_hist_pre_min_em(symbol: str = "000001",
                               start_time: str = "09:00:00",
                               end_time: str = "15:50:00",
                               ) -> pd.DataFrame:
    """
    东方财富网-行情首页-沪深京 A 股-每日分时行情包含盘前数据
    http://quote.eastmoney.com/concept/sh603777.html?from=classic
    :param symbol: 股票代码
    :type symbol: str
    :param start_time: 开始时间
    :type start_time: str
    :param end_time: 结束时间
    :type end_time: str
    :return: 每日分时行情包含盘前数据
    :rtype: pandas.DataFrame
    """
    code_id_dict = code_id_map_em()
    url = "https://push2.eastmoney.com/api/qt/stock/trends2/get"
    params = {
        "fields1": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58",
        "ut": "fa5fd1943c7b386f172d6893dbfba10b",
        "ndays": "1",
        "iscr": "1",
        "iscca": "0",
        "secid": f"{code_id_dict[symbol]}.{symbol}",
        "_": "1623766962675",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    temp_df = pd.DataFrame([item.split(",") for item in data_json["data"]["trends"]])
    temp_df.columns = [
        "时间",
        "开盘",
        "收盘",
        "最高",
        "最低",
        "成交量",
        "成交额",
        "最新价",
    ]
    temp_df.index = pd.to_datetime(temp_df["时间"])
    date_format = temp_df.index[0].date().isoformat()
    temp_df = temp_df[date_format + ' ' + start_time:date_format + ' ' + end_time]
    temp_df.reset_index(drop=True, inplace=True)
    temp_df["开盘"] = pd.to_numeric(temp_df["开盘"])
    temp_df["收盘"] = pd.to_numeric(temp_df["收盘"])
    temp_df["最高"] = pd.to_numeric(temp_df["最高"])
    temp_df["最低"] = pd.to_numeric(temp_df["最低"])
    temp_df["成交量"] = pd.to_numeric(temp_df["成交量"])
    temp_df["成交额"] = pd.to_numeric(temp_df["成交额"])
    temp_df["最新价"] = pd.to_numeric(temp_df["最新价"])
    temp_df['时间'] = pd.to_datetime(temp_df['时间']).astype(str)
    
    temp_df.columns = [
        "time",
        "open",
        "close",
        "high",
        "low",
        "vol",
        "amount",
        "last"
        ]

    return temp_df


if __name__ == "__main__":

    stock_zh_a_spot_em_df = stock_zh_a_spot_em()
    print(stock_zh_a_spot_em_df)

    stock_zh_a_hist_df = stock_zh_a_hist_em(
        symbol="600519", period='daily', start_date="20210101", end_date="20221231", adjust="hfq")
    print(stock_zh_a_hist_df)
    '''
    stock_zh_a_hist_min_em_df = stock_zh_a_hist_min_em(symbol="833454")
    print(stock_zh_a_hist_min_em_df)
  
    stock_zh_a_hist_pre_min_em_df = stock_zh_a_hist_pre_min_em(symbol="833454")
    print(stock_zh_a_hist_pre_min_em_df)

    stock_zh_a_hist_min_em_df = stock_zh_a_hist_min_em(symbol="000001", period='60', adjust='hfq', start_date="2022-04-15 09:32:00", end_date="2022-04-15 14:40:00")
    print(stock_zh_a_hist_min_em_df)

    stock_zh_a_hist_df = stock_zh_a_hist_em(symbol="833454", period="daily", start_date="20170301", end_date='20211115', adjust="hfq")
    print(stock_zh_a_hist_df)
    '''


   