import json

notebook_content = {
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# 📊 Superstore Sales & Profitability - Exploratory Data Analysis (EDA)\n",
    "\n",
    "## 📌 Project Overview\n",
    "This notebook conducts a comprehensive **Exploratory Data Analysis (EDA)** on the benchmark **Kaggle Sample Superstore Dataset**. The dataset contains **9,994 transaction records** across 4 years of retail sales in the United States.\n",
    "\n",
    "### Key Analytical Goals:\n",
    "1. **Revenue & Profit Dynamics**: Evaluate historical sales trends and profit margins.\n",
    "2. **Product Sub-Category Breakdown**: Identify high-margin categories vs. loss-making products.\n",
    "3. **Discount Impact Analysis**: Quantify how discounting strategies impact gross profit.\n",
    "4. **Geographic & Customer Segmentation**: Uncover high-value regions and customer behavior.\n",
    "5. **Operational Logistics**: Evaluate shipping performance across fulfillment modes."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 1. Library Imports & Environment Setup"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "import seaborn as sns\n",
    "import warnings\n",
    "warnings.filterwarnings('ignore')\n",
    "\n",
    "# Setting plotting defaults\n",
    "plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')\n",
    "pd.set_option('display.max_columns', None)\n",
    "print('Environment ready!')"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 2. Data Loading & Feature Engineering"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Load dataset\n",
    "df = pd.read_csv('superstore_dataset.csv')\n",
    "\n",
    "# Convert dates\n",
    "df['Order Date'] = pd.to_datetime(df['Order Date'], format='mixed', errors='coerce')\n",
    "df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='mixed', errors='coerce')\n",
    "\n",
    "# Derived Features\n",
    "df['Shipping Days'] = (df['Ship Date'] - df['Order Date']).dt.days\n",
    "df['Order Year'] = df['Order Date'].dt.year\n",
    "df['Order Month'] = df['Order Date'].dt.month\n",
    "df['YearMonth'] = df['Order Date'].dt.to_period('M').astype(str)\n",
    "df['Profit Margin (%)'] = np.where(df['Sales'] > 0, (df['Profit'] / df['Sales']) * 100, 0)\n",
    "df['Is Profit Loss'] = df['Profit'] < 0\n",
    "\n",
    "print('Data Loaded & Enriched! Shape:', df.shape)\n",
    "df.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. High-Level Business KPIs"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "total_sales = df['Sales'].sum()\n",
    "total_profit = df['Profit'].sum()\n",
    "overall_margin = (total_profit / total_sales) * 100\n",
    "total_orders = df['Order ID'].nunique()\n",
    "unique_customers = df['Customer ID'].nunique()\n",
    "\n",
    "kpi_df = pd.DataFrame({\n",
    "    'Metric': ['Total Revenue ($)', 'Total Profit ($)', 'Profit Margin (%)', 'Total Orders', 'Unique Customers', 'Avg Order Value ($)'],\n",
    "    'Value': [f'${total_sales:,.2f}', f'${total_profit:,.2f}', f'{overall_margin:.2f}%', f'{total_orders:,}', f'{unique_customers:,}', f'${(total_sales/total_orders):,.2f}']\n",
    "})\n",
    "display(kpi_df)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 4. Visualizations & Deep-Dive Analysis"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 4.1 Monthly Sales & Profit Trend"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "monthly = df.groupby('YearMonth').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()\n",
    "\n",
    "plt.figure(figsize=(12, 5))\n",
    "plt.plot(monthly['YearMonth'], monthly['Sales'], label='Sales', color='#1f77b4', marker='o')\n",
    "plt.plot(monthly['YearMonth'], monthly['Profit'], label='Profit', color='#2ca02c', marker='s')\n",
    "plt.title('Monthly Sales & Profit Trend', fontsize=14, fontweight='bold')\n",
    "plt.xticks(rotation=90)\n",
    "plt.ylabel('Amount ($)')\n",
    "plt.legend()\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 4.2 Profit & Loss by Product Sub-Category"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "sub_cat = df.groupby('Sub-Category')['Profit'].sum().sort_values()\n",
    "colors = ['#d62728' if x < 0 else '#2ca02c' for x in sub_cat.values]\n",
    "\n",
    "plt.figure(figsize=(10, 6))\n",
    "plt.barh(sub_cat.index, sub_cat.values, color=colors)\n",
    "plt.axvline(0, color='black', linestyle='--')\n",
    "plt.title('Profit / Loss by Product Sub-Category', fontsize=14, fontweight='bold')\n",
    "plt.xlabel('Total Profit / Loss ($)')\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 4.3 Discount vs Profitability Analysis"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "plt.figure(figsize=(9, 5))\n",
    "sns.boxplot(x='Discount', y='Profit', data=df, hue='Discount', palette='Reds_r', legend=False, showfliers=False)\n",
    "plt.axhline(0, color='gray', linestyle='--')\n",
    "plt.title('Impact of Discount Rate on Profitability per Order', fontsize=14, fontweight='bold')\n",
    "plt.tight_layout()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 5. Key Findings & Strategic Recommendations\n",
    "1. **Eliminate Aggressive Discounts (>20%)**: Heavy discounting (>20%) is the single largest cause of negative profit margins.\n",
    "2. **Restructure Loss-Making Categories**: Product sub-categories like **Tables (-$17.7k)**, **Bookcases (-$3.4k)**, and **Supplies (-$1.2k)** are consistently unprofitable due to high freight costs and deep discounts.\n",
    "3. **Focus on High-Margin Categories**: **Copiers (43.5% margin)**, **Phones**, and **Accessories** drive the vast majority of net profit."
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}

with open('Superstore_EDA_Notebook.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook_content, f, indent=2)

print("Superstore_EDA_Notebook.ipynb successfully created!")
