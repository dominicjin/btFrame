
class Broker:
    def __init__(self, cash=0):
        self.cash = cash  # 当前现金
        self.stockValue = 0  # 当前持仓的市值
        self.position ={}
        # self.position = False  # 是否持有仓位
        self.order = []

    def execute(self, order):
        order_value = order.price * order.amount
        if order.orderType == "BUY":
            self.cash -= order_value
            self.stock_value += order_value
            self.position[order.asset] = self.position(order.asset,0) + order.amount
        elif order.orderType == "SELL":
            self.cash += order_value
            self.stock_value -= order_value
            self.position[order.asset] = self.position(order.asset,0) - order.amount

    def get_totalValue(self):
        return self.cash + self.stock_value

    def get_cash(self):
        return self.cash

    def get_stockValue(self):
        return self.stockValue

