
# 明确做周期
#
## 首先判断趋势，判断趋势的定义，需要明确，初步假设是30分钟的线作为趋势
## 在大的趋势里面是宽开仓严止损还是严开仓宽止损了？（严开仓宽止损感官上好点），
## 趋势转震荡，盈利出来，
## 点，线，空间的关系是由点构成线，线构成空间
## 趋势比价格重要，最重要的是确定趋势
### 上涨的周期时候考虑买点，下跌的周期考虑卖点，震荡的时候考虑买卖点
## 下跌的时候没有量说明散户没有人接盘，弱势反弹没有量没有持久性
import talib as ta
import numpy as np
import logs
logger = logs.logger
# from app.talibs import Hangqing
from app.hanshupd import hanshu

from app.dingding import Message

msg = Message()

class Updown(object):
    def __init__(self ,df):
        self.df =df

    def junxianpanduan(self):
        ma_5 = ta.WMA(self.df['close'], timeperiod=3)
        ma_15 = ta.WMA(self.df['close'], timeperiod=25)
        ma_30 = ta.WMA(self.df['close'], timeperiod=45)

        self.df['ma_5'] = ma_5
        self.df['ma_15'] = ma_15
        self.df['ma_30'] = ma_30

        self.df['close_ma15'] = self.df['ma_5' ] -self.df['ma_15']
        self.df['close_ma30'] = self.df['close'] - self.df['ma_30']

        self.df['close_30'] = self.df['close_ma30'].apply(lambda x: 1 if x > 0 else 0)
        self.df['close_ma30_bl'] = (self.df['close'] - self.df['ma_30']) /self.df['ma_30']
        rates = list(self.df['close_ma30_bl'])

        close_list = list(self.df['close'])

        # rates = (close_list[-1]-close_list[-15])/close_list[-15]

        # sum_5 = self.df['lable_5_10'].iloc[len(self.df) - 5:len(self.df)].sum()
        # #sum_30 = self.df['lable_5_30'].iloc[len(self.df) - 15:len(self.df)].sum()
        #
        # close_15 = self.df['close_15'].iloc[len(self.df) - 15:len(self.df)].sum()
        close_30 = self.df['close_30'].iloc[len(self.df) - 13:len(self.df)].sum()
        hshu = hanshu(self.df)

        df1 = self.df.iloc[-60:]
        roc3 = hshu.ROC(df1, 10, "close_ma30")

        ## 长周期使用
        #        if  close_30 >15 and np.sum(roc3[-15:])>0.01 :
        #            close_mean =1
        #        elif close_30 <5 and np.sum(roc3[-15:])< -0.01:
        #            close_mean = 2
        #        else:
        #            close_mean = 3
        ## 短周期的排列
        roc3_5 = hshu.ROC(df1, 3, "close_ma15")
        sum_5 = np.sum(roc3_5[-2:])
        if sum_5 > 0.012:

            mean_a = 1

        elif sum_5 < -0.012:

            mean_a = 2
        else:
            mean_a = 3
        return close_30, mean_a, roc3, rates



    def uptwo(self):
        rates_10 = list(ta.WMA(self.df['close'], timeperiod=5))
        
        rates_10_rate = list(ta.WMA(self.df['close'], timeperiod=3))
        self.df['timepri']=rates_10_rate 
        self.df['close_timepri'] = (self.df['close']-self.df['timepri'])/self.df['timepri']
        rates_10_list = list(self.df['close_timepri'])

        angle = hanshu(self.df).angle(rates_10[-20:])
        rates_5_1 = list(ta.WMA(self.df['close'], timeperiod=60))

        angle_lable = hanshu(self.df).angle_panduan_list(rates_10[-30:])
        #angle = hanshu(self.df).angle(rates_5_1[-20:])

       
        hshu = hanshu(self.df)
        logger = logs.logger
        tupo = hanshu(self.df).pingtantupo_kai(100)
        list_open = list(self.df['open'])
        list_high = list(self.df['high'])
        list_low = list(self.df['low'])
        list_close = list(self.df['close'])
        list_volume = list(self.df['volume'])
        vol, lable_staus, mean_a, qushi_b, quxiang, c, bodong_d, bofu_e, obv_f, k_vlue, d_value, diff_k, RSI_g, KAMA_h, lista_k_buy_one, lista_k_buy_two, lista_k_buy_three, \
        lista_k_sell_one, lista_k_sell_two, lista_k_sell_three, list_up_down, k_red, k_blue = hshu.hunza(list_open,
                                                                                                         list_high,
                                                                                                         list_low,
                                                                                                         list_close,
                                                                                                         list_volume)

        # BOP, AROONOSC, cci, CMO, MFI, MOM, PLUS_DI, RSI, WILLR = hshu.ivszhibiao()

        mean_rate = hshu.ratepingtan(2)

        lable_cci = hshu.ccise(3)
        lable_kelch = hshu.BBANDS(3.8, 3.8)
        lable_quantile = hshu.fenweishu(30)

        roc3_one = hshu.ROC(self.df, 3, "close")
        lable_pingjun, junxian = hshu.pingjunxian()
        daimaigaomai = hshu.dimaigaomai(50, 1, 0.7)

        volbl_bl_duanju = hanshu(self.df).volbl_bl_duanju(10,3)


        self.df['timepri']=ta.WMA(self.df['close'], timeperiod=3)
        self.df['close_timepri'] = (self.df['close']-self.df['timepri'])/self.df['timepri']
        rates_45 = list(self.df['close_timepri'])
        panduan_rate = hanshu(self.df).panduan_rate(rates_45)
        list_suma_15 = hanshu(self.df).rates_sum(rates_45)


        
        dianwei = 0
        if vol == 1:
            
            dianwei = 1
            money_k = 2
            logger.info('uptwo多头成交量占优')
