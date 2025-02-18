from Order import *
from DataFeed import *
from Position import *
from Broker import *
from draw import *
from PlotManager import PlotManager

class BasicStrategy():
    def __init__(self, broker, datafeed:list[DataFeed]):
        self.datas: list[DataFeed] = datafeed ##List
        self.broker: Broker= broker
        self.positions: dict[str, Position] = {}
        self.order_pending = []
        self.value = list()
        self.plot_manager = PlotManager()
        self.trade_signals = []  # 添加交易信号列表
        self.signal_groups = []  # 默认在RSI图上显示信号，子类可以修改这个列表
        # self.position = Position()

    def next():
        raise NotImplementedError("You must implement the function")
    

    def addData(self, datafeed):
        if isinstance(datafeed, list):
            self.data += datafeed
        else:
            self.data.append(datafeed)

    def buy(self, asset, price=None, size=None):
        order = Order('BUY', asset, price, size)
        self.order_pending.append(order)
        # 添加买入信号
        self.add_trade_signal('BUY', self.datas[0].data.index[IndexCount.get_index()])
        return order


    def sell(self, asset, price=None, size=None):
        order = Order('SELL', asset, price, size)
        self.order_pending.append(order)
        # 添加卖出信号
        self.add_trade_signal('SELL', self.datas[0].data.index[IndexCount.get_index()])
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

    def add_subplot(self, title, data_items):
        """
        添加子图配置
        title: 子图标题
        data_items: 列表，每个元素是一个字典，包含：
            - name: 数据名称
            - data: 数据
            - color: 颜色（可选）
            - plot_type: 绘图类型（可选，如 'line', 'scatter' 等）
            - extra: 额外配置（可选，如水平线等）
        """
        self.plot_manager.add_subplot(title, data_items)
        
    def add_trade_signal(self, signal_type: str, current_time):
        """
        添加交易信号到所有指定的图表组
        """
        signal = {
            'index': current_time,
            'text': signal_type,
            'color': 'g' if signal_type == 'BUY' else 'r',
            'style': '^' if signal_type == 'BUY' else 'v'
        }
        self.trade_signals.append(signal)
        
       # self.plot_manager.add_markers(data_group, [signal])
        