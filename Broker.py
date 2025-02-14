
class Broker:
    def __init__(self, cash=0):
        self.cash = cash  # 当前现金
        self.stockValue = 0  # 当前持仓的市值
        self.position ={}
        # self.position = False  # 是否持有仓位
        self.order = []

    def execute(self, order):
        order_value = order.price * order.quantity

        if order.orderType == "BUY":
            self.cash -= order_value
            self.stockValue += order_value
            self.position[order.asset] = self.position.get(order.asset,0) + order.quantity
        elif order.orderType == "SELL":
            self.cash += order_value
            self.stockValue -= order_value
            self.position[order.asset] = self.position.get(order.asset,0) - order.quantity

    def updateValue(self, price:dict):
        self.stockValue = self.multiply_and_sum(price, self.position)

    @staticmethod
    def multiply_and_sum(dict1, dict2):
        # 初始化累加结果
        result = 0
        
        # 遍历第一个字典的所有键
        for key in dict1:
            # 如果字典2中也有相同的键
            if key in dict2:
                # 相同键的值相乘并累加
                result += dict1[key] * dict2[key]
        
        return result
    

    def get_totalValue(self):
        return self.cash + self.stock_value

    def get_cash(self):
        return self.cash

    def get_stockValue(self):
        return self.stockValue

