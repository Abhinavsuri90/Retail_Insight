# Customer Segmentation & Market Basket Analysis

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.0+-orange.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/status-active-success.svg)](https://github.com)

> Machine Learning-Powered Customer Intelligence for E-Commerce Analytics

This project applies unsupervised machine learning to discover customer behavioral patterns and product associations in retail transaction data, transforming 500,000+ transactions into actionable business insights.

---

## Table of Contents

- [Overview](#overview)
- [Key Results](#key-results)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Methodology](#methodology)
- [Project Structure](#project-structure)
- [Results](#results)
- [Requirements](#requirements)
- [License](#license)

---

## Overview

This data science project addresses the challenge of customer intelligence in non-contractual retail settings where explicit churn signals are absent. Using a two-stage unsupervised learning approach, we identify natural customer segments and discover product purchase patterns.

**Problem Solved:** Marketing blindness - inability to differentiate customer value and predict purchase behavior  
**Solution:** RFM-based segmentation + Apriori association mining  
**Dataset:** UCI Online Retail II (541,909 transactions, Dec 2009 - Dec 2011)

---

## Key Results

### Customer Segmentation

| Segment | Population | Avg Recency | Avg Orders | Avg Lifetime Value |
|---------|------------|-------------|------------|-------------------|
| **At-Risk** | 70.4% | 44 days | 3.7 | £1,359 |
| **Loyal** | 24.6% | 248 days | 1.6 | £481 |
| **VIP** | 0.3% | 7 days | 82.5 | £127,338 |
| **Elite** | 4.7% | 16 days | 22.3 | £12,709 |

**Critical Finding:** 5% of customers generate 47.7% of total revenue (£4.2M of £8.9M)

### Product Associations

- **20 high-confidence rules** discovered (confidence ≥ 60%)
- **Maximum lift: 21.3×** (Regency Teacup collections)
- **Average confidence: 71.7%**
- **Pattern:** Color-coordinated home decor sets purchased together

---

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/customer-segmentation.git
cd customer-segmentation

# Install dependencies
pip install -r requirements.txt
```

### Download Dataset

Download the Online Retail II dataset from [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/Online+Retail+II) and place it in `data/raw/online_retail_II.xlsx`

### Run Analysis

**Option 1: Automated Script (Recommended)**
```bash
python run_analysis.py
```

**Option 2: Step-by-Step Notebooks**
```bash
jupyter notebook notebooks/01_data_cleaning.ipynb
jupyter notebook notebooks/02_feature_engineering_rfm.ipynb
jupyter notebook notebooks/03_clustering.ipynb
jupyter notebook notebooks/04_market_basket.ipynb
```

**Option 3: View Pre-Generated Results**
```bash
open dashboard.html
```

---

## Usage

### Running the Complete Analysis

The `run_analysis.py` script executes the entire pipeline:

```bash
python run_analysis.py
```

**Outputs:**
- `data/processed/rfm_features.csv` - Customer RFM metrics
- `data/processed/customer_segments.csv` - Cluster assignments
- `data/processed/association_rules.csv` - Product associations
- Console output with detailed statistics

**Execution Time:** 2-5 minutes on standard hardware

### Interactive Dashboard

Open `dashboard.html` in any web browser to view:
- Customer segment profiles with statistics
- Market basket analysis results
- Visual business insights
- Methodology overview

### Jupyter Notebooks

Execute notebooks sequentially for detailed exploration:

1. **01_data_cleaning.ipynb**: Data preprocessing and quality checks
2. **02_feature_engineering_rfm.ipynb**: RFM metric calculation
3. **03_clustering.ipynb**: K-Means segmentation with validation
4. **04_market_basket.ipynb**: Apriori algorithm and association rules

---

## Methodology

### Data Preprocessing

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
│
└── reports/
    └── final_insights_academic.md      # Academic research paper
```

---

## Results

### Segment Characterization

**Cluster 0 - At-Risk Customers (70.4%)**
- High recency (44 days average)
- Low engagement (3.7 orders)
- Moderate value (£1,359)
- Action: Win-back campaigns required

**Cluster 1 - Loyal Customers (24.6%)**
- Very high recency (248 days)
- Minimal activity (1.6 orders)
- Low value (£481)
- Action: Reactivation strategies

**Cluster 2 - VIP Customers (0.3%)**
- Extremely active (7 days recency)
- Very high frequency (82.5 orders)
- Ultra high value (£127,338)
- Action: Concierge service, priority support

**Cluster 3 - Elite Whales (4.7%)**
- Recent activity (16 days)
- High frequency (22.3 orders)
- High value (£12,709)
- Action: Exclusive benefits, personalized engagement

### Association Rules Sample

| Antecedent | Consequent | Support | Confidence | Lift |
|------------|-----------|---------|------------|------|
| Roses Regency Teacup | Green Regency Teacup | 2.7% | 90% | 21.3× |
| Pink Regency Teacup | Roses Regency Teacup | 2.7% | 74% | 20.7× |
| Green Regency Teacup | Pink Regency Teacup | 2.9% | 69% | 19.2× |

**Insight:** VIP customers purchase color-coordinated teacup sets, indicating style-driven buying behavior

---

## Requirements

### Core Dependencies

```
pandas >= 1.3.0
numpy >= 1.21.0
scikit-learn >= 1.0.0
matplotlib >= 3.4.0
seaborn >= 0.11.0
mlxtend >= 0.19.0
openpyxl >= 3.0.0
jupyter >= 1.0.0
```

### System Requirements

- Python 3.8 or higher
- 4GB RAM minimum
- 50MB storage for dataset
- Modern web browser (for dashboard)

---

## Technical Implementation

### Algorithms Used

1. **K-Means Clustering** (MacQueen, 1967)
   - Partitions customers into K behaviorally homogeneous groups
   - Minimizes within-cluster sum of squares (WCSS)
   - Validated using Elbow Method and Silhouette Analysis

2. **Apriori Algorithm** (Agrawal et al., 1993)
   - Discovers frequent itemsets in transaction data
   - Generates association rules with support and confidence thresholds
   - Measures strength using lift metric

### Statistical Validation

- **Elbow Method**: Optimal K=4 identified at inflection point
- **Silhouette Score**: 0.45+ indicating reasonable cluster quality
- **Lift Analysis**: Values >2 indicate strong non-random associations

---

## Business Applications

### Recommended Actions

**For At-Risk Segment (70.4%):**
- Automated email win-back campaigns
- Time-limited discount offers
- Re-engagement surveys

**For VIP/Elite Segments (5%):**
- Dedicated account managers
- Early access to new products
- Exclusive loyalty benefits
- Priority customer service

**Product Strategy:**
- Bundle Regency teacup collections
- Implement "Frequently Bought Together" recommendations
- Create curated style-based collections

**Marketing Optimization:**
- Differential spend allocation by segment
- Personalized messaging based on cluster
- Predictive churn modeling for high-value customers

---

## Academic Context

**Research Area:** Retail Analytics, Customer Relationship Management  
**ML Paradigm:** Unsupervised Learning  
**Techniques:** Clustering, Association Mining, Feature Engineering  
**Dataset:** UCI ML Repository - Online Retail II  

**References:**
- Hughes, A.M. (1994). Strategic Database Marketing
- MacQueen, J. (1967). K-Means Classification Method
- Agrawal, R. et al. (1993). Mining Association Rules
- Fader, P.S. et al. (2005). RFM and Customer Lifetime Value

Complete bibliography available in `reports/final_insights_academic.md`

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

```bash
git clone https://github.com/yourusername/customer-segmentation.git
cd customer-segmentation
pip install -r requirements.txt
```

### Areas for Improvement

- Temporal modeling (time-series analysis of customer behavior)
- Deep learning approaches (autoencoders for segmentation)
- Real-time streaming analytics
- Additional datasets for validation
- Deployment pipeline (Docker, API endpoints)

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Citation

If you use this project in your research or work, please cite:

```bibtex
@software{customer_segmentation_2026,
  title={Customer Segmentation and Market Basket Analysis},
  author={Your Name},
  year={2026},
  url={https://github.com/yourusername/customer-segmentation}
}
```

---

## Acknowledgments

- UCI Machine Learning Repository for providing the Online Retail II dataset
- scikit-learn community for excellent ML tools
- mlxtend library for association rule mining implementation

---

**Project Status:** Complete and ready for production use  
**Last Updated:** January 2026  
**Maintained by:** [Your Name](https://github.com/yourusername)
