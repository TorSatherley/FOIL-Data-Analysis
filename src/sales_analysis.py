import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataframe
df = pd.read_pickle('../data/sales_level_dataset.pkl')

# Flag any cancelled orders
df['IsCancelled'] = df['InvoiceNo'].astype(str).str.startswith('C')

# Filter out any cancelled orders
df_sales = df[~df['IsCancelled']].copy()

## Total Sales ##
# Create a new total price column as a result of unit price times quantity
if 'TotalPrice' not in df_sales.columns:
    df_sales['TotalPrice'] = df_sales['Quantity'] * df_sales['UnitPrice']
# Sum them all
total_sales = df_sales['TotalPrice'].sum()
with open('../outputs/sales_analysis.txt', 'w') as log:
    log.write(f"💰 Total Sales (excluding cancellations): £{total_sales:,.2f}\n")

plt.figure(figsize=(6, 4))
plt.text(0.5, 0.5, f'£{total_sales:,.2f}', fontsize=48, fontweight='bold', 
         ha='center', va='center', color='royalblue')
plt.axis('off')
plt.title('Total Revenue', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('../outputs/total_revenue_big_number.png')


## Revenue over time ##

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['Revenue'] = df['Quantity'] * df['UnitPrice']
df = df.set_index('InvoiceDate')
monthly_sales = df['Revenue'].resample('M').sum()
monthly_sales = monthly_sales[~((monthly_sales.index.year == 2011) & (monthly_sales.index.month == 12))]

plt.figure(figsize=(12, 6))
monthly_sales.plot(kind='line', marker='o')
plt.title('Monthly Sales Revenue')
plt.ylabel('Revenue (£)')
plt.xlabel('Month')
plt.grid(True)
plt.tight_layout()
plt.savefig('../outputs/revenue_over_time.png')

## Average Order Value ## 
# Sum revenue per order
order_revenue = df.groupby('InvoiceNo')['Revenue'].sum()
average_order_value = order_revenue.mean()
with open('../outputs/sales_analysis.txt', 'a') as log:
    log.write(f'Average Order Value: £{average_order_value:.2f}\n')
plt.figure(figsize=(6, 4))
plt.text(0.5, 0.5, f'£{average_order_value:,.2f}', fontsize=48, fontweight='bold', 
         ha='center', va='center', color='seagreen')
plt.axis('off')
plt.title('Average Order Value (AOV)', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('../outputs/average_order_value_big_number.png')


# Top 10 items sold by quantity ##

top_qty = (
    df_sales
    .groupby(['StockCode', 'Description'], as_index=False)
    .agg({
        'Quantity': 'sum',
        'UnitPrice': 'mean'  # Calculates average unit price per product
    })
    .round({'UnitPrice': 2})
    .sort_values(by='Quantity', ascending=False)
    .head(20)
    .reset_index(drop=True)
)
with open('../outputs/sales_analysis.txt', 'a') as log:
    log.write(f"\n🏆 Top 20 Products by Quantity Sold:\n{top_qty}\n")

    item_sales = df_sales.groupby('StockCode')['Quantity'].sum()

# Then, get the overall average across all unique items
average_qty_per_item = item_sales.mean()
with open('../outputs/sales_analysis.txt', 'a') as log:
    log.write(f"\n📦 On average, each item sold {average_qty_per_item:.2f} units across the year.\n")

sns.set(style="whitegrid")
plt.figure(figsize=(10, 8))
ax = sns.barplot(
    data=top_qty,
    y='Description',
    x='Quantity',
    palette='viridis'
)
# Assign unitprice
for i, row in top_qty.iterrows():
    ax.text(
        row['Quantity'] + 500,
        i,                     
        f"£{row['UnitPrice']:.2f}",
        va='center',
        fontsize=9,
        color='black'
    )

plt.title('Top 20 Products by Quantity Sold', fontsize=16)
plt.xlabel('Quantity Sold')
plt.ylabel('Product Description')
plt.tight_layout()
plt.savefig('../outputs/top_20_items_sold_quantity.png')