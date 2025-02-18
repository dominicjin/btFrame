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

# class test():
#     params = (('first', 2), ('second', 15))
#     def __init__(self):
#         pass

#     def get_param(self):
#         print(self.params["first"])
#         return  
    
#     def params(self):
        

# t = test()
# t.get_param()

# import pandas as pd
# import matplotlib.pyplot as plt

# df = pd.Series([6, 9, 5])

# plt.plot(df.index, df.values)
# plt.show()

# def func(*args, **kwargs):
#     # print(kwargs)
#     print("args:",args)
#     print("kwargs:",kwargs)
#     print("args[0]:",args[0])
#     print("kwargs['a']:",kwargs['a'])

# func(1,23,a=1, b=2)
import pandas as pd
import numpy as np

df = pd.DataFrame([1,2,3,0,5], [6,0,8,9,10])
df = df.replace(0, np.nan)
df.inter
print(df)

