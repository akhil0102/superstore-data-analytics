# 🌾 Global Food Security & Agricultural Climate Resilience (Societal Data Analytics)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Analytics-150458?style=for-the-badge&logo=pandas)
![UN SDG 2](https://img.shields.io/badge/UN%20SDG-Zero%20Hunger-DDA63A?style=for-the-badge)
![Climate Resilience](https://img.shields.io/badge/Climate-Action-397A4C?style=for-the-badge)

A data analytics project addressing **United Nations Sustainable Development Goal 2 (Zero Hunger)** and **SDG 13 (Climate Action)**. 

This repository analyzes **1,500 records across 25 nations (2000–2025)** to quantify climate impact, severe drought risks, crop yield drops, and global food insecurity vulnerability.

---

## 📌 Project Overview
Climate change and extreme weather events threaten crop productivity and food security worldwide. 

This project investigates:
1. **Crop Yield Resilience**: Assessing how severe droughts affect staple crops (Wheat, Rice, Maize, Soybeans, Potatoes, Cassava).
2. **Climate Vulnerability**: Identifying the top 15 nations most vulnerable to food insecurity.
3. **Rainfall & Temperature Anomalies**: Quantifying the threshold below which rainfall deficits trigger food shortages.
4. **Policy Interventions**: Recommending data-driven agricultural interventions for international aid organizations.

---

## 📊 Key Societal Indicators

```text
================ GLOBAL FOOD SECURITY KPIs ================
Total Nations Analyzed            : 25 Countries
Total Geographic Regions          : 9 Regions
Average Crop Yield                : 10.34 Tonnes / Ha
Global Food Insecurity Index      : 39.7 / 100
Severe Drought Frequency (%)      : 10.1%
High Vulnerability Population (%) : 13.7%
Total Analysis Records (2000-2025): 1,500
===========================================================
```

---

## 🎨 Visual Charts & Analytics

All generated charts are located in `food_charts/`:

| Chart File | Analytical Focus |
| :--- | :--- |
| `food_charts/1_crop_yield_by_region.png` | Regional agricultural productivity ranking |
| `food_charts/2_drought_yield_impact.png` | Comparison of staple crop yields with vs. without drought |
| `food_charts/3_food_insecurity_by_country.png` | Top 15 nations by Food Insecurity Index |
| `food_charts/4_rainfall_vs_insecurity.png` | Scatter plot showing rainfall deficit vs. hunger vulnerability |
| `food_charts/5_risk_distribution_by_region.png` | Stacked risk distribution across global regions |

---

## 📁 Repository Structure

```text
├── Food_Security_Analytics_Notebook.ipynb   # Complete interactive Jupyter Notebook
├── food_security_analysis.py                 # Data processing & KPI script
├── food_security_visualizations.py           # Script generating 5 visual chart PNGs
├── practical_food_demo.py                    # Live terminal execution demo script
├── generate_food_dataset.py                  # Dataset generator script
├── global_food_security.csv                  # Raw dataset (1,500 records x 15 features)
├── food_charts/                              # Directory containing 5 PNG charts
├── food_summaries/                           # Aggregated CSV summary tables
└── README.md                                 # Project documentation
```

---

## 🚀 How to Run locally

### 1. Run Data Processing
```bash
python food_security_analysis.py
```

### 2. Generate Visual Charts
```bash
python food_security_visualizations.py
```

### 3. Run Live Demo
```bash
python practical_food_demo.py
```

---

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).
