#!/usr/bin/env bash

import pandas as  pd
import requests
from bs4 import BeautifulSoup


def sw_index_cons(symbol: str = "801011") -> pd.DataFrame:
    """
    申万指数成份信息-包括一级和二级行业都可以查询
    http://www.swsindex.com/idx0210.aspx?swindexcode=801010
    :param symbol: 指数代码
    :type symbol: str
    :return: 申万指数成份信息
    :rtype: pandas.DataFrame
    """
    url = f"http://www.swsindex.com/downfile.aspx?code={symbol}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html5lib")
    data = []
    table = soup.findAll("table")[0]
    rows = table.findAll("tr")
    for row in rows:
        cols = row.findAll("td")
        if len(cols) >= 4:
            stock_code = cols[0].text
            stock_name = cols[1].text
            weight = cols[2].text
            start_date = cols[3].text

            data.append(
                {
                    "stock_code": stock_code,
                    "stock_name": stock_name,
                    "start_date": start_date,
                    "weight": weight,
                }
            )
    temp_df = pd.DataFrame(data)
    temp_df["start_date"] = pd.to_datetime(temp_df["start_date"]).dt.date
    temp_df["weight"] = pd.to_numeric(temp_df["weight"])
    return temp_df


def sw_index_legulegu_cons(symbol: str = "851921.SI") -> pd.DataFrame:
    """
    乐咕乐股-申万一，二，三级-行业成份
    https://legulegu.com/stockdata/index-composition?industryCode=851921.SI
    :param symbol: 三级行业的行业代码
    :type symbol: str
    :return: 行业成份
    :rtype: pandas.DataFrame
    """
    url = f"https://legulegu.com/stockdata/index-composition?industryCode={symbol}"
    temp_df = pd.read_html(url)[0]
    temp_df.columns = [
        "no",
        "stock_code",
        "display_name",
        "in_time",
        "sw_L1",
        "sw_L2",
        "sw_L3",
        "close",
        "pe",
        "pe_ttm",
        "pb",
        "dy",
        "mv",
    ]
    temp_df["close"] = pd.to_numeric(temp_df["close"], errors="coerce")
    temp_df["pe"] = pd.to_numeric(temp_df["pe"], errors="coerce")
    temp_df["pe_ttm"] = pd.to_numeric(temp_df["pe_ttm"], errors="coerce")
    temp_df["pb"] = pd.to_numeric(temp_df["pb"], errors="coerce")
    temp_df["dy"] = pd.to_numeric(temp_df["dy"].str.strip("%"), errors="coerce")
    temp_df["mv"] = pd.to_numeric(temp_df["mv"], errors="coerce")
    return temp_df


if __name__ == "__main__":
    try:
        print(sw_index_cons(symbol="801011"))
        print(sw_index_cons(symbol="801016"))
        print(sw_index_legulegu_cons("801017.SI"))
    except:
        pass





