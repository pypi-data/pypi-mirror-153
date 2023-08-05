from rrdata.utils.rqLogs import rq_util_log_expection, rq_util_log_info
from rrdata.utils.rqPgsql import read_data_from_pg
from rrdata.utils.rqParameter import SWL_LEVEL

rq_util_log_info(SWL_LEVEL().LEVEL)

def get_index_sw_class(level=""):
    df = read_data_from_pg("swl_list",)
    #rq_util_log_info(f"swl index class from rrdara:swl_list. \n {df}")
    if not level:
        return df
    elif level in SWL_LEVEL().LEVEL:
        df = df[df.level == level]
        return df
    else:
        rq_util_log_expection("swl level code is not exist ! ")


if  __name__ == '__main__':
    rq_util_log_info(f"swl index class from rrdara:swl_list. \n {get_index_sw_class()}")
    for l in SWL_LEVEL().LEVEL:
        rq_util_log_info(f"swl level: {l}\n{get_index_sw_class(l)}")

    
    


