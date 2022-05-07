
import numpy as np

class xingtai(object):
    # def __init__(self,high,close,low,open):
    #     self.high = high
    #     self.close = close
    #     self.low = low
    #     self.open = open

    def Kred(self,high,close,low,open):
        # if close ==high:
        a =-99
        b= -99
        open = open+0.1
        if close >open:
            ## 几乎是阳
            
            if (high-close)/(high-open)<0.2:
                a = 0
            elif  (high-close)/(high-open)>=0.2 and (high-close)/(high-open)<0.5 :
                a = 1
            elif (high - close) / (high - open) >= 0.5 and (high - close) / (high - open) < 0.7:
                a = 2
            #  上影线
            else:
                a =3
	        
        elif close <open:
            # 全阴线
            if  (close-low)/(open-low)<0.2:
                b= 1
            elif (close-low)/(open-low)>=0.2 and (close-low)/(open-low) <0.7:
                b = 2
            ## 下影线
            else:
                b = 3
        return a,b
    def changyingxian(self,high,close,low,open):
        kuandu = high-low
        rate = close-open
        try:
            if np.abs(rate/kuandu) <0.5:
                a = 1
            else:
                a =2
        except:
            a =2
        return  a
    def bili(self,high,close,low,opens):
        if (close-opens)/opens >0.008:
            rate = 1
        elif (close-opens)/opens >0.0035 and (close-opens)/opens <=0.008:
            rate =2
        elif (close-opens)/opens>0 and (close-opens)/opens <=0.0035:
            rate = 3
        elif (close-opens)/opens>-0.003 and (close-opens)/opens <=0:
            rate = 4
        elif (close-opens)/opens>-0.008 and (close-opens)/opens <=-0.003:
            rate = 5
        else:
            rate = 8
        return rate



# def zhuangtai():
#
# # ATR的值小于某一个值
#     pass


