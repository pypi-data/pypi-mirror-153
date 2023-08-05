# see MyTT in github : mpquant/MyTT

# import modules
from MyTT import *
from rrdata.stock import stock
# get data -- df(price)

df = stock.get_price(code, count=120,frequency='1d')
CLOSE=df.close.values
# indicator
def MA(S,N):
    return pd.Series(S).rolling(N).mean().values
MA5 = MA(CLOSE,5)

