import pandas as pd

OPENML_CSV = 'openml_datasets.csv'

df = pd.read_csv(OPENML_CSV)
items = df['name'].iloc[1:10,].to_list()
print(items)