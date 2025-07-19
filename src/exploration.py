import pandas as pd

# load the data into pandas dataframe
df = pd.read_excel('../data/Online Retail.xlsx', engine='openpyxl')
print('data loaded!')

# explore the data to see which cleaning methods might be needed
print("Initial data shape:", df.shape)
print("\nMissing values per column:\n", df.isnull().sum())
print("\nData types:\n", df.dtypes)
print("\nSample data:\n", df.head())

# look at how many orders were cancelled 
df['IsCancelled'] = df['InvoiceNo'].astype(str).str.startswith('C')
print("Cancelled order breakdown:\n", df['IsCancelled'].value_counts())
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']
cancelled_revenue = df[df['IsCancelled']]['TotalPrice'].sum()
print(f"\nTotal cancelled revenue: £{cancelled_revenue:,.2f}")
total_revenue = df['TotalPrice'].sum()
percent_cancelled = (cancelled_revenue / total_revenue) * 100
print(f"Cancelled orders account for {percent_cancelled:.2f}% of all revenue.")


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


# Total and cancelled orders by country
country_cancellation = df.groupby('Country').agg(
    total_orders=('InvoiceNo', 'count'),
    cancelled_orders=('IsCancelled', 'sum')
)
country_cancellation['cancel_rate'] = country_cancellation['cancelled_orders'] / country_cancellation['total_orders']
country_cancellation = country_cancellation.sort_values(by='cancel_rate', ascending=False)


from scipy.stats import chi2_contingency
# Create contingency table: rows = countries, columns = [cancelled, not_cancelled]
contingency = df.groupby('Country')['IsCancelled'].value_counts().unstack(fill_value=0)

chi2, p, dof, expected = chi2_contingency(contingency)

print(f"Chi-squared test p-value: {p:.4f}")


import seaborn as sns
import matplotlib.pyplot as plt

# Top 10 countries by cancellation rate
top_cancel_countries = country_cancellation.head(10).reset_index()

sns.barplot(x='cancel_rate', y='Country', data=top_cancel_countries)
plt.title('Top 10 Countries by Order Cancellation Rate')
plt.xlabel('Cancellation Rate')
plt.ylabel('Country')
plt.tight_layout()
plt.show()
