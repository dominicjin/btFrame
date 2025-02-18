from BasciStrategy import *
from myIndicator import *
import pandas as pd
from Order import *
from PlotManager import PlotManager

class RSIStrategy(BasicStrategy):
    def __init__(self, broker, data):
        super().__init__(broker, data)
        # print(type(self.data[0].data['Close']))
        self.period = 14
        self.overbought = 70
        self.oversell = 30
        self.position = False


        # 设置要显示交易信号的图表组
        self.signal_groups = ['RSI', 'dif']  # 在RSI和价格图上都显示信号
        
        # Indicator
        self.dif = SimpleIndicator('dif', self.datas[0].data['Close'] - self.datas[1].data['Close'])
        self.rsi = RSI(self.dif.data, period=self.period)
        
        # 配置绘图
        self.plot_manager.add_line('Total Assets', self.value)
        
        # 价格数据都放在"价格走势"组
        self.plot_manager.add_line('Spot Price', self.datas[0].data['Close'], 
                                 group='Price Trend')
        self.plot_manager.add_line('Future Price', self.datas[1].data['Close'], 
                                 group='Price Trend')
        
        # 价差数据
        self.plot_manager.add_line('dif', self.dif.data)
        
        # RSI数据
        self.plot_manager.add_line('RSI', self.rsi.data, color='orange')
        self.plot_manager.add_horizontal_line('RSI', 70)
        self.plot_manager.add_horizontal_line('RSI', 30, color='g')
        
        # self.rsi.save_data("./postprocess/rsi.csv")
        
    def next(self):
        if pd.isna(self.rsi[0]):
            return
        
        sellSignal = self.rsi[0] > self.overbought and self.position
        buySignal = self.rsi[0] < self.oversell and (not self.position)
        
        if buySignal:
            self.buy()  # buy 方法会自动添加交易信号
            self.position = True

        if sellSignal:
            self.sell()  # sell 方法会自动添加交易信号
            self.position = False
            
    def buy(self, price=None, size=1):
        order = [Order('BUY', "spot_BTC", size=size), Order('SELL', "future_BTC", size=size)]
        self.order_pending.extend(order)
        self.add_trade_signal('BUY', self.datas[0].data.index[IndexCount.get_index()])
        return order
    
    def sell(self, price=None, size=1):
        order = [Order('SELL', "spot_BTC", size=size), Order('BUY', "future_BTC", size=size)]
        self.order_pending.extend(order)
        self.add_trade_signal('SELL', self.datas[0].data.index[IndexCount.get_index()])
        return order
    
