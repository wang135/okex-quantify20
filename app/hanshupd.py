
### 上涨阶，急跌是加仓的好机会，下跌时候，急涨是加空的好机会
## 趋势指标，震荡指标，在趋势中啥时候是反转指标，什么是趋势起来，
##震荡中，低买高卖，低买的定义是 通过哪些指标确定，同理高卖通过哪些指标确认
import pandas as pd
from app.dingyiuhanyi import xingtai
import talib as ta
import numpy as np

import math

class hanshu(object):
    def __init__(self ,df):
        self.df = df

    def MOM(self, n):
        M = pd.Series(self.df['close'].diff(n), name = 'Momentum_' + str(n))
        df1 = self.df.join(M)
        return df1
    def ROC(self ,df1, n,name):
        M = df1[name].diff(n - 1)
        N = df1["close"].shift(n - 1)
        ROC = pd.Series(M /np.abs(N), name = 'ROC_' + str(n))
        # df1 = df1.join(ROC)
        list_ROC = list(ROC.values)
        return list_ROC
   ##三重指数平滑平均线
    def TRIX(self ,df, n):
        EX1 = pd.DataFrame.ewm(df['close'], span=n).mean()
        EX2 = pd.DataFrame.ewm(EX1, span=n).mean()
        EX3 = pd.DataFrame.ewm(EX2, span=n).mean()
        i = 0
        ROC_l = [0]
        while i + 1 <= df.index[-1]:
            ROC = (EX3[i + 1] - EX3[i]) / EX3[i]
            ROC_l.append(ROC)
            i = i + 1
        Trix = pd.Series(ROC_l, name='Trix')
        list_Trix = list(Trix.values)
        return list_Trix

    # 顺势指标
    def CCI(self, n):
        PP = (self.df['high'] + self.df['low'] + self.df['close']) / 3
        CCI = pd.Series((PP - PP.rolling(n).mean()) / PP.rolling(n).std(), name='CCI_' + str(n))
        # df1 = self.df.join(CCI)
        list_CCI = list(CCI.values)
        return list_CCI

    ## 强力指标
    def FORCE(self, n):
        F = pd.Series(self.df['close'].diff(n) * self.df['volue'].diff(n), name='Force_' + str(n))
        list_F = list(F.values)
        return list_F
    # 成交量
    def volbl(self ,n):
        ## 成交量和涨跌的关系
        df1 = self.df.iloc[len(self.df ) -n:len(self.df)]
        df1['close_open'] =df1['close'].pct_change()
        df1['v_lable'] = df1['close_open'].apply(lambda x: 1 if x > 0 else -1)
        df1['volue_lable'] = df1['v_lable'] * df1['volume']
        # df = self.df.dropna()
        red = df1[df1['volue_lable'] > 0]
        blue = df1[df1['volue_lable'] < 0]
        if (red['volue_lable'].sum() - red['volue_lable'].max()) / (len(red) - 1) > 1.1 * (
                ((np.abs(blue['volue_lable'].sum())) - np.abs(blue['volue_lable'].min())) / (len(blue) - 1)) or \
                red['volue_lable'].sum() > 1.2 * (np.abs(blue['volue_lable'].sum())):
            a = 1
        elif ((red['volue_lable'].sum() - red['volue_lable'].max()) / (len(red) - 1)) < 0.9 * (
                ((np.abs(blue['volue_lable'].sum())) - np.abs(blue['volue_lable'].min())) / (len(blue) - 1)) or \
                1.2 * red['volue_lable'].sum() < np.abs(blue['volue_lable'].sum()):
            a = 2

        else:
            a = 3
        return a

     ###成交量的比例
    def volbl_bl(self,n):
        df1 = self.df.iloc[len(self.df) - n:len(self.df)]
        df1['close_open'] = df1['close'].pct_change()
        df1['v_lable'] = df1['close_open'].apply(lambda x: 1 if x > 0 else -1)
        df1['volue_lable'] = df1['v_lable'] * df1['volume']
        # df = self.df.dropna()
        red = df1[df1['volue_lable'] > 0]
        blue = df1[df1['volue_lable'] < 0]
        bisum = red['volue_lable'].sum() / (np.abs(blue['volue_lable'].sum()))
        if bisum >2:
            a = 1
        elif bisum>1 and bisum <=2:
            a = 2

        elif bisum<=1 and bisum >=-1:
            a = 3
        elif bisum <=-1 and bisum >=-2:
            a = 4
        else:
            a = 5
        return a
    def volbl_bl_zhi(self,n):
        df1 = self.df.iloc[len(self.df) - n:len(self.df)]
        df1['close_open'] = df1['close'].pct_change()
        df1['v_lable'] = df1['close_open'].apply(lambda x: 1 if x > 0 else -1)
        df1['volue_lable'] = df1['v_lable'] * df1['volume']
        # df = self.df.dropna()
        red = df1[df1['volue_lable'] > 0]
        blue = df1[df1['volue_lable'] < 0]
        if len(blue)>0:
            bisum = red['volue_lable'].sum() / (np.abs(blue['volue_lable'].sum()))
        else:
            bisum= -99

        return bisum
    def volbl_bl_duanju(self,n,k):
        df1 = self.df.iloc[len(self.df) - n:len(self.df)]
        df2 = self.df.iloc[len(self.df) - k*n:len(self.df) - n]
        sum_volue_df1 = df1['volume'].sum()/n
        sum_volue_df2 = df2['volume'].sum()/((k-1)*n)

        bisum=sum_volue_df1/sum_volue_df2
        return bisum
    def rates_sum(self,ma_30_rate1):
        list_suma1=[]
       # ma_30_rate1 = list(df1['ma_30_rate'])
        for ii in range(9, len(ma_30_rate1)):
            sum_a1 = np.sum(ma_30_rate1[ii - 10:ii])
            #print(sum_a1)
            list_suma1.append(sum_a1)
        return list_suma1
    def panduan_rate(self,ma_30_rate1):
        list_suma1 = self.rates_sum(ma_30_rate1)
        #print('list_suma1list_suma1list_suma1list_suma1',list_suma1)
        if list_suma1[-1]>list_suma1[-5:-4] and list_suma1[-1]>0.01 and list_suma1[-1]< 0.5:
            a =1
        elif list_suma1[-1]<list_suma1[-5:-4] and list_suma1[-1]< -0.01 and list_suma1[-1]> -0.5:
            a = 2
        else:
            a = 3
        return a 

    def volbl_shuanxuan(self ,n,m):
        ## 成交量和涨跌的关系
        df1 = self.df.iloc[len(self.df ) -n:len(self.df)]
        df1['close_open'] =df1['close'].pct_change()
        df1['v_lable'] = df1['close_open'].apply(lambda x: 1 if x > 0 else -1)
        df1['volue_lable'] = df1['v_lable'] * df1['volume']
        # df = self.df.dropna()
        red = df1[df1['volue_lable'] > 0]
        blue = df1[df1['volue_lable'] < 0]
        if (red['volue_lable'].sum() - red['volue_lable'].max()) / (len(red) - 1) > 1.1 * (
                ((np.abs(blue['volue_lable'].sum())) - np.abs(blue['volue_lable'].min())) / (len(blue) - 1)) or \
                red['volue_lable'].sum() > m * (np.abs(blue['volue_lable'].sum())):
            a = 1
        elif ((red['volue_lable'].sum() - red['volue_lable'].max()) / (len(red) - 1)) < 0.9 * (
                ((np.abs(blue['volue_lable'].sum())) - np.abs(blue['volue_lable'].min())) / (len(blue) - 1)) or \
                m * red['volue_lable'].sum() < np.abs(blue['volue_lable'].sum()):
            a = 2

        else:
            a = 3
        return a
    ##突破平台（需要用长周期）
    def pingtantupo(self, n):
        df1 = self.df.iloc[-n:]
        # rates_three = self.ROC(df1,5)[-1]
        if df1['close'][-2:].mean() > 1.005 * df1.iloc[-n:-6]['close'].quantile(q=0.95) and \
                df1['volume'][-2:].mean() > 1.5*df1.iloc[-n:-6]['volume'].mean() and df1['close'][-1:].mean() > df1.iloc[-4:-2]['close'].max() and df1['close'][-1:].mean() >df1['close'][-3:-9].max():
            lable_staus = 1
        elif df1['close'][-2:].mean() < 0.991 * df1.iloc[-n:-6]['close'].quantile(q=0.05) and \
                df1['volume'][-1:].mean() > 1.1*df1.iloc[-n:-6]['volume'].mean() and df1['close'][-1:].mean() < df1.iloc[-4:-2]['close'].mean() :
            lable_staus = 2
        else:
            lable_staus = 3
        return lable_staus

    def angle(self,v1):
        v2 = []
        for ii in v1:
            v2.append(0)
        dx1 = v1[2] - v1[0]
        dy1 = v1[3] - v1[1]
        dx2 = v2[2] - v2[0]
        dy2 = v2[3] - v2[1]
        angle1 = math.atan2(dy1, dx1)
        angle1 = int(angle1 * 180 / math.pi)
        # print(angle1)
        angle2 = math.atan2(dy2, dx2)
        angle2 = int(angle2 * 180 / math.pi)
        # print(angle2)
        if angle1 * angle2 >= 0:
            included_angle = abs(angle1 - angle2)
        else:
            included_angle = abs(angle1) + abs(angle2)
        if included_angle > 180:
            included_angle = 360 - included_angle
        return included_angle

    def angle_panduan(self,V1):
        included_angle = self.angle(V1)
        if included_angle>45 and included_angle<90:
            a = 1
        elif included_angle>90 and included_angle<135:
            a = 2
        else:
            a = 3
        return a
    ## 此函数是判断长期趋势
    def angle_panduan_list(self, V1):
        list_angle = []
        for ii in range(10, len(V1)):
            list_ag = V1[ii - 9:ii]
            aa = self.angle(list_ag)
            # print(aa)
            list_angle.append(aa)
        a = ''

        angle1_dayu = [x  for x in list_angle[-5:] if x <90]
        angle1_xiaoyu = [x  for x in list_angle[-5:] if x >90]

        if len(angle1_dayu) >1:
            angle1_dayu1 = angle1_dayu
        else:
            angle1_dayu1 = [0]

        if len(angle1_xiaoyu) >1:
            angle1_xiaoyu1 = angle1_xiaoyu
        else:
            angle1_xiaoyu1 = [0]
            
        if np.mean(angle1_dayu1) < 90:
            if  np.mean(angle1_dayu1) >50:
                a = 1
            elif np.max(angle1_dayu1) >40 and np.mean(angle1_dayu1) >40:
                a = 4
            else:
                a = 6
        elif np.mean(angle1_xiaoyu1 ) > 90:
            if  np.mean(angle1_xiaoyu1) <125:
                a = 2
            elif np.min(angle1_xiaoyu1 ) <125 and np.mean(angle1_xiaoyu1 ) <130:
                a = 5
            else:
                a = 7
        else:
            a = 3
        return a
    def angle_panduan_list_angle(self, V1):
        list_angle = []
        for ii in range(10, len(V1)):
            list_ag = V1[ii - 8:ii]
            aa = self.angle(list_ag)
            # print(aa)
            list_angle.append(aa)
        return list_angle

    def jidiezhang(self,df1, n):
        return 3
    def pingtantupo_kai(self, n):
        df1 = self.df.iloc[-n:]
        # rates_three = self.ROC(df1,5)[-1]
        if df1['close'][-2:].mean() > 1.002*df1.iloc[-n:-2]['close'].quantile(q=0.97) :
            # and roc[name][-1:].mean() >0.015 :
            lable_staus = 1
        elif df1['close'][-2:].mean() < 0.998 * df1.iloc[-n:-2]['close'].quantile(q=0.003) :
            lable_staus = 2
        else:
            lable_staus = 3
        return lable_staus

    def pingtantupo_xuqu(self, n):
        
        df1 = self.df.iloc[-n:]
        # rates_three = self.ROC(df1,5)[-1]
        if df1['close'][-2:].mean() > df1.iloc[-n:-8]['close'].quantile(q=0.97) :
            # and roc[name][-1:].mean() >0.015 :
            lable_staus = 1
        elif df1['close'][-2:].mean() <  df1.iloc[-n:-8]['close'].quantile(q=0.003) :
            lable_staus = 2
        else:
            lable_staus = 3
        return lable_staus

    def tupojiandi(self,n):
        rates = (self.df.iloc[-6:-2]['close'].mean()-self.df.iloc[-n:-(n-1)]['close'].mean())/self.df.iloc[-n:-(n-1)]['close'].mean()
        if self.df.iloc[-12:-6]['close'].max() > self.df.iloc[-n:-6]['close'].mean()  and 1.02*self.df.iloc[-6:-1]['close'].mean() \
            < self.df.iloc[-12:-6]['close'].max():
            a = 2
        elif self.df.iloc[-12:-6]['close'].min() < self.df.iloc[-n:-6]['close'].mean()  and 1.02*self.df.iloc[-6:-1]['close'].mean() \
                >1.02* self.df.iloc[-12:-6]['close'].min():
            a = 1
        else:
            a = 3
        return a
    ## 通过收益率里判断(短周期)缺点震荡的时候每次都是最高价或者最低价
    def ratepingtan(self, n):
        rate_list = self.ROC(self.df, n,"close")[-15:]

        red_list = [x for x in rate_list if x > 0]
        blue_list = [x for x in rate_list if x < 0]
        if sum(rate_list) > 0.01:
            if len(red_list) > len(blue_list):
                ## 多头强势指标
                mean_rate = 1
            else:
                # red线突然拉升
                mean_rate = 2
        elif sum(rate_list) < -0.01:
            ## 空头强势指标
            if len(red_list) < len(blue_list):
                mean_rate = 3
            else:
                ##blue反转下跌
                mean_rate = 4
        else:
            if len(red_list) / len(blue_list) > 2:
                # 红线多
                mean_rate = 5
            elif 1 < len(red_list) / len(blue_list) <= 2:
                mean_rate = 6
            elif 0.5 < len(red_list) / len(blue_list) <= 1:
                mean_rate = 7
            else:
                mean_rate = 8
        return mean_rate

    ## 在一定周期内，价格低成交量大则上涨，价格高成交量大，未来下跌（定义反转指标）
    import numpy as np
    ## 顺势指标
    def ccise(self, n):
        list_cci = self.CCI(n)
        lable_cci = 0
        if np.mean(list_cci[-3:0]) > 1.4:
            lable_cci = 1
        elif np.mean(list_cci[-3:0]) < -1.45:
            lable_cci = 2
        else:
            lable_cci = 3
        return lable_cci

    ## 此指标是假定通过一定周期的下跌或者上张，成交量急剧放大，且价格有一定的回升或者下跌，则行情反转了
    def fenweishu(self, n):
        df1 = self.df.iloc[-n:]
        quantile_big = df1.iloc[-n:-4]['close'].quantile(q=0.99)
        quantile_min = df1.iloc[-n:-4]['close'].quantile(q=0.01)

        zhengfu_close = (df1['high'][-3:-1].max() - df1['low'][-3:-1].min()) / df1['close'][-2:-1].mean()
        if df1['low'][-3:-1].min() < quantile_min and df1['volume'][-3:-1].mean() > 2* df1['volume'][-n:-4].mean() \
                and df1['high'][-1:].mean() > quantile_min and zhengfu_close > 0.18:
            lable_quantile = 1
        elif df1['high'][-3:-1].max() > quantile_big and df1['volume'][-3:-1].mean() > 2 * df1['volume'][-n:-4].mean() \
                and df1['low'][-1:].mean() < quantile_big and zhengfu_close > 0.02:
            lable_quantile = 2
        else:
            lable_quantile = 3
        return lable_quantile

    ##

    def BBANDS(self,m,n):
        self.df['upper'], self.df['middle'], self.df['lower'] = ta.BBANDS(
            self.df.close.values,
            timeperiod=30,
            nbdevup=m,
            nbdevdn=n,
            matype=0)

        self.df['up_c'] = self.df['upper'] - self.df['close']
        self.df['do_c'] = self.df['lower'] - self.df['close']
        self.df['M_clo'] = self.df['middle'] - self.df['close']

        df2 = self.df
        if df2['up_c'].iloc[-1:].mean() / df2['close'].iloc[-1:].mean() < -0.001 and df2['up_c'].iloc[-2:].mean() / df2['close'].iloc[-2:].mean() > -0.016 and df2.iloc[-1:]['close'].mean() < df2.iloc[-80:-2]['close'].quantile(q=0.98):

            lable_kelch = 2
        elif df2['do_c'].iloc[-1:].mean() / df2['close'].iloc[-1:].mean() > 0.001 and \
                df2['do_c'].iloc[-2:].mean() / df2['close'].iloc[-2:].mean() < 0.016 and df2.iloc[-1:]['close'].mean() > df2.iloc[-80:-2]['close'].quantile(q=0.05)  :

            lable_kelch = 1
        else:
            lable_kelch = 3
        return lable_kelch


    def BBANDS_ccc(self,m,n):
        self.df['upper'], self.df['middle'], self.df['lower'] = ta.BBANDS(
            self.df.close.values,
            timeperiod=30,
            nbdevup=m,
            nbdevdn=n,
            matype=0)

        #self.df['up_c'] = self.df['upper'] - self.df['close']
        #self.df['do_c'] = self.df['lower'] - self.df['close']
        #self.df['M_clo'] = self.df['middle'] - self.df['close']
        self.df['ccc'] = ( self.df['close']- self.df['middle'])/ self.df['middle']
        df2 = self.df
        if df2['ccc'].iloc[-2:].mean() :

            lable_kelch = 2
        elif df2['do_c'].iloc[-1:].mean() / df2['close'].iloc[-1:].mean() > 0.001 and \
                df2['do_c'].iloc[-2:].mean() / df2['close'].iloc[-2:].mean() < 0.016 and df2.iloc[-1:]['close'].mean() > df2.iloc[-80:-2]['close'].quantile(q=0.05)  :

            lable_kelch = 1
        else:
            lable_kelch = 3
        return lable_kelch


    # 肯特纳通道
    def KELCH(self, df1, n):
        """  缺陷在与暴跌的或者暴涨就买了 """
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

        dd = df2['M_lable'].iloc[-9:-1].value_counts()
        dd_dict = dd.to_dict()
        print(dd_dict)
        try:
            ones = dd_dict[1]
            # zero = dd_dict[0]
        except:
            ones = 0
            # zero = 0
        try:
            zero = dd_dict[0]
        except:
            zero = 0
        if df2['up_c'].iloc[-2:].mean() / df2['close'].iloc[-2:].mean() < -0.005  \
            and  df2['up_c'].iloc[-2:].mean() / df2['close'].iloc[-2:].mean() > -0.016 \
            and zero < 7 and df2.iloc[-1:]['close'].mean() < df2.iloc[-30:-2]['close'].quantile(q=0.95):
            lable_kelch = 2
        elif df2['do_c'].iloc[-2:].mean() / df2['close'].iloc[-2:].mean() > 0.005 and \
                df2['do_c'].iloc[-2:].mean() / df2['close'].iloc[-2:].mean() < 0.016  and ones < 7 \
                and df2.iloc[-1:]['close'].mean() > df2.iloc[-30:-2]['close'].quantile(q=0.05):
            lable_kelch = 1
        else:
            lable_kelch = 3
        return lable_kelch
    # 肯特纳通道
    def KELCH_zhengdang(self, df1, n):
        """  缺陷在与暴跌的或者暴涨就买了 """
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

        dd = df2['M_lable'].iloc[-9:-1].value_counts()
        dd_dict = dd.to_dict()
        #print(dd_dict)
        try:
            ones = dd_dict[1]
            # zero = dd_dict[0]
        except:
            ones = 0
            # zero = 0
        try:
            zero = dd_dict[0]
        except:
            zero = 0
        if df2['up_c'].iloc[-1:].mean() / df2['close'].iloc[-1:].mean() < -0.005  \
            and  df2['up_c'].iloc[-1:].mean() / df2['close'].iloc[-1:].mean() > -0.016 \
            and zero < 7 :
            lable_kelch = 2
        elif df2['do_c'].iloc[-1:].mean() / df2['close'].iloc[-1:].mean() > 0.005 and \
                df2['do_c'].iloc[-1:].mean() / df2['close'].iloc[-1:].mean() < 0.016  and ones < 7 :
            lable_kelch = 1
        else:
            lable_kelch = 3
        return lable_kelch


    def KELCH_shangzhang(self, df1, n):
        """  缺陷在与暴跌的或者暴涨就买了 """
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



        if df2['up_c'].iloc[-2:].mean() / df2['close'].iloc[-2:].mean() < -0.015 \
            and df2.iloc[-1:]['close'].mean() < df2.iloc[-30:-2]['close'].quantile(q=0.95)\
                and df2.iloc[-2:]['volume'].mean() < 3*df2.iloc[-30:-2]['volume'].mean() and zero < 7:
            lable_kelch = 2
        elif df2['do_c'].iloc[-2:].mean() / df2['close'].iloc[-2:].mean() > 0.005 \
            and df2.iloc[-1:]['close'].mean() > df2.iloc[-30:-2]['close'].quantile(q=0.08) \
                and df2.iloc[-2:]['volume'].mean() < 3 * df2.iloc[-30:-2]['volume'].mean() and ones < 7  :
            lable_kelch = 1
        else:
            lable_kelch = 3
        return lable_kelch


    def KELCH_xiadie(self, df1, n):
        """  缺陷在与暴跌的或者暴涨就买了 """
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



        if df2['up_c'].iloc[-2:].mean() / df2['close'].iloc[-2:].mean() < -0.006 \
            and df2.iloc[-1:]['close'].mean() < df2.iloc[-30:-2]['close'].quantile(q=0.90) and df2.iloc[-2:]['volume'].mean() < 3*df2.iloc[-30:-2]['volume'].mean() and zero < 7:
            lable_kelch = 2
        elif df2['do_c'].iloc[-2:].mean() / df2['close'].iloc[-2:].mean() > 0.010 \
            and df2.iloc[-1:]['close'].mean() > df2.iloc[-30:-2]['close'].quantile(q=0.05) \
                and df2.iloc[-2:]['volume'].mean() < 3 * df2.iloc[-30:-2]['volume'].mean() and ones < 7  :
            lable_kelch = 1
        else:
            lable_kelch = 3
        return lable_kelch


    def pingjunxian(self):
        ma_5 = ta.WMA(self.df['close'], timeperiod=5)
        ma_15 = ta.WMA(self.df['close'], timeperiod=15)
        ma_30 = ta.WMA(self.df['close'], timeperiod=38)

        self.df['ma_5'] = ma_5
        self.df['ma_15'] = ma_15
        self.df['ma_30'] = ma_30

        self.df['close_ma15'] = self.df['ma_5'] - self.df['ma_15']
        self.df['close_ma30'] = self.df['ma_5'] - self.df['ma_30']
        self.df['close_ma30_bl'] = self.df['close_ma30']/self.df['close']
