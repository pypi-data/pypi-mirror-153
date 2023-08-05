import pandas as pd
import requests
from bs4 import BeautifulSoup


def sw_index_info(level="L2") -> pd.DataFrame:
    """
    乐咕乐股-申万三级-分类
    https://legulegu.com/stockdata/sw-industry-overview#level1
    :return: 分类
    :rtype: pandas.DataFrame
    """
    url = "https://legulegu.com/stockdata/sw-industry-overview"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    levelTtems=f"level{level[-1]}Items"
    code_raw = soup.find("div", attrs={"id": levelTtems}).find_all(
        "div", attrs={"class": "lg-industries-item-chinese-title"}
    )
    name_raw = soup.find("div", attrs={"id": levelTtems}).find_all(
        "div", attrs={"class": "lg-industries-item-number"}
    )
    value_raw = soup.find("div", attrs={"id": levelTtems}).find_all(
        "div", attrs={"class": "lg-sw-industries-item-value"}
    )
    code = [item.get_text() for item in code_raw]
    name = [item.get_text().split("(")[0] for item in name_raw]
    num = [item.get_text().split("(")[1].split(")")[0] for item in name_raw]
    num_1 = [
        item.find_all("span", attrs={"class": "value"})[0].get_text().strip()
        for item in value_raw
    ]
    num_2 = [
        item.find_all("span", attrs={"class": "value"})[1].get_text().strip()
        for item in value_raw
    ]
    num_3 = [
        item.find_all("span", attrs={"class": "value"})[2].get_text().strip()
        for item in value_raw
    ]
    num_4 = [
        item.find_all("span", attrs={"class": "value"})[3].get_text().strip()
        for item in value_raw
    ]
    temp_df = pd.DataFrame([code, name, num, num_1, num_2, num_3, num_4]).T
    temp_df.columns = [
        "index_code",
        "index_name",
        "cons_num",
        "pe",
        "pe_ttm",
        "pb",
        "dy",
    ]
    temp_df["cons_num"] = pd.to_numeric(temp_df["cons_num"])
    temp_df["pe"] = pd.to_numeric(temp_df["pe"])
    temp_df["pe_ttm"] = pd.to_numeric(temp_df["pe_ttm"])
    temp_df["pb"] = pd.to_numeric(temp_df["pb"])
    temp_df["dy"] = pd.to_numeric(temp_df["dy"])
    return temp_df


def sw_index_class(level="L1"):
    """
    swl L1, L2, L3 class
    乐咕乐股-申万一，二，三级-分类
    https://legulegu.com/stockdata/sw-industry-overview#level1
    """
    sw_level=f"level{level[-1]}"
    #print(sw_level)
    df_swl = pd.DataFrame()
    swl_spot= sw_index_info(sw_level)
    df_swl["index_code"] = swl_spot["index_code"]
    df_swl["index_symbol"] = df_swl["index_code"].map(lambda x: x[:6])
    df_swl["index_name"] = swl_spot["index_name"]
    df_swl["level"] = f"{level}"
    df_swl["name_level"] = swl_spot["index_name"] + "_" + df_swl["level"]
    print(f"get_swl_{level}_index")
    return df_swl


def sw_index_class_all():
    df = pd.DataFrame() 
    for level in ["L1", "L2", "L3"]:
        df = pd.concat([df,sw_index_class(level)])
    return df


if __name__ == '__main__':
    print(sw_index_info("L1"))
    print(sw_index_info("L2"))
    print(sw_index_info("L3"))
    print(sw_index_class_all())
  

