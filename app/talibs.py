
from binance_f import RequestClient
from binance_f.model import *
from binance_f.constant.test import *
from binance_f.base.printobject import *
import pandas as pd

from app.authorization import api_key, api_secret,passphrase

from app.dingyiuhanyi import xingtai
import talib as ta
from app.OkexAPI import Okex

from app.hanshupd import hanshu
import numpy as np
import pandas as pd
from Fenlei.shangsheng import  Updown
from Fenlei.pingcang import Pingcangorder

from app.dingding import Message
import time
import time
import logs
logger = logs.logger

localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 

msg = Message()

class Hangqing(object):
    def __init__(self,data):
        self.data = data


    def pingju(self,times):
        list_open = []
        list_close = []
        list_low = []
        list_high = []
        list_closeTime = []
        list_quoteAssetVolume = []
        request_client = RequestClient(api_key=None, secret_key=None)
        if times =="3m":
            aa = CandlestickInterval.MIN3
        elif times =="5m":
            aa = CandlestickInterval.MIN5
        elif times =="1m":
            aa = CandlestickInterval.MIN1
        elif times =="15m":
            aa = CandlestickInterval.MIN15
        elif times =="30m":
            aa = CandlestickInterval.MIN30
        elif times =="1H":
            aa =CandlestickInterval.HOUR1
        elif  times =="4H":
            aa = CandlestickInterval.HOUR4
        elif  times =="1m":
            aa = CandlestickInterval.MIN1
        else:
        
            aa = CandlestickInterval.DAY1
        #print(aa)
        

        result = request_client.get_candlestick_data(symbol=self.data['instId'], interval=aa,
                                                     startTime=None, endTime=None, limit=1000)

        #print("======= Kline/Candlestick Data =======")
        # PrintMix.print_data(result[0])
        for uu in result:
            list_open.append(uu.open)
            list_close.append(uu.close)
            list_low.append(uu.low)
            list_high.append(uu.high)
            list_closeTime.append(uu.closeTime)
            list_quoteAssetVolume.append(uu.quoteAssetVolume)
        df = pd.DataFrame()
        df['open'] = list_open
        df['high'] = list_high
        df['low'] = list_low
        df['close'] = list_close
        df['volume'] = list_quoteAssetVolume
        df['closeTime'] = list_closeTime

        
        df = df.astype(float)

        #print(df)
        return df
    def timesss(self,n,df):
        list_close=list(df['close'])
        list_open=list(df['open'])
        list_high=list(df['high'])
        list_low=list(df['low'])
        lit_vol = list(df['volume'])
        num = int(len(df) /n)
        close_l = []
        open_l = []
        high_l = []
        low_l = []
        vol_l =[]
        for ii in range(1, num+1):
            close_l.append(list_close[n*ii-1])
            open_l.append(list_open[n*(ii - 1)])
            high_l.append(np.max(list_high[n*(ii - 1):n*ii-1]))
            low_l.append(np.min(list_low[n*(ii - 1):n*ii-1]))
            vol_l.append(np.sum(lit_vol[n*(ii - 1):n*ii-1]))
#     close_l.append(list_close[-1])
#     open_l.append(list_open[- 1])
#     high_l.append(np.max(list_high[-1]))
#     low_l.append(np.min(list_low[-1]))
#     vol_l.append(np.sum(lit_vol[-1]))
        df = pd.DataFrame()
        df['open'] = open_l
        df['high'] = high_l
        df['low'] = low_l
        df['close'] = close_l
        df['volume'] = vol_l
        return df

    def shuchudf(self):

        df = self.pingju("3m")
        #print('df1df1df1df1',df)
        df1 = self.timesss(4, df)
        #print('df1df1df1df1',df1)
        udz = Updown(df1)
        close_30_sum, mean_a, roc, rates = udz.junxianpanduan()
        logger.info("15分钟" + str(close_30_sum))

        list_suma_15 = hanshu(df).rates_sum(rates)

        #rates_duanqi = (list(df1['close'])[-1] - np.mean(list(df1['close'])[-30:-29])) / np.mean(list(df1['close'])[-30:-29])
        df['timepri']=ta.EMA(df['close'], timeperiod=45)
        df['close_timepri'] = (df['close']-df['timepri'])/df['timepri']
        rates_45_df = list(df['close_timepri'])
        rates_duanqi=np.mean(rates_45_df[-2:])
        close_45 = list(ta.EMA(df['close'], timeperiod=20))
        #print('close_45close_45close_45close_45',close_45[-30:])
        close_45_anger =0


        df1['timepri']=ta.EMA(df1['close'], timeperiod=30)
        df1['close_timepri'] = (df1['close']-df1['timepri'])/df1['timepri']
        list_up = [0]
        list_down = [0]
        logger.info(self.data['instId'] + "close_time"+str(list(df1['close_timepri'])[-6:]))
        for ii in list(df1['close_timepri'])[-10:]:
            #print('iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii',ii)
            if ii >0.008 :
                list_up.append(ii)
            elif ii < -0.008:
                list_down.append(ii)
            else:
                pass
        bl_up = len(list_up)/2
        bl_down = len(list_down)/2
        sum_up = np.sum(list_up)
        sum_down = np.sum(list_down)
        bl_rate_up = sum_up/len(list_up)
        bl_rate_down = sum_up/len(list_down)
        
