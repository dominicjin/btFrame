
from Order import *
from DataFeed import *
from Position import *
from Broker import *

class BasicStrategy():
    def __init__(self, broker, datafeed:list[DataFeed]):
        self.datas: list[DataFeed] = datafeed ##List
        self.broker: Broker= broker
        self.positions: dict[str, Position] = {}
        self.order_pending = []
        self.value = list()
        # self.position = Position()

    def next():
        raise NotImplementedError("You must implement the function")
    

    def addData(self, datafeed):
        if isinstance(datafeed, list):
            self.data += datafeed
        else:
            self.data.append(datafeed)

    def buy(self, asset, price=None, size=None):
        order = Order('BUY', asset, size, price)
        self.order_pending.append(order)
        return order


    def sell(self, asset):
        order = Order('SELL', asset)
        self.order_pending.append(order)
        return order

    ## default: use first data current open price
    def order_execute(self, order:Order, index=0):
        order.status = 'success'

        ## default: open[0]
        found = False
        for _, data in enumerate(self.datas):
            if order.asset == data.asset:
                found = True
                order.price = data.open[0]
        if not found:
            raise ValueError("not found value")

        if order.orderType == "BUY":
            if not order.size:
                order.size = self.calculateQuantity(self.broker.cash, order.price)
            if order.asset not in self.positions:
                self.positions[order.asset] = Position(order.asset, order.price, order.size)
            else:
                self.positions[order.asset].long_position(order.price, order.size)
            self.broker.update_cash(-order.price * order.size)

        elif order.orderType == "SELL":
            if not order.size:
                order.size = self.positions[order.asset].size
            if order.asset not in self.positions:
                self.positions[order.asset] = Position(order.asset, order.price, -order.size)
            else:
                self.positions[order.asset].short_position(order.price, order.size)
            self.broker.update_cash(order.price * order.size)

    def update_value(self, value):
        self.value.append(value)

    @staticmethod
    def calculateQuantity(cash, price):
        size = cash // price
        value = price * size
        index = 1
        while value <= 0.98 * cash:
            print(cash, price)
            quantity = int(cash / price * 10 ** index) / (10 ** index)
            value = price * size
            index += 1
        return size
        