from Indicator import *

class SMA(Indicator):
    def __init__(self, datafeed:pd.Series, period:int):
        super().__init__(f"SMA_{period}")
        self.period = period
        self.datafeed = datafeed
        self.calculate()

    def calculate(self):
        self.data = self.datafeed.rolling(window=self.period).mean()

class MACD(Indicator):
    def __init__(self, datafeed:pd.Series, shortPeriod, longPeriod, signalPeriod=9):
        super.__init__(f"MACD_{shortPeriod}_{longPeriod}")
        self.shortPeriod = shortPeriod
        self.longPeriod = longPeriod
        self.signalPeriod = signalPeriod
        self.datafeed = datafeed

    def calculate(self):
        short_ema = self.datafeed.ewm(span=self.shortPeriod, adjust=False).mean()
        long_ema = self.datafeed.ewm(span=self.longPeriod, adjust=False).mean()
        dif_ema = short_ema - long_ema
        dea = dif_ema.rolling(window=self.signalPeriod).mean()
        macd = dif_ema - dea        
        self.data = macd

def main():
    testlist = pd.Series([1,2,3,4,6,8,10])
    period = 3
    sma_3 = SMA(testlist, period)
    print("hello")
    print(sma_3[0], sma_3[3], sma_3[5], sma_3[20])
    IndexCount.increment()
    print(sma_3[0], sma_3[3], sma_3[5], sma_3[20])
    
    SMA.increment()

    print(SMA.get_index())
    # print(sma_3[0], sma_3[3], sma_3[5], sma_3[20])
    # print(sma_3[-1], sma_3[-2], sma_3[5], sma_3[20])
    # print(testlist.rolling(window=period).mean())
    return 


if __name__ == "__main__":
    main()