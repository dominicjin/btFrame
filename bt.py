from backtest.Account import *
from Indicator import *
from BasciStrategy import *
from Order import *

class Backtest:
    def __init__(self, broker=Broker()):
        self.strategy = None
        self.broker = broker
        # self.plot_data = PlotData()
        self.data= []
        # self.visualizer = Visualizer(self.plot_data)

    def run(self):
        ## initialize
        
        # execute order
        if self.strategy.order_pending:
            for order in self.strategy.order_pending:
                self.strategy.order_execute(order)
                self.broker.order.append(order.orderInfo())
                self.broker.execute(order)
            self.strategy.order_pending = []
        # update 


        ## start strategy
        while True:
            
            self.strategy.next()

            # 每次执行策略并生成订单
            # order = self.strategy.next(data, self.account)



            IndexCount.increment()


        # 添加总资产数据并更新图形
        self.plot_data.add('Total Portfolio Value', total_value)
        self.visualizer.plot()

    def SetStrategy(self, strategy):
        self.strategy = strategy
    
    def AddDataFeed(self, dataFeed):
        self.data.append(dataFeed)
        

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
