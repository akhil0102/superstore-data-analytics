import pandas as pd
import numpy as np
import os

def load_and_clean_food_data(file_path="global_food_security.csv"):
    """
    Loads, cleans, and enriches the Global Food Security dataset.
    """
    print(f"Loading Global Food Security dataset from {file_path}...")
    df = pd.read_csv(file_path)
    
    # 1. Temperature Anomaly (Baseline: 2000-2005 mean per region)
    baseline_temp = df[df['Year'] <= 2005].groupby('Region')['Avg_Temperature_C'].transform('mean')
    df['Temp_Anomaly_C'] = round(df['Avg_Temperature_C'] - baseline_temp, 2)
    
    # 2. Risk Categorization
    df['Insecurity_Risk_Level'] = pd.cut(
        df['Food_Insecurity_Index'], 
        bins=[-0.1, 30, 60, 100], 
        labels=['Low Risk', 'Moderate Risk', 'High Vulnerability']
    )
    
    df['Yield_Category'] = pd.cut(
        df['Crop_Yield_Tonnes_per_Ha'],
        bins=[-0.1, 2.5, 6.0, 100],
        labels=['Low Yield', 'Moderate Yield', 'High Yield']
    )
    
    # 3. Climate Vulnerability Composite Score
    drought_score = np.where(df['Severe_Drought'] == 'Yes', 30, 0)
    temp_score = np.where(df['Temp_Anomaly_C'] > 1.5, 25, 10)
    yield_deficit_score = np.where(df['Yield_Category'] == 'Low Yield', 35, 10)
    
    df['Climate_Vulnerability_Score'] = round(df['Food_Insecurity_Index'] * 0.5 + drought_score * 0.3 + temp_score * 0.2, 1)
    
    print(f"Dataset Loaded & Cleaned Successfully! Shape: {df.shape}")
    return df

def compute_societal_kpis(df):
    """
    Computes key societal metrics for food security & agricultural resilience.
    """
    total_records = len(df)
    total_countries = df['Country'].nunique()
    total_regions = df['Region'].nunique()
    avg_yield = df['Crop_Yield_Tonnes_per_Ha'].mean()
    avg_insecurity_score = df['Food_Insecurity_Index'].mean()
    drought_pct = (df['Severe_Drought'].value_counts(normalize=True).get('Yes', 0)) * 100
    high_risk_pct = (df['Insecurity_Risk_Level'].value_counts(normalize=True).get('High Vulnerability', 0)) * 100
    avg_temp_anomaly = df['Temp_Anomaly_C'].mean()

    kpis = {
        "Total Countries Analyzed": int(total_countries),
        "Total Geographic Regions": int(total_regions),
        "Average Crop Yield (Tonnes/Ha)": round(avg_yield, 2),
        "Global Food Insecurity Index": round(avg_insecurity_score, 1),
        "Severe Drought Frequency (%)": round(drought_pct, 1),
        "High Vulnerability Population (%)": round(high_risk_pct, 1),
        "Avg Temperature Anomaly (°C)": round(avg_temp_anomaly, 2),
        "Total Records (2000-2025)": int(total_records)
    }
    return kpis

def generate_food_summaries(df, output_dir="food_summaries"):
    """
    Exports structured analytical summary CSVs.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Regional Security Summary
    region_summary = df.groupby('Region').agg(
        Avg_Crop_Yield=('Crop_Yield_Tonnes_per_Ha', 'mean'),
        Avg_Food_Insecurity=('Food_Insecurity_Index', 'mean'),
        Drought_Incidents=('Severe_Drought', lambda x: (x == 'Yes').sum()),
        Avg_Rainfall_mm=('Annual_Rainfall_mm', 'mean'),
        Avg_Temp_C=('Avg_Temperature_C', 'mean')
    ).reset_index().sort_values(by='Avg_Food_Insecurity', ascending=False)
    region_summary.to_csv(os.path.join(output_dir, "regional_security_summary.csv"), index=False)

    # 2. Crop Performance & Climate Impact
    crop_summary = df.groupby('Crop_Type').agg(
        Avg_Yield=('Crop_Yield_Tonnes_per_Ha', 'mean'),
        Drought_Yield_Drop_Pct=('Crop_Yield_Tonnes_per_Ha', lambda x: round(
            ((x[df.loc[x.index, 'Severe_Drought'] == 'No'].mean() - x[df.loc[x.index, 'Severe_Drought'] == 'Yes'].mean()) 
             / x[df.loc[x.index, 'Severe_Drought'] == 'No'].mean()) * 100, 1)
        ),
        Avg_Fertilizer=('Fertilizer_Usage_kg_ha', 'mean'),
        Avg_Pesticide=('Pesticide_Usage_kg_ha', 'mean')
    ).reset_index().sort_values(by='Avg_Yield', ascending=False)
    crop_summary.to_csv(os.path.join(output_dir, "crop_climate_summary.csv"), index=False)

    # 3. High Risk / Vulnerable Countries
    country_risk = df.groupby(['Country', 'Region']).agg(
        Avg_Insecurity_Index=('Food_Insecurity_Index', 'mean'),
        Avg_Crop_Yield=('Crop_Yield_Tonnes_per_Ha', 'mean'),
        Drought_Years_Count=('Severe_Drought', lambda x: (x == 'Yes').sum()),
        Climate_Vulnerability=('Climate_Vulnerability_Score', 'mean')
    ).reset_index().sort_values(by='Avg_Insecurity_Index', ascending=False)
    country_risk.to_csv(os.path.join(output_dir, "high_risk_countries.csv"), index=False)

    print(f"Food Security summary tables exported to '{output_dir}/' directory.")
    return region_summary, crop_summary, country_risk

if __name__ == "__main__":
    df = load_and_clean_food_data()
    kpis = compute_societal_kpis(df)
    print("\n================ GLOBAL FOOD SECURITY KPIs ================")
    for k, v in kpis.items():
        print(f"{k:<35}: {v}")
    print("===========================================================\n")
    
    reg, crop, ctry = generate_food_summaries(df)
