# use eastmoney data (hist and spot)
 see akshare/stock_feature/stock_hist_em.py

 if just caculate 250 days(52 weeks hist days),
 use qfq for default

 df = pd.merge(df_factor, df_p, how='left', on='code').sort_values(by = 'code')
    df['trade_date'] = pd.to_datetime(df['trade_date'], format='%Y-%m-%d')
    delist_code = fetch_delist_stock(trade_date)
    df=df[~df['code'].isin(delist_code)]

   delist_code = fetch_delist_stock(trade_date)
    res=res[~res['code'].isin(delist_code)]
    res.fillna({'pct_chg':0,'vol':0,'amount':0}, inplace=True)
    
df21=df1.drop(labels=[1,3],axis=0)   # axis=0 表示按行删除，删除第1行和第3行
删除指定的某几列
df4=df1.drop(labels=['gender',"age"],axis=1)  # axis=1 表示按列删除，删除gender、age列