from selenium import webdriver
from my_fake_useragent import UserAgent
from lxml import etree
import json

"""
序号，股票代码，股票简称，现价（元），涨跌幅（%）
"""


def selenium_test():
    # 配置Chrome浏览器
    chrome_options = webdriver.ChromeOptions()  # 创建一个配置
    ua = UserAgent().random  # 随机抽取一个ua
    print('user-agent: ', ua)
    chrome_options.add_argument('user-agent=' + str(ua))
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_argument('blink-settings=imagesEnabled=false')
    chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--disable-gpu')  # 禁用gpu加速

    # 发送请求
    url = 'http://www.iwencai.com/stockpick/search?typed=1&preParams=&ts=1&f=1&qs=result_rewrite&selfsectsn=&querytype=stock&searchfilter=&tid=stockpick&w=%E6%8D%A2%E6%89%8B%E7%8E%87%3E5%25&queryarea='
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    # 获取源码
    html = driver.page_source

    # 保存网页源码到demo.html文件
    # with open('demo.html', 'w', encoding='utf8') as fp:
    #     fp.write(html)

    # 解析数据
    html = etree.HTML(html)
    tr_list_1 = html.xpath("//div[@class='static_con']//table//tbody/tr")
    tr_list_2 = html.xpath("//div[@class='scroll_tbody_con']//tbody/tr")

    info_all_1 = list()
    info_all_2 = list()

    #
    for tr in tr_list_1:
        info_line = list()
        xuhao = tr.xpath("./td[1]/div/text()")[0]
        bianhao = tr.xpath("./td[3]/div/text()")[0]
        name = tr.xpath("./td[4]/div/a/text()")[0]
        info_line.append(xuhao)
        info_line.append(bianhao)
        info_line.append(name)
        info_all_1.append(info_line)
    # print(info_all_1)

    for tr in tr_list_2:
        info_line = list()
        xianjia = tr.xpath("./td[1]/div/text()")[0]
        zhangdiefu = tr.xpath("./td[2]/div/text()")[0]
        info_line.append(xianjia)
        info_line.append(zhangdiefu)
        info_all_2.append(info_line)
    # print(info_all_2)

    info_all = list()
    for sub_list_1, sub_list_2 in zip(info_all_1, info_all_2):  # 同时遍历两个列表, 合并他们的每一个元素为一个列表
        list_temp = sub_list_1 + sub_list_2
        info_all.append(list_temp)

    print(info_all)  # 最终结果

    # 保存结果
    # with open('data.txt', 'w', encoding='utf-8') as fp:
    #     json.dump(info_all, fp)

    # time.sleep(3)   # 等待
    driver.quit()   # 关闭


if __name__ == '__main__':
    selenium_test()

