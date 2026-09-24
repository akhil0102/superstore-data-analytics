import pandas as pd
import numpy as np
import os

def load_and_clean_data(file_path="superstore_dataset.csv"):
    """
    Loads, cleans, and enriches the Superstore dataset.
    """
    print(f"Loading dataset from {file_path}...")
    df = pd.read_csv(file_path)
    
    # 1. Date Conversion
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='mixed', errors='coerce')
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='mixed', errors='coerce')
    
    # 2. Time & Duration Features
    df['Shipping Days'] = (df['Ship Date'] - df['Order Date']).dt.days
    df['Order Year'] = df['Order Date'].dt.year
    df['Order Month'] = df['Order Date'].dt.month
    df['YearMonth'] = df['Order Date'].dt.to_period('M').astype(str)
    
    # 3. Financial Metrics
    df['Profit Margin (%)'] = np.where(df['Sales'] > 0, (df['Profit'] / df['Sales']) * 100, 0)
    df['Unit Price'] = np.where(df['Quantity'] > 0, df['Sales'] / df['Quantity'], 0)
    df['Is Profit Loss'] = df['Profit'] < 0
    
    # 4. Cleaning
    df['Postal Code'] = df['Postal Code'].fillna('Unknown').astype(str)
    
    print(f"Dataset Loaded Successfully! Shape: {df.shape}")
    return df

def compute_executive_kpis(df):
    """
    Computes top-level business KPIs.
    """
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    total_quantity = df['Quantity'].sum()
    total_orders = df['Order ID'].nunique()
    total_customers = df['Customer ID'].nunique()
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0
    profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
    avg_ship_days = df['Shipping Days'].mean()
    loss_orders_count = df[df['Is Profit Loss']]['Order ID'].nunique()

    kpis = {
        "Total Revenue ($)": round(total_sales, 2),
        "Total Profit ($)": round(total_profit, 2),
        "Overall Profit Margin (%)": round(profit_margin, 2),
        "Total Units Sold": int(total_quantity),
        "Total Orders": int(total_orders),
        "Total Unique Customers": int(total_customers),
        "Average Order Value ($)": round(avg_order_value, 2),
        "Average Shipping Time (Days)": round(avg_ship_days, 1),
        "Loss-Making Orders": int(loss_orders_count)
    }
    return kpis

def generate_summary_tables(df, output_dir="data_summaries"):
    """
    Generates structured aggregation tables for category, region, discount, and month.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Category Performance
    cat_summary = df.groupby(['Category', 'Sub-Category']).agg(
        Total_Sales=('Sales', 'sum'),
        Total_Profit=('Profit', 'sum'),
        Total_Quantity=('Quantity', 'sum'),
        Avg_Discount=('Discount', 'mean'),
        Profit_Margin_Pct=('Profit Margin (%)', 'mean')
    ).reset_index().sort_values(by='Total_Sales', ascending=False)
    cat_summary.to_csv(os.path.join(output_dir, "category_summary.csv"), index=False)
    
    # Regional Performance
    region_summary = df.groupby(['Region', 'Segment']).agg(
        Total_Sales=('Sales', 'sum'),
        Total_Profit=('Profit', 'sum'),
        Total_Orders=('Order ID', 'nunique'),
        Avg_Profit_Margin=('Profit Margin (%)', 'mean')
    ).reset_index().sort_values(by='Total_Sales', ascending=False)
    region_summary.to_csv(os.path.join(output_dir, "region_summary.csv"), index=False)
    
    # Monthly Sales & Profit Trend
    monthly_summary = df.groupby('YearMonth').agg(
        Total_Sales=('Sales', 'sum'),
        Total_Profit=('Profit', 'sum'),
        Order_Count=('Order ID', 'nunique')
    ).reset_index().sort_values(by='YearMonth')
    monthly_summary.to_csv(os.path.join(output_dir, "monthly_summary.csv"), index=False)
    
    # Discount Impact Analysis
    discount_summary = df.groupby(pd.cut(df['Discount'], bins=[-0.01, 0, 0.2, 0.4, 0.6, 1.0], labels=['0%', '1-20%', '21-40%', '41-60%', '>60%'])).agg(
        Order_Count=('Row ID', 'count'),
        Total_Sales=('Sales', 'sum'),
        Total_Profit=('Profit', 'sum'),
        Avg_Profit_Margin=('Profit Margin (%)', 'mean')
    ).reset_index()
    discount_summary.to_csv(os.path.join(output_dir, "discount_impact_summary.csv"), index=False)

    print(f"Summary tables exported to '{output_dir}/' directory.")
    return cat_summary, region_summary, monthly_summary, discount_summary

if __name__ == "__main__":
    df = load_and_clean_data()
    kpis = compute_executive_kpis(df)
    print("\n================ EXECUTIVE KPIs ================")
    for k, v in kpis.items():
        print(f"{k:<30}: {v}")
    print("================================================\n")
    
    cat, reg, month, disc = generate_summary_tables(df)