#        elif  vol == 1 and panduan_rate == 1 and k_vlue < 85 and (angle_lable== 1 ) and angle >50 and rates_10_list[-1]>-0.001:
#            msg.dingding_warn("uptwo多头成交量占优")
#            dianwei = 3
#            money_k = 2
#            logger.info('uptwo多头成交量占优')
#        elif (angle_lable ==1 or angle_lable ==4 ) and angle >45 and angle <90 and rates_10_list[-1]>-0.001:
#            msg.dingding_warn("uptwoangle均线买入")
#            dianwei = 3
#            money_k = 2
#            logger.info('uptwoangle均线买入')
#        elif volbl_bl_duanju>4 and angle >50 and angle <90 and rates_10_list[-1]>-0.001:
#            dianwei = 3
#            money_k = 2
#            logger.info('uptwovolbl_bl_duanju买入')
#            msg.dingding_warn("uptwovolbl_bl_duanju买入")
#        elif angle_lable == 2 :
#            dianwei = 3
#            money_k = 1
#            logger.info('uptwoangle_lable卖出')
#            msg.dingding_warn("uptwoangle_lable卖出")
        elif volbl_bl_duanju>2 and angle >90 and angle <135 :
            dianwei = 2
            money_k =1
            logger.info('uptwovolbl_bl_duanju卖入')
            msg.dingding_warn("uptwouptwovolvolbl_bl_duanju卖入")
        elif tupo == 1:
            msg.dingding_warn("uptwo多头突破向上")
            dianwei = 1
            money_k = 1
            logger.info('uptwo多头突破向上')
#        elif tupo == 2:
#            msg.dingding_warn("uptwo多头突破下跌")
#            dianwei = 2
#            money_k = 1
#            logger.info('uptwo多头突破向下')
#        elif k_vlue > 96 and tupo != 1:
#            dianwei = 2
#            money_k = 1
#            msg.dingding_warn("uptwo多头K值指标卖出")
#            logger.info('uptwo多头K值指标卖出')
        elif lable_cci == 1:
            dianwei = 1
            money_k = 2
            msg.dingding_warn("uptwo顺势指标买入")
            logger.info('uptwo顺势指标买入')



        else:
            dianwei = 0
            money_k = 0
        return dianwei, money_k


    def downone(self):
        # rates_5 = list(ta.WMA(self.df['close'], timeperiod=5))
        # angle = hanshu(self.df).angle(rates_5[-8:])
        # angle_panduan = hanshu(self.df).angle_panduan(rates_5[-6:])

        rates_10_rate = list(ta.WMA(self.df['close'], timeperiod=30))
        self.df['timepri']=rates_10_rate 
        self.df['close_timepri'] = (self.df['close']-self.df['timepri'])/self.df['timepri']
        rates_30_list = list(self.df['close_timepri'])

        rates_10 = list(ta.WMA(self.df['close'], timeperiod=3))

        angle = hanshu(self.df).angle(rates_10[-20:])
        
        rates_5_1 = list(ta.EMA(self.df['close'], timeperiod=3))

        angle_lable = hanshu(self.df).angle_panduan_list(rates_5_1[-20:])
        #angle = hanshu(self.df).angle(rates_5_1[-20:])



        #panduan_rate = hanshu(self.df).panduan_rate(rates_15)
        tupo = hanshu(self.df).pingtantupo_kai(120)
        #rates_45 = list(ta.WMA(self.df['close'], timeperiod=30))
        self.df['timepri']=ta.WMA(self.df['close'], timeperiod=19)
        self.df['close_timepri'] = (self.df['close']-self.df['timepri'])/self.df['timepri']
        rates_45 = list(self.df['close_timepri'])
        list_suma_15 = hanshu(self.df).rates_sum(rates_45)
        panduan_rate = hanshu(self.df).panduan_rate(rates_45)
        
        volbl_bl = hanshu(self.df).volbl_bl(30)

        volbl_bl_duanju = hanshu(self.df).volbl_bl_duanju(10,4)
        if  angle >90 and angle <145:
            dianwei = 2
            money_k = 1
            msg.dingding_warn("downone空头成交量占优")
