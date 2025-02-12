import pandas as pd
from Indicator import *

class DataFeed(IndexCount):
    def __init__(self, datafeed, assetName):
        self.data = datafeed
        self.asset = assetName

    def close(self):
        return SimpleIndicator('close', self.data['Close'])
    
    def open(self):
        return SimpleIndicator('open', self.data['Open'])
    
    def volume(self):
        return SimpleIndicator('volume', self.data['Volume'])
    
    def low(self):
        return SimpleIndicator('low', self.data['Low'])
    
    def high(self):
        return SimpleIndicator('high', self.data['High'])
    
    def total_value(self):
        return SimpleIndicator('total_value', self.data['total_value'])
    

class SimpleIndicator(Indicator):
    def __init__(self, name, datafeed:pd.Series):
        super().__init__(name)
        self.datafeed = datafeed

    def calculate(self):
        self.data = self.datafeed
