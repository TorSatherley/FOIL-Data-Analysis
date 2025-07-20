import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_pickle('../data/sales_level_dataset.pkl')

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

with open('../outputs/deeper-exploration.txt', 'w') as f:
    # Flag cancelled orders
    df['IsCancelled'] = df['InvoiceNo'].astype(str).str.startswith('C')
    # Write cancelled order counts
    print("Cancelled order breakdown:\n", df['IsCancelled'].value_counts(), file=f)
    
    # Calculate revenues
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
    cancelled_revenue = df[df['IsCancelled']]['TotalPrice'].sum()
    total_revenue = df['TotalPrice'].sum()
    percent_cancelled = (cancelled_revenue / total_revenue) * 100
    
    # Write cancelled revenue and percentage
    print(f"\nTotal cancelled revenue: £{cancelled_revenue:,.2f}", file=f)
    print(f"Cancelled orders account for {percent_cancelled:.2f}% of all revenue.", file=f)



# Total and cancelled orders by product
product_cancellation = df.groupby('StockCode').agg(
    total_orders=('InvoiceNo', 'count'),
    cancelled_orders=('IsCancelled', 'sum')
)
product_cancellation['cancel_rate'] = product_cancellation['cancelled_orders'] / product_cancellation['total_orders']
# Sort by highest cancellation rate
product_cancellation = product_cancellation.sort_values(by='cancel_rate', ascending=False)
# Optional: filter to only products with at least 20 orders for statistical relevance
filtered_products = product_cancellation[product_cancellation['total_orders'] >= 20]

# Print cancelled products to txt
with open('../outputs/deeper-exploration.txt', 'a') as log:
    log.write("\nTop 10 Products by Cancellation Rate (min 20 orders):\n")
    log.write(filtered_products.head(10).to_string())
    log.write("\n")

# Total and cancelled orders by country
country_cancellation = df.groupby('Country').agg(
    total_orders=('InvoiceNo', 'count'),
    cancelled_orders=('IsCancelled', 'sum')
)
country_cancellation['cancel_rate'] = country_cancellation['cancelled_orders'] / country_cancellation['total_orders']
country_cancellation = country_cancellation.sort_values(by='cancel_rate', ascending=False)

with open('../outputs/deeper-exploration.txt', 'a') as log:
    log.write("\nTop 10 Countries by Cancellation Rate:\n")
    log.write(country_cancellation.head(10).to_string())
    log.write("\n")

from scipy.stats import chi2_contingency
# Create contingency table: rows = countries, columns = [cancelled, not_cancelled]
contingency = df.groupby('Country')['IsCancelled'].value_counts().unstack(fill_value=0)

chi2, p, dof, expected = chi2_contingency(contingency)

with open('../outputs/deeper-exploration.txt', 'a') as log:
    log.write(f"\nChi-squared test p-value: {p:.4f}\n")


# Top 10 countries by cancellation rate
top_cancel_countries = country_cancellation.head(10).reset_index()

sns.barplot(x='cancel_rate', y='Country', data=top_cancel_countries)
plt.title('Top 10 Countries by Order Cancellation Rate')
plt.xlabel('Cancellation Rate')
plt.ylabel('Country')
plt.tight_layout()
plt.savefig('../outputs/top_10_cancellation_by_country.png')
plt.close()

# Revenue breakdown by country
country_revenue = df.groupby('Country').agg(
    country_revenue=('TotalPrice', 'sum')
)
country_revenue['revenue_pct'] = (country_revenue['country_revenue'] / total_revenue) * 100
country_revenue = country_revenue.sort_values(by='revenue_pct', ascending=False)

with open('../outputs/deeper-exploration.txt', 'a') as log:
    log.write("\nTop 20 Countries by Revenue Percentage:\n")
    log.write(country_revenue.head(20).to_string(formatters={'revenue_pct': '{:.2f}%'.format}))
    log.write("\n")
