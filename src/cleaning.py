import pandas as pd

# Base dataset
df = pd.read_excel('../data/Online Retail.xlsx', engine='openpyxl')

# Identify and remove any double or trailing spaces in descriptions and remove
df['Description'] = (
    df['Description']
    .astype(str)
    .str.strip()              # Remove leading/trailing whitespace
    .str.replace(r'\s+', ' ', regex=True)  # Replace multiple spaces with a single space
    .str.upper()              # Standardise casing to uppercase
)


# SALES-LEVEL DATASET (keep all rows, including missing CustomerID)
sales_df = df.copy()
sales_df.to_pickle('../data/sales_level_dataset.pkl')

# CUSTOMER-BEHAVIOUR DATASET (drop rows with missing CustomerID)
customer_df = df.dropna(subset=['CustomerID']).copy()
customer_df.to_pickle('../data/customer_behaviour_dataset.pkl')



