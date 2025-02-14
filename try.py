# import pandas as pd

# data = pd.read_csv("../data/BTCUSDT_1d.csv", sep=',', index_col='Open time')
# print(data.iloc[1])
# print(data.iloc[1].iloc[1])
# print(type(data.iloc[1].iloc[1]))

# # data.set_index("lll", inplace=True)
# # print(data)
# data.index = pd.to_datetime(data.index)
# print(type(data.index[1]))
# print(data.index[1])

class test():
    params = (('first', 2), ('second', 15))
    def __init__(self):
        pass

    def get_param(self):
        print(self.params["first"])
        return  
    
    def params(self):
        

t = test()
t.get_param()