#        elif list_suma_15[-1] < -0.06 and (angle > 90 and angle < 110) and rates_30_list[-1]<0:
#            dianwei = 2
#            money_k = 1
#            msg.dingding_warn("downone空头成交量占优")
#            logger.info('downone空头成交量占优')
#        elif (angle_lable ==2 or angle_lable ==5 ) and angle >90 and angle <125 and rates_30_list[-1]<0:
#            dianwei = 2
#            money_k = 2
#            msg.dingding_warn("downone空头angle")
#            logger.info('downone空头angle')
        elif angle_lable ==1 :
            dianwei = 1
            money_k = 1
            logger.info('downone空头angle_lable买入')
            msg.dingding_warn("downone空头angle_lable买入")


        
#        elif list_suma_15[-1] > np.mean(list_suma_15[-5:-3]) and np.mean(list_suma_15[-5:-3]) > np.mean(
#                list_suma_15[-7:-5]) and volbl_bl == 1 and angle == 1:
#            dianwei = 1
#            money_k = 1
#            msg.dingding_warn("downone多头头成交量占优")
#            logger.info('downone多头头成交量占优')
#        elif volbl_bl == 1 and self.df['volume'].iloc[-6:0].mean() > 3 * self.df['volume'].iloc[-40:-10].mean():
#            dianwei = 1
#            money_k = 0
        elif tupo == 1:
            msg.dingding_warn("downone多头突破向上")
            dianwei = 1
            money_k = 1
            logger.info('downone多头突破向上')
        
        elif tupo == 2:
            msg.dingding_warn("downone多头突破下跌")
            dianwei = 2
            money_k = 1
            logger.info('downone多头突破向下')
#        elif volbl_bl_duanju>4 and angle >40 and angle <90:
#            dianwei = 1
#            money_k = 2
#            logger.info('volbl_bl_duanju买入')
#        elif volbl_bl_duanju>4 and angle >90 and angle <140:
#            dianwei = 2
#            money_k = 2
#            logger.info('volbl_bl_duanju买入')
        else:
            dianwei = 0
            money_k = 0
        return dianwei, money_k




    # 长期震荡，短期震荡
    def zhendang(self):

        rates_10 = list(ta.WMA(self.df['close'], timeperiod=3))

        angle = hanshu(self.df).angle(rates_10[-20:])
        rates_5_1 = list(ta.EMA(self.df['close'], timeperiod=3))

        angle_lable = hanshu(self.df).angle_panduan_list(rates_5_1[-20:])
        #angle = hanshu(self.df).angle(rates_5_1[-20:])

        hshu = hanshu(self.df)
        logger = logs.logger

        list_open = list(self.df['open'])
        list_high = list(self.df['high'])
        list_low = list(self.df['low'])
        list_close = list(self.df['close'])
        list_volume = list(self.df['volume'])
        vol, lable_staus, mean_a, qushi_b, quxiang, c, bodong_d, bofu_e, obv_f, k_vlue, d_value, diff_k, RSI_g, KAMA_h, lista_k_buy_one, lista_k_buy_two, lista_k_buy_three, \
        lista_k_sell_one, lista_k_sell_two, lista_k_sell_three, list_up_down, k_red, k_blue = hshu.hunza(list_open,
                                                                                                         list_high,
                                                                                                         list_low,
                                                                                                         list_close,
                                                                                                         list_volume)

        lable_kelch = hshu.BBANDS(2.9, 2.9)
        tupo = hshu.pingtantupo(80)
        # max_close = hshu.max_close(100)
        # mean_rate = hshu.ratepingtan(2)
        lable_cci = hshu.ccise(3)
        roc_rate = np.mean(hshu.ROC(self.df, 3, "close")[-2:])

        roc_rate_sum = np.sum(hshu.ROC(self.df, 3, "close")[-5:])
        volbl_bl_duanju = hanshu(self.df).volbl_bl_duanju(10, 4)




        dianwei = 0
        if k_vlue < 4 and tupo != 2:
            dianwei = 1
            money_k = 2
            msg.dingding_warn("K值指标买入")
            logger.info('震荡K值指标买入')
