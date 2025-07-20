import pandas as pd

# Load dataframe
df = pd.read_pickle('../data/sales_level_dataset.pkl')

# Flag any cancelled orders
df['IsCancelled'] = df['InvoiceNo'].astype(str).str.startswith('C')

# Filter out any cancelled orders
df_sales = df[~df['IsCancelled']].copy()

# Create a new total price column as a result of unit price times quantity
if 'TotalPrice' not in df_sales.columns:
    df_sales['TotalPrice'] = df_sales['Quantity'] * df_sales['UnitPrice']

# Sum them all
total_sales = df_sales['TotalPrice'].sum()

with open('../outputs/analysis.txt', 'a') as log:
    log.write(f"💰 Total Sales (excluding cancellations): £{total_sales:,.2f}\n")

