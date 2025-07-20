import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_pickle('../data/customer_behaviour_dataset.pkl')

# Standardise all codes to uppercase
df['StockCode'] = df['StockCode'].astype(str).str.upper()
# Define unwanted stock codes and patterns
unwanted_exact = [
    'AMAZONFEE', 'B', 'BANK CHARGES', 'C2', 'CRUK',
    'D', 'DOT', 'M', 'POST', 'S'
]
# Filter out unwanted codes
df = df[
    ~df['StockCode'].isin(unwanted_exact) & # Remove exact matches
    ~df['StockCode'].str.startswith('GIFT') # Remove anything starting with 'GIFT'
].copy()

# Flag any cancelled orders
df['IsCancelled'] = df['InvoiceNo'].astype(str).str.startswith('C')

# Filter out any cancelled orders
df_customers = df[~df['IsCancelled']].copy()

## Revenue By Customer ## 
# Make sure InvoiceDate is datetime
df_customers['InvoiceDate'] = pd.to_datetime(df_customers['InvoiceDate'])
# Calculate revenue per row if not done yet
df_customers['Revenue'] = df_customers['Quantity'] * df_customers['UnitPrice']
# Group by customer (assuming 'CustomerID' column)
customer_stats = df_customers.groupby('CustomerID').agg(
    total_revenue=('Revenue', 'sum'),
    order_count=('InvoiceNo', 'nunique'),
    first_order=('InvoiceDate', 'min'),
    last_order=('InvoiceDate', 'max')
).reset_index()

# Inspect top customers by total revenue
top_customers = customer_stats.sort_values(by='total_revenue', ascending=False).head(20)
with open('../outputs/customers_analysis.txt', 'w') as log:
    print('Top customers by revenue:\n', top_customers[['CustomerID', 'total_revenue', 'order_count']], file=log)

# Ensure CustomerID is a string
top_customers['CustomerID'] = top_customers['CustomerID'].astype(str)

# Plot setup
plt.figure(figsize=(12, 6))
bars = plt.barh(top_customers['CustomerID'], top_customers['total_revenue'], color='royalblue')

plt.xlabel('Total Revenue (£)', fontsize=12)
plt.ylabel('Customer ID', fontsize=12)
plt.title('Top 20 Customers: Revenue and Order Count', fontsize=14, fontweight='bold')
plt.gca().invert_yaxis()
plt.grid(axis='x', linestyle='--', alpha=0.6)

# Add labels: Revenue + Order Count
for i, bar in enumerate(bars):
    width = bar.get_width()
    order_count = top_customers.iloc[i]['order_count']
    label = f'£{width:,.2f} ({int(order_count)} orders)'
    plt.text(width + 10, bar.get_y() + bar.get_height() / 2, label, va='center', fontsize=10)

plt.tight_layout()
plt.savefig('../outputs/top_customers_revenue_and_orders.png')

# Show total number of customers
total_customers = df_customers['CustomerID'].nunique()
print(f'Total number of customers: {total_customers}')