from Order import *
from Position import *

class Broker:
    def __init__(self):
        self._cash = 0  # 当前现金
        self._stockValue = 0  # 当前持仓的市值
        # self.position = False  # 是否持有仓位
        self._order: list[Order]= list()
        self.cerebo = None

    def set_cash(self, cash):
        self._cash = cash

    def add_cash(self, cash):
        self._cash += cash

    def update_stockValue(self, positions:dict[str, Position], price:dict):


        currentValue = 0
        for asset, position in positions.items():
            if asset in price:
                currentValue += position.size * price[asset]
                position.update_price(price[asset])
        # print("current stocks value", currentValue)
        self._stockValue = currentValue
    
    def update_cash(self, cash):
        self._cash += cash

    def add_order(self, order:Order):
        self._order.append(order.orderInfo())

    def orderInfo(self):
        return self._order

    @property
    def value(self):
        return self._cash + self._stockValue

    @property
    def cash(self):
        return self._cash

    @property
    def stockValue(self):
        return self._stockValue

