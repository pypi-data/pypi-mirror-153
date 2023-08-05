import pandas as pd

from rrdata.rrdatad.index import *

class SwIndex(object):

    def __init__(self) -> None:
        self.LEVEL=["L1","L2","L3"]
        

    def get_swl_class_cons(self,level="L1"):
        swl_cons = pd.DataFrame()
        for code in sw_index_class(level=level)['index_symbol'].values:
            print(code)
            try:
                swl_cons = pd.concat([swl_cons,sw_index_cons(symbol=code)])
            except Exception as e:
               pass
            print(swl_cons)
        return swl_cons


if __name__ == "__main__":
    swl = SwIndex()
    sw_cons = swl.get_swl_class_cons("L3")
    print(sw_cons)
