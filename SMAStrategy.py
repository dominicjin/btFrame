from BasciStrategy import *
from myIndicator import *
import pandas as pd

class SMAStrategy(BasicStrategy):
    def __init__(self, broker, data):
        super().__init__(broker, data)
        # print(type(self.data[0].data['Close']))
        self.shortPeriod = 9
        self.longPeriod = 26
        # self.close = SimpleIndicator("Close", self.data[0].data['Close'])
        # Indicator
        self.smaShort = SMA(self.data[0].data['Close'], period=self.shortPeriod)
        self.smaLong = SMA(self.data[0].data['Close'], period=self.longPeriod)
        self.crossOver = Crossover(self.smaShort, self.smaLong)
        self.macd = MACD(self.data[0].data['Close'], self.shortPeriod, self.longPeriod)
        
        
    def next(self):
        if pd.isna(self.smaShort[0]) or pd.isna(self.smaLong[0]) or pd.isna(self.macd[0]) or pd.isna(self.crossOver[0]):
            # print(1)
            return
        
        upOrDown =  1 if (self.macd[0] - self.macd[-1]>0) else 0
        buySignal = upOrDown and self.crossOver[0] == 1 and self.broker.position.get(self.asset[0], 0) == 0
        sellSignal = self.crossOver[0] == -1 and self.broker.position.get(self.asset[0], 0) != 0  
        
        if buySignal:
            # print(f"time is {self.close.datafeed.index[0]}")
            print("buy buy buy", IndexCount.get_index())
            self.buy(self.asset[0])
        if sellSignal:
            # print(f"time is {self.close.index[0]}")
            print("sell sell sell", IndexCount.get_index())
            self.sell(self.asset[0])
