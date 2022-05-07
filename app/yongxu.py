
from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *

import pandas as pd
from app.authorization import apiKey, apiSecretKey
import talib as ta
from app.talibs import Hangqing
from app.orders import Order
import numpy as np
import time
from app.hanshupd import hanshu
import math
class Shuchu(object):


    def shuxuan(self ,df):

        tupo = hanshu(df).pingtantupo_xuqu(50)
        tupo1 = hanshu(df).pingtantupo_xuqu(60)
        # ccise = hanshu(df).ccise(30)

        volbl_shuanxuan = hanshu(df).volbl_shuanxuan(20 ,2)
        roc3_one = np.sum(hanshu(df).ROC(df, 3, "close")[-3])

        volbl_bl = hanshu(df).volbl_bl(15)

        #rates_sum = hanshu(df).rates_sum()
        ma_5 = ta.WMA(df['close'], timeperiod=3)
        ma_15 = ta.EMA(df['close'], timeperiod=15)
        ma_30 = ta.WMA(df['close'], timeperiod=45)

        df['ma_5'] = ma_5
        df['ma_15'] = ma_15
        df['ma_30'] = ma_30

        df['close_ma15'] = df['ma_5'] - df['ma_15']
        df['close_ma30'] = df['close'] - df['ma_30']

        df['close_30'] = df['close_ma30'].apply(lambda x: 1 if x > 0 else 0)
        sum_5 = df['close_30'].iloc[len(df) - 20:len(df)].sum()

        df['close_ma30_bl'] = (df['close'] - df['ma_30']) /df['close']
        rates_list = list(df['close_ma30_bl'])

        list_up = [0]
        list_down = [0]
        for ii in list(df['close_ma30_bl'])[-2:]:
            if ii >0.008 :
                list_up.append(ii)
            elif ii < -0.008:
                list_down.append(ii)
            else:
                pass
        bl_up = len(list_up)/6
        bl_down = len(list_down)/6
        sum_up = np.sum(list_up)
        sum_down = np.sum(list_down)
        bl_rate_up = sum_up/len(list_up)
        bl_rate_down = sum_up/len(list_down)
        if len(df) >800:
            #print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',rates_list )
            #print('ddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd',rates_list)
            rates_sum_5 = hanshu(df).rates_sum(rates_list )
    
            
            panduan_rate = hanshu(df).panduan_rate(list(ma_15))
            #panduan_rate_list = hanshu(df).angle_panduan_list_angle(list(ma_15)[-50:])

            
            df['ADX'] = ta.ADX(df['high'], df['low'], df['close'], timeperiod=10)
    
            df['list_ROC'] = hanshu(df).ROC(df, 3 ,"ADX")
            df['list_ROC1_c'] = hanshu(df).ROC(df, 2 ,"list_ROC")
            roc_5 = hanshu(df).ROC(df ,3 ,"close_ma30")
            rates = (df.iloc[-2:]['close'].mean( ) -df.iloc[-30:-29]['close'].mean() ) /df.iloc[-30:-29]['close'].mean()
    
            tupojiandi = hanshu(df).tupojiandi(90)


            ## 夹角的角度
            angle_panduan = hanshu(df).angle_panduan_list(list(ma_15)[-40:])
            angle = hanshu(df).angle(list(ma_15)[-10:])
            volbl_bl_duanju = hanshu(df).volbl_bl_duanju(2,6)
            if   volbl_bl_duanju >4 :
                a = 1
            if rates_list[-1] >0.01 or rates_list[-1] < -0.01:
                a = 1
            if  bl_rate_up > 0.01 or  bl_rate_down< -0.01:
                a = 1
            if   roc3_one>0.001 or roc3_one< -0.001 :
    
                a =2
            #if tupo1 == 1 and volbl_bl == 1 :
            #    a = 1
            #if tupo1 == 2 and volbl_bl == 5 :
            #    a = 1
            #elif np.mean(panduan_rate_list[-10:]) >65 and np.mean(panduan_rate_list[-10:]) <115:
            #    a = 2
