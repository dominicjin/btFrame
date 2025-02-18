# import pandas as pd
from Indicator import *
from myIndicator import SimpleIndicator

class DataFeed(IndexCount):
    def __init__(self, asset:str, datafeed:pd.DataFrame):
        """
        asset: stry
        datafeed: pd数据源
    
        """
        self.data = datafeed
        self.asset = asset
        self._close = None
        self._open = None
        self._volume = None
        self._low = None
        self._high = None

    def __len__(self):
        return len(self.data)

    @property
    def close(self):
        
        if not self._close:
            self._close = SimpleIndicator('close', self.data['Close'])
        return self._close
    
    @property
    def open(self):
        if not self._open:
            self._open = SimpleIndicator('open', self.data['Open'])
        return self._open
    @property
    def volume(self):
        if not self._volume:
            self._volume = SimpleIndicator('volume', self.data['Volume'])
        return self._volume
    @property
    def low(self):
        if not self._low:
            self.low = SimpleIndicator('low', self.data['Low'])
        return self._low
    @property
    def high(self):
        if not self._high:
            self._high = SimpleIndicator('high', self.data['High'])
        return self._high
    @property
    def total_value(self):
        return SimpleIndicator('total_value', self.data['total_value'])
    
    @property
    def dif(self):
        return SimpleIndicator('dif', self.data['Dif'])
    