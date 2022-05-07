def diffs(opens,close):
    if opens-close>0:
        a = 1
    else:
        a = 2
    return a
import backtrader as bt
import numpy as np
import datetime
import matplotlib
#from matplotlib.font_manager import *
import matplotlib.pyplot as plt
class TestStrategy(bt.Strategy):
    """
    继承并构建自己的bt策略
    """

    def log(self, txt, dt=None, doprint=False):
        ''' 日志函数，用于统一输出日志格式 '''
        if doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):

        # 初始化相关数据
        self.dataclose = self.datas[0].close
        self.dataopen = self.datas[0].open
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.hidd = diffs(self.dataclose,self.dataopen)

        # 五日移动平均线
#         self.sma5 = bt.indicators.SimpleMovingAverage(
#             self.datas[0], period=5)
#         # 十日移动平均线
#         self.sma10 = bt.indicators.SimpleMovingAverage(
#             self.datas[0], period=10)
    def notify_order(self, order):
            """
            订单状态处理

            Arguments:
                order {object} -- 订单状态
            """
            if order.status in [order.Submitted, order.Accepted]:
                # 如订单已被处理，则不用做任何事情
                return

            # 检查订单是否完成
            if order.status in [order.Completed]:
                if order.isbuy():
                    self.buyprice = order.executed.price
                    self.buycomm = order.executed.comm
                self.bar_executed = len(self)

            # 订单因为缺少资金之类的原因被拒绝执行
            elif order.status in [order.Canceled, order.Margin, order.Rejected]:
                self.log('Order Canceled/Margin/Rejected')

            # 订单状态处理完成，设为空
            self.order = None
    def notify_trade(self, trade):
            """
            交易成果

            Arguments:
                trade {object} -- 交易状态
            """
            if not trade.isclosed:
                return

            # 显示交易的毛利率和净利润
            self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                     (trade.pnl, trade.pnlcomm), doprint=True)

    def next(self):
        ''' 下一次执行 '''

        # 记录收盘价
        self.log('Close, %.2f' % self.dataclose[0])

        # 是否正在下单，如果是的话不能提交第二次订单
        if self.order:
            return

        # 是否已经买入
        if not self.position:
            # 还没买，如果 MA5 > MA10 说明涨势，买入
            if self.hidd >0:
                self.order = self.buy()
        else:
# 已经买了，如果 MA5 < MA10 ，说明跌势，卖出
            if self.hidd <0:
                self.order = self.sell()

    def stop(self):
        self.log(u'(金叉死叉有用吗) Ending Value %.2f' %
                 (self.broker.getvalue()), doprint=True)
if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)
    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    datapath_1=r'C:\Users\finup\Desktop\fsdownload\ETH_USDT.csv'
    #datapath_2='/home/yjj/stock_data_day/000002.SZ.csv'
    # Create a Data Feed
    data_1 = bt.feeds.GenericCSVData(
        dataname=datapath_1,
        # Do not pass values before this date
        #datetime=1,
        timeframe = bt.TimeFrame.Minutes,
        fromdate=datetime.datetime(2019, 11, 27),
        # Do not pass values after this date
        todate=datetime.datetime(2021, 3, 31),
        dtformat=('%Y-%m-%d %H:%M:%S'),
        tmformat=('%H:%M:%S'),
        datetime=0,
        open=1,
        close=4,
        high=2,
        low=3,
        volume=5,
        #openinterest=6,
        #code=-1,
        reverse=False)
#     data_2 = bt.feeds.GenericCSVData(
#         dataname=datapath_2,
#         # Do not pass values before this date
#         fromdate=datetime.datetime(1991, 12, 23),
#         # Do not pass values after this date
#         todate=datetime.datetime(2017, 12, 31),
#         dtformat=('%Y-%m-%d'),
#         tmformat=('%H.%M.%S'),
#         date=0,
#         open=1,
#         close=2,
#         high=3,
#         low=4,
#         volume=5,
#         openinterest=6,
#         reverse=False)

    # Add the Data Feed to Cerebro
    cerebro.adddata(data_1)
    #cerebro.adddata(data_2)

    # Set our desired cash start
    cerebro.broker.setcash(100000.0)
    cerebro.broker.setcommission(commission=0.001)
    cerebro.addsizer(bt.sizers.FixedSize, stake=100)
    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.plot()
