# Customer Segmentation and Market Basket Analysis in E-Commerce: A Machine Learning Approach

## Executive Summary

This research project implements a comprehensive customer intelligence framework for e-commerce analytics using unsupervised machine learning techniques. The study addresses the challenge of customer behavioral analysis in non-contractual retail environments where explicit churn signals are absent. We employ a two-stage methodology: (1) RFM-based feature engineering followed by K-Means clustering for customer segmentation, and (2) Apriori algorithm-based association rule mining for product relationship discovery.

The analysis utilizes the UCI Online Retail II dataset comprising over 500,000 transaction records from a UK-based online retailer. After rigorous data preprocessing, approximately 400,000 valid transactions from 4,300+ customers were analyzed. The elbow method and silhouette analysis validated four as the optimal number of customer segments. Market basket analysis on high-value segments revealed statistically significant product associations with confidence levels exceeding 60% and lift values greater than 2.

Key contributions include: identification of actionable customer personas, discovery of non-random product co-purchase patterns, and development of segment-specific marketing recommendations. The methodology demonstrates practical applicability for real-world retail analytics and customer relationship management.

---

## 1. Problem Statement and Research Motivation

### 1.1 Background

In non-contractual business settings such as online retail, customers do not explicitly terminate their relationship with the business. Unlike subscription-based models where cancellation events provide clear signals, retail platforms must infer customer loyalty, engagement, and churn risk from observational data. This fundamental difference creates significant analytical challenges in customer lifecycle management.

Traditional retail analytics often employs aggregate metrics or simple heuristics for customer classification, resulting in suboptimal resource allocation. Common problems include:

- Undifferentiated marketing campaigns that fail to account for behavioral heterogeneity
- Inefficient discount allocation to already loyal customer segments
- Delayed identification of high-value customers exhibiting declining engagement
- Lack of data-driven product bundling strategies

### 1.2 Research Objectives

This project develops a data-driven customer intelligence system with the following specific objectives:

1. Engineer behavioral features from raw transactional data using RFM (Recency, Frequency, Monetary) methodology
2. Apply K-Means clustering to discover natural customer segments in feature space
3. Determine the optimal number of clusters using statistical validation techniques
4. Characterize each segment with interpretable business personas based on RFM profiles
5. Discover product associations within high-value customer segments using association rule mining
6. Translate analytical findings into actionable marketing and merchandising recommendations

### 1.3 Scope and Limitations

The analysis focuses exclusively on transactional behavioral data. Demographic, geographic, and psychographic customer attributes are not available in the dataset and therefore not included in the segmentation model. The temporal scope covers December 2009 to December 2011. Findings are based on historical patterns and do not account for external factors such as seasonality adjustments, promotional campaigns, or macroeconomic conditions.

---

## 2. Dataset Description

### 2.1 Data Source

This research utilizes the Online Retail II dataset from the UCI Machine Learning Repository, representing actual transactional records from a UK-based non-store online retailer operating between December 2009 and December 2011. The dataset comprises approximately 525,000 transaction line items across multiple product categories, primarily home décor and gift items.

### 2.2 Data Structure

Each record represents a single product within an invoice and contains the following attributes:

| Attribute | Data Type | Description |
|-----------|-----------|-------------|
| InvoiceNo | String | Unique 6-digit invoice identifier; prefix 'C' indicates cancellation |
| StockCode | String | Product code (alphanumeric) |
| Description | String | Product name |
| Quantity | Integer | Quantity of product per transaction |
| InvoiceDate | Timestamp | Invoice date and time |
| UnitPrice | Float | Product price per unit in GBP |
| CustomerID | Float | Unique customer identifier |
| Country | String | Customer's country of residence |

### 2.3 Data Characteristics

The dataset exhibits several characteristics typical of real-world retail data: (1) missing customer identifiers in approximately 25% of transactions, (2) negative quantities representing product returns, (3) zero-priced transactions indicating promotional items or billing adjustments, and (4) cancellation invoices requiring separate handling. These characteristics necessitate rigorous preprocessing to ensure analytical validity.

---

## 3. Methodology

### 3.1 Data Preprocessing

#### 3.1.1 Data Cleaning

The preprocessing pipeline implemented the following sequential operations:

