import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi
import math
api = KaggleApi()
api.authenticate()
import pandas as pd

MAX_DS = 100
MAX_PAGE = math.ceil(MAX_DS/20)

datasets = []
for i in range(MAX_PAGE):
    datasets = datasets + api.datasets_list(search='Computer Science', page=i)
                
df = pd.DataFrame(datasets)
df.to_csv('kaggle_ds_list.csv')

# df = pd.DataFrame(datasets)
# # df.to_csv('kaggle_ds_list.csv')
# print(df.columns.values)

