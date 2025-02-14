
from Order import *
from DataFeed import *

class BasicStrategy():
    def __init__(self, broker, datafeed:list):
        self.data = datafeed ##List
        self.asset = [i.asset for i in datafeed]
        self.broker = broker
        self.order_pending = []

    def next():
        raise NotImplementedError("You must implement the function")
    
    def notifyOrder(self, order):
        pass

    def addData(self, datafeed):
        if isinstance(datafeed, list):
            self.data += datafeed
        else:
            self.data.append(datafeed)

    def buy(self, asset="123", quantity=None, price=None):
        order = Order('BUY', asset, quantity, price)
        self.order_pending.append(order)
        return order


    def sell(self, asset):
        order = Order('SELL', asset)
        self.order_pending.append(order)
        return order

    ## default: use first data current open price
    def order_execute(self, order:Order, index=0, type='Open'):
        order.status = 'Success'

        order.price = self.data[index].open[0]
        if order.orderType == "BUY":
            order.quantity = self.calculateQuantity(self.broker.get_cash(), order.price)
        elif order.orderType == "SELL":
            order.quantity = self.broker.position[order.asset]

    @staticmethod
    def calculateQuantity(cash, price):
        quantity = cash // price
        value = price * quantity
        index = 1
        while value <= 0.98 * cash:
            quantity = int(cash / price * 10 ** index) / (10 ** index)
            value = price * quantity
            index += 1
        return quantity
        