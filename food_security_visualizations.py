import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from food_security_analysis import load_and_clean_food_data

# Set styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

def create_food_visualizations(df, output_dir="food_charts"):
    """
    Generates 5 publication-quality societal analytics charts.
    """
    os.makedirs(output_dir, exist_ok=True)
    print(f"Generating Food Security visual charts in '{output_dir}/'...")

    # Chart 1: Average Crop Yield by Region
    plt.figure(figsize=(11, 6))
    region_yield = df.groupby('Region')['Crop_Yield_Tonnes_per_Ha'].mean().sort_values(ascending=False)
    sns.barplot(x=region_yield.values, y=region_yield.index, palette='Greens_r', hue=region_yield.index, legend=False)
    plt.title('Global Agricultural Productivity: Avg Crop Yield by Region (Tonnes/Ha)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Average Yield (Tonnes / Hectare)', fontsize=11)
    plt.ylabel('Geographic Region', fontsize=11)
    
    for i, v in enumerate(region_yield.values):
        plt.text(v + 0.1, i, f"{v:.2f} t/ha", va='center', fontsize=9, fontweight='bold')

    plt.tight_layout()
    chart1_path = os.path.join(output_dir, '1_crop_yield_by_region.png')
    plt.savefig(chart1_path, dpi=300)
    plt.close()

    # Chart 2: Severe Drought Impact on Crop Yields
    plt.figure(figsize=(11, 6))
    sns.barplot(x='Crop_Type', y='Crop_Yield_Tonnes_per_Ha', hue='Severe_Drought', data=df, palette=['#2ca02c', '#d62728'])
    plt.title('Impact of Severe Drought on Crop Yields across Staple Crops', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Staple Crop Type', fontsize=11)
    plt.ylabel('Crop Yield (Tonnes / Hectare)', fontsize=11)
    plt.legend(title='Severe Drought Event', frameon=True)
    plt.tight_layout()
    chart2_path = os.path.join(output_dir, '2_drought_yield_impact.png')
    plt.savefig(chart2_path, dpi=300)
    plt.close()

    # Chart 3: Top Vulnerable Countries (Food Insecurity Index)
    plt.figure(figsize=(11, 7))
    country_risk = df.groupby('Country')['Food_Insecurity_Index'].mean().sort_values(ascending=False).head(15)
    colors = ['#d62728' if v > 50 else '#ff7f0e' for v in country_risk.values]
    
    plt.barh(country_risk.index[::-1], country_risk.values[::-1], color=colors[::-1])
    plt.axvline(50, color='red', linestyle='--', label='High Risk Threshold (Index > 50)')
    plt.title('Top 15 Most Vulnerable Nations by Food Insecurity Index', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Food Insecurity Risk Index (Higher = More Vulnerable)', fontsize=11)
    plt.ylabel('Country', fontsize=11)
    plt.legend(loc='lower right')
    plt.tight_layout()
    chart3_path = os.path.join(output_dir, '3_food_insecurity_by_country.png')
    plt.savefig(chart3_path, dpi=300)
    plt.close()

    # Chart 4: Annual Rainfall vs Crop Yield
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Annual_Rainfall_mm', y='Food_Insecurity_Index', hue='Severe_Drought', style='Severe_Drought', data=df, palette={'Yes': '#d62728', 'No': '#1f77b4'}, alpha=0.7)
    plt.title('Annual Rainfall (mm) vs. Food Insecurity Risk Index', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Annual Rainfall (mm)', fontsize=11)
    plt.ylabel('Food Insecurity Index (1-100)', fontsize=11)
    plt.axvline(450, color='gray', linestyle=':', label='Low Rainfall Threshold (< 450mm)')
    plt.legend(title='Drought Event')
    plt.tight_layout()
    chart4_path = os.path.join(output_dir, '4_rainfall_vs_insecurity.png')
    plt.savefig(chart4_path, dpi=300)
    plt.close()

    # Chart 5: Food Insecurity Risk Level Distribution by Region
    plt.figure(figsize=(12, 6))
    pivot = pd.crosstab(df['Region'], df['Insecurity_Risk_Level'], normalize='index') * 100
    pivot.plot(kind='bar', stacked=True, color=['#2ca02c', '#ff7f0e', '#d62728'], figsize=(12, 6), edgecolor='white')
    plt.title('Food Insecurity Risk Distribution Across Global Regions (%)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Region', fontsize=11)
    plt.ylabel('Percentage of Sample (%)', fontsize=11)
    plt.xticks(rotation=45, ha='right')
    plt.legend(title='Risk Level', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    chart5_path = os.path.join(output_dir, '5_risk_distribution_by_region.png')
    plt.savefig(chart5_path, dpi=300)
    plt.close()

    print(f"All 5 Food Security charts successfully generated in '{output_dir}/'!")

if __name__ == "__main__":
    df = load_and_clean_food_data()
    create_food_visualizations(df)
