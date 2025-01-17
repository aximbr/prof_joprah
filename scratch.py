import pandas as pd
import openml
import os

import tkinter as tk
from tkinter import messagebox, ttk

#openml.config.cache_directory = os.path.expanduser('.')

# OPENML_CSV = 'openml_datasets.csv'

# df = pd.read_csv(OPENML_CSV)
# # items = df['name'].iloc[1:10,].to_list()

# items = [tuple(r) for r in df[['name', 'version', 'NumberOfInstances']].to_numpy()]

# x= 'an'

# for item in items:
#     if 'an' in str(item[0]):
#         print(item[0])
OPENML_CSV = 'openml_datasets.csv'

try:
    df = pd.read_csv(OPENML_CSV)
except FileNotFoundError:
    openml.config.cache_directory = os.path.expanduser('.')
    df = openml.datasets.list_datasets(output_format="dataframe")
    df.to_csv(OPENML_CSV, index=False)

print(df.info)

