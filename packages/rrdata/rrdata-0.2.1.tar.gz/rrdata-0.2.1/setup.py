# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rrdata',
 'rrdata.common',
 'rrdata.rrdatac',
 'rrdata.rrdatac.index',
 'rrdata.rrdatac.indicator_tech',
 'rrdata.rrdatac.stock',
 'rrdata.rrdatad',
 'rrdata.rrdatad.index',
 'rrdata.rrdatad.industry',
 'rrdata.rrdatad.record',
 'rrdata.rrdatad.stock',
 'rrdata.rrdatad.trade_calender',
 'rrdata.temp',
 'rrdata.temp.zvt',
 'rrdata.tushare_client',
 'rrdata.utils',
 'rrdata.web']

package_data = \
{'': ['*'], 'rrdata.rrdatad.index': ['swsindex/*']}

setup_kwargs = {
    'name': 'rrdata',
    'version': '0.2.1',
    'description': '',
    'long_description': 'rrdata is python project for china stock analysis.\n\ndefault database id rrdata\n\nanalysis database is rralpha/rqfactor\n\n\nrrdatad is fetch all data form open source(web/api);\ninclude:\n(stock--sina/eastmoney/tusharepro;\nindex --- swsindex.com / legulegu.com / \nfund -- \n)\ncron  record  to database rrdata;\n\n\nrrdatac is api to get data from my database server or web(realtime/spot)\n\nsefult analysis alpha factor to database rralpha cronly.\n\n\n\nusage:\n\n1.rrdsk init;\n\na. run rqLocalize for mkdir ~/.rrsdk/setting for config\n\nb. cp config.json and config.ini to path(setting)\n\nc. config include: sql password / database-server-ip/name/port, sql-uri, tusharepro-token and so on.\n\nd. .rrsdk save to romepeng/.rrsdk.git (private) by git push;\n\n2. get rrdata --data(index/stock/fund/bond) by rrdatac(rrdata) api;\n\n   get quant alpha factor from database rqfactor or rralpha\n\n3. you can show your analysis results to web by streamlit / pyecharts / hightcharts  and so on;\n\n\n\n\n',
    'author': 'romepeng',
    'author_email': 'romepeng@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/romepeng/rrdata.git',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
