from draw import * 
from account import *
from datafeed import *

class Backtest:
    def __init__(self, broker):
        self.strategy = None
        self.data = []
        self.broker = broker
        self.plot_data = PlotData()
        self.indicator = 
        # self.visualizer = Visualizer(self.plot_data)

    def run(self):
        total_value = []  # 存储每个时间点的总资产值

        while True:
            data = self.data_feed.next()
            if data is None:
                break

            # 每次执行策略并生成订单
            order = self.strategy.next(data, self.account)
            if order:
                self.broker.execute(order)

            # 记录总资产值
            total_value.append(self.account.cash + self.account.stock_value)

        # 添加总资产数据并更新图形
        self.plot_data.add('Total Portfolio Value', total_value)
        self.visualizer.plot()

    def SetStrategy(self, strategy):
        self.strategy = strategy
    
    def AddDataFeed(self, dataFeed):
        self.data_feed.append(dataFeed)
        

def main():
    cash = 1e5
    account = Account(cash)
    broker = Broker(account)

    bt = Backtest(broker)
    path = "/home/ubuntu/dualMovingAveStra/data/"
    filename = "BTCUSDT_1d.csv"
    dataFeed = DataFeed(path+filename)
    bt.AddDataFeed(dataFeed)

    bt.run()


    bt.plot()
    return




if __name__=="__main__":
    main()
