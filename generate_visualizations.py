import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from eda_analysis import load_and_clean_data

# Set styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

def create_visualization_suite(df, output_dir="charts"):
    """
    Generates high-resolution EDA plots and saves them to disk.
    """
    os.makedirs(output_dir, exist_ok=True)
    print(f"Generating EDA visual charts in '{output_dir}/'...")
    
    # Chart 1: Monthly Sales & Profit Trend
    plt.figure(figsize=(12, 6))
    monthly = df.groupby('YearMonth').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    monthly['YearMonth_dt'] = pd.to_datetime(monthly['YearMonth'], format='%Y-%m')
    monthly = monthly.sort_values('YearMonth_dt')
    
    plt.plot(monthly['YearMonth'], monthly['Sales'], label='Sales ($)', color='#1f77b4', linewidth=2.5, marker='o')
    plt.plot(monthly['YearMonth'], monthly['Profit'], label='Profit ($)', color='#2ca02c', linewidth=2.5, marker='s')
    
    plt.title('Superstore Revenue & Profit Trend Over Time', fontsize=15, fontweight='bold', pad=15)
    plt.xlabel('Year-Month', fontsize=12, labelpad=10)
    plt.ylabel('Amount ($)', fontsize=12, labelpad=10)
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.legend(fontsize=11, loc='upper left')
    plt.tight_layout()
    chart1_path = os.path.join(output_dir, '1_sales_profit_trend.png')
    plt.savefig(chart1_path, dpi=300)
    plt.close()

    # Chart 2: Profit by Sub-Category (Identifying Loss Makers)
    plt.figure(figsize=(12, 7))
    sub_cat = df.groupby('Sub-Category')['Profit'].sum().sort_values()
    colors = ['#d62728' if x < 0 else '#2ca02c' for x in sub_cat.values]
    
    bars = plt.barh(sub_cat.index, sub_cat.values, color=colors, edgecolor='none')
    plt.axvline(0, color='black', linestyle='--', linewidth=1)
    plt.title('Total Profit / Loss by Product Sub-Category', fontsize=15, fontweight='bold', pad=15)
    plt.xlabel('Total Profit / Loss ($)', fontsize=12, labelpad=10)
    plt.ylabel('Sub-Category', fontsize=12)
    
    # Annotate values
    for bar in bars:
        width = bar.get_width()
        offset = 1500 if width >= 0 else -6000
        plt.text(width + offset, bar.get_y() + bar.get_height()/2, f"${width:,.0f}", 
                 va='center', fontsize=9, fontweight='bold', color='black' if width >= 0 else '#a70000')

    plt.tight_layout()
    chart2_path = os.path.join(output_dir, '2_profit_by_subcategory.png')
    plt.savefig(chart2_path, dpi=300)
    plt.close()

    # Chart 3: Discount vs Profitability Impact
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Discount', y='Profit', data=df, palette='Reds_r', showfliers=False)
    plt.title('Impact of Discount Level on Order Profitability', fontsize=15, fontweight='bold', pad=15)
    plt.xlabel('Discount Rate', fontsize=12, labelpad=10)
    plt.ylabel('Profit per Order ($)', fontsize=12, labelpad=10)
    plt.axhline(0, color='gray', linestyle='--', linewidth=1)
    plt.tight_layout()
    chart3_path = os.path.join(output_dir, '3_discount_vs_profit.png')
    plt.savefig(chart3_path, dpi=300)
    plt.close()

    # Chart 4: Regional & Segment Performance Heatmap
    plt.figure(figsize=(10, 6))
    pivot = df.pivot_table(index='Region', columns='Segment', values='Profit', aggfunc='sum')
    sns.heatmap(pivot, annot=True, fmt=',.0f', cmap='YlGnBu', cbar_kws={'label': 'Total Profit ($)'}, linewidths=1)
    plt.title('Total Profit by Region and Customer Segment', fontsize=15, fontweight='bold', pad=15)
    plt.xlabel('Customer Segment', fontsize=12, labelpad=10)
    plt.ylabel('Region', fontsize=12, labelpad=10)
    plt.tight_layout()
    chart4_path = os.path.join(output_dir, '4_regional_segment_heatmap.png')
    plt.savefig(chart4_path, dpi=300)
    plt.close()

    # Chart 5: Shipping Mode Performance
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    ship_mode = df.groupby('Ship Mode').agg(
        Order_Count=('Order ID', 'nunique'),
        Avg_Days=('Shipping Days', 'mean')
    ).reset_index()

    ax1.pie(ship_mode['Order_Count'], labels=ship_mode['Ship Mode'], autopct='%1.1f%%', 
            colors=['#4c72b0', '#55a868', '#c44e52', '#8172b0'], startangle=140, explode=[0.05]*len(ship_mode))
    ax1.set_title('Order Share by Ship Mode', fontsize=13, fontweight='bold')

    sns.barplot(x='Ship Mode', y='Avg_Days', data=ship_mode, ax=ax2, palette='Blues_d')
    ax2.set_title('Average Shipping Days by Mode', fontsize=13, fontweight='bold')
    ax2.set_ylabel('Average Days', fontsize=11)
    for p in ax2.patches:
        ax2.annotate(f"{p.get_height():.1f} days", (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 5), textcoords='offset points', fontweight='bold')

    plt.tight_layout()
    chart5_path = os.path.join(output_dir, '5_shipping_mode_analysis.png')
    plt.savefig(chart5_path, dpi=300)
    plt.close()

    print(f"All 5 charts successfully generated and saved to '{output_dir}/'!")

if __name__ == "__main__":
    df = load_and_clean_data()
    create_visualization_suite(df)