#         df2 = self.pingju("HOUR1")
#         #df2 = self.timesss(10, df)
#         udz2 = Updown(df2)
#         close_30_sum2, mean_a2, roc2, rates2 = udz2.junxianpanduan()
#
#         list_suma_30 = hanshu(df).rates_sum(rates2)
#         logger.info("30分钟" + str(close_30_sum2))
#
#         rates_changqi = (list(df2['close'])[-1] - np.mean(list(df2['close'])[-98:-97])) / np.mean(list(df2['close'])[-98:-97])
#         close_45 = list(ta.EMA(df2['close'], timeperiod=60))
#         close_45_anger = hanshu.angle_panduan_list(close_45)
#
# #        df2['timepri']=ta.EMA(df2['close'], timeperiod=30)
# #        df2['close_timepri'] = (df2['close']-df2['timepri'])/df2['timepri']
# #        rates_45_df2 = list(df2['close_timepri'])
# #        rates_changqi = rates_45_df2[-1]
#         print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',rates_duanqi,rates_changqi,len(df2))
        return (df,df1, close_30_sum,  roc, rates, list_suma_15,  rates_duanqi, close_45_anger,len(list_up),len(list_down),sum_up,sum_down)

    def celv(self):

        df,df1, close_30_sum,  roc, rates, list_suma_15,  rates_duanqi, close_45_anger,len_list_up,len_list_down,sum_up,sum_down = self.shuchudf()
        bl_rate_up = sum_up/len_list_up
        bl_rate_down = sum_down/len_list_down
        logger.info(self.data['instId'] + "bl_rate_up"+str(sum_up ))
        logger.info(self.data['instId'] + "bl_rate_down"+str(sum_down))
        close_sell = float(list(df1['close'])[-1])
        udz1 = Updown(df)
        n_rate = 2*df['close'].iloc[-200:-10].std() / df['close'].iloc[-200:-10].mean()
        #
        logger.info(self.data['instId'] + "正态分布"+str(n_rate))
        rates_changqi_num = 0.04
        rates_duanqi_num = 0.008
        if bl_rate_up>0.01 and len_list_up>2 :
            dianwei, money_k = udz1.uptwo()
            hang_status = 1
            msg.dingding_warn(self.data['instId']+" 大周期上升")
            logger.info(self.data['instId'] + " 最近强势")
        elif bl_rate_down< -0.01 and len_list_down>2:
            dianwei, money_k = udz1.downone()
            hang_status = 2
            logger.info(self.data['instId'] + " 最近弱势")
            msg.dingding_warn(self.data['instId']+" 最近弱势")
#
#        if  rates_duanqi > rates_duanqi_num :
#            # msg.dingding_warn(self.data['instId']+" 大周期上升")
#            logger.info(self.data['instId'] + " 最近强势")
#            dianwei, money_k = udz1.uptwo()
#            hang_status = 1
#        elif rates_duanqi < -rates_duanqi_num:
#            logger.info(self.data['instId'] + " 最近弱势")
#            dianwei, money_k = udz1.downone()
#            hang_status = 2
#
#
#
        else:
            dianwei, money_k = udz1.zhendang()
            hang_status = 10
            logger.info(self.data['instId'] + " 震荡")
            msg.dingding_warn(self.data['instId']+" 震荡")
        #logger.info(self.data['instId'] + str(rates_duanqi))
        return (hang_status, dianwei, close_sell, money_k)




#    def shangpingcang(self):
#        df1 = self.pingju("3m")
#        n_rate = df1['close'].iloc[-90:].std() / df1['close'].iloc[-90:].mean()
#        n_bodong = np.min([n_rate*2.5,0.015])
#        pc = Pingcangorder(df1)
#        ping_lable = pc.pingcangzhibia(60, 35)
#        bongdong = pc.bongdong(n_rate*2)
#        mean_a = pc.junxian(0.002, 3,20)
#        jinxian_lable = pc.smass(23,0.006,0.003)
#        shangying = pc.shanying(0.01, 0.012)
#        max_vol = pc.max_vol(120,7)
#        angerjiaodu = pc.angerjiaodu()
#        chengjiaoliang = pc.chengjiaoliang(2)
#        return (ping_lable, bongdong, mean_a, jinxian_lable, shangying, max_vol,angerjiaodu,chengjiaoliang)
    def shangpingcang(self):
        df1 = self.pingju("5m")
        pc = Pingcangorder(df1)
        n_rate = df1['close'].iloc[-90:].std() / df1['close'].iloc[-90:].mean()
        n_bodong = pc.bongdong(n_rate*2)
        #if n_rate <0.01:
        bongdong = 0
        shangying=0
        
        
        ping_lable = pc.pingcangzhibia(60, 35)
        #bongdong = 0
        mean_a = pc.junxian(0.002, 3,25)
        jinxian_lable = 0
        #shangying = 0
        max_vol = 0
        angerjiaodu = 0
        chengjiaoliang = 0
        return (ping_lable, bongdong, mean_a, jinxian_lable, shangying, max_vol,angerjiaodu,chengjiaoliang)


    def qiangshizhengdang(self):
        df1 = self.pingju("5m")
        n_rate = df1['close'].iloc[-90:].std() / df1['close'].iloc[-90:].mean()
        n_bodong = np.min([n_rate*2.5,0.015])
        pc = Pingcangorder(df1)
        ping_lable = pc.pingcangzhibia(55, 35)
        bongdong = pc.bongdong(n_rate*2)
        mean_a = pc.junxian(0.002, 4,20)
        jinxian_lable = pc.smass(30,0.005,0.004)
        shangying = pc.shanying(0.01, 0.012)
        max_vol = pc.max_vol(140,5)
        roc_lable = pc.jidiezhang(df1, 70)
        angerjiaodu = pc.angerjiaodu()
        chengjiaoliang = pc.chengjiaoliang(2.5)
        return (ping_lable, bongdong, mean_a, jinxian_lable, shangying, max_vol,roc_lable,angerjiaodu,chengjiaoliang)       

