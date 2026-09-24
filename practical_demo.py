import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv('superstore_dataset.csv')

print("="*60)
print("PRACTICAL EXERCISE 1: DATA INSPECTION")
print("="*60)
print(f"Total Rows (Transactions) : {df.shape[0]}")
print(f"Total Columns (Features)  : {df.shape[1]}")
print("\nFirst 3 transactions:")
print(df[['Order ID', 'Category', 'Sub-Category', 'Sales', 'Discount', 'Profit']].head(3).to_string(index=False))

print("\n" + "="*60)
print("PRACTICAL EXERCISE 2: PROFITABLE VS LOSS-MAKING PRODUCTS")
print("="*60)
top_profit = df.groupby('Product Name')['Profit'].sum().nlargest(3)
top_loss = df.groupby('Product Name')['Profit'].sum().nsmallest(3)

print("Top 3 Most Profitable Individual Products:")
for name, val in top_profit.items():
    print(f"  * {name[:50]:<50} : +${val:,.2f}")

print("\nTop 3 Highest Loss-Making Products:")
for name, val in top_loss.items():
    print(f"  * {name[:50]:<50} : -${abs(val):,.2f}")

print("\n" + "="*60)
print("PRACTICAL EXERCISE 3: PROVING THE DISCOUNT LOSS")
print("="*60)
high_disc = df[df['Discount'] > 0.20]
total_high_disc_loss = high_disc['Profit'].sum()
avg_loss_per_order = high_disc['Profit'].mean()

print(f"Total orders with >20% Discount  : {len(high_disc)}")
print(f"Total Net Financial Loss        : -${abs(total_high_disc_loss):,.2f}")
print(f"Average Loss Per Order          : -${abs(avg_loss_per_order):,.2f}")

print("\n" + "="*60)
print("PRACTICAL EXERCISE 4: CUSTOMER REVENUE RANKING")
print("="*60)
top_customers = df.groupby('Customer Name').agg(
    Total_Spent=('Sales', 'sum'),
    Total_Profit=('Profit', 'sum'),
    Total_Orders=('Order ID', 'nunique')
).sort_values(by='Total_Spent', ascending=False).head(3)

print("Top 3 High-Value Customers:")
print(top_customers.to_string())
print("="*60)
