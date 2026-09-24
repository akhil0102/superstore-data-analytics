import pandas as pd
import numpy as np

def generate_global_food_security_dataset(output_file="global_food_security.csv", num_rows=1500, seed=42):
    """
    Generates a realistic, rich dataset for Global Food Security & Agricultural Production (2000 - 2025).
    """
    np.random.seed(seed)
    
    countries = [
        "India", "China", "United States", "Brazil", "Nigeria", "Indonesia", 
        "Pakistan", "Bangladesh", "Ethiopia", "Egypt", "Vietnam", "Kenya", 
        "Ukraine", "Argentina", "Mexico", "South Africa", "Turkey", "France", 
        "Germany", "Canada", "Australia", "Thailand", "Sudan", "Tanzania", "Uganda"
    ]
    
    regions = {
        "India": "South Asia", "China": "East Asia", "United States": "North America", 
        "Brazil": "South America", "Nigeria": "Sub-Saharan Africa", "Indonesia": "Southeast Asia", 
        "Pakistan": "South Asia", "Bangladesh": "South Asia", "Ethiopia": "Sub-Saharan Africa", 
        "Egypt": "Middle East & North Africa", "Vietnam": "Southeast Asia", "Kenya": "Sub-Saharan Africa", 
        "Ukraine": "Europe", "Argentina": "South America", "Mexico": "North America", 
        "South Africa": "Sub-Saharan Africa", "Turkey": "Middle East & North Africa", "France": "Europe", 
        "Germany": "Europe", "Canada": "North America", "Australia": "Oceania", 
        "Thailand": "Southeast Asia", "Sudan": "Sub-Saharan Africa", "Tanzania": "Sub-Saharan Africa", 
        "Uganda": "Sub-Saharan Africa"
    }
    
    crops = ["Wheat", "Rice", "Maize (Corn)", "Soybeans", "Potatoes", "Cassava"]
    years = list(range(2000, 2026))
    
    data = []
    
    for _ in range(num_rows):
        country = np.random.choice(countries)
        region = regions[country]
        crop = np.random.choice(crops)
        year = np.random.choice(years)
        
        # Base environmental factors
        base_temp = 14.0 if region in ["Europe", "North America"] else (26.0 if region == "Sub-Saharan Africa" else 22.0)
        temp = round(base_temp + np.random.normal(0, 1.8) + (year - 2000) * 0.04, 2)  # Global warming trend
        
        base_rainfall = 600 if region == "Middle East & North Africa" else (1400 if region == "Southeast Asia" else 950)
        rainfall = round(max(150, base_rainfall + np.random.normal(0, 250)), 1)
        
        drought = "Yes" if rainfall < 450 or (temp > base_temp + 2.5 and np.random.rand() > 0.6) else "No"
        
        # Agricultural inputs
        pesticide = round(max(0.2, np.random.gamma(2.5, 1.2)), 2)
        fertilizer = round(max(10, np.random.gamma(5.0, 20.0)), 1)
        
        # Crop Yield Calculation (Tonnes / Hectare)
        crop_base_yield = {"Wheat": 3.8, "Rice": 4.2, "Maize (Corn)": 5.5, "Soybeans": 2.8, "Potatoes": 22.0, "Cassava": 14.0}
        yield_val = crop_base_yield[crop]
        
        # Adjust yield based on climate & inputs
        if drought == "Yes":
            yield_val *= np.random.uniform(0.45, 0.75) # 25-55% drop during drought
        if temp > base_temp + 3.0:
            yield_val *= 0.85
            
        yield_val += (fertilizer * 0.015) + (pesticide * 0.1) + np.random.normal(0, 0.3)
        yield_val = round(max(0.5, yield_val), 2)
        
        # Food Insecurity Risk Index (1 to 100)
        # Higher score = more vulnerable/insecure
        poverty_factor = 45 if region == "Sub-Saharan Africa" else (30 if region in ["South Asia", "Middle East & North Africa"] else 12)
        yield_impact = (1.0 / (yield_val / crop_base_yield[crop])) * 15
        drought_impact = 20 if drought == "Yes" else 0
        
        food_insecurity_index = round(min(98.0, max(5.0, poverty_factor + yield_impact + drought_impact + np.random.normal(0, 5))), 1)
        
        data.append({
            "Country": country,
            "Region": region,
            "Year": year,
            "Crop_Type": crop,
            "Crop_Yield_Tonnes_per_Ha": yield_val,
            "Avg_Temperature_C": temp,
            "Annual_Rainfall_mm": rainfall,
            "Severe_Drought": drought,
            "Fertilizer_Usage_kg_ha": fertilizer,
            "Pesticide_Usage_kg_ha": pesticide,
            "Food_Insecurity_Index": food_insecurity_index
        })
        
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    print(f"Dataset generated successfully! File: {output_file}, Rows: {len(df)}")
    return df

if __name__ == "__main__":
    generate_global_food_security_dataset()