#        roc3 = self.ROC(self.df, 3, "close_ma30")
#        roc3_5 = self.ROC(self.df, 3, "close_ma15")

        ## t周期价格在均线下面，t+n周期在价格上面，且满足收益率的一定条件
        lists_bl = list(self.df['close_ma30_bl'])

        if np.sum(lists_bl[-30:-10]) < 0 and np.sum(lists_bl[-10:]) > 0 and np.sum(lists_bl[-8:]) > 0.029 :
            roc_lable = 1
        elif np.sum(lists_bl[-30:-10]) > 0 and np.sum(lists_bl[-10:]) < 0 and np.sum(lists_bl[-8:]) < -0.029:
            roc_lable = 2
        else:
            roc_lable = 3



        ##
        if  self.df.iloc[-3:]['close_ma30_bl'].sum() >0.014:
            junxian = 1
        elif  self.df.iloc[-3:]['close_ma30_bl'].sum() <-0.014:
            junxian = 2
        else:
            junxian =3



        return roc_lable,junxian



    ##

    ## 震荡情况下，不跌破38均线的情况下，价格低于一定周期的10%，价格高于一定价位卖出

    # lk越小，买点越低，也就是越严格。hk越大，卖点越宽松，越小卖点越严格
    def dimaigaomai(self,n,lk,hk):
        highs_close = self.df.iloc[-n:-4]['close'].quantile(q=0.95)
        low_close = self.df.iloc[-n:-4]['close'].quantile(q=0.05)
        closes = self.df.iloc[-1:]['close'].mean()
        if closes < lk*low_close:
            dimai = 1
        elif hk*closes > highs_close:
            dimai =2
        else:
            dimai = 3
        return dimai
        ##定义成交量，收益率，时间性的关系,底部成交量大，则反转

    def vu_rate_time(self, close, t, n):
        df2 = self.df.iloc[-n:]
        rates = self.ROC(df2, t, close)
        df1 = self.df.iloc[len(self.df) - n:len(self.df)]
        df1['close_open'] = df1['close'].pct_change()
        df1['v_lable'] = df1['close_open'].apply(lambda x: 1 if x > 0 else -1)
        df1['volue_lable'] = df1['v_lable'] * df1['volume']
        # df = self.df.dropna()
        red = df1[df1['volue_lable'] > 0]
        blue = df1[df1['volue_lable'] < 0]
        red_sum = red['volue_lable'].sum()
        blue_sum = np.abs(blue['volue_lable'].sum())
        # if rates >0.1 and red_sum/blue_sum >3:
        #     pass
        return rates, red_sum, blue_sum


    def hunza(self, list_open, list_high, list_low, list_close, list_volue):
        ma_5 = ta.WMA(np.array(list_close[::-1]), timeperiod=5)
        ma_15 = ta.WMA(np.array(list_close[::-1]), timeperiod=20)
        ma_30 = ta.WMA(np.array(list_close[::-1]), timeperiod=35)

        self.df['ma_5'] = ma_5
        self.df['ma_15'] = ma_15
        self.df['ma_30'] = ma_30
        self.df['ma_5_15'] = self.df['close'] - self.df['ma_15']
        self.df['ma_5_30'] = self.df['close'] - self.df['ma_30']

        self.df['close_ma30_bl'] = (self.df['close'] - self.df['ma_30']) /self.df['ma_30']


        #self.df['close_ma30_bl'] = (self.df['close'] - self.df['ma_30']) / self.df['ma_30']
        #self.df['lable_5_10'] = self.df['ma_5_15'].apply(lambda x: 1 if x > 0 else 0)
        #self.df['lable_5_30'] = self.df['ma_5_30'].apply(lambda x: 1 if x > 0 else 0)

        # self.df['close_ma30_bl_sum'] = self.df['close_ma30_bl'].apply(lambda x: 1 if x > 0.005 else(-1 if x <-0.05 else 0)

        # ADX
        ADX = ta.ADX(np.array(list_high[::-1]), np.array(list_low[::-1]), np.array(list_close[::-1]), timeperiod=10)
        self.df['ADX'] = ADX
        # 波动指标
        ATR = ta.ATR(np.array(list_high[::-1]), np.array(list_low[::-1]), np.array(list_close[::-1]), timeperiod=5)

        STOCHF_fastk, STOCHF_fastd = ta.STOCHF(np.array(list_high[::-1]), np.array(list_low[::-1]),
                                               np.array(list_close[::-1]), fastk_period=5, fastd_period=3,
                                               fastd_matype=0)
        self.df['STOCHF_fastk'] = STOCHF_fastk
        self.df['STOCHF_fastd'] = STOCHF_fastd
        PLUS_DM = ta.PLUS_DM(np.array(list_high[::-1]), np.array(list_low[::-1]), timeperiod=6)

        # 真实波幅
        ATR_3 = ta.ATR(np.array(list_high[::-1]), np.array(list_low[::-1]), np.array(list_close[::-1]), timeperiod=3)
        ATR_20 = ta.ATR(np.array(list_high[::-1]), np.array(list_low[::-1]), np.array(list_close[::-1]), timeperiod=20)

        # 能量潮
        OBV = ta.OBV(np.array(list_close[::-1]), np.array(list_volue[::-1]))
        self.df['OBV'] = OBV
        # 平均线
        mean_a = 4
        #sum_5 = self.df['lable_5_10'].iloc[len(self.df) - 10:len(self.df)].sum()
        #sum_30 = self.df['lable_5_30'].iloc[len(self.df) - 7:len(self.df)].sum()

        #rates_three = self.ROC(self.df, 10,"close")[-1]
        #close_mean_10 = self.df['close'].iloc[len(self.df) - 4:len(self.df)].median()
        #close_mean_20 = self.df['close'].iloc[len(self.df) - 10:len(self.df) - 4].median()
        rate_close_ma30_bl_sum = np.mean(list(self.df['close_ma30_bl'])[-20:])
       # rate_close_ma30_bl_mean = np.mean(list(self.df['close_ma30_bl'])[-10:])
        #two_rate_close_ma30_bl = np.mean(list(self.df['close_ma30_bl'])[-2:])
        if rate_close_ma30_bl_sum > 0.005  :

            mean_a = 1

        elif rate_close_ma30_bl_sum < -0.005  :

            mean_a = 2
        else:
            mean_a = 3
        # 趋势
        quxiang = self.df['ADX'].iloc[3:].mean()
        qushi_b = 0
        quxiang1 = self.df['ADX'].iloc[len(self.df) - 10:len(self.df) - 8].mean()
        quxiang2 = self.df['ADX'].iloc[len(self.df) - 8:len(self.df) - 6].mean()
        quxiang3 = self.df['ADX'].iloc[len(self.df) - 5:len(self.df) - 2].mean()
        quxiang4 = self.df['ADX'].iloc[len(self.df) - 2:len(self.df)].mean()
        if (quxiang4 > quxiang3 > quxiang2 or quxiang4 > quxiang3 > quxiang1) and quxiang4 > 35:
            qushi_b = 1
        else:
            qushi_b = 3

        c = 0
        # K值
        k_vlue = self.df['STOCHF_fastk'].iloc[len(self.df) - 3:len(self.df)].mean()
        d_value = self.df['STOCHF_fastd'].iloc[len(self.df) - 3:len(self.df)].mean()
        if k_vlue > 55 and k_vlue - d_value > 0:
            diff_k = 1
        elif k_vlue < 35 and k_vlue - d_value < 0:
            diff_k = 2
        else:
            diff_k = 0

        # 波动指标
        bodong_d = 0
        if PLUS_DM[-1] > 25:
            bodong_d = 1
        elif PLUS_DM[-1] < 6:
            bodong_d = 2
        else:
            bodong_d = 3

        bofu_e = 0
        if ATR_3[-1] >= 1.2 * ATR_20[-1]:
            bofu_e = 1
        elif ATR_3[-1] < 0.8 * ATR_20[-12:].mean():
            bofu_e = 2
        else:
            bofu_e = 3

        # 能量潮
        obv_20 = self.df['OBV'].iloc[len(self.df) - 20:len(self.df)].mean()
        obv_2 = self.df['OBV'].iloc[len(self.df) - 2:len(self.df)].mean()
        obv_f = 0
        if obv_2 - 1.3 * obv_20 > 0:
            obv_f = 1
        elif obv_2 - 0.7 * obv_20 < 0:
            obv_f = 2
        else:
            obv_f = 3

        ## 相对强弱
        RSI = ta.RSI(np.array(list_close[::-1]), timeperiod=8)
        self.df['RSI'] = RSI
        RSI_20 = self.df['RSI'].iloc[len(self.df) - 2:len(self.df)].mean()
        RSI_g = 0
        if RSI_20 > 55 and RSI_20 < 90:
            RSI_g = 1
        elif RSI_20 < 38:
            RSI_g = 2

        else:
            pass

        ##KAMA
        KAMA_5 = ta.KAMA(np.array(list_close[::-1]), timeperiod=5)
        KAMA_15 = ta.KAMA(np.array(list_close[::-1]), timeperiod=15)
        KAMA_30 = ta.KAMA(np.array(list_close[::-1]), timeperiod=30)
        KAMA_h = 0
        if KAMA_5[-3:].mean() - KAMA_30[-3:].mean() > 0:
            KAMA_h = 1
        elif KAMA_5[-3:].mean() - KAMA_30[-3:].mean() < 0:
            KAMA_h = 2
        else:
            KAMA_h = 3

        xitai = xingtai()

        lista_k_buy_one = []
        lista_k_buy_two = []
        lista_k_buy_three = []

        lista_k_sell_one = []
        lista_k_sell_two = []
        lista_k_sell_three = []

        list_up_down = []
        k_red = []
        k_blue = []
        for ii in range(7):

            reds, blues = xitai.Kred(float(list_high[ii]), float(list_close[ii]), float(list_low[ii]),
                                     float(list_open[ii]))
            k_red.append(reds)
            k_blue.append(blues)
            rate = xitai.bili(float(list_high[ii]), float(list_close[ii]), float(list_low[ii]), float(list_open[ii]))
            if rate == 1:
                lista_k_buy_one.append(0)
            elif rate == 2:
                lista_k_buy_two.append(0)
            elif rate == 3:
                lista_k_buy_three.append(0)
            elif rate == 6:
                lista_k_sell_one.append(0)
            elif rate == 5:
                lista_k_sell_two.append(0)
            elif rate == 4:
                lista_k_sell_three.append(0)
            else:
                pass
            # if reds ==0 and rate ==1:
            #     lista_k_buy_one.append(0)
            # elif reds ==0 and rate ==1:
            #     lista_k_buy_two.append(0)
            # elif reds < 3 and rate == 2:
            #     lista_k_buy_three.append(0)
            # elif blues == 0 and rate == 6:
            #     lista_k_sell_one.append(0)
            # elif blues ==2 and rate == 6:
            #     lista_k_sell_two.append(0)
            # elif blues == 3 and rate >= 5:
            #     lista_k_sell_three.append(0)
            # elif reds==3 or blues ==3:
            #     list_up_down.append(0)
            # else:
            #     pass

        # reds_0,blues_0 = xitai.Kred(float(list_high[0]),float(list_close[0]),float(list_low[0]),float(list_open[0]))
        # reds_1, blues_1 = xitai.Kred(float(list_high[1]), float(list_close[1]), float(list_low[1]), float(list_open[1]))
        # reds_2, blues_2 = xitai.Kred(float(list_high[2]), float(list_close[2]), float(list_low[2]), floist_open[2]))
        # reds_3, blues_3 = xitai.Kred(float(list_high[3]), float(list_close[3]), float(list_low[3]), float(list_open[3]))
        # reds_4, blues_4 = xitai.Kred(float(list_high[4]), float(list_close[4]), float(list_low[4]), float(list_open[4]))
        # reds_5, blues_5 = xitai.Kred(float(list_high[5]), float(list_close[5]), float(list_low[5]), float(list_open[5]))
        # reds_6, blues_6 = xitai.Kred(float(list_high[6]), float(list_close[6]), float(list_low[6]), float(list_open[6]))
        # reds_7, blues_7= xitai.Kred(float(list_high[7]), float(list_close[7]), float(list_low[7]), float(list_open[7]))
        # reds_8, blues_8 = xitai.Kred(float(list_high[8]), float(list_close[8]), float(list_low[8]), float(list_open[8]))

        ### 收盘价和一定周期的价格比较
        lable_staus = 0
        # df2 = self.df.iloc[len(self.df)-40:len(self.df)-2:]
        # roc = self.ROC(df2,30)
        # name = 'ROC_' + str(30)
        if self.df['close'][-2:].mean() > 1.005 * self.df['close'][-33:-2].median():
            # and roc[name][-1:].mean() >0.015 :
            lable_staus = 1
        elif self.df['close'][-2:].mean() < 0.994 * self.df['close'][-30:-2].median():
            lable_staus = 2
        else:
            lable_staus = 3

        vol = self.volbl(20)

        # rate = xitai.bili(float(list_high[0]),float(list_close[0]),float(list_low[0]),float(list_open[0]))
        return vol, lable_staus, mean_a, qushi_b,quxiang, c, bodong_d, bofu_e, obv_f, k_vlue, d_value, diff_k, RSI_g, KAMA_h, lista_k_buy_one, lista_k_buy_two, lista_k_buy_three, \
               lista_k_sell_one, lista_k_sell_two, lista_k_sell_three, list_up_down, k_red, k_blue

    def zhibiao(self):
        self.df['ad'] = ta.AD(self.df['high'], self.df['low'], self.df['close'], self.df['volume'])
        self.df['ADOSC'] = ta.ADOSC(self.df['high'], self.df['low'], self.df['close'], self.df['volume'], fastperiod=3,
                                    slowperiod=10)
        self.df['OBV'] = ta.OBV(self.df['close'], self.df['volume'])
        ##动量指标
        self.df['ADX'] = ta.ADX(self.df['high'], self.df['low'], self.df['close'], timeperiod=14)
        self.df['ADXR'] = ta.ADXR(self.df['high'], self.df['low'], self.df['close'], timeperiod=14)
        self.df['AROONOSC'] = ta.AROONOSC(self.df['high'], self.df['low'], timeperiod=14)
        self.df['BOP'] = ta.BOP(self.df['open'], self.df['high'], self.df['low'], self.df['close'])
        self.df['cci'] = ta.CCI(self.df['high'], self.df['low'], self.df['close'], timeperiod=14)
        self.df['CMO'] = ta.CMO(self.df['close'], timeperiod=14)
        self.df['DX'] = ta.DX(self.df['high'], self.df['low'], self.df['close'], timeperiod=14)
        # MACD =
        dif, dem, histogram = ta.MACD(self.df['close'], fastperiod=12, slowperiod=26, signalperiod=9)
        # MACDEXT =
        self.df['dif'] = dif
        self.df['dem'] = dem
        self.df['histogram'] = histogram
        dif1, dem1, histogram1 = ta.MACDEXT(self.df['close'], fastperiod=12, fastmatype=0, slowperiod=26, slowmatype=0,
                                            signalperiod=9,
                                            signalmatype=0)
        self.df['dif_EXT'] = dif1
        self.df['dem_EXT'] = dem1
        self.df['histogram_EXT'] = histogram1
        self.df['MFI'] = ta.MFI(self.df['high'], self.df['low'], self.df['close'], self.df['volume'], timeperiod=14)

        self.df['MINUS_DI'] = ta.MINUS_DI(self.df['high'], self.df['low'], self.df['close'], timeperiod=14)
        self.df['MINUS_DM'] = ta.MINUS_DM(self.df['high'], self.df['low'], timeperiod=14)
        self.df['MOM'] = ta.MOM(self.df['close'], timeperiod=10)
        self.df['PLUS_DI'] = ta.PLUS_DI(self.df['high'], self.df['low'], self.df['close'], timeperiod=14)
        self.df['PPO'] = ta.PPO(self.df['close'], fastperiod=12, slowperiod=26, matype=0)
        self.df['ROCP'] = ta.ROCP(self.df['close'], timeperiod=10)
        self.df['RSI'] = ta.RSI(self.df['close'], timeperiod=14)
        # 随机指标, 俗称KD
        slowk, slowd = ta.STOCH(self.df['high'], self.df['low'], self.df['close'], fastk_period=5, slowk_period=3,
                                slowk_matype=0, slowd_period=3,
                                slowd_matype=0)
        self.df['slowk'] = slowk
        self.df['slowd'] = slowd
        ##威廉指标
        self.df['WILLR'] = ta.WILLR(self.df['high'], self.df['low'], self.df['close'], timeperiod=14)
        df1 = self.df
        return df1

    def ivszhibiao(self):
        df1 = self.zhibiao()
        BOP = df1['BOP'].values[-2:].mean()
        AROONOSC = df1['AROONOSC'].values[-2:].mean()
        cci = df1['cci'].values[-2:].mean()
        CMO = df1['CMO'].values[-2:].mean()
        MFI = df1['MFI'].values[-2:].mean()
        MOM = df1['MOM'].values[-2:].mean()
        PLUS_DI = df1['PLUS_DI'].values[-2:].mean()
        RSI = df1['RSI'].values[-2:].mean()
        WILLR = df1['WILLR'].values[-2:].mean()
        return BOP, AROONOSC, cci, CMO, MFI, MOM, PLUS_DI, RSI, WILLR