#        elif (angle_lable ==1 or angle_lable ==4) and angle >90 and angle <140:
#            dianwei = 3
#            money_k = 1
#            msg.dingding_warn("震荡夹角向上买入")
#            logger.info('震荡夹角向上买入')
        elif volbl_bl_duanju >3 and angle >50 and angle <90:
            dianwei = 1
            money_k = 1
            logger.info('volbl_bl_duanju买入')
            msg.dingding_warn("volbl_bl_duanju买入")
#        elif volbl_bl_duanju >3 and angle >90 and angle <120:
#            dianwei = 5
#            money_k = 2
#            msg.dingding_warn("volbl_bl_duanju卖出")
#            logger.info('volbl_bl_duanju卖出')
#        elif (angle_lable ==1 or angle_lable ==4) and angle >45 and angle <90:
#            dianwei = 4
#            money_k = 1
#            msg.dingding_warn("volbl_bl_duanju震荡夹角向上买入")
#            logger.info('volbl_bl_duanju震荡夹角向上买入')
#        elif (angle_lable ==2 or angle_lable ==5) and  angle >90 and angle <120::
#            dianwei = 5
#            money_k = 1
#            msg.dingding_warn("volbl_bl_duanju震荡夹角向下卖出")
#            logger.info('volbl_bl_duanju震荡夹角向下卖出')
        elif (angle_lable ==2 or angle_lable ==5) and angle >90 and angle <120:
            dianwei = 2
            money_k = 1
            msg.dingding_warn("angle震荡夹角向下卖出")
            logger.info('angle震荡夹角向下卖出')
        elif (angle_lable ==1 or angle_lable ==4) and angle >50 and angle <90:
            dianwei = 1
            money_k = 1
            msg.dingding_warn("angle震荡夹角向上买入")
#            logger.info('angle震荡夹角向上买入')
#        elif tupo == 1:
#            msg.dingding_warn("震荡多头突破向上")
#            dianwei = 1
#            money_k = 2
#            logger.info('震荡多头突破向上')
#        elif tupo == 2:
#            msg.dingding_warn("震荡多头突破下跌")
#            dianwei = 2
#            money_k = 1
#            logger.info('震荡多头突破向下')
        #        elif mean_a == 1 and vol==1  and roc_rate_sum<0.1 and k_vlue<75:
        #            dianwei = 4
        #            msg.dingding_warn("短期多头")
        #            logger.info('短期多头')
        #        elif mean_a == 2 and vol==2 and k_vlue>35  and roc_rate_sum>-0.1:
        #            dianwei = 5
        #            msg.dingding_warn("短期空头")
        #            logger.info('短期空头')

        elif lable_kelch == 1 and tupo != 2 :
            dianwei = 4
            money_k = 2
            msg.dingding_warn("肯特纳通道买入")
            logger.info('肯特纳通道买入')
        elif lable_kelch == 2 and tupo != 1 :
            dianwei = 5
            money_k = 2
            msg.dingding_warn("肯特纳通道卖出")
            logger.info('震荡肯特纳通道卖出')


        else:
            dianwei = 3
            money_k = 1
        # elif d_value > 92 and tupo !=1:
        #     dianwei = 2
        #     msg.dingding_warn("K指标卖出")
        # elif mean_rate==2 or mean_rate==1 :
        #     dianwei =1
        #     msg.dingding_warn("震荡K线反转上升")
        # elif mean_rate==4 or mean_rate==3:
        #     dianwei =2
        #     msg.dingding_warn("震荡K线反转下跌")
        return dianwei, money_k
