

from app.talibs import Hangqing
from app.dingding import Message

class Jushu(object):
    def __init__(self,data,path):
        self.data = data
        self.path = path
    def shuchu(self):
        tab = Hangqing(self.data, self.path)
        msg = Message()
        a, b, c, d, e, f, k_vlue, d_value = tab.pingju()
        dicta = {}
        dicta['品种'] = "DOGE-USDT"
        if a == 1:
            dicta['平均线'] = "上涨阶段"
        elif a == 2:
            dicta['平均线'] = "下跌阶段"
        else:
            dicta['平均线'] = "震荡阶段"

        if b == 1:
            dicta['ADX'] = "趋势很强"
        elif b == 2:
            dicta['ADX'] = "趋势强"
        else:
            dicta['ADX'] = "趋势一般"

        dicta['K值'] = k_vlue
        dicta['D值'] = d_value
        if e == 1:
            dicta['ATR'] = "波动大"
        elif e == 2:
            dicta['ATR'] = "波动小"
        else:
            dicta['ATR'] = "波动正常"

        if f == 1:
            dicta['OBV'] = "能量潮大"
        elif f == 2:
            dicta['OBV'] = "能量潮小"
        else:
            dicta['OBV'] = "能量潮正常"
        msg.dingding_warn(str(dicta))
        return dicta