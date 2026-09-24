# 📊 Superstore Sales & Profitability Analytics (Kaggle EDA Project)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-3.0-150458?style=for-the-badge&logo=pandas)
![Seaborn](https://img.shields.io/badge/Seaborn-Visualization-3776AB?style=for-the-badge)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter)

An end-to-end **Exploratory Data Analysis (EDA)** and **Business Intelligence** project investigating 4 years of retail transactions (9,994 records) from the benchmark **Kaggle Sample Superstore Dataset**.

---

## 📌 Project Overview
Retail businesses often focus heavily on revenue growth while masking underlying profit erosion caused by unmonitored promotional discounting and freight costs. 

This analytics project investigates:
1. **Financial Performance**: Historical sales vs. profit trends across regions and categories.
2. **Product Profitability**: Identifying high-margin copiers vs. loss-making tables & bookcases.
3. **The Discount Trap**: Quantifying how discounts >20% cause negative profit margins.
4. **Logistics**: Evaluating shipping modes and transit times.

---

## 📊 Key Business Findings & KPIs

```text
================ EXECUTIVE KPIs ================
Total Revenue                 : $2,297,200.86
Total Net Profit              : $286,397.02
Overall Profit Margin (%)     : 12.47%
Total Orders                  : 5,009
Total Unique Customers        : 793
Average Order Value           : $458.61
Loss-Making Orders            : 1,318 (26.3% of orders)
================================================
```

### 1. The Discount Trap (Impact of Discount Level on Profit)
> **Key Finding**: Discounts over **20%** consistently cause net financial losses!
- **0% Discount**: Average Profit per Order = **+$66.90**
- **1–20% Discount**: Average Profit per Order = **+$24.10**
- **21–40% Discount**: Average Profit per Order = **-$47.30** (Loss)
- **>60% Discount**: Average Profit per Order = **-$103.50** (Heavy Loss)

### 2. Product Profitability Ranking
- 🏆 **Top Winner**: **Copiers** (+$55,617.82 Net Profit | 37.4% Margin)
- 🔴 **Biggest Loss Driver**: **Tables** (-$17,725.48 Net Loss | -8.6% Margin)

---

## 🎨 Visual Charts Preview

All generated plots are stored in the `charts/` directory:

| Chart | Focus |
| :--- | :--- |
| `charts/1_sales_profit_trend.png` | Monthly revenue vs. profit trends over 4 years |
| `charts/2_profit_by_subcategory.png` | Ranking of 17 product sub-categories by net profit/loss |
| `charts/3_discount_vs_profit.png` | Seaborn boxplot illustrating profit erosion by discount rate |
| `charts/4_regional_segment_heatmap.png` | Profitability matrix across 4 US regions and 3 customer segments |
| `charts/5_shipping_mode_analysis.png` | Distribution of order fulfillment modes and transit days |

---

## 📁 Repository Structure

```text
├── Superstore_EDA_Notebook.ipynb   # Complete interactive Jupyter Notebook
├── eda_analysis.py                  # Core data cleaning & KPI computation script
├── generate_visualizations.py       # Script generating 5 visual chart PNGs
├── practical_demo.py                # Live hands-on practical exercise script
├── superstore_dataset.csv           # Raw dataset (9,994 rows x 21 features)
├── charts/                          # Directory containing exported visual PNG plots
├── data_summaries/                  # Aggregated CSV summaries (Category, Region, Discount)
├── README.md                        # Project documentation
└── .gitignore                       # Git ignore rules
```

---

## 🚀 How to Run locally

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/superstore-data-analytics.git
cd superstore-data-analytics
```

### 2. Install dependencies
```bash
pip install pandas numpy matplotlib seaborn openpyxl
```

### 3. Run Analysis & Scripts
```bash
# Run data analysis & generate summary CSVs
python eda_analysis.py

# Generate chart visual PNGs
python generate_visualizations.py

# Run interactive practical exercises
python practical_demo.py
```

---

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).
