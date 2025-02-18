from Broker import *
from Indicator import *
from BasciStrategy import *
from Order import *
# from SMAStrategy import *
from RSIStrategy import *
from DataFeed import *
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from Broker import *
from draw import *
from matplotlib.ticker import MaxNLocator

class cerebo:
    def __init__(self):
        self.strategy: BasicStrategy = None
        self.broker = Broker()
        self.broker.cerebo = self
        self.plot_data = PlotData()
        self.datas: list[DataFeed]= list()
        self.indicator = list()
        # self.value = list()
        # self.visualizer = Visualizer(self.plot_data)

    def run(self):
        ## initialize

        ## start strategy
        while True:
            # execute order
            if self.strategy.order_pending:
                for order in self.strategy.order_pending:
                    self.strategy.order_execute(order)
                    self.broker.add_order(order)
                self.strategy.order_pending = []
            
            self.strategy.next()
            self.broker.update_stockValue(self.strategy.positions,
                                        {data.asset:data.close[0] for data in self.datas})
            self.strategy.update_value(self.broker.value)

            IndexCount.increment()
            if IndexCount.get_index() >= len(self.datas[0]):
                break

        # 只处理收盘和数据保存，不画图
        self.close()

    def add_strategy(self, strategy):
        self.strategy = strategy(self.broker, self.datas)
    
    def add_dataFeed(self, *dataFeeds):
        for dataFeed in dataFeeds:
            self.datas.append(dataFeed)
    
    def plot(self):
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号

        # 获取子图配置
        subplots = self.strategy.plot_manager.subplots
        n_subplots = len(subplots)
        
        # 创建图表
        fig, axes = plt.subplots(n_subplots, 1, figsize=(15, 4*n_subplots), sharex=True)
        if n_subplots == 1:
            axes = [axes]
        
        index = pd.to_datetime(self.datas[0].data.index)
        max_ticks = 20
        
        # 绘制每个子图
        for ax, subplot_config in zip(axes, subplots):
            # 设置标题
            ax.set_title(subplot_config['title'], fontsize=12)
            
            # 绘制数据项
            for item in subplot_config['items']:
                # 绘制主数据
                ax.plot(index, item['data'], 
                       label=item['name'],
                       color=item.get('color'))
                ax.xaxis.set_major_locator(MaxNLocator(max_ticks))
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
                ax.xaxis.set_tick_params(rotation=45, labelsize=10)
                # ax.xaxis.set_major_locator(mdates.DayLocator(interval = len(self.datas[0].data) //10))
                
                # 处理额外配置
                if 'extra' in item:
                    if 'hlines' in item['extra']:
                        for hline in item['extra']['hlines']:
                            ax.axhline(**hline)
                    if 'markers' in item['extra']:
                        for marker in item['extra']['markers']:
                            marker_time = pd.to_datetime(marker['index'])
                            
                            # 找到最接近的时间点并获取对应的y值
                            # closest_time = min(item['data'].index, 
                                            # key=lambda x: abs(pd.to_datetime(x) - marker_time))
                            # print(type(closest_time))
                            # print(closest_time)
                            y_value = item['data'].index
                            
                            # 绘制标记点和注释
                            ax.plot(marker_time, y_value,
                                  marker['style'], 
                                  color=marker['color'],
                                  markersize=10,
                                  label=marker.get('text', ''))
                            
                            # 添加文本标注
                            ax.annotate(marker['text'],
                                      xy=(marker_time, y_value),
                                      xytext=(5, 5),
                                      textcoords='offset points',
                                      fontsize=10)
            
            ax.legend(fontsize=10)
            ax.grid(True)
        
        # 设置x轴格式
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # 保存图片
        fig.savefig("./postprocess/strategy_analysis.png", dpi=300, bbox_inches='tight')
        plt.close()

    def close(self):
        """
        处理策略结束后的工作：
        1. 平掉所有持仓
        2. 添加交易信号标记
        """
        # 1. 平掉所有持仓
        current_prices = {data.asset: data.close[-1] for data in self.datas}
        for asset, position in self.strategy.positions.items():
            if position.size != 0:
                # 记录最后的平仓信号
                self.strategy.add_trade_signal('SELL' if position.size > 0 else 'BUY', 
                                            self.datas[0].data.index[-1])
                # 更新账户价值
                self.broker.update_cash(position.size * current_prices[asset])
                position.size = 0

        # 2. 添加所有交易信号标记到指定的图表组
        if self.strategy.trade_signals:
            for group in self.strategy.signal_groups:
                self.strategy.plot_manager.add_markers(group, self.strategy.trade_signals)


    # @property
    # def data(self):
    #     return self.datas[0]


