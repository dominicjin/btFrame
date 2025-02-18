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
    def __init__(self, dataFeed:pd.Series, shortPeriod, longPeriod, signalPeriod=9):
        super().__init__(f"MACD_{shortPeriod}_{longPeriod}")
        self.shortPeriod = shortPeriod
        self.longPeriod = longPeriod
        self.signalPeriod = signalPeriod
        self.dataFeed = dataFeed
        self.calculate()
    

    def calculate(self):
        # 直接使用 pandas 的 ewm
        short_ema = self.dataFeed.ewm(span=self.shortPeriod, adjust=False).mean()
        long_ema = self.dataFeed.ewm(span=self.longPeriod, adjust=False).mean()
        dif_ema = short_ema - long_ema
        dea = dif_ema.ewm(span=self.signalPeriod, adjust=False).mean()  # DEA 也应该用 EMA 而不是简单移动平均
        macd = dif_ema - dea
        macd.index = self.dataFeed.index        
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
    # 可以删除整个测试函数，或者保留但注释掉打印语句
    testlist = pd.Series([1,2,3,4,6,8,10])
    period = 3
    sma_3 = SMA(testlist, period)
    print("hello")  # 删除
    print(sma_3[0], sma_3[3], sma_3[5], sma_3[20])  # 删除
    IndexCount.increment()
    print(sma_3[0], sma_3[3], sma_3[5], sma_3[20])  # 删除
    
    SMA.increment()
    print(SMA.get_index())  # 删除


if __name__ == "__main__":
    main()