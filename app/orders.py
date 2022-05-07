

from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *

from app.talibs import Hangqing
from app.authorization import apiKey, apiSecretKey
from app.OkexAPI import Okex
import pandas as pd
from app.dingding import Message
import numpy as np
import logs
logger = logs.logger
msg = Message()
class Order(object):

    def __init__(self, data):
        self.data = data





    ###查询持仓情况
    def chicang(self):
        request_client = RequestClient(api_key=apiKey, secret_key=apiSecretKey)
        result = request_client.get_account_information_v2()
        aa = result.positions
        pd_chanpn = pd.DataFrame()
        symbol_lst = []
        positionAmt_lst = []
        unrealizedProfit_lst = []
        positionSide_lst = []
        for bb in aa:
            #print(bb.unrealizedProfit,bb.symbol,bb.positionAmt)
            if bb.positionAmt != 0:
                symbol_lst.append(bb.symbol)
                positionAmt_lst.append(bb.positionAmt)
                unrealizedProfit_lst.append(bb.unrealizedProfit)
                positionSide_lst.append(bb.positionSide)
        pd_chanpn['symbol'] = symbol_lst
        pd_chanpn['positionAmt'] = positionAmt_lst
        pd_chanpn['unrealizedProfit'] = unrealizedProfit_lst
        pd_chanpn['positionSide'] = positionSide_lst
        #print(pd_chanpn)
        return pd_chanpn
    
    def timepingcang(self):
        import time 
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        a = now[11:13]
        a1 = now[14:16]
        if a =="02" and (a1 == "00" or  a1 == "05" or a1 == "59"):
            b= 1
        elif  a =="05" and (a1 == "00"  or a1 == "05" or a1 == "59"):
            b= 1
        elif a =="17" and (a1 == "00"  or a1 == "05" or a1 == "59"):
            b= 1
        else:
            b = 0
        return b
            

    ## 平仓
    def pingcang(self,side,quantity):
        # params = {
        #     "instId": self.data['instId'],
        #     "mgnMode": "cross",
        #     "ccy": "USDT",
        #
        # }

        if side == "BUY":
            positionSide = "SHORT"
        else:
            positionSide = "LONG"
        request_client = RequestClient(api_key=apiKey, secret_key=apiSecretKey)
        result = request_client.post_order(symbol=self.data['instId'], side=side, ordertype=OrderType.MARKET,
                                           quantity=float(quantity),
                                           positionSide=positionSide)
        if result.status == 'NEW':
            pass
        else:
            pass
        return 0


