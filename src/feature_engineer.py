"""
Advanced Feature Engineering Module
====================================
Creates RFM + Tenure + Diversity + Temporal + Behavioral features.

Implements log transformations and sophisticated behavioral metrics.
"""

import pandas as pd
import numpy as np
from scipy.stats import entropy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA


class FeatureEngineer:
    """Advanced feature engineering for customer behavioral analysis"""
    
    def __init__(self, df_clean):
        self.df = df_clean
        self.rfm = None
        self.snapshot_date = df_clean['InvoiceDate'].max() + pd.Timedelta(days=1)
        
    def compute_rfm_base(self):
        """Compute base RFM metrics"""
        print("\n" + "="*80)
        print("ADVANCED FEATURE ENGINEERING")
        print("="*80)
        
        self.rfm = self.df.groupby('Customer ID').agg({
            'InvoiceDate': lambda x: (self.snapshot_date - x.max()).days,
            'Invoice': 'nunique',
            'TotalPrice': 'sum'
        }).rename(columns={
            'InvoiceDate': 'Recency',
            'Invoice': 'Frequency',
            'TotalPrice': 'Monetary'
        })
        
        print(f"✓ Base RFM computed for {len(self.rfm):,} customers")
        
    def add_tenure(self):
        """Add Tenure (T) - customer age in days"""
        tenure = self.df.groupby('Customer ID')['InvoiceDate'].apply(
            lambda x: (self.snapshot_date - x.min()).days
        )
        self.rfm['Tenure'] = tenure
        print(f"✓ Added Tenure (T) - customer age metric")
        
    def add_interpurchase_time(self):
        """Average days between consecutive purchases"""
        def calc_interpurchase(dates):
            sorted_dates = sorted(dates)
            if len(sorted_dates) <= 1:
                return 0
            diffs = [(sorted_dates[i+1] - sorted_dates[i]).days 
                    for i in range(len(sorted_dates)-1)]
            return np.mean(diffs) if diffs else 0
        
        interpurchase = self.df.groupby('Customer ID')['InvoiceDate'].apply(calc_interpurchase)
        self.rfm['InterpurchaseTime'] = interpurchase
        print(f"✓ Added Interpurchase Time - purchase rhythm metric")
        
    def add_diversity_index(self):
        """Product diversity using entropy (Shannon index)"""
        def calc_diversity(items):
            value_counts = items.value_counts()
            probs = value_counts / len(items)
            return entropy(probs)  # Higher = more diverse
        
        diversity = self.df.groupby('Customer ID')['StockCode'].apply(calc_diversity)
        self.rfm['DiversityIndex'] = diversity
        print(f"✓ Added Diversity Index - product variety metric")
        
    def add_seasonality_flag(self):
        """Flag for holiday/seasonal shoppers"""
        # Extract month
        df_with_month = self.df.copy()
        df_with_month['Month'] = df_with_month['InvoiceDate'].dt.month
        
        # Calculate % of spending in Nov/Dec (months 11, 12)
        holiday_spend = df_with_month[df_with_month['Month'].isin([11, 12])].groupby('Customer ID')['TotalPrice'].sum()
        total_spend = df_with_month.groupby('Customer ID')['TotalPrice'].sum()
        
        holiday_pct = (holiday_spend / total_spend).fillna(0)
        self.rfm['IsHolidayShopper'] = (holiday_pct > 0.5).astype(int)
        print(f"✓ Added Seasonality Flag - holiday shopping pattern")
        
    def add_avg_order_value(self):
        """Average order value per customer"""
        aov = self.df.groupby('Customer ID')['TotalPrice'].mean()
        self.rfm['AvgOrderValue'] = aov
        print(f"✓ Added Average Order Value (AOV)")
        
    def add_unique_products(self):
        """Count of unique products purchased"""
        unique_products = self.df.groupby('Customer ID')['StockCode'].nunique()
        self.rfm['UniqueProducts'] = unique_products
        print(f"✓ Added Unique Products count")
        
    def add_return_rate(self, return_rate_df=None):
        """Add return rate if available"""
        if return_rate_df is not None and not return_rate_df.empty:
            self.rfm = self.rfm.join(return_rate_df, how='left')
            self.rfm['ReturnRate'] = self.rfm['ReturnRate'].fillna(0)
            print(f"✓ Added Return Rate metric")
    
    def apply_log_transformation(self):
        """Log transform skewed features (critical for K-Means)"""
        log_cols = ['Recency', 'Frequency', 'Monetary', 'Tenure', 'AvgOrderValue']
        
        for col in log_cols:
            if col in self.rfm.columns:
                self.rfm[f'{col}_Log'] = np.log1p(self.rfm[col])
        
        print(f"✓ Applied log transformation to {len(log_cols)} features")
        
    def add_nlp_features(self, n_components=5):
        """Extract TF-IDF features from product descriptions"""
        print("\n" + "="*80)
        print("NLP FEATURE EXTRACTION")
        print("="*80)
        
        # Get product descriptions per customer
        customer_products = self.df.groupby('Customer ID')['Description'].apply(
            lambda x: ' '.join(x.dropna().astype(str))
        )
        
        # TF-IDF vectorization
        tfidf = TfidfVectorizer(max_features=100, stop_words='english')
        tfidf_matrix = tfidf.fit_transform(customer_products)
        
        # PCA to reduce to 5 taste components
        pca = PCA(n_components=n_components, random_state=42)
        taste_features = pca.fit_transform(tfidf_matrix.toarray())
        
        # Add to RFM
        taste_df = pd.DataFrame(
            taste_features,
            index=customer_products.index,
            columns=[f'Taste_{i+1}' for i in range(n_components)]
        )
        
        self.rfm = self.rfm.join(taste_df, how='left')
        self.rfm[[f'Taste_{i+1}' for i in range(n_components)]] = self.rfm[[f'Taste_{i+1}' for i in range(n_components)]].fillna(0)
        
        print(f"✓ Added {n_components} NLP taste profile features")
        print(f"  Explained variance: {pca.explained_variance_ratio_.sum()*100:.1f}%")
        
    def get_features(self):
        """Return all engineered features"""
        return self.rfm
    
    def execute_pipeline(self, return_rate_df=None, include_nlp=True):
        """Run complete feature engineering pipeline"""
        self.compute_rfm_base()
        self.add_tenure()
        self.add_interpurchase_time()
        self.add_diversity_index()
        self.add_seasonality_flag()
        self.add_avg_order_value()
        self.add_unique_products()
        self.add_return_rate(return_rate_df)
        self.apply_log_transformation()
        
        if include_nlp:
            try:
                self.add_nlp_features()
            except Exception as e:
                print(f"⚠️  NLP features skipped: {e}")
        
        print(f"\n✓ Feature engineering complete: {self.rfm.shape[1]} total features")
        print(f"\nFeature Summary:")
        print(self.rfm.describe().T[['mean', '50%', 'max']].round(2))
        
        return self.rfm