#            elif rates> 0.02 or rates <-0.02:
#                a = 1
            elif angle<90 and angle>75:
                a = 2
            elif angle>90 and angle<115:
                a = 2
            elif angle_panduan==1 or angle_panduan==2 :
                a = 2
            elif tupo == 1 and df.iloc[-5:-1, :]['list_ROC1_c'].sum() > 30 and sum_5 > 10:
                a = 2
            elif tupo == 2 and df.iloc[-5:-1, :]['list_ROC1_c'].sum() > 30 and sum_5 < 3:
                a = 2
            elif tupojiandi == 1:
                a = 2
            elif tupojiandi == 1:
                a = 2
            elif df['close_ma30_bl'].iloc[-10:].mean() > 0.004 and roc3_one > 0.002:
                a = 2
    
            elif df['close_ma30_bl'].iloc[-10:].mean() < -0.004 and roc3_one < -0.002:
                a = 2
            elif np.mean(roc_5[-2:]) > np.mean(roc_5[-5:-2]) > np.mean(roc_5[-9:-5]) and np.mean(roc_5[-1:]) > 0.005 and \
                    df.iloc[-2:-1, :]['ADX'].mean() > 40:
                a = 2
            elif np.mean(roc_5[-2:]) < np.mean(roc_5[-5:-2]) < np.mean(roc_5[-9:-5]) and np.mean(roc_5[-1:]) < -0.005 and \
                    df.iloc[-2:-1, :]['ADX'].mean() > 40:
                a = 2
            elif volbl_bl == 1 or volbl_bl == 5:
                a = 3
            elif volbl_shuanxuan == 1 or volbl_shuanxuan == 2:
                a = 2
            elif (df['close_ma30_bl'].iloc[-10:].mean() > 0.002 or df['close_ma30_bl'].iloc[-10:].mean() < -0.002) and volbl_shuanxuan == 1:
                a = 2
            # elif df['ADX'].iloc[-3:].mean()>40:
            #    a = 1
            else:
                a = 2
        else:
            a = 2
        print("namesssssssssssssssssssssssssssssssss",a)
        return a

    def yongxuheyue(self):
        request_client = RequestClient(api_key=apiKey, secret_key=apiSecretKey)
        result = request_client.get_ticker_price_change_statistics()
        # PrintMix.print_data(result)
        df1 = pd.DataFrame()
        list_symbol = []
        list_priceChangePercent = []
        list_volume = []
        list_lastPrice = []
        for tt in result:
            if tt.symbol[-4:] == "USDT":
                symbol = tt.symbol
                list_symbol.append(symbol)
                priceChangePercent = tt.priceChangePercent
                list_priceChangePercent.append(priceChangePercent)
                volume = tt.volume
                list_volume.append(volume)
                lastPrice = tt.lastPrice
                list_lastPrice.append(lastPrice)

        df1['symbol'] = list_symbol
        df1['priceChangePercent'] = list_priceChangePercent
        df1['volume'] = list_volume
        df1['lastPrice'] = list_lastPrice
        df2 = df1.sort_values(by="volume")
        # df3 = df2[(df2['volume'] > 500000)&((df2['priceChangePercent'] >2)|(df2['priceChangePercent'] <-2))]
        df3 = df2[(df2['volume'] > 5000000)]
        symbol_list = list(df3['symbol'])[0:100]
        #return symbol_list
        shu_list = []
        one_list = []
        two_list = []
        three_list = []
        #datas = {}
        for names in symbol_list:
            data ={"instId":names}
            time.sleep(2)
            df = Hangqing(data).pingju("15m")
            a = self.shuxuan(df)
            print("aaaaaaaaaaaaaaaaaaaaaaaa",a)
            if a ==1:
                one_list.append(names)
            elif a ==2:
                two_list.append(names)
            elif a ==3:
                three_list.append(names)
            else:
                shu_list.append(names)
        datas = {}
        chicang_lis = list(Order(datas).chicang()['symbol'])
        #if len(list(set(one_list+chicang_lis)))>15:

        all_list = list(set(one_list+chicang_lis))
        #elif len(list(set(one_list+two_list+chicang_lis)))>15:
        #    all_list = list(set(one_list+two_list+chicang_lis))
        #else:
        #    all_list = list(set(one_list+three_list +two_list+chicang_lis))
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",all_list)
        return all_list
