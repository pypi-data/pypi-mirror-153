#!/usr/bin/python
""" see bigquant doc
    DataSource("basic_info_IndustrySw").read(instruments=stock_lists)
    out: DataFrame
"""

from rrdata.common import read_df_from_table, save_df_to_pgsql
from rrdata.common.engine_pgsql import engine


class RrdataD(object):
    """ see:
        bigquant DataSource("trade_days").read() 
        also add  can change:
        source database/sql_driver
    """
    def __init__(self,table_name, 
               datasource=engine(driver="", db_name="rrdata"),
                ):
        """ driver: ""-default - poasgresql/ psycopg2   db_name  rrdata/rrshare/rrfactor"""
        self.table_name = table_name
        self.engine = datasource

    def __repr__(self) -> str:  # name 
        return f"<{self.__class__.__name__} table_name={self.table_name}>"

    def read(self):  # read artubuite
        return  read_df_from_table(self.table_name, self.engine)

    #def save(self, data):
    #    return save_df_to_pgsql(data, self.table_name)


if  __name__ == "__main__":
    print(RrdataD("swl_list").__repr__())
    RrdataD('stock_list').read()
    #RrdataD('trade_days').read()
    



