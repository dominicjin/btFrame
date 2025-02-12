import pandas as pd

class DataFeed:
    def __init__(self, filename):
        self.data = pd.read_csv(filename, sep=',', index_col='Open time')  # 读取市场数据
        self.index = 0  # 当前数据的位置

    def next(self):
        if self.index < len(self.data):
            current_data = self.data.iloc[self.index]
            self.index += 1
            return current_data
        return None

class Indicator:
    def __init__(self, datafeed, name):
        self.datafeed = datafeed
        self.name = name
        self.data = pd.Series()
        self.data.index = datafeed.index

    def calculate(self):
        raise NotImplementedError("subclasses should implement this method")
    
    def get_data(self):
        return self.data

class SMA(Indicator):
    def __init__(self, datafeed, period, pricetype):
        super.__init__(datafeed, f"SMA_{period}")
        self.period = period
        self.pricetype = pricetype

    def calculate(self):
        self.data = self.datafeed[self.pricetype].rolling(windows=self.period).mean()

class MACD(Indicator):
    def __init__(self, datafeed, shortPeriod, longPeriod, pricetype, signalPeriod=9):
        super.__init__(datafeed, f"MACD_{shortPeriod}_{longPeriod}")
        self.shortPeriod = shortPeriod
        self.longPeriod = longPeriod
        self.pricetype = pricetype
        self.signalPeriod = signalPeriod

    def calculate(self):
        short_ema = self.datafeed[self.pricetype].ewm(span=self.shortPeriod, adjust=False).mean()
        long_ema = self.datafeed[self.pricetype].ewm(span=self.longPeriod, adjust=False).mean()
        dif_ema = short_ema - long_ema
        dea = dif_ema.rolling(window=self.signalPeriod).mean()
        macd = dif_ema - dea        
        self.data = macd

        