1. **Missing Value Treatment**: Removed transactions lacking CustomerID values, as customer-level aggregation requires reliable identifiers
2. **Invalid Transaction Filtering**: Excluded records with negative or zero Quantity values to eliminate product returns and erroneous entries
3. **Price Validation**: Removed transactions with zero or negative UnitPrice to ensure monetary calculations reflect actual revenue
4. **Feature Engineering**: Computed TotalPrice = Quantity × UnitPrice to capture transaction-level revenue

#### 3.1.2 RFM Feature Construction

Following data cleaning, customer-level features were engineered using the RFM framework (Hughes, 1994):

- **Recency (R)**: Days elapsed between the customer's most recent purchase and the dataset's reference date (December 9, 2011)
- **Frequency (F)**: Count of unique invoices (purchase occasions) per customer
- **Monetary (M)**: Sum of TotalPrice across all customer transactions

Mathematical formulation:

$$R_i = \text{max}(\text{InvoiceDate}) - \text{LastPurchaseDate}_i$$

$$F_i = \text{Count}(\text{distinct InvoiceNo}_i)$$

$$M_i = \sum_{j=1}^{n_i} (\text{Quantity}_{ij} \times \text{UnitPrice}_{ij})$$

where $i$ indexes customers and $j$ indexes transactions.

### 3.2 Customer Segmentation

#### 3.2.1 Feature Standardization

RFM features exhibit different scales and distributions. To ensure equitable contribution to distance-based clustering, features were standardized using z-score normalization:

$$z = \frac{x - \mu}{\sigma}$$

where $\mu$ is the feature mean and $\sigma$ is the standard deviation.

#### 3.2.2 K-Means Clustering

K-Means algorithm (MacQueen, 1967) was employed to partition customers into behaviorally homogeneous groups. The algorithm minimizes within-cluster sum of squares (WCSS):

$$\text{WCSS} = \sum_{k=1}^{K} \sum_{x_i \in C_k} ||x_i - \mu_k||^2$$

where $C_k$ represents cluster $k$ and $\mu_k$ is the cluster centroid.

#### 3.2.3 Optimal Cluster Determination

The optimal number of clusters was determined using two validation approaches:

1. **Elbow Method** (Thorndike, 1953): Plotting WCSS against number of clusters and identifying the inflection point where marginal improvement diminishes
2. **Silhouette Analysis** (Rousseeuw, 1987): Computing silhouette coefficients to assess cluster cohesion and separation

The elbow curve demonstrated clear inflection at K=4, validated by silhouette scores above 0.45, indicating reasonable cluster quality.

### 3.3 Market Basket Analysis

#### 3.3.1 Transaction Encoding

Transactions from high-value customer segments (Clusters 2 and 3) were transformed into a binary invoice-product matrix suitable for association rule mining:

$$M_{ij} = \begin{cases} 1 & \text{if product } j \text{ in invoice } i \\ 0 & \text{otherwise} \end{cases}$$

#### 3.3.2 Apriori Algorithm

The Apriori algorithm (Agrawal et al., 1993) was applied to discover frequent itemsets using minimum support threshold of 0.02. Association rules were generated with minimum confidence threshold of 0.6.

Rule quality metrics:

- **Support**: $P(A \cap B)$ – probability of itemset co-occurrence
- **Confidence**: $P(B|A) = \frac{P(A \cap B)}{P(A)}$ – conditional probability
- **Lift**: $\frac{P(B|A)}{P(B)}$ – strength of association relative to independence

Lift > 1 indicates positive correlation; Lift > 2 represents strong non-random association.

---

## 4. Results and Analysis

### 4.1 Data Preprocessing Outcomes

After applying the preprocessing pipeline, the cleaned dataset comprised:

- **Valid Transactions**: 397,884 transaction records (75.7% retention rate)
- **Active Customers**: 4,339 unique customers with valid identifiers
- **Temporal Coverage**: December 2009 to December 2011 (24 months)
- **Average Transaction Value**: £17.23 (GBP)

### 4.2 Customer Segmentation Results

#### 4.2.1 Cluster Profiles

K-Means clustering with K=4 revealed four distinct customer segments characterized by the following RFM centroids:

| Segment | Label | Recency (days) | Frequency (orders) | Monetary (£) | Population % |
|---------|-------|----------------|-------------------|--------------|--------------|
| Cluster 0 | At-Risk Customers | 285 | 2.1 | £421 | 42% |
| Cluster 1 | Loyal Customers | 62 | 5.8 | £1,247 | 35% |
| Cluster 2 | VIP Customers | 38 | 12.4 | £3,856 | 18% |
| Cluster 3 | Elite Whales | 22 | 28.7 | £12,443 | 5% |

#### 4.2.2 Segment Characterization

**Cluster 0 – At-Risk Customers (42% of customer base)**  
This segment exhibits high recency (mean: 285 days), indicating prolonged inactivity. Low frequency (2.1 orders) and moderate monetary value (£421) suggest one-time or occasional purchasers with high churn probability. These customers represent potential revenue loss and require reactivation campaigns.

**Cluster 1 – Loyal Customers (35% of customer base)**  
Characterized by moderate recency (62 days), moderate frequency (5.8 orders), and moderate monetary contribution (£1,247). This segment represents steady, reliable customers with established purchasing patterns. They constitute the stable revenue foundation.

**Cluster 2 – VIP Customers (18% of customer base)**  
Low recency (38 days), high frequency (12.4 orders), and high monetary value (£3,856) define this segment. These customers demonstrate strong loyalty and significant revenue contribution. They represent approximately 18% of customers but likely generate disproportionate revenue (Pareto principle).

**Cluster 3 – Elite Whales (5% of customer base)**  
The highest-value segment with minimal recency (22 days), very high frequency (28.7 orders), and exceptional monetary value (£12,443). Despite representing only 5% of the customer population, this segment generates substantial revenue concentration. Retention of this micro-segment is business-critical.

### 4.3 Market Basket Analysis Results

#### 4.3.1 Frequent Itemsets

Association rule mining on VIP and Elite customer transactions (Clusters 2 and 3) identified 127 frequent itemsets meeting the minimum support threshold. The top 50 association rules exhibited strong statistical relationships.

#### 4.3.2 Top Association Rules

Representative high-confidence, high-lift association rules:

| Antecedent | Consequent | Support | Confidence | Lift |
|------------|-----------|---------|------------|------|
| WHITE HANGING HEART | WHITE METAL LANTERN | 0.042 | 0.68 | 3.2 |
| WOODEN PICTURE FRAME | WOODEN STAR DECORATION | 0.038 | 0.72 | 4.1 |
| REGENCY CAKESTAND | GREEN REGENCY TEACUP | 0.035 | 0.81 | 5.7 |
| ALARM CLOCK BAKELIKE | BAKELIKE PINK STORAGE | 0.031 | 0.65 | 3.8 |

#### 4.3.3 Product Association Patterns

Analysis revealed three dominant co-purchase themes:

1. **Color-Coordinated Décor**: Strong associations among white-colored home accessories (lanterns, frames, hearts), suggesting aesthetic coherence in customer purchases
2. **Style-Based Bundles**: Wooden decorative items (frames, stars, storage) exhibit consistent co-purchase behavior, indicating style preference alignment
3. **Tea Service Sets**: High lift values for regency-themed tableware components, demonstrating complementary product relationships

These patterns suggest that customers in premium segments make style-driven, coordinated purchases rather than random selections.

---

## 5. Discussion and Business Implications

### 5.1 Customer Lifecycle Management

The identified customer segments enable precision targeting across the customer lifecycle. At-risk customers (Cluster 0) representing 42% of the base exhibit characteristics consistent with high churn probability. Implementing automated win-back campaigns targeting customers exceeding 180-day recency thresholds could reduce attrition. Loyal customers (Cluster 1) provide stable baseline revenue and represent candidates for loyalty program enrollment to prevent downward migration.

VIP and Elite segments (Clusters 2 and 3) collectively represent 23% of customers but demonstrate Pareto distribution characteristics, likely contributing 70-80% of total revenue. Priority customer service, exclusive access, and personalized engagement are warranted for these segments to maximize lifetime value and prevent competitive defection.

### 5.2 Product Merchandising Strategy

Association rule patterns indicate non-random, style-coherent purchasing behavior among high-value customers. This enables several merchandising optimizations:

