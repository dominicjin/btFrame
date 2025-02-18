import pandas as pd
from DataFeed import *
from cerebo import *


def main():
    spot = pd.read_csv("../biance_data_acquire/data/spot_BTCUSDT_1d.csv", sep=',', index_col='Open time')
    future = pd.read_csv("../biance_data_acquire/data/future_BTCUSDT_1d.csv", sep=',', index_col='Open time')

    spotDataFeed = DataFeed("spot_BTC", spot)
    futureDataFeed = DataFeed("future_BTC", future)
    bt = cerebo()
    bt.broker.set_cash(0)
    bt.add_dataFeed(spotDataFeed, futureDataFeed)
    bt.add_strategy(RSIStrategy)
    bt.run()
    bt.plot()
    # print(bt.broker.orderInfo())
    return




if __name__=="__main__":
    main()