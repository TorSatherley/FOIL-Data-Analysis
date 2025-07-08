import pandas as pd

# load the data into pandas dataframe
df = pd.read_excel('../data/Online Retail.xlsx', engine='openpyxl')
print('data loaded!')

# explore the data to see which cleaning methods might be needed
print("Initial data shape:", df.shape)
print("\nMissing values per column:\n", df.isnull().sum())
print("\nData types:\n", df.dtypes)
print("\nSample data:\n", df.head())