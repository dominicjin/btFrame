from Indicator import *

class SimpleIndicator(Indicator):
    def __init__(self, name, datafeed:pd.Series):
        super().__init__(name)
        self.datafeed = datafeed
        self.calculate()

    def calculate(self):
        self.data = self.datafeed

class SMA(Indicator):
    def __init__(self, datafeed:pd.Series, period:int):
        super().__init__(f"SMA_{period}")
        self.period = period
        self.datafeed = datafeed
        self.calculate()

    def calculate(self):
        self.data = self.datafeed.rolling(window=self.period).mean()
    
class RSI(Indicator):
    def __init__(self, datafeed:pd.Series, period=14):
        super().__init__(f"RSI_{period}")
        self.datafeed = datafeed
        self.period = period
        self.calculate()

    def calculate(self):
        delta = self.datafeed.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.period).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        self.data = rsi

    def save_data(self, filename):
        self.data.to_csv(filename)
        




class MACD(Indicator):
    def __init__(self, data:pd.Series, shortPeriod, longPeriod, signalPeriod=9):
        super().__init__(f"MACD_{shortPeriod}_{longPeriod}")
        self.shortPeriod = shortPeriod
        self.longPeriod = longPeriod
        self.signalPeriod = signalPeriod
        self.data = data
        self.calculate()
    

    def calculate(self):
        def ExpotentialAverage(data, period):
            span = 2/(period+1)
            ema = [data.iloc[0]]
            for i in range(1,len(data)):
                ema.append(ema[i-1] * (1 - span) + data.iloc[i] * span)    ## loc ==> label ; iloc ==> index ; series 加减 需要索引，type一致，不然需要 .value
            ema_pd = pd.Series(ema)
            return  ema_pd
        short_ema = ExpotentialAverage(self.data, self.shortPeriod).ewm(span=self.shortPeriod, adjust=False).mean()
        long_ema = ExpotentialAverage(self.data, self.longPeriod).ewm(span=self.longPeriod, adjust=False).mean()
        dif_ema = short_ema - long_ema
        dea = dif_ema.rolling(window=self.signalPeriod).mean()
        macd = dif_ema - dea        
        self.data = macd


class Crossover(Indicator):
    def __init__(self, data1:pd.Series, data2:pd.Series):
        super().__init__("Crossover")
        if len(data1) != len(data2):
            raise ValueError("length of data1 is not equal to data2")
        
        self.data1 = data1
        self.data2 = data2
        self.calculate()

    def calculate(self):
        length = len(self.data1)
        result = []

        for index in range(0, length):
            # 跳过NaN值
            if pd.isna(self.data1[index]) or pd.isna(self.data2[index]) or pd.isna(self.data1[index-1]) or pd.isna(self.data2[index-1]):
                result.append(pd.NA)
                continue
            
            # 计算交叉
            if self.data1[index-1] < self.data2[index-1] and self.data1[index] > self.data2[index]:
                result.append(1)  # 金叉
            elif self.data1[index-1] > self.data2[index-1] and self.data1[index] < self.data2[index]:
                result.append(-1)   # 死叉
            else:
                result.append(0)
        self.data = pd.Series(result)



        



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