
import openml

# Uncomment and set your OpenML cache directory
import os
openml.config.cache_directory = os.path.expanduser('.')

datasets_df = openml.datasets.list_datasets(output_format="dataframe")
datasets_df.to_csv("openml_datasets.csv", index=False)
# print(datasets_df.columns.values)
# #select_df = datasets_df[ (datasets_df['NumberOfMissingValues'] == 0)]
# print(datasets_df.iloc[0:2,])