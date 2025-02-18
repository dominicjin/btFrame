import pandas as pd

class IndexCount:
    # 静态变量 index
    __index = 0
    
    @staticmethod
    def increment():
        """静态方法，用于增加 index 的值"""
        IndexCount.__index += 1
    
    @staticmethod
    def get_index():
        """静态方法，获取当前 index 的值"""
        return IndexCount.__index
    

class Indicator(IndexCount):
    def __init__(self, name:str):
        self.name = name
        self.data = pd.Series()

    ## virtual 
    def calculate(self):
        raise NotImplementedError("subclasses should implement this method")
    
    def get_data(self):
        return self.data
    
    def __getitem__(self, key):
        
        current_key = self.get_index() + key
        
        if current_key >= 0 and current_key < len(self.data):
            return self.data.iloc[current_key]
        else:
            # print(f"magic key:{current_key}")
            # print(f"len:{len(self.data)}")
            return False
        
    def __len__(self):
        return len(self.data)
            
