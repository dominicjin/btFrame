import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from DataFeed import *
from cerebo import *
from Strategy import *

def main():
    # spot = pd.read_csv("../../data_acquire/data/spot_BTCUSDT_1d.csv", sep=',', index_col='Open time')
    path = "/home/ubuntu/data_acquire/data/GRIFFAINUSDT/"
    symbol = "GRIFFAINUSDT"
    name = "future"
    interval = "15m"
    name = f"{name}_{symbol}_{interval}"
    data = pd.read_csv(path+f"{name}.csv", sep=',', index_col='Open time')
    data = data.replace([0, ' '], np.nan)
    data = data.astype(float)
    data = data.interpolate(method='linear')
    data.index = pd.to_datetime(data.index)
    # print(data.iloc[287:293])
    # print(data['Close'].iloc[287:293])
    # spotDataFeed = DataFeed("spot_BTC", spot)
    dataFeed = DataFeed(name, data)
    bt = cerebo()
    bt.broker.set_cash(1e5)
    bt.add_dataFeed(dataFeed)
    bt.add_strategy(Strategy)
    bt.run()
    bt.plot()
    # print(bt.broker.orderInfo())
    return




if __name__=="__main__":
    main()