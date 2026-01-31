# 🛍️ RetailInsight - AI-Powered Customer Analytics

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.8+-orange.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/status-production-success.svg)](https://github.com)

> **Advanced Machine Learning for E-Commerce Intelligence**  
> Transform 500K+ transactions into actionable business insights with professional-grade customer segmentation and product recommendations.

---

## 📊 Dataset

**Source:** UCI Online Retail II Dataset  
**Backup Download:** [Google Drive Folder](https://drive.google.com/drive/folders/1Orpo8SFt8LukT79ydY1eIMUjsNtvHtTX?usp=drive_link)

📥 Download `online_retail_II.xlsx` and place in `data/raw/` folder

**Details:** 541,909 transactions | 4,372 customers | Dec 2009 - Dec 2011 | UK retail

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

# 2. Get dataset (if not included)
# Download from: https://drive.google.com/drive/folders/1Orpo8SFt8LukT79ydY1eIMUjsNtvHtTX?usp=drive_link
# Place online_retail_II.xlsx in data/raw/ folder

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run analytics pipeline (2 minutes)
python retail_analytics_professional.py

# 5. Run market basket analysis
python run_market_basket.py

# 6. Open dashboards (Cmd+Click the URLs in terminal)
# - Executive Dashboard: KPIs, segments, revenue analysis
# - Product Recommender: Live search, bundles, lift metrics
```

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
---

## 🔬 How It Works

### Data Processing

The pipeline cleans 541K transactions down to 396K by:
- Removing test/invalid transactions
- Matching cancellations to adjust revenue
- Capping extreme outliers
- Filtering records without customer IDs

### Feature Engineering

Built 20 features from transaction data:

**Customer Behavior:**
- Recency, Frequency, Monetary (RFM basics)
- Purchase patterns (time between orders, diversity)
- Order economics (avg value, return rate)

**Product Preferences:**
- TF-IDF analysis of product descriptions
- 5 "taste profile" dimensions via PCA
- Captures customer style preferences

### Clustering Approach

Used both K-Means and Gaussian Mixture Models:
- Tested 2-10 clusters with validation metrics
- Settled on K=2 (best silhouette score: 0.178)
- PCA reduced 14 features to 5 components
- Random Forest identified top predictors

### Association Mining

FP-Growth algorithm finds product bundles:
- Min support: 2% (items bought together often enough)
- Min confidence: 60% (reliable recommendations)
- Focused on VIP customers for quality insights

---

## 💻 Tech Stack

Python 3.13 • pandas • NumPy • scikit-learn • Plotly • MLxtend • Bootstrap 5

---

## 📈 Use Cases

- **Customer Retention**: Identify and engage high-value segments
- **Product Strategy**: Bundle items with strong purchase correlations
- **Marketing**: Personalize campaigns based on cluster behavior
- **Inventory**: Stock complementary products near each other

---

## 📝 License

MIT License - see LICENSE file

---

**⭐ Star this repo if you found it useful!**