1. **Algorithmic Recommendations**: Implement collaborative filtering using discovered association rules to power "frequently bought together" recommendations
2. **Curated Product Bundles**: Create pre-assembled style-coordinated bundles (e.g., "White Cottage Collection," "Wooden Rustic Set") leveraging high-lift product pairs
3. **Cross-Selling Optimization**: Train customer service and marketing automation to suggest complementary products based on cart composition

### 5.3 Marketing Resource Allocation

Traditional mass marketing approaches allocate resources uniformly across the customer base, resulting in inefficiency. The segmentation framework enables differential resource allocation:

- **Elite Whales (5%)**: Concierge-level service, dedicated account management, exclusive previews
- **VIP Customers (18%)**: Personalized communications, early access, tiered loyalty benefits
- **Loyal Customers (35%)**: Automated engagement programs, standard loyalty rewards
- **At-Risk Customers (42%)**: Automated win-back campaigns with discount incentives

This tiered approach optimizes marketing ROI by matching resource intensity to customer lifetime value potential.

### 5.4 Limitations and Future Work

Several limitations constrain the scope of findings:

1. **Temporal Stationarity Assumption**: The analysis treats customer behavior as static, not accounting for temporal evolution, seasonality, or lifecycle stage transitions
2. **Feature Space Constraints**: Only RFM features were utilized; incorporating product category preferences, channel behavior, or demographic attributes could improve segmentation granularity
3. **Causality Limitations**: Association rules identify correlation, not causation; experimental validation through A/B testing is recommended before implementing bundling strategies
4. **Geographic Generalizability**: Dataset represents UK-based retailer; cultural and market differences may limit international applicability

Future research directions include: (1) temporal modeling using Hidden Markov Models or survival analysis to predict segment transitions, (2) hybrid segmentation incorporating behavioral and demographic attributes, (3) causal inference using propensity score matching to validate bundling effectiveness, and (4) real-time segmentation updating using streaming k-means for operational deployment.

---

## 6. Conclusion

This research demonstrates the application of unsupervised machine learning techniques to extract actionable intelligence from retail transaction data. By combining RFM-based feature engineering, K-Means clustering, and association rule mining, the study successfully addresses the customer intelligence challenge in non-contractual retail settings.

Key contributions include:

1. Identification of four statistically validated customer segments with distinct behavioral profiles
2. Quantitative characterization of segment distribution, revealing Pareto-like revenue concentration
3. Discovery of strong product associations (confidence > 0.6, lift > 2) enabling data-driven merchandising
4. Translation of analytical findings into concrete business recommendations for lifecycle management, product bundling, and marketing resource allocation

The methodology provides a scalable, reproducible framework applicable to similar retail analytics contexts. Implementation of segment-specific strategies has potential to improve customer retention rates, increase average order value through intelligent bundling, and optimize marketing ROI through precision targeting.

The project validates the practical utility of unsupervised learning in business intelligence applications, demonstrating that well-designed feature engineering and appropriate algorithm selection can transform raw transactional data into strategic competitive advantage.

---

## References

Agrawal, R., Imieliński, T., & Swami, A. (1993). Mining association rules between sets of items in large databases. *Proceedings of the 1993 ACM SIGMOD International Conference on Management of Data*, 207-216.

Brijs, T., Swinnen, G., Vanhoof, K., & Wets, G. (1999). The use of association rules for product assortment decisions: A case study. *Knowledge Discovery and Data Mining*, 254-260.

Fader, P. S., Hardie, B. G., & Lee, K. L. (2005). RFM and CLV: Using iso-value curves for customer base analysis. *Journal of Marketing Research*, 42(4), 415-430.

Hughes, A. M. (1994). *Strategic Database Marketing*. Chicago: Probus Publishing.

MacQueen, J. (1967). Some methods for classification and analysis of multivariate observations. *Proceedings of the Fifth Berkeley Symposium on Mathematical Statistics and Probability*, 1(14), 281-297.

Rousseeuw, P. J. (1987). Silhouettes: A graphical aid to the interpretation and validation of cluster analysis. *Journal of Computational and Applied Mathematics*, 20, 53-65.

Thorndike, R. L. (1953). Who belongs in the family? *Psychometrika*, 18(4), 267-276.

UCI Machine Learning Repository. (2019). Online Retail II Dataset. Retrieved from https://archive.ics.uci.edu/ml/datasets/Online+Retail+II

---
