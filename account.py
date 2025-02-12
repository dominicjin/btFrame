
class Account:
    def __init__(self, cash):
        self.cash = cash  # 当前现金
        self.stock_value = 0  # 当前持仓的市值
        self.position = False  # 是否持有仓位

    def buy(self, price, amount):
        self.position = True
        self.cash -= price * amount  # 扣除现金
        self.stock_value += price * amount  # 增加持仓的市值

    def sell(self, price, amount):
        self.position = False
        self.cash += price * amount  # 增加现金
        self.stock_value -= price * amount  # 减少持仓的市值

class Broker:
    def __init__(self, account):
        self.account = account  # 与账户进行绑定
        self.orders = []  # 存储所有的订单

    def execute(self, order):
        if order.execute():  # 执行订单
            if order.action == "buy":
                self.account.buy(order.price, order.amount)
            elif order.action == "sell":
                self.account.sell(order.price, order.amount)
            self.orders.append(order)

class Order:
    def __init__(self, action, price, amount, status="pending"):
        self.action = action  # 'buy' 或 'sell'
        self.price = price  # 订单的价格
        self.amount = amount  # 订单的数量
        self.status = status  # 订单状态 ('pending', 'filled', 'cancelled')

    def execute(self):
        if self.status == "pending":
            self.status = "filled"  # 完成订单
            return True
        return False
