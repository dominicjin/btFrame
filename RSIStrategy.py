from BasciStrategy import *
from myIndicator import *
import pandas as pd
from Order import *

class RSIStrategy(BasicStrategy):
    def __init__(self, broker, data):
        super().__init__(broker, data)
        # print(type(self.data[0].data['Close']))
        self.period = 14
        self.overbought = 70
        self.oversell = 30
        self.position = False

        # Indicator
        self.dif = SimpleIndicator('dif', self.datas[0].data['Close'] - self.datas[1].data['Close'])
        self.rsi = RSI(self.dif.data, period=self.period)

        # self.rsi.save_data("./postprocess/rsi.csv")
        
    def next(self):
        print(self.datas[0].data.index[IndexCount.get_index()])
        if pd.isna(self.rsi[0]):
            return
        
        sellSignal = self.rsi[0] > self.overbought and  self.position
        buySignal = self.rsi[0] < self.oversell and (not self.position)
        
        if buySignal:
            # print(f"time is {self.close.datafeed.index[0]}")
            print(self.datas[0].data.index[IndexCount.get_index()])
            print("buy buy buy", IndexCount.get_index())
            print(self.rsi[0])

            self.buy()
            self.position = True

        if sellSignal:
            # print(f"time is {self.close.index[0]}")
            print(self.datas[0].data.index[IndexCount.get_index()])
            print("sell sell sell", IndexCount.get_index())
            print(self.rsi[0])

            # print(self.rsi[0] > self.overbought)
            # print(self.position)
            # print(sellSignal)
            # print()
            self.sell()
            self.position = False

    def buy(self, price=None, size=1):
        order = [Order('BUY', "spot_BTC", size=size), Order('SELL', "future_BTC", size=size)]
        self.order_pending.extend(order)
        return order
    
    def sell(self, price=None, size=1):
        order = [Order('SELL', "spot_BTC", size=size), Order('BUY', "future_BTC", size=size)]
        self.order_pending.extend(order)
        return order
    
