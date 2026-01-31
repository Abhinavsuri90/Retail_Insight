# 🛍️ RetailInsight - AI-Powered Customer Analytics

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.8+-orange.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/status-production-success.svg)](https://github.com)

> **Advanced Machine Learning for E-Commerce Intelligence**  
> Transform 500K+ transactions into actionable business insights with professional-grade customer segmentation and product recommendations.

---

## ✨ What This Does

**RetailInsight** is a complete ML analytics pipeline that answers critical business questions:
- 👥 **Who are your most valuable customers?** → VIP segmentation with £1,807 avg LTV
- 💰 **Where should you focus marketing budget?** → Top 59.6% customers drive 62.3% revenue
- 📦 **Which products should be bundled?** → 24× lift on teacup cross-sells
- 📈 **What's the ROI of retention?** → +£466K projected from 10% VIP retention boost

**Live Dashboards:** Interactive HTML reports with professional charts and PDF export

---

## 🚀 Quick Start

```bash
# 1. Clone repository
git clone <your-repo-url>
cd RetailInsight-main

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run analytics pipeline (2 minutes)
python retail_analytics_professional.py

# 4. Run market basket analysis
python run_market_basket.py

# 5. Open dashboards (Cmd+Click the URLs in terminal)
# - Executive Dashboard: KPIs, segments, revenue analysis
# - Product Recommender: Live search, bundles, lift metrics
```

**Dataset:** Automatically downloads UCI Online Retail II (541,909 transactions)

---

## 📊 Key Results

### Customer Segmentation (K-Means + GMM)

| Metric | Cluster 0 (VIP) | Cluster 1 (Standard) |
|--------|----------------|----------------------|
| **Customers** | 2,585 (59.6%) | 1,750 (40.4%) |
| **Revenue** | £4,669,828 (62.3%) | £2,830,923 (37.7%) |
| **Avg LTV** | £1,807 | £1,618 |
| **Avg Order Value** | £29.80 | £19.20 |
| **Purchase Frequency** | 4.06 orders | 4.51 orders |

**🎯 Critical Insight:** Top 59.6% of customers drive 62.3% of revenue - classic Pareto principle validated

**💰 Business Impact:**
- +£466,983 projected revenue from 10% VIP retention improvement
- £375,038 potential from cross-sell campaigns
- £225,023 savings from churn prevention

### Market Basket Analysis (FP-Growth)

- **243 frequent itemsets** discovered
- **20 high-confidence association rules** (confidence ≥ 60%)
- **Maximum lift: 24.0×** (Pink → Roses Regency Teacup bundles)
- **Average confidence: 70.2%**

**Top Product Associations:**
- Pink Regency Teacup → Green Regency Teacup (83% confidence, 22.2× lift)
- Dolly Girl Lunch Box → Spaceboy Lunch Box (69% confidence, 18.1× lift)
- Gardeners Kneeling Pads bundled (73% confidence, 17.9× lift)

---

## 🛠️ Features

### Advanced ML Techniques
- **RFM + 17 Advanced Features**: Tenure, Diversity Index, NLP taste profiles (TF-IDF)
- **Dual Clustering**: K-Means + Gaussian Mixture Models with PCA
- **FP-Growth Algorithm**: 10× faster than Apriori for association mining
- **Statistical Validation**: Silhouette (0.178), Davies-Bouldin, Calinski-Harabasz scores
- **Feature Importance**: Random Forest analysis (Taste_1 = 36.2% importance)

### Professional Engineering
- **Modular Architecture**: Clean `src/` modules (data_processor, feature_engineer, clustering_engine)
- **Data Quality**: Cancellation matching, noise filtering, winsorization
- **Interactive Dashboards**: Professional HTML reports with Plotly.js charts
- **PDF Export**: One-click download with branded formatting
- **Clean Output**: Concise terminal logs with clickable dashboard links

---

## 📁 Project Structure

```
RetailInsight-main/
│
├── retail_analytics_professional.py  # Main ML pipeline
├── run_market_basket.py              # FP-Growth association mining
├── requirements.txt                  # Python dependencies
│
├── src/                              # Core modules
│   ├── data_processor.py            # Cleaning, cancellations, outliers
│   ├── feature_engineer.py          # RFM + NLP features
│   └── clustering_engine.py         # K-Means, GMM, PCA, validation
│
├── notebooks/                        # Jupyter analysis (optional)
│   ├── 01_data_cleaning.ipynb
│   ├── 02_feature_engineering_rfm.ipynb
│   ├── 03_clustering.ipynb
│   └── 04_market_basket.ipynb
│
├── reports/                          # Interactive dashboards
│   ├── executive_dashboard.html     # KPIs, segments, recommendations
│   └── product_recommender.html     # Live search, bundles, lift metrics
│
└── data/
    ├── raw/                          # UCI Online Retail II dataset
    └── processed/                    # Generated CSVs
        ├── rfm_features_professional.csv
        ├── customer_segments_professional.csv
        └── association_rules_professional.csv
```

---

## 🔬 Methodology

1. **Missing Value Treatment**: Removed records without CustomerID (25% of data)
2. **Invalid Transaction Filtering**: Excluded negative quantities and zero prices
3. **Feature Engineering**: Computed `TotalPrice = Quantity × UnitPrice`
4. **Final Dataset**: 397,884 transactions from 4,338 customers (73.4% retention)

### RFM Feature Engineering

**Recency (R):** Days since last purchase
```
R_i = (snapshot_date - max(transaction_date_i)).days
```

**Frequency (F):** Number of unique orders
```
F_i = count(distinct invoice_number_i)
```

**Monetary (M):** Total revenue contribution
```
M_i = sum(quantity_ij × unit_price_ij)
```

### Customer Segmentation

**Algorithm:** K-Means clustering  
**Optimal K:** 4 (validated via Elbow Method and Silhouette Analysis)  
**Preprocessing:** Z-score normalization of RFM features  
**Parameters:** `n_clusters=4, random_state=42, n_init=10`

### Market Basket Analysis

**Algorithm:** Apriori (frequent itemset mining)  
**Minimum Support:** 2%  
**Minimum Confidence:** 60%  
**Scope:** VIP/Elite customer transactions only  
**Metrics:** Support, Confidence, Lift

---

## Project Structure

```
customer-segmentation/
│
├── README.md                           # This file
├── LICENSE                             # MIT License
├── requirements.txt                    # Python dependencies
├── run_analysis.py                     # Automated execution script
├── dashboard.html                      # Interactive results viewer
│
├── notebooks/                          # Jupyter analysis notebooks
│   ├── 01_data_cleaning.ipynb
│   ├── 02_feature_engineering_rfm.ipynb
│   ├── 03_clustering.ipynb
│   └── 04_market_basket.ipynb
│
├── data/
│   ├── raw/
│   │   └── online_retail_II.xlsx       # Original dataset (not included)
│   └── processed/                      # Generated by run_analysis.py
│       ├── rfm_features.csv
│       ├── customer_segments.csv
│       └── association_rules.csv

### 1. **Data Cleaning Pipeline**
- **Noise Filtering**: Remove test transactions (StockCode: POST, BANK, etc.)
- **Cancellation Matching**: Adjust revenue for return transactions
- **Winsorization**: Cap quantity/price outliers at 5th/95th percentiles
- **Missing Data**: Drop records without Customer ID
- **Result**: 541,909 → 396,370 transactions (74.7% retention)

### 2. **Feature Engineering (20 Features)**

**RFM Core:**
- **Recency**: Days since last purchase
- **Frequency**: Total number of orders
- **Monetary**: Lifetime customer value

**Behavioral Metrics:**
- **Tenure**: Customer lifetime (days)
- **Interpurchase Time**: Avg days between orders
- **Diversity Index**: Shannon entropy of product variety
- **Avg Order Value**: Mean transaction amount
- **Return Rate**: Cancellation frequency

**NLP Features (TF-IDF):**
- **Taste Profiles**: 5 PCA-reduced dimensions from product descriptions
- **Explained Variance**: 26.9% of product preference patterns

### 3. **Clustering (K-Means + GMM)**
- **Optimal K Determination**: Silhouette, Davies-Bouldin, Calinski-Harabasz
- **Selected K**: 2 (Silhouette = 0.178)
- **PCA Reduction**: 14 features → 5 components (68.8% variance)
- **Algorithms**: K-Means (WCSS=18,637) + Gaussian Mixture (BIC=58,798)
- **Validation**: Feature importance via Random Forest

### 4. **Market Basket Analysis (FP-Growth)**
- **Algorithm**: FP-Growth (faster than Apriori)
- **Min Support**: 2.0% (244 itemsets)
- **Min Confidence**: 60% (20 rules)
- **VIP Segment**: Top 2 clusters by LTV
- **Output**: Association rules with confidence, support, lift

---

## 💻 Technical Stack

**Core:** Python 3.13, pandas 3.0, NumPy 2.4, scikit-learn 1.8  
**ML:** K-Means, GMM, PCA, Random Forest, TF-IDF, FP-Growth (MLxtend 0.24)  
**Viz:** Plotly 6.5, Matplotlib, Seaborn  
**UI:** Bootstrap 5.3, Font Awesome, custom CSS/JavaScript

---

## 📈 Business Applications

1. **VIP Retention Programs**: Target Cluster 0 with exclusive benefits
2. **Product Bundling**: Create teacup sets based on 24× lift associations
3. **Inventory Planning**: Stock color-coordinated items together
4. **Marketing Segmentation**: Personalized campaigns by cluster
5. **Churn Prevention**: Identify at-risk customers via recency thresholds

---

## 📝 License

MIT License - see LICENSE file for details

---

**⭐ If you found this helpful, consider starring the repo!**


