from app.talibs import Hangqing
from app.dingding import Message
from app.orders import Order
import pandas as pd
from app.yongxu import Shuchu
import time
import os
import sys
import logs
logger = logs.logger
def yunxing(lista):
    for names in lista:
        time.sleep(3)
        data = {'instId':names,
        'side':"1m",
           'sz':100}
        path = "/api/v5/market/candles"
        ord = Order(data)
        ord.jiaoyi()
    return "aa"

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #lista = ["ETHUSDT"]
    #symbol_list = Shuchu().yongxuheyue()
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    data = {}
    listname = []
    yong_list =  ["ETHUSDT","DOGEUSDT","BTCUSDT"]
    chicang_lis = list(Order(data).chicang()['symbol'])

    print("dddddddddddddddddddddddddddddd",now[14:16])
   
    symbol_list = Shuchu().yongxuheyue()
    

    alls_list =symbol_list +yong_list+chicang_lis       
    for names in alls_list:
        datas = {'instId':names}
        ord = Order(datas)
        ord.jiaoyi()