#    def zhengpingcang(self):
#        df1 = self.pingju("5m")
#        n_rate = 1.5 * df1['close'].iloc[-90:].std() / df1['close'].iloc[-90:].mean()
#        pc = Pingcangorder(df1)
#        ping_lable = pc.pingcangzhibia(80, 75)
#        bongdong = pc.bongdong(n_rate)
#        #mean_a = pc.junxian(0.003, 2)
#        mean_a = pc.junxian(0.002,7,30)
#        lable_di = pc.BBANDS(df1,3.8,4.6)
#        shangying = pc.shanying(0.008, 0.01)
#        max_vol = pc.max_vol(150,6)
#        # hshu = hanshu(df1)
#        # roc_lable, junxian = hshu.pingjunxian()
#        roc_lable = pc.jidiezhang(df1, 70)
#        junxian = 0
#        return (ping_lable, bongdong, mean_a, roc_lable, junxian, lable_di, shangying, max_vol)



    def zhengpingcang(self):
        df1 = self.pingju("5m")
        n_rate = 1.5 * df1['close'].iloc[-90:].std() / df1['close'].iloc[-90:].mean()
        #if n_rate <0.01:
        bongdong =0
        #shangying=0
      
       
        pc = Pingcangorder(df1)
        ping_lable = pc.pingcangzhibia(60, 35)
        #bongdong = 0
        #mean_a = pc.junxian(0.003, 2)
        mean_a = pc.junxian(0.002,3,60)
        lable_di = 0
        shangying =  pc.shanying(0.008, 0.01)
        max_vol = 0
        # hshu = hanshu(df1)
        # roc_lable, junxian = hshu.pingjunxian()
        roc_lable =0
        junxian = 0
        return (ping_lable, bongdong, mean_a, roc_lable, junxian, lable_di, shangying, max_vol)
    def mysqlsell(self,namess, order, lables):
        import pymysql.cursors
        import pymysql
        df1,close_30_sum,close_30_sum2,roc,rate,rate2= self.shuchudf()
        closes = list(df1['close'])[-1]
        import datetime
        timess = datetime.datetime.now()
        # timess = "33"

        connection = pymysql.connect(host='47.93.194.57',
                                     port=3306,
                                     user='root',
                                     password='1160329981wj',
                                     db='xunibi',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:

                # 执行sql语句，插入记录
                SQL = """insert into jiaoyijilu(names,times,close,orderss,lable) values (%s,%s,%s,%s,%s)"""
                cursor.execute(SQL, (namess, timess, closes, order, lables))
                # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
                connection.commit()
        except Exception as e:
            print('***** Logging failed with this error:', str(e))
        return "aa"

    def cangwei(self):

        df = self.pingju("3m")
        #print(df)
#        pdjieguo = hanshu(df)
#
#        vol,lable_staus,mean_a, qushi_b, c, bodong_d, bofu_e, obv_f, k_vlue, d_value, diff_k, RSI_g, KAMA_h, lista_k_buy_one, lista_k_buy_two, lista_k_buy_three, \
#        lista_k_sell_one, lista_k_sell_two, lista_k_sell_three, list_up_down = pdjieguo.hunza(list_open, list_high,
#                                                                                              list_low, list_close,
#                                                                                              list_volue)
#
#        BOP, AROONOSC, cci, CMO, MFI, MOM, PLUS_DI, RSI, WILLR = pdjieguo.ivszhibiao()
        a = 0
#        if  mean_a == 1 and KAMA_h==1 and  vol==1 :
#            a = 1
#
#
#        elif mean_a ==2   and KAMA_h==2  and  vol==2:
#            a = 2
#
#        elif mean_a != 1 and mean_a != 2 and (k_vlue >95 or lable_staus==2):
#            a = 3
#        elif mean_a != 1 and mean_a != 2 and (k_vlue <15 or lable_staus==1):
#            a = 4
#
#        # elif  k_vlue >99:
#        #      a = 2
#
#        else:
#            a = 0

        return a

