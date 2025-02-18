import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from BasciStrategy import *
from myIndicator import *
import pandas as pd

class Strategy(BasicStrategy):
    def __init__(self, broker, data):
        super().__init__(broker, data)
        # print(type(self.data[0].data['Close']))
        self.shortPeriod = 9
        self.longPeriod = 26
        self.position = False
        # self.close = SimpleIndicator("Close", self.data[0].data['Close'])
        # Indicator
        self.smaShort = SMA(self.datas[0].data['Close'], period=self.shortPeriod)
        self.smaLong = SMA(self.datas[0].data['Close'], period=self.longPeriod)
        self.crossOver = Crossover(self.smaShort, self.smaLong)
        self.macd = MACD(self.datas[0].data['Close'], self.shortPeriod, self.longPeriod)
        self.signal_groups = ['Price Trend', 'MACD']

        self.plot_manager.add_line('Total Assets', self.value)
        
        self.plot_manager.add_line('Price', self.datas[0].data['Close'], 
                                 group='Price Trend')
        self.plot_manager.add_line(self.smaShort.name, self.smaShort.data, 
                                 group='Price Trend')
        self.plot_manager.add_line(self.smaLong.name, self.smaLong.data, 
                                 group='Price Trend')
        self.plot_manager.add_line(self.macd.name, self.macd.data, 
                                 group='MACD')
    
        
    def next(self):
        if pd.isna(self.smaShort[0]) or pd.isna(self.smaLong[0]) or pd.isna(self.macd[0]) or pd.isna(self.crossOver[0]) or pd.isna(self.macd[-1]):
            return
        
        upOrDown =  1 if (self.macd[0] - self.macd[-1]>0 and self.macd[-1] > self.macd[-2]) else 0
        buySignal = upOrDown and self.crossOver[0] == 1 and self.position == False
        sellSignal = (self.crossOver[0] == -1 or (self.macd[0] - self.macd[-1] < 0 and self.macd[-1] < self.macd[-2])) and self.position == True
        
        if buySignal:
            print("buy buy buy", self.datas[0].data.index[IndexCount.get_index()])
            self.buy(self.datas[0].asset)
            self.position = True
        if sellSignal:
            print("sell sell sell", self.datas[0].data.index[IndexCount.get_index()])
            self.sell(self.datas[0].asset)
            self.position = False
