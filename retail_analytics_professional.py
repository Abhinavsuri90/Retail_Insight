#!/usr/bin/env python3
"""
RETAIL INSIGHT: PROFESSIONAL ML PIPELINE

This implementation uses:
- Advanced data cleaning (cancellation matching, winsorization)
- Sophisticated feature engineering (RFM + Tenure + Diversity + NLP)
- Multiple clustering algorithms (K-Means + GMM)
- PCA dimensionality reduction
- Statistical validation (Silhouette, Davies-Bouldin)
- Feature importance analysis

Date: January 2026
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data_processor import DataProcessor
from feature_engineer import FeatureEngineer
from clustering_engine import ClusteringEngine
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


def main():
    """Execute professional-grade ML pipeline"""
    
    print("\n🔷 RETAIL INSIGHT - ML Analytics Pipeline")
    print(f"   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # =========================================================================
    # PHASE 1: DATA ACQUISITION & CLEANING
    # =========================================================================
    print("📥 Data Processing...")
    
    processor = DataProcessor('data/raw/online_retail_II.xlsx')
    df_clean = processor.execute_pipeline()
    
    # Get return rate data
    return_rate = processor.get_return_rate_by_customer()
    
    # =========================================================================
    # PHASE 2: ADVANCED FEATURE ENGINEERING
    # =========================================================================
    print("🔧 Feature Engineering...")
    
    engineer = FeatureEngineer(df_clean)
    rfm_features = engineer.execute_pipeline(return_rate_df=return_rate, include_nlp=True)
    
    # Save intermediate results
    os.makedirs('data/processed', exist_ok=True)
    rfm_features.to_csv('data/processed/rfm_features_professional.csv')
    
    # =========================================================================
    # PHASE 3: ADVANCED CLUSTERING
    # =========================================================================
    print("🎯 Clustering & Segmentation...")
    
    clusterer = ClusteringEngine(rfm_features)
    clustered_data, metrics, importance = clusterer.execute_pipeline(
        use_pca=True,
        fit_gmm=True
    )
    
    clusterer.save_results('data/processed/customer_segments_professional.csv')
    
    # =========================================================================
    # PHASE 4: BUSINESS INSIGHTS
    # =========================================================================
    print("💡 Generating Insights...")
    
    generate_business_insights(clustered_data, df_clean)
    
    # =========================================================================
    # COMPLETION
    # =========================================================================
    print("\n✅ Analysis Complete")
    print("   📊 Files: data/processed/rfm_features_professional.csv")
    print("            data/processed/customer_segments_professional.csv\n")
    
    return clustered_data


def generate_business_insights(clustered_data, df_clean):
    """Generate actionable business recommendations"""
    
    # Calculate key metrics
    total_revenue = df_clean['TotalPrice'].sum()
    total_customers = len(clustered_data)
    
    # Analyze by cluster
    cluster_col = 'Cluster_KMeans' if 'Cluster_KMeans' in clustered_data.columns else 'Cluster'
    
    cluster_revenue = clustered_data.groupby(cluster_col)['Monetary'].sum().sort_values(ascending=False)
    cluster_counts = clustered_data[cluster_col].value_counts().sort_index()
    cluster_avg_ltv = clustered_data.groupby(cluster_col)['Monetary'].mean().sort_values(ascending=False)
    
    print("\n📊 Results Summary:")
    print(f"   Customers: {total_customers:,} | Revenue: £{total_revenue:,.0f} | Segments: {clustered_data[cluster_col].nunique()}")
    
    print("\n💎 Segment Performance:")
    for cluster in sorted(cluster_revenue.index):
        revenue = cluster_revenue[cluster]
        count = cluster_counts[cluster]
        avg_ltv = cluster_avg_ltv[cluster]
        revenue_pct = revenue / total_revenue * 100
        
        print(f"   Cluster {cluster}: {count:,} customers | £{revenue:,.0f} ({revenue_pct:.1f}%) | Avg LTV: £{avg_ltv:,.0f}")
    
    # Find VIP segment
    vip_cluster = cluster_avg_ltv.index[0]
    vip_count = cluster_counts[vip_cluster]
    vip_revenue = cluster_revenue[vip_cluster]
    
    print(f"\n🎯 Key Insight: Cluster {vip_cluster} = VIP Segment ({vip_count/total_customers*100:.1f}% customers, {vip_revenue/total_revenue*100:.1f}% revenue)")
    
    # Business impact
    retention_improvement = 0.10
    projected_revenue = vip_revenue * retention_improvement
    print(f"💰 Projected Impact: +£{projected_revenue:,.0f} with 10% VIP retention improvement")
    
    # =========================================================================
    # INTERACTIVE DASHBOARDS
    # =========================================================================
    exec_dashboard = os.path.abspath('reports/executive_dashboard.html')
    prod_recommender = os.path.abspath('reports/product_recommender.html')
    
    print("\n📈 Interactive Dashboards:")
    print(f"   Executive: file://{exec_dashboard}")
    print(f"   Recommender: file://{prod_recommender}")
    print("   💡 Cmd+Click to open\n")


if __name__ == '__main__':
    result = main()
