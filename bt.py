from Broker import *
from Indicator import *
from BasciStrategy import *
from Order import *
from SMAStrategy import *
from DataFeed import *
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class Backtest:
    def __init__(self, broker=Broker()):
        self.strategy = None
        self.broker = broker
        # self.plot_data = PlotData()
        self.data= []
        self.totalValue = []
        # self.visualizer = Visualizer(self.plot_data)

    def run(self):
        ## initialize

        ## start strategy
        while True:
            # execute order
            if IndexCount.get_index() >= len(self.data[0]):
                break

            if self.strategy.order_pending:
                for order in self.strategy.order_pending:
                    self.strategy.order_execute(order)
                    self.broker.order.append(order.orderInfo())
                    self.broker.execute(order)
                self.strategy.order_pending = []
            
            # print(type(self.data[0].close))
            self.strategy.next()
            self.broker.updateValue(dict(zip(self.strategy.asset,[d.close[0] for d in self.data])))
            self.totalValue.append(self.broker.cash + self.broker.stockValue)
            print(self.totalValue[-1])
            IndexCount.increment()

        fig, ax = plt.subplots()
        ax.plot(self.data[0].data.index, self.totalValue)
        ax.set_xlabel('Date')
        ax.set_ylabel('Total Portfolio Value')
        ax.grid(None, which='major', axis='both')
        ax.xaxis.set_major_locator(mdates.DayLocator(interval = len(self.strategy.data[0]) //10))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_tick_params(rotation=45, labelsize=5)
        # ax.xaxis.tick
        # plt.show()
        fig.savefig("my.png")
        # calculate value
        # 添加总资产数据并更新图形
        # self.plot_data.add('Total Portfolio Value', total_value)
        # self.visualizer.plot()

    def SetStrategy(self, strategy):
        self.strategy = strategy(self.broker, self.data)
    
    def AddDataFeed(self, dataFeed):
        self.data.append(dataFeed)
        

def main():
    broker = Broker(1e6)
    data = pd.read_csv("../data/BTCUSDT_1d.csv", sep=',', index_col='Open time')
    datafeed = DataFeed(data, "123")
    bt = Backtest(broker)
    bt.AddDataFeed(datafeed)
    bt.SetStrategy(SMAStrategy)
    bt.run()
    return




if __name__=="__main__":
    main()
