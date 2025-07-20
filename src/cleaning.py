import pandas as pd

# Base dataset
df = pd.read_excel('../data/Online Retail.xlsx', engine='openpyxl')

# Iduntify non-SKU codes and filter them out
exclude_codes = ['D', 'S', 'AMAZONFEE', 'BANK CHARGES', 'M']
df = df[~df['StockCode'].isin(exclude_codes)].copy()

# SALES-LEVEL DATASET (keep all rows, including missing CustomerID)
sales_df = df.copy()
sales_df.to_pickle('../data/sales_level_dataset.pkl')

# CUSTOMER-BEHAVIOUR DATASET (drop rows with missing CustomerID)
customer_df = df.dropna(subset=['CustomerID']).copy()
customer_df.to_pickle('../data/customer_behaviour_dataset.pkl')



