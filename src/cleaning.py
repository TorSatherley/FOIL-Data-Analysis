import pandas as pd

# Base dataset
df = pd.read_excel('../data/Online Retail.xlsx', engine='openpyxl')

# SALES-LEVEL DATASET (keep all rows, including missing CustomerID)
sales_df = df.copy()
sales_df.to_pickle('../data/sales_level_dataset.pkl')

# CUSTOMER-BEHAVIOUR DATASET (drop rows with missing CustomerID)
customer_df = df.dropna(subset=['CustomerID']).copy()
customer_df.to_pickle('../data/customer_behaviour_dataset.pkl')



