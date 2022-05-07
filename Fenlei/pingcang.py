import logs

logger = logs.logger
# from app.talibs import Hangqing
from app.hanshupd import hanshu
from app.dingyiuhanyi import xingtai
from app.dingding import Message
import talib as ta
import numpy as np
import pandas as pd
import logs

logger = logs.logger


class Pingcangorder(object):
    def __init__(self, df):
        self.df = df

    # def junxianpanduan(self,n,m):
    #     ma_5 = ta.WMA(self.df['close'], timeperiod=5)
    #     ma_15 = ta.WMA(self.df['close'], timeperiod=15)
    #     ma_30 = ta.WMA(self.df['close'], timeperiod=38)
    #
    #     self.df['ma_5'] = ma_5
    #     self.df['ma_15'] = ma_15
    #     self.df['ma_30'] = ma_30
    #     self.df['ma_5_15'] = self.df['ma_5'] - self.df['ma_30']
    #
    #     self.df['lable_5_10'] = self.df['ma_5_15'].apply(lambda x: 1 if x > 0 else 0)
    #
    #     sum_5 = self.df['lable_5_10'].iloc[len(self.df) -15:len(self.df)].sum()
    #
    #     hshu = hanshu(self.df)
    #     #roc_lable,junxian = hshu.pingjunxian()
    #
    #
    #     roc3 = hshu.ROC(self.df,m,"close")
    #     ## 短周期的排列
    #     #roc2_rate = np.sum(hshu.ROC(df1, 30,"close")[2:0])
    #     ## 30个周期如果是回调了1.8%，则止损，适用场景在全部场景
    #     if np.mean(roc3[-2:]) >n :
    #
    #         mean_a = 1
    #
    #     elif np.mean(roc3[-2:]) < -n:
    #
    #         mean_a = 2
    #     else:
    #         mean_a = 3
    #
    #     high_df = self.df['high'].iloc[-10:].max()
    #     low_df = self.df['high'].iloc[-10:].min()
    #     close_df = self.df['close'].iloc[-1:].mean()
    #     rate_high = (high_df-close_df)/close_df
    #     rate_low = (close_df-low_df)/close_df
    #     if rate_high >0.008 and high_df > 1.008*self.df['close'].iloc[-80:-8].quantile(q=0.9):
    #
    #         bodongs = 2
    #     elif rate_low >0.008 and low_df <0.993*self.df['close'].iloc[-80:-8].quantile(q=0.1):
    #
    #         bodongs =1
    #     else:
    #         bodongs = 3
    #
    #
    #
    #     #### n个周期在30日均线止损
    #
    #     logger.info('平仓指标均线' + str(mean_a) + '平仓指标短时间波动大' + str(bodongs))
    #     return (mean_a,bodongs)

    def bongdong(self, n):
        high_df = self.df['high'].iloc[-4:].max()
        low_df = self.df['low'].iloc[-4:].min()
        close_df = self.df['close'].iloc[-1:].mean()
        rate_high = (high_df - close_df) / close_df
        rate_low = (close_df - low_df) / close_df
        hshu = hanshu(self.df)
        rates =hshu.ROC(self.df,7,"close")[-30:]

        if rate_high > n and high_df > 1.008 * self.df['close'].iloc[-80:-8].quantile(q=0.9) and np.max(rates)>0.018 :

            bodongs = 2
        elif rate_low > n and low_df < 0.92 * self.df['close'].iloc[-80:-8].quantile(q=0.1) and np.max(rates) < -0.018:



            bodongs = 1
        else:
            bodongs = 3
        return bodongs
    def angerjiaodu(self):
        hshu = hanshu(self.df)
        ma_5 = list(ta.WMA(self.df['close'], timeperiod=3))
        anger1 = hshu.angle_panduan_list(ma_5[-40:-10])
        anger2 = hshu.angle_panduan_list(ma_5[-20:])
        #anger1 = np.mean(anger1_list) 
        #anger2 = np.mean(anger2_list) 
        if anger2==2 and anger1==5:
            a = 2
        elif anger2==1 and anger1==4:
            a = 1
        else:
            a = 3
        return a
    def gaodipingcang(self,n):

        lable_di = 3
        if self.df['close'].iloc[-1:].mean() > self.df['close'].iloc[-n:].quantile(q=0.92):
            lable_di = 2
        elif self.df['close'].iloc[-1:].mean() < self.df['close'].iloc[-n:].quantile(q=0.12):
            lable_di = 1
        else:
            lable_di = 3
        return lable_di


    def KELCH_pingcang(self, df1, n):
        """  缺陷在与暴跌的或者暴涨就买了 """

        rates_2 = list(ta.WMA(self.df['close'], timeperiod=8))
        angle = hanshu(self.df).angle(rates_2[-5:])

        
        KelChM = pd.Series(((df1['high'] + df1['low'] + df1['close']) / 3).rolling(n).mean(), name='KelChM')
        KelChU = pd.Series(((4 * df1['high'] - 2 * df1['low'] + df1['close']) / 3).rolling(n).mean(),
                           name='KelChU')
        KelChD = pd.Series(((-2 * df1['high'] + 4 * df1['low'] + df1['close']) / 3).rolling(n).mean(),
                           name='KelChD')
        df2 = df1.join(KelChM)
        df2 = df2.join(KelChU)
        df2 = df2.join(KelChD)
        df2['up_c'] = df2['KelChU'] - df2['close']
        df2['do_c'] = df2['KelChD'] - df2['close']
        df2['M_clo'] = df2['KelChM'] - df2['close']
        df2['M_lable'] = df2['M_clo'].apply(lambda x: 1 if x > 0.001 else (0 if x < -0.001 else -1))
        #
        dd = df2['M_lable'].iloc[-9:-1].value_counts()
        dd_dict = dd.to_dict()
        # print(dd_dict)
        try:
            ones = dd_dict[1]
            #zero = dd_dict[0]
        except:
            ones = 0
            #zero = 0
        try:
            zero = dd_dict[0]
        except:
            zero = 0
        if df2['up_c'].iloc[-1:].mean() / df2['close'].iloc[-2:].mean() < -0.005  \
                and df2.iloc[-1:]['close'].mean() < df2.iloc[-85:-2]['close'].quantile(q=0.97) and zero < 7 and angle<55:
            lable_kelch = 2
        elif df2['do_c'].iloc[-1:].mean() / df2['close'].iloc[-2:].mean() > 0.007  \
                and df2.iloc[-1:]['close'].mean() > df2.iloc[-85:-2]['close'].quantile(q=0.05) and ones<7 and angle>135:
            lable_kelch = 1
        else:
            lable_kelch = 3
        return lable_kelch
    def BBANDS(self,df,m,n):
        
        df['upper'], df['middle'], df['lower'] = ta.BBANDS(
            df.close.values,
            timeperiod=30,
            nbdevup=m,
            nbdevdn=n,
            matype=0)

        self.df['up_c'] = df['upper'] - df['close']
        self.df['do_c'] = df['lower'] - df['close']
        self.df['M_clo'] = df['middle'] - df['close']

        df2 = df
        if df2['up_c'].iloc[-1:].mean() / df2['close'].iloc[-1:].mean() < -0.001 and df2['up_c'].iloc[-2:].mean() / df2['close'].iloc[-2:].mean() > -0.016 and df2.iloc[-1:]['close'].mean() < df2.iloc[-80:-2]['close'].quantile(q=0.98):

            lable_kelch = 2
        elif df2['do_c'].iloc[-1:].mean() / df2['close'].iloc[-1:].mean() > 0.001 and \
                df2['do_c'].iloc[-2:].mean() / df2['close'].iloc[-2:].mean() < 0.016 and df2.iloc[-1:]['close'].mean() > df2.iloc[-80:-2]['close'].quantile(q=0.05)  :

            lable_kelch = 1
        else:
            lable_kelch = 3
        return lable_kelch

    def jidiezhang(self,df1, n):
        return 3




    def chengjiaoliang(self,m):
        highs_close = self.df.iloc[-100:-4]['close'].quantile(q=0.90)
        low_close = self.df.iloc[-100:-4]['close'].quantile(q=0.05)
        xitai = xingtai()
        #        a,b = xitai.Kred(self.df['high'].iloc[-1:].mean(), self.df['close'].iloc[-1:].mean(), self.df['low'].iloc[-1:].mean(),
        #                   self.df['open'].iloc[-1:].mean())
        e = xitai.changyingxian(self.df['high'].iloc[-1:].mean(), self.df['close'].iloc[-1:].mean(),
                                self.df['low'].iloc[-1:].mean(),
                                self.df['open'].iloc[-1:].mean())
        sum_volume = self.df['volume'].iloc[-2:].max()
        if sum_volume > self.df['volume'].iloc[-13:-5].mean()*m and e==1 and self.df['high'].iloc[-2:-1].mean() >highs_close :
            a = 2
        elif sum_volume > self.df['volume'].iloc[-13:-5].mean()*m and e==1 and self.df['low'].iloc[-2:-1].mean() < low_close:
            a = 1
        else:
            a = 3
        return a

    ##上影线和下影线平仓
    def shanying(self,rate,zhengfurate):
        hshu = hanshu(self.df)
        # roc_lable,junxian = hshu.pingjunxian()

        roc3 = hshu.ROC(self.df, 20, "close")
        xitai = xingtai()
