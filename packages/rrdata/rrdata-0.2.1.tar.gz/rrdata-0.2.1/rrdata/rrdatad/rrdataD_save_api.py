#!/usr/bin/python
""" see bigquant doc
    DataSource("basic_info_IndustrySw").read(instruments=stock_lists)
    out: DataFrame
"""
from rrdata.common.engine_pgsql import engine


class RrdataDSave(object):
    """ see:
        bigquant DataSource("trade_days").read() 
        also add  can change:
        save data(dataframe) to database-table by sql_driver
    """
    def __init__(self, table_name, 
               con=engine(driver="", db_name="rrdata"),
               if_exists='replace' ):
        """ driver: ""-default - poasgresql/ psycopg2   db_name  rrdata/rrshare/rrfactor"""
        self.table_name = table_name
        self.engine = con
        self.if_exists = if_exists

    def __repr__(self) -> str:  # name 
        return f"<{self.__class__.__name__} table_name={self.table_name}>"

   
    def save(self, data):
        try:
            data.to_sql(self.table_name, con=self.engine, if_exists=self.if_exists, index=False)
            print(f"Saved {len(data)} rows to Table:<{self.table_name}>/DB:<{self.engine}>, finish !")
        except Exception as e:
            print(e)


if  __name__ == "__main__":
    #from rrdata.rrdatad.stock.fetch_stock_list import  fetch_stock_list_tusharepro
    #data = fetch_stock_list_tusharepro()
    #table_name = 'stock_list_tspro'
    #print(RrdataDSave(table_name).__repr__())
    #RrdataDSave(table_name).save(data)
    from rrdata.rrdatad.stock.stock_zh_a_hist_em import stock_zh_a_spot_em
    print(stock_zh_a_spot_em())
    RrdataDSave("stock_spot_20220525").save(stock_zh_a_spot_em())
    



