import matplotlib.pyplot as plt
import pandas as pd

class PlotData:
    def __init__(self):
        self.data = {}  # 存储所有需要绘制的数据，key: 指标名称, value: 数据

    def add(self, name, values):
        """添加新的绘制数据"""
        self.data[name] = values

    def get(self, name)->pd.Series:
        """获取指定名称的数据"""
        return self.data.get(name, None)

    def update(self, name, values):
        """更新已有的数据"""
        if name in self.data:
            self.data[name] = values

class Visualizer:
    def __init__(self, plot_data):
        self.plot_data = plot_data
        self.fig, self.ax = plt.subplots(figsize=(12, 8))

    def plot(self):
        self.ax.clear()  # 每次更新清空前一图形

        # 绘制价格（始终绘制）
        self.ax.plot(self.plot_data.get('close_price'), label="Close Price", color='black', alpha=0.6)

        # 绘制所有已添加的指标数据
        for name, values in self.plot_data.data.items():
            if name != 'close_price':  # 跳过价格数据
                self.ax.plot(values, label=name)

        # 添加图例和标题
        self.ax.legend()
        self.ax.set_title('Strategy Visualization')
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel('Price / Value')

        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()