#    def buy(self,side,quantity):
#        
#        if side=="BUY":
#            positionSide="LONG"
#        else:
#            positionSide = "SHORT"
#        request_client = RequestClient(api_key=apiKey, secret_key=apiSecretKey)
#        result = request_client.post_order(symbol=self.data['instId'], side=side, ordertype=OrderType.MARKET, quantity=float(quantity),
#                                           positionSide=positionSide)
#        if result.status== 'NEW':
#            pass
#        else:
#            pass
#        return 0

    def buy(self,side,quantity):
        try:

            if side=="BUY":
                positionSide="LONG"
            else:
                positionSide = "SHORT"
            request_client = RequestClient(api_key=apiKey, secret_key=apiSecretKey)
            result = request_client.post_order(symbol=self.data['instId'], side=side, ordertype=OrderType.MARKET, quantity=float(quantity),
                                               positionSide=positionSide)
            if result.status== 'NEW':
                pass
            else:
                pass
        except:
            print("buy错误buy错误buy错误buy错误buy错误buy错误buy错误buy错误buy错误")
        return 0

    def jiaoyi(self):


        pd_chanpn = self.chicang()
        print("pd_chanpnpd_chanpnpd_chanpnpd_chanpn",pd_chanpn)

        try:
            list_instId = list(pd_chanpn['symbol'])
        except:
            list_instId = []
        try:

            df_uplRatio = pd_chanpn[pd_chanpn['symbol']==self.data['instId']]
        except:
            df_uplRatio = pd.DataFrame()
        #print("df_uplRatiodf_uplRatiodf_uplRatio",df_uplRatio)
        uplRatio = 0
        posCcy=0
        if len(df_uplRatio) !=0:
            positionAmt = list(df_uplRatio['positionAmt'])[0]
            unrealizedProfit= list(df_uplRatio['unrealizedProfit'])[0]
            positionSide= list(df_uplRatio['positionSide'])

        else:
            positionAmt = 0
            unrealizedProfit= 0
            positionSide = ""

            



        ## 行情的参数
        hang = Hangqing(self.data)
        hang_status,lable,close_sell,money_k = hang.celv()

        limit_num =7
        basemoney = 100

        if "ETHUSDT" ==self.data['instId']:
            money=basemoney*money_k*2
        elif "BTCUSDT" ==self.data['instId']:
            money=basemoney*money_k*2
        elif "BNBUSDT" ==self.data['instId']:
            money=basemoney*money_k*3
        else:
            money=basemoney*money_k*1/2
            
        
        if close_sell >9000:
            sell_num = round(money /close_sell, 3)
        elif close_sell <=4:
            sell_num = int(money/close_sell)
        elif close_sell >4 and close_sell<10 :
            sell_num =  round(money /close_sell, 1)
        elif close_sell >10 and close_sell<100 :
            sell_num =  round(money /close_sell,0)
        else:
            sell_num = round(money /close_sell, 2)
        #if sell_num==0 and close_sell<90:
        #    sell_num=1
       # else:
       #     sell_num = sell_num
        print("sell_numsell_numsell_numsell_num",self.data['instId'] ,close_sell)
        try:
            uplRatio =  unrealizedProfit/(close_sell* np.abs(positionAmt))
        except:
            uplRatio =0

        logger.info(self.data['instId'] + 'lirunlv'+str(uplRatio))


        ### 账户状态
        
        print("positionAmtpositionAmtpositionAmtpositionAmt",self.data['instId'] ,positionAmt)
        print("uplRatiuplRatiouplRatio",self.data['instId'] ,uplRatio)


        yong_list =  ["ETHUSDT","BTCUSDT"]


        timepingcang = self.timepingcang()
        if hang_status==1 or hang_status==2  :
            if self.data['instId'] not in list_instId:
                if lable ==1:
                    print("aaaaaaaaaaaaaaaaaaa",sell_num)
                    if len(pd_chanpn) <limit_num and self.data['instId'] not in yong_list :
                        self.buy("BUY", sell_num)
                        msg.dingding_warn(self.data['instId'] + "多头买入")
                        #hang.mysqlsell(self.data['instId'], "buy", "0")
                        msg.dingding_warn(self.data['instId'] + "多头买入")
                    elif self.data['instId']  in yong_list:
                        self.buy("BUY", sell_num)
                        msg.dingding_warn(self.data['instId'] + "多头买入")
                        #hang.mysqlsell(self.data['instId'], "buy", "0")
                        msg.dingding_warn(self.data['instId'] + "多头买入")
                    else:
                        pass
                elif lable ==2:
                    if len(pd_chanpn) <limit_num and self.data['instId'] not in yong_list:
                        self.buy("SELL", sell_num)
                        msg.dingding_warn(self.data['instId'] + "空头卖出")
                        #hang.mysqlsell(self.data['instId'], "sell", "0")
                        msg.dingding_warn(self.data['instId'] + "空头卖出")
                        logger.info(self.data['instId'] + '空头卖出')
                    elif self.data['instId']  in yong_list:
                        self.buy("SELL", sell_num)
                        msg.dingding_warn(self.data['instId'] + "空头卖出")
                        #hang.mysqlsell(self.data['instId'], "sell", "0")
                        msg.dingding_warn(self.data['instId'] + "空头卖出")
                        logger.info(self.data['instId'] + '空头卖出')
                    else:
                        pass
                else:
                    pass
            else:
                #positionSide = list(df_uplRatio[df_uplRatio['symbol'] == self.data['instId']]['positionSide'])
                ping_lable,bongdong,mean_a,jinxian_lable,shangying ,max_vol,angerjiaodu,chengjiaoliang  = hang.shangpingcang()
                logger.info(self.data['instId']+"{0} {1} {2} {3} {4} {5} {6} {7} {8} ".format(lable,mean_a,bongdong,ping_lable,jinxian_lable,shangying ,max_vol,angerjiaodu,chengjiaoliang ))
                if   mean_a==1 or bongdong==1 or ping_lable==1 or jinxian_lable==1 or lable ==1 or shangying ==1 or max_vol ==1 or angerjiaodu==1 or chengjiaoliang==1 or timepingcang==1:
                    #logger.info(self.data['instId'] ,str(lable),str(mean_a),str(bongdong),str(ping_lable),str(jinxian_lable)  )
                    if  'SHORT' in positionSide:
                        positionAmt_num = np.abs(list(df_uplRatio[(df_uplRatio['symbol']== self.data['instId'])& (df_uplRatio['positionSide']=='SHORT')]['positionAmt'])[0])
                        self.pingcang("BUY", np.abs(positionAmt_num))
                        #hang.mysqlsell(self.data['instId'], "buy", "1")
                        msg.dingding_warn(self.data['instId'] + "uptwo空头平仓")
                        logger.info(self.data['instId'] + 'uptwo空头平仓')
                    if uplRatio > 0.03 and lable == 1:
                        self.buy("BUY", sell_num)
                        #hang.mysqlsell(self.data['instId'], "buy", "0")
                        logger.info(self.data['instId'] + '多头有盈利继续买')
                    elif uplRatio > 0.05 :
                        positionAmt_num = np.abs(list(df_uplRatio[(df_uplRatio['symbol']== self.data['instId'])& (df_uplRatio['positionSide']=='LONG')]['positionAmt'])[0])
                        self.pingcang("SELL", np.abs(positionAmt_num))
                        #hang.mysqlsell(self.data['instId'], "buy", "0")
                        logger.info(self.data['instId'] + 'uptwo多头有盈利平仓')
                        msg.dingding_warn(self.data['instId'] + "uptwo多头有盈利平仓")
