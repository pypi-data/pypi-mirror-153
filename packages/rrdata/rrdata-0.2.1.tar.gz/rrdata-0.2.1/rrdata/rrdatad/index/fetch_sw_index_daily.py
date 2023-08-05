# -*- coding:utf-8 -*-
"""
Date: 2022/1/26 13:10
Desc: 申万指数-申万一级、二级和三级
http://www.swsindex.com/IdxMain.aspx
https://legulegu.com/stockdata/index-composition?industryCode=851921.SI
"""
import time
import json
import pandas as pd
import requests
from bs4 import BeautifulSoup


def sw_index_daily(
    symbol: str = "801011",
    start_date: str = "2019-12-01",
    end_date: str = "2020-12-07",
) -> pd.DataFrame:
    """
    申万指数一级和二级日频率行情数据
    http://www.swsindex.com/idx0200.aspx?columnid=8838&type=Day
    :param symbol: 申万指数
    :type symbol: str
    :param start_date: 开始日期
    :type start_date: str
    :param end_date: 结束日期
    :type end_date: str
    :return: 申万指数日频率行情数据
    :rtype: pandas.DataFrame
    """
    #start_date = "-".join([start_date[:4], start_date[4:6], start_date[6:]])
    #end_date = "-".join([end_date[:4], end_date[4:6], end_date[6:]])
    url = "http://www.swsindex.com/excel2.aspx"
    params = {
        "ctable": "swindexhistory",
        "where": f" swindexcode in ('{symbol}') and BargainDate >= '{start_date}' and BargainDate <= '{end_date}'",
    }
    r = requests.get(url, params=params)
    soup = BeautifulSoup(r.text, "html5lib")
    data = []
    table = soup.findAll("table")[0]
    rows = table.findAll("tr")
    for row in rows:
        cols = row.findAll("td")
        if len(cols) >= 10:
            symbol = cols[0].text
            index_name = cols[1].text
            date = cols[2].text
            open_ = cols[3].text
            high = cols[4].text
            low = cols[5].text
            close = cols[6].text
            vol = cols[7].text
            amount = cols[8].text
            change_pct = cols[9].text
            data.append(
                {
                    "index_code": symbol.replace(",", ""),
                    "index_name": index_name.replace(",", ""),
                    "date": date.replace(",", ""),
                    "open": open_.replace(",", ""),
                    "high": high.replace(",", ""),
                    "low": low.replace(",", ""),
                    "close": close.replace(",", ""),
                    "vol": vol.replace(",", ""),
                    "amount": amount.replace(",", ""),
                    "change_pct": change_pct.replace(",", ""),
                }
            )
    temp_df = pd.DataFrame(data)
    temp_df["date"] = pd.to_datetime(temp_df["date"]).dt.date
    temp_df["open"] = pd.to_numeric(temp_df["open"])
    temp_df["high"] = pd.to_numeric(temp_df["high"])
    temp_df["low"] = pd.to_numeric(temp_df["low"])
    temp_df["close"] = pd.to_numeric(temp_df["close"])
    temp_df["vol"] = pd.to_numeric(temp_df["vol"])
    temp_df["amount"] = pd.to_numeric(temp_df["amount"])
    temp_df["change_pct"] = pd.to_numeric(temp_df["change_pct"])
    return temp_df


def sw_index_daily_indicator(
    symbol: str = "801011",
    start_date: str = "2019-12-01",
    end_date: str = "2021-09-07",
    data_type: str = "Day",
) -> pd.DataFrame:
    """
    申万一级和二级行业历史行情指标
    http://www.swsindex.com/idx0200.aspx?columnid=8838&type=Day
    :param symbol: 申万指数
    :type symbol: str
    :param start_date: 开始时间
    :type start_date: str
    :param end_date: 结束时间
    :type end_date: str
    :param data_type: choice of {"Day": 日报表, "Week": 周报表}
    :type data_type: str
    :return: 申万指数不同频率数据
    :rtype: pandas.DataFrame
    """
    #start_date = "-".join([start_date[:4], start_date[4:6], start_date[6:]])
    #end_date = "-".join([end_date[:4], end_date[4:6], end_date[6:]])
    url = "http://www.swsindex.com/excel.aspx"
    params = {
        "ctable": "V_Report",
        "where": f" swindexcode in ('{symbol}') and BargainDate >= '{start_date}' and BargainDate <= '{end_date}' and type='{data_type}'",
    }
    r = requests.get(url, params=params)
    soup = BeautifulSoup(r.text, "html5lib")
    data = []
    table = soup.findAll("table")[0]
    rows = table.findAll("tr")
    for row in rows:
        cols = row.findAll("td")
        if len(cols) >= 14:
            symbol = cols[0].text
            index_name = cols[1].text
            date = cols[2].text
            close = cols[3].text
            volume = cols[4].text
            chg_pct = cols[5].text
            turn_rate = cols[6].text
            pe = cols[7].text
            pb = cols[8].text
            v_wap = cols[9].text
            turnover_pct = cols[10].text
            float_mv = cols[11].text
            avg_float_mv = cols[12].text
            dividend_yield_ratio = cols[13].text
            data.append(
                {
                    "index_code": symbol,
                    "index_name": index_name,
                    "date": date,
                    "close": close,
                    "volume": volume,
                    "chg_pct": chg_pct,
                    "turn_rate": turn_rate,
                    "pe": pe,
                    "pb": pb,
                    "vwap": v_wap,
                    "float_mv": float_mv,
                    "avg_float_mv": avg_float_mv,
                    "dividend_yield_ratio": dividend_yield_ratio,
                    "turnover_pct": turnover_pct,
                }
            )
    temp_df = pd.DataFrame(data)
    temp_df["date"] = pd.to_datetime(temp_df["date"]).dt.date
    temp_df["close"] = pd.to_numeric(temp_df["close"])
    temp_df["volume"] = temp_df["volume"].apply(lambda x: x.replace(",", ""))
    temp_df["volume"] = pd.to_numeric(temp_df["volume"])
    temp_df["chg_pct"] = pd.to_numeric(temp_df["chg_pct"])
    temp_df["turn_rate"] = pd.to_numeric(temp_df["turn_rate"])
    temp_df["pe"] = pd.to_numeric(temp_df["pe"])
    temp_df["pb"] = pd.to_numeric(temp_df["pb"])
    temp_df["vwap"] = pd.to_numeric(temp_df["vwap"])
    temp_df["float_mv"] = temp_df["float_mv"].apply(lambda x: x.replace(",", ""))
    temp_df["float_mv"] = pd.to_numeric(
        temp_df["float_mv"],
    )
    temp_df["avg_float_mv"] = temp_df["avg_float_mv"].apply(
        lambda x: x.replace(",", "")
    )
    temp_df["avg_float_mv"] = pd.to_numeric(temp_df["avg_float_mv"])
    temp_df["dividend_yield_ratio"] = pd.to_numeric(temp_df["dividend_yield_ratio"])
    temp_df["turnover_pct"] = pd.to_numeric(temp_df["turnover_pct"])
    return temp_df

