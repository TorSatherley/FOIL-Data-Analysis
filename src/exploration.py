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