#                    elif uplRatio < -0.3 and lable == 1:
#                        self.pingcang("SELL", positionAmt)
#                        hang.mysqlsell(self.data['instId'], "buy", "0")
#                        logger.info(self.data['instId'] + '多头止损') 
                    else:
                        print(self.data['instId'] + "uptwo持有仓位盈利不足")
                        msg.dingding_warn(self.data['instId'] + "uptwo买点出现，现在持有仓位")
                if  mean_a==2 or bongdong==2 or ping_lable==2 or jinxian_lable==2 or lable ==2 or shangying ==2 or max_vol ==2 or angerjiaodu==2 or chengjiaoliang ==2 or timepingcang==1:
                    print(df_uplRatio)
                    #positionAmt_num = np.abs(list(df_uplRatio[(df_uplRatio['symbol']==self.data['instId']) & (df_uplRatio['positionSide'] == 'LONG')]['positionAmt'])[0])
                    if  'LONG' in positionSide:
                        positionAmt_num = np.abs(list(df_uplRatio[(df_uplRatio['symbol']==self.data['instId']) & (df_uplRatio['positionSide'] == 'LONG')]['positionAmt'])[0])
                        self.pingcang("SELL", np.abs(positionAmt_num))
                        msg.dingding_warn(self.data['instId'] + "多头平仓")
                        logger.info(self.data['instId'] + '多头平仓')
                        #hang.mysqlsell(self.data['instId'], "sell", "1")
                    elif uplRatio > 0.02 :
                        positionAmt_num = np.abs(list(df_uplRatio[(df_uplRatio['symbol']==self.data['instId']) & (df_uplRatio['positionSide'] == 'SHORT')]['positionAmt'])[0])
                        self.pingcang("BUY", np.abs(positionAmt_num))
                        #hang.mysqlsell(self.data['instId'], "buy", "0")
                        logger.info(self.data['instId'] + '空头有盈利平仓')
                        msg.dingding_warn(self.data['instId'] + "空头有盈利平仓")
                    else:
                        pass
                else:
                    #positionSide = list(df_uplRatio[df_uplRatio['symbol'] == self.data['instId']]['positionSide'])
                    if uplRatio < -0.02 and 'SHORT' in positionSide:
                        positionAmt_num = np.abs(list(df_uplRatio[(df_uplRatio['symbol'] == self.data['instId']) & (
                                    df_uplRatio['positionSide'] == 'SHORT')]['positionAmt'])[0])
                        self.pingcang("BUY",  np.abs(positionAmt_num))
                        #hang.mysqlsell(self.data['instId'], "buy", "1")
                        msg.dingding_warn(self.data['instId'] + "上涨情况下空头止损平仓")
                        logger.info(self.data['instId'] + '上涨情况下空头止损平仓')
                   # elif uplRatio >0.03 and 'SHORT' in positionSide:
                    
                    if uplRatio < -0.02 and  'LONG' in positionSide:
                        positionAmt_num = np.abs(list(df_uplRatio[(df_uplRatio['symbol'] == self.data['instId']) & (
                                df_uplRatio['positionSide'] == 'LONG')]['positionAmt'])[0])
                        self.pingcang("SELL", np.abs(positionAmt_num) )
                        msg.dingding_warn(self.data['instId'] + "上涨情况下多头止损平仓")
                        logger.info(self.data['instId'] + '上涨情况多头止损平仓')
                    if uplRatio > 0.05 and  'LONG' in positionSide:
                        positionAmt_num = np.abs(list(df_uplRatio[(df_uplRatio['symbol'] == self.data['instId']) & (
                                df_uplRatio['positionSide'] == 'LONG')]['positionAmt'])[0])
                        self.pingcang("SELL", np.abs(positionAmt_num))
                        msg.dingding_warn(self.data['instId'] + "上涨情况下多头盈利平仓")
                        logger.info(self.data['instId'] + '上涨情况多头盈利平仓')
                    if uplRatio > 0.05 and  'SHORT' in positionSide:
                        positionAmt_num = np.abs(list(df_uplRatio[(df_uplRatio['symbol'] == self.data['instId']) & (
                                df_uplRatio['positionSide'] == 'LONG')]['positionAmt'])[0])
                        self.pingcang("BUY", np.abs(positionAmt_num ))
                        msg.dingding_warn(self.data['instId'] + "上涨情况下空头盈利平仓")
                        logger.info(self.data['instId'] + '上涨情况空头盈利平仓')
                    else:
                        pass
        elif hang_status==12 :
            if self.data['instId'] not in list_instId:
                if lable==1 :
                    if len(pd_chanpn) <limit_num :
                        self.buy("BUY", sell_num)
                        
                        #hang.mysqlsell(self.data['instId'], "buy", "0")
                        msg.dingding_warn(self.data['instId'] + "空头买入")
                        logger.info(self.data['instId'] + '空头买入')
                elif lable ==2:
                    if len(pd_chanpn) <limit_num:
                        self.buy("SELL", sell_num)
                        #hang.mysqlsell(self.data['instId'], "sell", "0")
                        msg.dingding_warn(self.data['instId'] + "空头卖出")
                        logger.info(self.data['instId'] + '空头卖出')
            else:
                #positionSide = list(df_uplRatio[df_uplRatio['symbol'] == self.data['instId']]['positionSide'])
                ping_lable, bongdong, mean_a,jinxian_lable,shangying ,max_vol,angerjiaodu,chengjiaoliang  = hang.shangpingcang()
                logger.info(self.data['instId']+"{0} {1} {2} {3} {4} {5} {6} {7} {8}".format(lable,mean_a,bongdong,ping_lable,jinxian_lable,shangying ,max_vol,angerjiaodu,chengjiaoliang ))
                if  mean_a==1 or bongdong==1 or ping_lable==1 or  jinxian_lable==1 or lable ==1 or shangying ==1 or max_vol ==1 or angerjiaodu==1 or chengjiaoliang ==1 or timepingcang==1:
                    #logger.info(self.data['instId'] ,str(lable),str(mean_a), str(bongdong),str(ping_lable),str(jinxian_lable) )
                    #logger.info(self.data['instId']+"{0} {1} {2} {3} {4} {5} {6}".format(lable,mean_a,bongdong,ping_lable,jinxian_lable))
                    if 'SHORT' in positionSide:
                        positionAmt_num = np.abs(list(df_uplRatio[(df_uplRatio['symbol'] == self.data['instId']) & (
                                    df_uplRatio['positionSide'] == 'SHORT')]['positionAmt'])[0])
                        self.pingcang("BUY", positionAmt_num)
                        #hang.mysqlsell(self.data['instId'], "buy", "1")
                        msg.dingding_warn(self.data['instId'] + "空头平仓")
                        logger.info(self.data['instId'] + '空头平仓')
                    elif uplRatio > 0.03 :
                        self.pingcang("SELL", sell_num)
                        #hang.mysqlsell(self.data['instId'], "buy", "0")
                        logger.info(self.data['instId'] + '多头有盈利平仓')

                    else:
                        pass
                if mean_a==2 or lable ==2 or bongdong==2 or ping_lable==2 or  jinxian_lable==2 or lable ==2 or shangying ==2 or max_vol ==2 or angerjiaodu==2 or chengjiaoliang ==2:
                    #logger.info(self.data['instId'] ,str(lable),str(mean_a),str(bongdong),str(ping_lable),str(jinxian_lable) )
                    if 'LONG' in positionSide:
                        positionAmt_num = np.abs(list(df_uplRatio[(df_uplRatio['symbol'] == self.data['instId']) & (
                                df_uplRatio['positionSide'] == 'LONG')]['positionAmt'])[0])
                        self.pingcang("SELL", np.abs(positionAmt_num))
                        msg.dingding_warn(self.data['instId'] + "多头平仓")
                        logger.info(self.data['instId'] + '多头平仓')
                        #hang.mysqlsell(self.data['instId'], "sell", "1")
                    if uplRatio > 0.05 and lable == 2:
                        self.pingcang("BUY", np.abs(positionAmt_num))
                        logger.info(self.data['instId'] + '空头有盈利平仓')
                        msg.dingding_warn(self.data['instId'] + "空头有盈利平仓")
                    elif uplRatio < -0.05:
                        positionAmt_num = np.abs(list(df_uplRatio[(df_uplRatio['symbol'] == self.data['instId']) & (
                                df_uplRatio['positionSide'] == 'SHORT')]['positionAmt'])[0])
                        self.pingcang("BUY", np.abs(positionAmt_num))
                        msg.dingding_warn(self.data['instId'] + "止损出来")
                        logger.info(self.data['instId'] + '止损出来')
                        #hang.mysqlsell(self.data['instId'], "buy", "1")
                    else:
                        msg.dingding_warn(self.data['instId'] + "卖点出现，现在持有仓位")
                else:
                    if uplRatio < -0.03 and 'SHORT' in positionSide:
                        positionAmt_num = np.abs(list(df_uplRatio[(df_uplRatio['symbol'] == self.data['instId']) & (
                                df_uplRatio['positionSide'] == 'SHORT')]['positionAmt'])[0])
                        self.pingcang("BUY", positionAmt_num)
                        #hang.mysqlsell(self.data['instId'], "buy", "1")
                        msg.dingding_warn(self.data['instId'] + "下跌情况下空头止损平仓")
                        logger.info(self.data['instId'] + '下跌情况下空头止损平仓')
                    elif uplRatio < -0.03 and 'LONG' in positionSide:
                        positionAmt_num = np.abs(list(df_uplRatio[(df_uplRatio['symbol'] == self.data['instId']) & (
                                df_uplRatio['positionSide'] == 'LONG')]['positionAmt'])[0])
                        self.pingcang("SELL", np.abs(positionAmt_num))
                        msg.dingding_warn(self.data['instId'] + "下跌情况下多头止损平仓")
                        logger.info(self.data['instId'] + '下跌情况多头止损平仓')
                    elif uplRatio > 0.02 and 'SHORT' in positionSide:
                        positionAmt_num = np.abs(list(df_uplRatio[(df_uplRatio['symbol'] == self.data['instId']) & (
                                df_uplRatio['positionSide'] == 'LONG')]['positionAmt'])[0])
                        self.pingcang("BUY", np.abs(positionAmt_num))
                        msg.dingding_warn(self.data['instId'] + "下跌情况下空头盈利平仓")
                        logger.info(self.data['instId'] + '下跌情况空头盈利仓平仓')
                    elif uplRatio > 0.02 and 'LONG' in positionSide:
                        positionAmt_num = np.abs(list(df_uplRatio[(df_uplRatio['symbol'] == self.data['instId']) & (
                                df_uplRatio['positionSide'] == 'LONG')]['positionAmt'])[0])
                        self.pingcang("SELL", positionAmt_num)
                        msg.dingding_warn(self.data['instId'] + "下跌情况下空头盈利平仓")
                        logger.info(self.data['instId'] + '下跌情况空头盈利平仓')
                    else:
                        pass
        elif hang_status==11  :
            if self.data['instId'] not in list_instId:
                if lable ==1: 
                    if self.data['instId']  in yong_list:
	                    self.buy("BUY", sell_num)
	                    msg.dingding_warn(self.data['instId'] + "多头买入")
	                   #hang.mysqlsell(self.data['instId'], "buy", "0")
	                    msg.dingding_warn(self.data['instId'] + "多头买入")
                    
                elif lable ==2: 
                    if self.data['instId']  in yong_list:
	                    self.buy("SELL", sell_num)
	                    msg.dingding_warn(self.data['instId'] + "空头卖出")
	                   #hang.mysqlsell(self.data['instId'], "sell", "0")
	                    msg.dingding_warn(self.data['instId'] + "空头卖出")
	                    logger.info(self.data['instId'] + '空头卖出')
                
            else:
                #positionSide = list(df_uplRatio[df_uplRatio['symbol'] == self.data['instId']]['positionSide'])
                ping_lable,bongdong,mean_a,roc_lable, junxian,lable_di,shangying ,max_vol = hang.zhengpingcang()
                logger.info(self.data['instId']+"{0} {1} {2} {3} {4} {5} {6}{7} {8}".format(lable,mean_a,bongdong,ping_lable,roc_lable,junxian,lable_di,shangying ,max_vol))
                if ping_lable==1 or bongdong==1 or mean_a==1 or roc_lable==1 or junxian==1 or lable_di==1  or shangying ==1 or max_vol ==1 or lable ==1 or timepingcang==1 :
                    #logger.info(self.data['instId']+"{0} {1} {2} {3} {4} {5} {6}".format(lable,mean_a,bongdong,ping_lable,roc_lable,junxian,lable_di))
                    if 'SHORT' in positionSide:
                        positionAmt_num = np.abs(list(df_uplRatio[(df_uplRatio['symbol'] == self.data['instId']) & (
                                df_uplRatio['positionSide'] == 'SHORT')]['positionAmt'])[0])
                        self.pingcang("BUY", positionAmt_num)
                        #hang.mysqlsell(self.data['instId'], "buy", "1")
                        msg.dingding_warn(self.data['instId'] + "空头平仓")
                        logger.info(self.data['instId'] + '空头平仓')
                    elif uplRatio>0.04:
                        positionAmt_num = np.abs(list(df_uplRatio[(df_uplRatio['symbol'] == self.data['instId']) & (
                                df_uplRatio['positionSide'] == 'LONG')]['positionAmt'])[0])
                        self.pingcang("SELL", positionAmt_num)
                        msg.dingding_warn(self.data['instId'] + "多头盈利平仓")
                        logger.info(self.data['instId'] + '多头盈利平仓')
                    else:
                        pass
                if ping_lable==2 or bongdong==2 or mean_a==2 or roc_lable==2 or junxian==2 or lable_di==2 or shangying ==2 or max_vol ==2 or  lable ==2:
                    #logger.info(self.data['instId'],lable,mean_a,bongdong,ping_lable,roc_lable,junxian,lable_di)
                    if  'LONG' in positionSide:
                        positionAmt_num = np.abs(list(df_uplRatio[(df_uplRatio['symbol'] == self.data['instId']) & (
                                df_uplRatio['positionSide'] == 'LONG')]['positionAmt'])[0])
                        self.pingcang("SELL", np.abs(positionAmt_num))
                        msg.dingding_warn(self.data['instId'] + "多头平仓")
                        logger.info(self.data['instId'] + '多头平仓')
                        #hang.mysqlsell(self.data['instId'], "sell", "1")
                    elif uplRatio>0.04:
                        positionAmt_num = np.abs(list(df_uplRatio[(df_uplRatio['symbol'] == self.data['instId']) & (
                                df_uplRatio['positionSide'] == 'SHORT')]['positionAmt'])[0])
                        self.pingcang("BUY", np.abs(positionAmt_num))
                        msg.dingding_warn(self.data['instId'] + "空头盈利平仓")
                        logger.info(self.data['instId'] + '空头盈利平仓')
                    else:
                        pass
                else:
                    if (uplRatio < -0.04 or uplRatio > 0.02 ) and positionSide == 'SHORT':
                        positionAmt_num = np.abs(list(df_uplRatio[(df_uplRatio['symbol'] == self.data['instId']) & (
                                df_uplRatio['positionSide'] == 'SHORT')]['positionAmt'])[0])
                        self.pingcang("BUY",positionAmt_num)
                        #hang.mysqlsell(self.data['instId'], "buy", "1")
                        msg.dingding_warn(self.data['instId'] + "上涨情况下空头止损平仓")
                        logger.info(self.data['instId'] + '上涨情况下空头止损平仓')
                    elif (uplRatio < -0.4 or uplRatio > 0.02) and positionSide == 'LONG':
                        positionAmt_num = np.abs(list(df_uplRatio[(df_uplRatio['symbol'] == self.data['instId']) & (
                                df_uplRatio['positionSide'] == 'LONG')]['positionAmt'])[0])
                        self.pingcang("SELL", np.abs(positionAmt_num))
                        msg.dingding_warn(self.data['instId'] + "上涨情况下多头止损平仓")
                        logger.info(self.data['instId'] + '上涨情况多头止损平仓')
                    else:
                        pass

        elif hang_status==8 or hang_status==9 :
            if self.data['instId'] not in list_instId:
                if lable == 4:
                    if len(pd_chanpn) <limit_num:
                        self.buy("BUY", sell_num)
                    #hang.mysqlsell(self.data['instId'], "buy", "0")
                        msg.dingding_warn(self.data['instId'] + "多头买入")
                elif lable == 5:
                    if len(pd_chanpn) <limit_num:
                        self.buy("SELL", sell_num)
                    #hang.mysqlsell(self.data['instId'], "sell", "0")
                        msg.dingding_warn(self.data['instId'] + "多头卖出")
                        logger.info(self.data['instId'] + '多头卖出')
                else:
                    pass
            else:
                positionSide = list(df_uplRatio[df_uplRatio['symbol'] == self.data['instId']]['positionSide'])
                ping_lable,bongdong,mean_a,jinxian_lable,shangying ,max_vol,roc_lable,angerjiaodu,chengjiaoliang = hang.qiangshizhengdang()
                logger.info(self.data['instId']+"{0} {1} {2} {3} {4} {5} {6} {7}{8}{9} ".format(lable,mean_a,bongdong,ping_lable,jinxian_lable,shangying ,max_vol,roc_lable,angerjiaodu,chengjiaoliang))
                if ping_lable==1 or bongdong==1 or mean_a==1  or jinxian_lable==1  or lable == 4 or shangying ==1 or max_vol ==1 or roc_lable==1 or angerjiaodu==1 or chengjiaoliang==1 or timepingcang==1:
                    #logger.info(self.data['instId']+"{0} {1} {2} {3} {4} {5} {6}".format(lable,mean_a,bongdong,ping_lable,roc_lable,junxian,lable_di))
                    if  'SHORT' in positionSide:
                        positionAmt_num = np.abs(list(df_uplRatio[(df_uplRatio['symbol'] == self.data['instId']) & (
                                df_uplRatio['positionSide'] == 'SHORT')]['positionAmt'])[0])
                        self.pingcang("BUY", positionAmt_num)
                        #hang.mysqlsell(self.data['instId'], "buy", "1")
                        msg.dingding_warn(self.data['instId'] + "空头平仓")
                        logger.info(self.data['instId'] + '空头平仓')
                    else:
                        pass
                if ping_lable==2 or bongdong==2 or mean_a==2  or jinxian_lable==2  or lable == 5 or shangying ==2 or max_vol ==2 or roc_lable==2 or angerjiaodu==2 or chengjiaoliang==2:
                    #logger.info(self.data['instId'],lable,mean_a,bongdong,ping_lable,roc_lable,junxian,lable_di)
                    if 'LONG' in positionSide:
                        positionAmt_num = np.abs(list(df_uplRatio[(df_uplRatio['symbol'] == self.data['instId']) & (
                                df_uplRatio['positionSide'] == 'LONG')]['positionAmt'])[0])
                        self.pingcang("SELL", positionAmt_num )
                        msg.dingding_warn(self.data['instId'] + "多头平仓")
                        logger.info(self.data['instId'] + '多头平仓')
                        #hang.mysqlsell(self.data['instId'], "sell", "1")
                    else:
                        pass
                else:
                    if uplRatio < -0.04 and  'SHORT' in positionSide:
                        positionAmt_num = np.abs(list(df_uplRatio[(df_uplRatio['symbol'] == self.data['instId']) & (
                                df_uplRatio['positionSide'] == 'SHORT')]['positionAmt'])[0])
                        self.pingcang("BUY", positionAmt_num )
                        #hang.mysqlsell(self.data['instId'], "buy", "1")
                        msg.dingding_warn(self.data['instId'] + "强震荡空头止损平仓")
                        logger.info(self.data['instId'] + '强震荡空头止损平仓')
                    elif uplRatio > 0.03 and  'SHORT' in positionSide:
                        positionAmt_num = np.abs(list(df_uplRatio[(df_uplRatio['symbol'] == self.data['instId']) & (
                                df_uplRatio['positionSide'] == 'SHORT')]['positionAmt'])[0])
                        self.buy("SELL",np.abs(positionAmt_num))
                        #hang.mysqlsell(self.data['instId'], "buy", "1")
                        msg.dingding_warn(self.data['instId'] + "强震荡空头盈利继续买入")
                        logger.info(self.data['instId'] + '上涨情况下空头止损平仓')
                    elif uplRatio < -0.4 and 'LONG' in positionSide:
                        positionAmt_num = np.abs(list(df_uplRatio[(df_uplRatio['symbol'] == self.data['instId']) & (
                                df_uplRatio['positionSide'] == 'LONG')]['positionAmt'])[0])
                        self.pingcang("SELL", np.abs(positionAmt_num))
                        msg.dingding_warn(self.data['instId'] + "上涨情况下多头止损平仓")
                        logger.info(self.data['instId'] + '上涨情况多头止损平仓')
                    elif uplRatio >0.03 and 'LONG' in positionSide:
                        positionAmt_num = np.abs(list(df_uplRatio[(df_uplRatio['symbol'] == self.data['instId']) & (
                                df_uplRatio['positionSide'] == 'LONG')]['positionAmt'])[0])
                        self.buy("BUY", positionAmt_num)
                        msg.dingding_warn(self.data['instId'] + "强震荡多头继续买入")
                        logger.info(self.data['instId'] + '强震荡多头继续买入')
                    else:
                        pass

        else:
            pass
        return "aa"








