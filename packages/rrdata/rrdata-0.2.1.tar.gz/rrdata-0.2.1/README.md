rrdata is python project for china stock analysis.

default database id rrdata

analysis database is rralpha/rqfactor


rrdatad is fetch all data form open source(web/api);
include:
(stock--sina/eastmoney/tusharepro;
index --- swsindex.com / legulegu.com / 
fund -- 
)
cron  record  to database rrdata;


rrdatac is api to get data from my database server or web(realtime/spot)

sefult analysis alpha factor to database rralpha cronly.



usage:

1.rrdsk init;

a. run rqLocalize for mkdir ~/.rrsdk/setting for config

b. cp config.json and config.ini to path(setting)

c. config include: sql password / database-server-ip/name/port, sql-uri, tusharepro-token and so on.

d. .rrsdk save to romepeng/.rrsdk.git (private) by git push;

2. get rrdata --data(index/stock/fund/bond) by rrdatac(rrdata) api;

   get quant alpha factor from database rqfactor or rralpha

3. you can show your analysis results to web by streamlit / pyecharts / hightcharts  and so on;




