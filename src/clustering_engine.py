"""
Advanced Clustering Engine Module
==================================
Implements multiple clustering algorithms with validation and explainability.

Techniques: K-Means, GMM, PCA, Silhouette Analysis, SHAP values.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, silhouette_samples, davies_bouldin_score, calinski_harabasz_score
from sklearn.ensemble import RandomForestClassifier
import warnings
warnings.filterwarnings('ignore')


class ClusteringEngine:
    """Advanced clustering with multiple algorithms and validation"""
    
    def __init__(self, rfm_data):
        self.rfm = rfm_data
        self.scaler = StandardScaler()
        self.pca = None
        self.kmeans_model = None
        self.gmm_model = None
        self.optimal_k = None
        self.feature_cols = None
        
    def select_features_for_clustering(self):
        """Select which features to use for clustering"""
        # Use log-transformed RFM + behavioral features
        feature_candidates = [col for col in self.rfm.columns if '_Log' in col or 'Taste_' in col or 
                            col in ['DiversityIndex', 'InterpurchaseTime', 'IsHolidayShopper', 'UniqueProducts']]
        
        # If no log features, use base RFM
        if not feature_candidates:
            feature_candidates = ['Recency', 'Frequency', 'Monetary']
        
        self.feature_cols = feature_candidates
        print(f"\nSelected {len(self.feature_cols)} features for clustering:")
        print(f"  {', '.join(self.feature_cols)}")
        
    def determine_optimal_k(self, k_range=range(2, 11)):
        """Find optimal K using multiple validation metrics"""
        print("\n" + "="*80)
        print("OPTIMAL CLUSTER DETERMINATION")
        print("="*80)
        
        # Prepare data
        if self.feature_cols is None:
            self.select_features_for_clustering()
        
        X = self.rfm[self.feature_cols].fillna(0)
        X_scaled = self.scaler.fit_transform(X)
        
        # Test different K values
        metrics = {
            'inertia': [],
            'silhouette': [],
            'davies_bouldin': [],
            'calinski_harabasz': []
        }
        
        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = kmeans.fit_predict(X_scaled)
            
            metrics['inertia'].append(kmeans.inertia_)
            metrics['silhouette'].append(silhouette_score(X_scaled, labels))
            metrics['davies_bouldin'].append(davies_bouldin_score(X_scaled, labels))
            metrics['calinski_harabasz'].append(calinski_harabasz_score(X_scaled, labels))
        
        # Display results
        results = pd.DataFrame(metrics, index=k_range)
        print("\nClustering Quality Metrics:")
        print(results.round(3))
        
        # Select optimal K (highest silhouette)
        self.optimal_k = k_range[np.argmax(metrics['silhouette'])]
        print(f"\n✓ Optimal K = {self.optimal_k} (Silhouette: {max(metrics['silhouette']):.3f})")
        
        return metrics, results
    
    def apply_pca(self, n_components=5):
        """Apply PCA for dimensionality reduction and visualization"""
        print("\n" + "="*80)
        print("PCA DIMENSIONALITY REDUCTION")
        print("="*80)
        
        X = self.rfm[self.feature_cols].fillna(0)
        X_scaled = self.scaler.fit_transform(X)
        
        self.pca = PCA(n_components=n_components, random_state=42)
        pca_features = self.pca.fit_transform(X_scaled)
        
        print(f"\n✓ Reduced {len(self.feature_cols)} features → {n_components} principal components")
        print(f"  Explained variance: {self.pca.explained_variance_ratio_.sum()*100:.1f}%")
        print(f"\n  Per component:")
        for i, var in enumerate(self.pca.explained_variance_ratio_, 1):
            print(f"    PC{i}: {var*100:.1f}%")
        
        # Store PCA features
        pca_df = pd.DataFrame(
            pca_features,
            index=self.rfm.index,
            columns=[f'PC{i+1}' for i in range(n_components)]
        )
        
        return pca_df
    
    def fit_kmeans(self, use_pca=False):
        """Fit K-Means clustering model"""
        print("\n" + "="*80)
        print(f"K-MEANS CLUSTERING (K={self.optimal_k})")
        print("="*80)
        
        # Prepare features
        if use_pca and self.pca is not None:
            X = self.rfm[[f'PC{i+1}' for i in range(self.pca.n_components_)]]
        else:
            X = self.rfm[self.feature_cols].fillna(0)
        
        X_scaled = self.scaler.fit_transform(X)
        
        # Fit model
        self.kmeans_model = KMeans(n_clusters=self.optimal_k, random_state=42, n_init=10)
        self.rfm['Cluster_KMeans'] = self.kmeans_model.fit_predict(X_scaled)
        
        # Compute silhouette score
        silhouette_avg = silhouette_score(X_scaled, self.rfm['Cluster_KMeans'])
        
        print(f"\n✓ K-Means fitted successfully")
        print(f"  Inertia (WCSS): {self.kmeans_model.inertia_:,.0f}")
        print(f"  Silhouette Score: {silhouette_avg:.3f}")
        
        # Show cluster distribution
        cluster_counts = self.rfm['Cluster_KMeans'].value_counts().sort_index()
        print(f"\n  Cluster Distribution:")
        for cluster, count in cluster_counts.items():
            print(f"    Cluster {cluster}: {count:,} customers ({count/len(self.rfm)*100:.1f}%)")
        
    def fit_gmm(self, use_pca=False):
        """Fit Gaussian Mixture Model (soft clustering)"""
        print("\n" + "="*80)
        print(f"GAUSSIAN MIXTURE MODEL (K={self.optimal_k})")
        print("="*80)
        
        # Prepare features
        if use_pca and self.pca is not None:
            X = self.rfm[[f'PC{i+1}' for i in range(self.pca.n_components_)]]
        else:
            X = self.rfm[self.feature_cols].fillna(0)
        
        X_scaled = self.scaler.fit_transform(X)
        
        # Fit GMM
        self.gmm_model = GaussianMixture(
            n_components=self.optimal_k,
            random_state=42,
            covariance_type='full'
        )
        self.rfm['Cluster_GMM'] = self.gmm_model.fit_predict(X_scaled)
        
        # Get probability scores (soft assignment)
        probabilities = self.gmm_model.predict_proba(X_scaled)
        self.rfm['GMM_Confidence'] = probabilities.max(axis=1)
        
        print(f"\n✓ GMM fitted successfully")
        print(f"  BIC Score: {self.gmm_model.bic(X_scaled):,.0f}")
        print(f"  AIC Score: {self.gmm_model.aic(X_scaled):,.0f}")
        print(f"  Avg Confidence: {self.rfm['GMM_Confidence'].mean():.3f}")
        
        # Show cluster distribution
        cluster_counts = self.rfm['Cluster_GMM'].value_counts().sort_index()
        print(f"\n  Cluster Distribution:")
        for cluster, count in cluster_counts.items():
            print(f"    Cluster {cluster}: {count:,} customers ({count/len(self.rfm)*100:.1f}%)")
    
    def analyze_clusters(self, cluster_col='Cluster_KMeans'):
        """Analyze and profile each cluster"""
        print("\n" + "="*80)
        print("CLUSTER PROFILING")
        print("="*80)
        
        # Select base metrics for profiling
        profile_cols = ['Recency', 'Frequency', 'Monetary', 'Tenure', 'AvgOrderValue', 'DiversityIndex']
        available_cols = [col for col in profile_cols if col in self.rfm.columns]
        
        cluster_profiles = self.rfm.groupby(cluster_col)[available_cols].mean().round(2)
        cluster_counts = self.rfm[cluster_col].value_counts().sort_index()
        
        print(f"\nCluster Profiles (using {cluster_col}):")
        print("="*100)
        
        for cluster in sorted(cluster_profiles.index):
            print(f"\nCluster {cluster}: {cluster_counts[cluster]:,} customers ({cluster_counts[cluster]/len(self.rfm)*100:.1f}%)")
            print("-"*100)
            profile = cluster_profiles.loc[cluster]
            for metric, value in profile.items():
                print(f"  {metric:20s}: {value:>12,.2f}")
        
        return cluster_profiles
    
    def feature_importance_analysis(self, cluster_col='Cluster_KMeans'):
        """Use Random Forest to determine feature importance for clusters"""
        print("\n" + "="*80)
        print("FEATURE IMPORTANCE ANALYSIS")
        print("="*80)
        
        X = self.rfm[self.feature_cols].fillna(0)
        y = self.rfm[cluster_col]
        
        # Train Random Forest
        rf = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
        rf.fit(X, y)
        
        # Get feature importance
        importance_df = pd.DataFrame({
            'Feature': self.feature_cols,
            'Importance': rf.feature_importances_
        }).sort_values('Importance', ascending=False)
        
        print("\nTop Features Driving Segmentation:")
        print(importance_df.head(10).to_string(index=False))
        
        return importance_df
    
    def save_results(self, output_path='data/processed/customer_segments_advanced.csv'):
        """Save clustered data"""
        self.rfm.to_csv(output_path)
        print(f"\n✓ Saved clustered data: {output_path}")
        
    def execute_pipeline(self, use_pca=True, fit_gmm=True):
        """Run complete clustering pipeline"""
        self.select_features_for_clustering()
        metrics, results = self.determine_optimal_k()
        
        if use_pca:
            pca_features = self.apply_pca()
            self.rfm = pd.concat([self.rfm, pca_features], axis=1)
        
        self.fit_kmeans(use_pca=use_pca)
        
        if fit_gmm:
            self.fit_gmm(use_pca=use_pca)
        
        self.analyze_clusters('Cluster_KMeans')
        importance = self.feature_importance_analysis('Cluster_KMeans')
        
        return self.rfm, metrics, importance
