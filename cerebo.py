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
import numpy as np

class cerebo:
    def __init__(self):
        self.strategy: BasicStrategy = None
        self.broker = Broker()
        self.broker.cerebo = self
        self.plot_data = PlotData()
        self.datas: list[DataFeed]= list()
        self.indicator = list()
        self.metrics = None

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

            
            if IndexCount.get_index() >= len(self.datas[0]) - 1:
                # 在结束前计算一次性能指标       
                self.close() 
                break
            IndexCount.increment()

        # 只处理收盘和数据保存，不画图
        

    def add_strategy(self, strategy):
        self.strategy = strategy(self.broker, self.datas)
    
    def add_dataFeed(self, *dataFeeds):
        for dataFeed in dataFeeds:
            self.datas.append(dataFeed)
    
    def calculate_metrics(self):
        """计算策略性能指标"""
        # 获取每日账户价值数据
        value_series = pd.Series(self.strategy.value, index=self.datas[0].data.index[:len(self.strategy.value)])
        # 计算每日收益率
        daily_returns = value_series.pct_change().dropna()
        
        # 计算年化收益率
        total_days = (value_series.index[-1] - value_series.index[0]).days
        total_return = (value_series.iloc[-1] / value_series.iloc[0]) - 1
        annual_return = (1 + total_return) ** (365 / total_days) - 1
        
        # 计算波动率（年化）
        volatility = daily_returns.std() * np.sqrt(365)
        
        # 计算夏普比率（假设无风险利率为3%）
        risk_free_rate = 0.03
        sharpe_ratio = (annual_return - risk_free_rate) / volatility
        
        # 计算最大回撤
        cummax = value_series.cummax()
        drawdown = (value_series - cummax) / cummax
        max_drawdown = drawdown.min()
        
        # 创建性能指标字典
        metrics = {
            "Annual Return": f"{annual_return:.2%}",
            "Annial Volatility": f"{volatility:.2%}",
            "Sharpe Ratio": f"{sharpe_ratio:.2f}",
            "Max Drawdown": f"{max_drawdown:.2%}"
        }
        
        return metrics

    def plot(self):
        # 设置中文字体
        # plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        # plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号

        # 获取子图配置
        subplots = self.strategy.plot_manager.subplots
        # print(subplots)
        n_subplots = len(subplots)
        
        # 创建图表
        fig, axes = plt.subplots(n_subplots, 1, 
                                figsize=(15, 5*n_subplots),  # 增加高度
                                constrained_layout=True)      # 使用 constrained_layout 替代 tight_layout
        if n_subplots == 1:
            axes = [axes]
        
        index = pd.to_datetime(self.datas[0].data.index)
        max_ticks = 20
        
        # 绘制每个子图
        for ax, subplot_config in zip(axes, subplots):
            # 设置标题，减小字体大小
            ax.set_title(subplot_config['title'], fontsize=10, pad=10)
            
            # 绘制数据项
            for item in subplot_config['items']:
                ax.plot(index, item['data'], 
                       label=item['name'],
                       color=item.get('color'))
                ax.xaxis.set_major_locator(MaxNLocator(max_ticks))
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
                ax.xaxis.set_tick_params(rotation=45, labelsize=8)  # 减小刻度标签大小
                
                # 处理额外配置
                if 'extra' in item:
                    if 'hlines' in item['extra']:
                        for hline in item['extra']['hlines']:
                            ax.axhline(**hline)
                    if 'markers' in item['extra']:
#                         '''
# item = {
#     'data': pd.Series([100, 102, 98, 103, ...]),  # 价格数据
#     'name': '股票价格',
#     'color': 'blue',
#     'extra': {
#         'hlines': [
#             {'y': 100, 'color': 'red', 'linestyle': '--'},  # 支撑线
#             {'y': 105, 'color': 'green', 'linestyle': '--'} # 压力线
#         ],
#         'markers': [
#             {
#                 'index': '2024-01-01',
#                 'style': '^',
#                 'color': 'green',
#                 'text': '买入信号'
#             },
#             {
#                 'index': '2024-01-15',
#                 'style': 'v',
#                 'color': 'red',
#                 'text': '卖出信号'
#             }
#         ]
#     }
# }
#                         '''
                        
                        # 在绘制markers之前，先创建一个集合记录已经添加的信号类型
                        signal_labels = set()
                        
                        for marker in item['extra']['markers']:
                            marker_time = marker['index']
                            y_value = item['data'][marker['index'].strftime('%Y-%m-%d %H:%M:%S')]
                            
                            # 只有当这个信号类型第一次出现时才添加到图例
                            label = marker.get('text', '')
                            if label in signal_labels:
                                label = ""
                            else:
                                signal_labels.add(label)
                            # 绘制标记点和注释
                            ax.plot(marker_time, y_value,
                                  marker['style'], 
                                  color=marker['color'],
                                  markersize=5,
                                  label=label)
                            
                            # 添加文本标注
                            ax.annotate(marker['text'],
                                      xy=(marker_time, y_value),
                                      xytext=(0, 10),
                                      textcoords='offset points',
                                      fontsize=5)
            
            ax.legend(fontsize=8, loc='upper left')  # 调整图例位置和大小
            ax.grid(True)
        
        # 使用已计算的指标
        metrics_text = "\n".join([f"{k}: {v}" for k, v in self.metrics.items()])
        axes[0].text(0.02, 0.98, metrics_text,
                    transform=axes[0].transAxes,
                    verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # 删除 tight_layout() 调用，因为我们使用了 constrained_layout
        # plt.tight_layout()  
        
        # 保存图片时设置更高的 dpi
        fig.savefig("./postprocess/strategy_analysis.png", 
                   dpi=300, 
                   bbox_inches='tight',
                   pad_inches=0.5)  # 增加边距
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


        self.metrics = self.calculate_metrics()

        # 直接使用已计算的指标
        print("\nperformance metrics:")
        for key, value in self.metrics.items():
            print(f"{key}: {value}")


