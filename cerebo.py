from Broker import *
from Indicator import *
from BasciStrategy import *
from Order import *
# from SMAStrategy import *
from RSIStrategy import *
from DataFeed import *
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from Broker import *
from draw import *

class cerebo:
    def __init__(self):
        self.strategy: BasicStrategy = None
        self.broker = Broker()
        self.broker.cerebo = self
        self.plot_data = PlotData()
        self.datas: list[DataFeed]= list()
        self.indicator = list()
        # self.value = list()
        # self.visualizer = Visualizer(self.plot_data)

    def run(self):
        ## initialize

        ## start strategy
        while True:
            # execute order
            if self.strategy.order_pending:
                for order in self.strategy.order_pending:
                    self.strategy.order_execute(order)
                    self.broker.add_order(order)
                self.strategy.order_pending = []
            
            self.strategy.next()
            self.broker.update_stockValue(self.strategy.positions,{data.asset:data.close[0] for data in self.datas})
            self.strategy.update_value(self.broker.value)

            IndexCount.increment()
            if IndexCount.get_index() >= len(self.datas[0]):
                break

        df = pd.Series(self.strategy.value)
        df.index = self.datas[0].data.index
        # fig, ax = plt.subplots()
        # ax.plot(self.data[0].data.index, self.totalValue)
        # ax.set_xlabel('Date')
        # ax.set_ylabel('Total Portfolio Value')
        # ax.grid(None, which='major', axis='both')
        # ax.xaxis.set_major_locator(mdates.DayLocator(interval = len(self.strategy.datas[0]) //10))
        # ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        # ax.xaxis.set_tick_params(rotation=45, labelsize=5)
        # ax.xaxis.tick
        # plt.show()
        # fig.savefig("my.png")
        # calculate value
        # 添加总资产数据并更新图形
        # self.plot_data.add('Total Portfolio Value', total_value)
        # self.visualizer.plot()

    def add_strategy(self, strategy):
        self.strategy = strategy(self.broker, self.datas)
    
    def add_dataFeed(self, *dataFeeds):
        for dataFeed in dataFeeds:
            self.datas.append(dataFeed)
    
    def plot(self):
        index = self.datas[0].data.index
        fig, ax = plt.subplots()
        ax.plot(index, self.strategy.value)
        fig.savefig("./postprocess/rsi.png", dpi=300)

    # @property
    # def data(self):
    #     return self.datas[0]


