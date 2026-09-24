import pandas as pd
import numpy as np

# Load dataset
df = pd.read_csv('global_food_security.csv')

print("="*65)
print("SOCIETAL ANALYTICS DEMO: GLOBAL FOOD SECURITY & CROP RESILIENCE")
print("="*65)
print(f"Total Transactions / Records : {len(df)}")
print(f"Countries Analyzed          : {df['Country'].nunique()}")
print(f"Timeframe                   : {df['Year'].min()} - {df['Year'].max()}")

print("\n" + "="*65)
print("PRACTICAL EXERCISE 1: TOP 5 MOST FOOD INSECURE NATIONS")
print("="*65)
vulnerable = df.groupby(['Country', 'Region'])['Food_Insecurity_Index'].mean().sort_values(ascending=False).head(5)
for (country, region), index_val in vulnerable.items():
    print(f"  * {country:<20} ({region:<20}) : Risk Index = {index_val:.1f} / 100")

print("\n" + "="*65)
print("PRACTICAL EXERCISE 2: DROUGHT IMPACT ON CROP YIELDS (TONNES/HA)")
print("="*65)
drought_impact = df.groupby(['Crop_Type', 'Severe_Drought'])['Crop_Yield_Tonnes_per_Ha'].mean().unstack()
drought_impact['Yield_Drop_%'] = round(((drought_impact['No'] - drought_impact['Yes']) / drought_impact['No']) * 100, 1)
print(drought_impact.to_string())

print("\n" + "="*65)
print("PRACTICAL EXERCISE 3: REGIONAL AGRICULTURAL PERFORMANCE")
print("="*65)
reg_perf = df.groupby('Region').agg(
    Avg_Yield=('Crop_Yield_Tonnes_per_Ha', 'mean'),
    Avg_Insecurity=('Food_Insecurity_Index', 'mean'),
    Drought_Years=('Severe_Drought', lambda x: (x == 'Yes').sum())
).sort_values(by='Avg_Insecurity', ascending=False)
print(reg_perf.to_string())
print("="*65)