def sw_index_daily_indicator(
    symbol: str = "801011",
    start_date: str = "2019-12-01",
    end_date: str = "2021-09-07",
    data_type: str = "Day",
) -> pd.DataFrame:
    """
    申万一级和二级行业历史行情指标
    http://www.swsindex.com/idx0200.aspx?columnid=8838&type=Day
    :param symbol: 申万指数
    :type symbol: str
    :param start_date: 开始时间
    :type start_date: str
    :param end_date: 结束时间
    :type end_date: str
    :param data_type: choice of {"Day": 日报表, "Week": 周报表}
    :type data_type: str
    :return: 申万指数不同频率数据
    :rtype: pandas.DataFrame
    """
    #start_date = "-".join([start_date[:4], start_date[4:6], start_date[6:]])
    #end_date = "-".join([end_date[:4], end_date[4:6], end_date[6:]])
    url = "http://www.swsindex.com/excel.aspx"
    params = {
        "ctable": "V_Report",
        "where": f" swindexcode in ('{symbol}') and BargainDate >= '{start_date}' and BargainDate <= '{end_date}' and type='{data_type}'",
    }
    r = requests.get(url, params=params)
    soup = BeautifulSoup(r.text, "html5lib")
    data = []
    table = soup.findAll("table")[0]
    rows = table.findAll("tr")
    for row in rows:
        cols = row.findAll("td")
        if len(cols) >= 14:
            symbol = cols[0].text
            index_name = cols[1].text
            date = cols[2].text
            close = cols[3].text
            volume = cols[4].text
            chg_pct = cols[5].text
            turn_rate = cols[6].text
            pe = cols[7].text
            pb = cols[8].text
            v_wap = cols[9].text
            turnover_pct = cols[10].text
            float_mv = cols[11].text
            avg_float_mv = cols[12].text
            dividend_yield_ratio = cols[13].text
            data.append(
                {
                    "index_code": symbol,
                    "index_name": index_name,
                    "date": date,
                    "close": close,
                    "volume": volume,
                    "chg_pct": chg_pct,
                    "turn_rate": turn_rate,
                    "pe": pe,
                    "pb": pb,
                    "vwap": v_wap,
                    "float_mv": float_mv,
                    "avg_float_mv": avg_float_mv,
                    "dividend_yield_ratio": dividend_yield_ratio,
                    "turnover_pct": turnover_pct,
                }
            )
    temp_df = pd.DataFrame(data)
    temp_df["date"] = pd.to_datetime(temp_df["date"]).dt.date
    temp_df["close"] = pd.to_numeric(temp_df["close"])
    temp_df["volume"] = temp_df["volume"].apply(lambda x: x.replace(",", ""))
    temp_df["volume"] = pd.to_numeric(temp_df["volume"])
    temp_df["chg_pct"] = pd.to_numeric(temp_df["chg_pct"])
    temp_df["turn_rate"] = pd.to_numeric(temp_df["turn_rate"])
    temp_df["pe"] = pd.to_numeric(temp_df["pe"])
    temp_df["pb"] = pd.to_numeric(temp_df["pb"])
    temp_df["vwap"] = pd.to_numeric(temp_df["vwap"])
    temp_df["float_mv"] = temp_df["float_mv"].apply(lambda x: x.replace(",", ""))
    temp_df["float_mv"] = pd.to_numeric(
        temp_df["float_mv"],
    )
    temp_df["avg_float_mv"] = temp_df["avg_float_mv"].apply(
        lambda x: x.replace(",", "")
    )
    temp_df["avg_float_mv"] = pd.to_numeric(temp_df["avg_float_mv"])
    temp_df["dividend_yield_ratio"] = pd.to_numeric(temp_df["dividend_yield_ratio"])
    temp_df["turnover_pct"] = pd.to_numeric(temp_df["turnover_pct"])
    return temp_df



if  __name__ ==  "__main__":
    daily = sw_index_daily(symbol="801995", start_date="2022-04-01", end_date="2022-05-11")
    print(daily)
    indicator = sw_index_daily_indicator(symbol="801010", start_date="2022-04-01", end_date="2022-05-09")
    print(indicator)	