#        a,b = xitai.Kred(self.df['high'].iloc[-1:].mean(), self.df['close'].iloc[-1:].mean(), self.df['low'].iloc[-1:].mean(),
#                   self.df['open'].iloc[-1:].mean())
        e = xitai.changyingxian(self.df['high'].iloc[-1:].mean(), self.df['close'].iloc[-1:].mean(), self.df['low'].iloc[-1:].mean(),
                   self.df['open'].iloc[-1:].mean())
        zhengfu = (self.df['high'].iloc[-1:].mean()-self.df['low'].iloc[-1:].mean())/self.df['close'].iloc[-1:].mean()
        # 一定周期上涨n，最后是长
        if roc3[-1] >rate and e==1 and zhengfu>zhengfurate and self.df['volume'].iloc[-1:].mean()>2*self.df['volume'].iloc[-50:-1].mean():
            lable = 2
        elif roc3[-1] < -rate and e == 1 and zhengfu>zhengfurate and self.df['volume'].iloc[-1:].mean()>2*self.df['volume'].iloc[-50:-1].mean():
            lable = 1
        else:
            lable = 3
        return lable

    def junxian(self, n, m,timeperiod):
        ma_5 = ta.EMA(self.df['close'], timeperiod=2)
        ma_15 = ta.EMA(self.df['close'], timeperiod=15)
        ma_30 = ta.EMA(self.df['close'], timeperiod=timeperiod)

        self.df['ma_5'] = ma_5
        self.df['ma_15'] = ma_15
        self.df['ma_30'] = ma_30
        self.df['ma_5_15'] = (self.df['ma_5'] - self.df['ma_30'])/self.df['close']

        # self.df['lable_5_10'] = self.df['ma_5_15'].apply(lambda x: 1 if x > 0 else 0)

        # sum_5 = self.df['lable_5_10'].iloc[len(self.df) - 15:len(self.df)].sum()

        #hshu = hanshu(self.df)
        # roc_lable,junxian = hshu.pingjunxian()

        #roc3 = hshu.ROC(self.df, m, "close")
        roc3 =list(self.df['ma_5_15'])
        ## 短周期的排列
        # roc2_rate = np.sum(hshu.ROC(df1, 30,"close")[2:0])
        ## 30个周期如果是回调了1.8%，则止损，适用场景在全部场景
        if np.mean(roc3[-m:]) > n:

            mean_a = 1

        elif np.mean(roc3[-m:]) < -n:

            mean_a = 2
        else:
            mean_a = 3
        return mean_a

    def smass(self, n,rate_1,rate_2):
        self.df['ma_5'] = ta.WMA(self.df['close'], timeperiod=5)
        ma_30 = ta.WMA(self.df['close'], timeperiod=n)
        self.df["ma_30"] = ma_30
        self.df['rates'] = (self.df["ma_30"] - self.df['ma_5'])/self.df["ma_30"]
        list_ROC = list(self.df['rates'])
        if np.mean(list_ROC[-30:-15]) > rate_1 and np.mean(list_ROC[-15:]) < -rate_2 :
            jinxian_lable = 2

        elif np.mean(list_ROC[-30:-15]) < -rate_1 and np.mean(list_ROC[-15:]) > rate_2:

            jinxian_lable = 1
        else:
            jinxian_lable = 3
        return jinxian_lable

    #成交量过大，则有可能反转
    def max_vol(self,n,m):
        hshu = hanshu(self.df)
        self.df['dm'] = ta.MINUS_DM(self.df.high, self.df.low,  timeperiod=14)
        #rates, red_sum, blue_sum = hshu.vu_rate_time("close",30,80)

        #rates1 = self.df.iloc[-3:]

        if self.df['volume'].iloc[-5:-2].mean()>m*self.df['volume'].iloc[-n:-8].mean() \
            and (self.df['high'].iloc[-5:-2].max()-self.df['close'].iloc[-5:-2].mean())/self.df['close'].iloc[-3:-2].mean()>0.008 \
            and self.df['close'].iloc[-1:].mean() <(self.df['high'].iloc[-5:-2].max()+self.df['low'].iloc[-5:-2].mean())/2:

            lable = 2
        elif self.df['volume'].iloc[-5:-2].max()>m*self.df['volume'].iloc[-n:-5].mean() \
            and (self.df['low'].iloc[-5:-2].min()-self.df['close'].iloc[-5:-2].mean())/self.df['close'].iloc[-5:-2].mean()< -0.008 \
            and self.df['close'].iloc[-1:].mean() >(self.df['close'].iloc[-5:-2].mean()+self.df['low'].iloc[-3:-2].mean())/2:
            lable = 1
        else:
            lable=3
        return lable

    ### 突破下跌，反转指标

    def pingcangzhibia(self, n, m):
        hshu = hanshu(self.df)
        logger = logs.logger
        #tupo = hshu.pingtantupo_kai(n)
        tupo = 3

        lable_quantile = hshu.fenweishu(m)
        logger.info('平仓指标突破' + str(tupo) + '平仓指标反转' + str(lable_quantile))
        ping_lable = 0
        if tupo == 1 or lable_quantile == 1:
            ping_lable = 1
        elif tupo == 2 or lable_quantile == 2:
            ping_lable = 2
        else:
            ping_lable = 3
        return ping_lable
