"""
Advanced Market Basket Analysis Module
=======================================
Implements FP-Growth algorithm for efficient association rule mining.

Includes cross-segment analysis and product bundling recommendations.
"""

import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import fpgrowth, association_rules
from mlxtend.preprocessing import TransactionEncoder
import warnings
warnings.filterwarnings('ignore')


class MarketBasketAnalyzer:
    """Advanced market basket analysis with FP-Growth"""
    
    def __init__(self, df_transactions, customer_segments=None):
        self.df = df_transactions
        self.segments = customer_segments
        self.basket = None
        self.frequent_itemsets = None
        self.rules = None
        
    def create_transaction_matrix(self, customer_filter=None):
        """Create binary transaction matrix"""
        
        # Filter customers if specified
        if customer_filter is not None:
            df_filtered = self.df[self.df['Customer ID'].isin(customer_filter)]
        else:
            df_filtered = self.df
        
        # Create basket
        basket = df_filtered.groupby(['Invoice', 'Description'])['Quantity'].sum().unstack().fillna(0)
        self.basket = (basket > 0).astype(int)
        
        return self.basket
    
    def mine_frequent_itemsets(self, min_support=0.02):
        """Mine frequent itemsets using FP-Growth (faster than Apriori)"""
        
        self.frequent_itemsets = fpgrowth(self.basket, min_support=min_support, use_colnames=True)
        
        return self.frequent_itemsets
        itemset_sizes = self.frequent_itemsets['itemsets'].apply(len).value_counts().sort_index()
        print(f"\n  Itemset size distribution:")
        for size, count in itemset_sizes.items():
            print(f"    {size}-item sets: {count}")
        
        return self.frequent_itemsets
    
    def generate_association_rules(self, metric="confidence", min_threshold=0.6):
        """Generate association rules from frequent itemsets"""
        
        self.rules = association_rules(
            self.frequent_itemsets,
            metric=metric,
            min_threshold=min_threshold
        )
        
        # Sort by lift (strongest associations first)
        self.rules = self.rules.sort_values('lift', ascending=False)
        
        return self.rules
    
    def display_top_rules(self, n=15):
        """Display top association rules"""
        print(f"\n🔗 Top {n} Product Associations:")
        print(f"{'Product A':<40} {'→':<3} {'Product B':<40} {'Conf%':<8} {'Lift'}")
        print("-"*100)
        
        for idx, row in self.rules.head(n).iterrows():
            ant = ', '.join(list(row['antecedents']))[:37]
            cons = ', '.join(list(row['consequents']))[:37]
            print(f"{ant:<40} {'→':<3} {cons:<40} {row['confidence']*100:<8.0f} {row['lift']:.1f}×")
    
    def cross_segment_analysis(self, cluster_col='Cluster_KMeans'):
        """Analyze product associations per customer segment"""
        
        if self.segments is None or cluster_col not in self.segments.columns:
            return
        
        segment_rules = {}
        
        for cluster in sorted(self.segments[cluster_col].unique()):
            # Get customers in this cluster
            cluster_customers = self.segments[self.segments[cluster_col] == cluster].index
            
            # Create transaction matrix for this segment
            self.create_transaction_matrix(customer_filter=cluster_customers)
            
            # Mine patterns
            min_support = max(0.01, 0.02 / (len(cluster_customers) / len(self.segments)))
            itemsets = self.mine_frequent_itemsets(min_support=min_support)
            
            if len(itemsets) > 0:
                rules = self.generate_association_rules(min_threshold=0.5)
                segment_rules[cluster] = rules
        
        return segment_rules
    
    def get_recommendations(self, product_name, top_n=5):
        """Get product recommendations for a given product"""
        if self.rules is None or len(self.rules) == 0:
            return pd.DataFrame()
        
        # Find rules where this product is the antecedent
        matching_rules = self.rules[
            self.rules['antecedents'].apply(lambda x: any(product_name.lower() in str(item).lower() for item in x))
        ]
        
        if len(matching_rules) == 0:
            return pd.DataFrame()
        
        # Return top N recommendations
        recommendations = matching_rules.head(top_n)[['consequents', 'confidence', 'lift', 'support']]
        return recommendations
    
    def save_results(self, output_path='data/processed/association_rules_professional.csv'):
        """Save association rules"""
        if self.rules is not None:
            # Convert frozensets to strings for CSV compatibility
            rules_export = self.rules.copy()
            rules_export['antecedents'] = rules_export['antecedents'].apply(lambda x: ', '.join(list(x)))
            rules_export['consequents'] = rules_export['consequents'].apply(lambda x: ', '.join(list(x)))
            
            rules_export.to_csv(output_path, index=False)
            print(f"\n✓ Saved: {output_path}")
    
    def execute_pipeline(self, min_support=0.02, min_confidence=0.6, analyze_segments=True):
        """Run complete market basket analysis pipeline"""
        # Overall analysis
        self.create_transaction_matrix()
        self.mine_frequent_itemsets(min_support=min_support)
        self.generate_association_rules(min_threshold=min_confidence)
        self.display_top_rules(15)
        
        # Cross-segment analysis
        if analyze_segments and self.segments is not None:
            segment_rules = self.cross_segment_analysis()
        
        # Save results
        self.save_results()
        
        return self.rules


def main():
    """Standalone execution for market basket analysis"""
    import os
    
    print("\n" + "█"*80)
    print("MARKET BASKET ANALYSIS - FP-GROWTH ALGORITHM")
    print("█"*80)
    
    # Load data
    print("\n✓ Loading transaction data...")
    
    # Check if clean data exists
    if os.path.exists('data/processed/customer_segments_professional.csv'):
        # Load from processed files
        segments = pd.read_csv('data/processed/customer_segments_professional.csv', index_col=0)
        
        # Need to reload transactions
        import sys
        sys.path.insert(0, 'src')
        from data_processor import DataProcessor
        
        processor = DataProcessor()
        df_transactions = processor.load_data()
        df_transactions = processor.clean_data()
        
        # Initialize analyzer
        analyzer = MarketBasketAnalyzer(df_transactions, segments)
        
        # Get VIP customers (top 2 clusters by average monetary value)
        cluster_col = 'Cluster_KMeans' if 'Cluster_KMeans' in segments.columns else 'Cluster'
        vip_clusters = segments.groupby(cluster_col)['Monetary'].mean().nlargest(2).index
        vip_customers = segments[segments[cluster_col].isin(vip_clusters)].index
        
        print(f"\n🛒 Market Basket Analysis")
        print(f"   VIP Segments: Clusters {list(vip_clusters)} | {len(vip_customers):,} customers")
        
        # Run analysis on VIP segment
        analyzer.create_transaction_matrix(customer_filter=vip_customers)
        itemsets = analyzer.mine_frequent_itemsets(min_support=0.02)
        rules = analyzer.generate_association_rules(min_threshold=0.6)
        
        print(f"   Found: {len(itemsets)} itemsets | {len(rules)} rules | Max Lift: {rules['lift'].max():.1f}×")
        
        analyzer.display_top_rules(20)
        analyzer.save_results()
        
        # Show dashboard link
        import os
        prod_recommender = os.path.abspath('reports/product_recommender.html')
        print(f"\n🛍️  Product Recommender: file://{prod_recommender}")
        print("   💡 Cmd+Click to open\n")
        
    else:
        print("❌ Please run retail_analytics_professional.py first")


if __name__ == '__main__':
    main()
