import pandas as pd
from typing import List, Dict, Any, Optional

class PlotManager:
    def __init__(self):
        self.data_items: Dict[str, Dict[str, Any]] = {}  # 存储所有数据项 数据名=》》数据 {'data', 'color', **kwargs}
        self.plot_groups: Dict[str, List[str]] = {}      # 存储分组信息 组名=》》list(数据名)
    
    def add_line(self, name: str, data: pd.Series, group: str = None, 
                color: Optional[str] = None, **kwargs):
        """
        添加一条线
        Args:
            name: 数据名称(唯一标识符)
            data: 数据序列
            group: 分组名称(子图标题), 如果不指定则使用name作为组名
            color: 线条颜色
            **kwargs: 其他绘图参数
        """
        if group is None:
            group = name
            
        # 存储数据项
        self.data_items[name] = {
            'data': data,
            'color': color,
            **kwargs
        }
        
        # 更新分组信息
        if group not in self.plot_groups:
            self.plot_groups[group] = []
        if name not in self.plot_groups[group]:
            self.plot_groups[group].append(name)
    
    def add_horizontal_line(self, group: str, y: float, 
                          color: str = 'r', linestyle: str = '--', 
                          alpha: float = 0.3):
        """
        向指定组添加水平线
        """
        if group not in self.plot_groups or not self.plot_groups[group]:
            return
            
        # 获取组中第一个数据项
        first_item = self.data_items[self.plot_groups[group][0]]
        
        # 添加水平线配置
        if 'extra' not in first_item:
            first_item['extra'] = {'hlines': []}
        elif 'hlines' not in first_item['extra']:
            first_item['extra']['hlines'] = []
            
        first_item['extra']['hlines'].append({
            'y': y,
            'color': color,
            'linestyle': linestyle,
            'alpha': alpha
        })
    
    def add_markers(self, group: str, markers: List[Dict[str, Any]]):
        """
        向指定组添加标记点
        Args:
            group: 组名
            markers: 标记点列表，每个标记点是一个字典，包含：
                - index: 标记点位置(x轴)
                - text: 标记文本
                - color: 标记颜色（可选）
                - style: 标记样式（可选）
        """
        if group not in self.plot_groups or not self.plot_groups[group]:
            return
            
        # 获取组中第一个数据项
        first_item = self.data_items[self.plot_groups[group][0]]
        
        # 添加标记点配置
        if 'extra' not in first_item:
            first_item['extra'] = {'markers': []}
        elif 'markers' not in first_item['extra']:
            first_item['extra']['markers'] = []
            
        first_item['extra']['markers'].extend(markers)
    
    @property
    def subplots(self):
        """
        生成用于绘图的子图配置
        """
        return [
            {
                'title': group,
                'items': [
                    {
                        'name': name,
                        **self.data_items[name]
                    } for name in items
                ]
            }
            for group, items in self.plot_groups.items()
        ]
    
    def clear(self):
        """
        清除所有绘图配置
        """
        self.data_items.clear()
        self.plot_groups.clear() 