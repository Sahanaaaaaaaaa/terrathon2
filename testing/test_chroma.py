import os
import pandas as pd
from chroma_db_integration import ChromaDBManager

def main():
    """Test the ChromaDB integration"""
    print("Testing ChromaDB integration")
    
    # Initialize the ChromaDB manager
    db_manager = ChromaDBManager(
        collection_name="test_products",
        persistence_path="./chroma_db_test"
    )
    
    # Check if data.csv exists, if not, create a small sample
    if not os.path.exists('data.csv'):
        print("Creating sample data.csv for testing")
        create_sample_data()
    
    # Process and import the data
    print("\nImporting data from data.csv to ChromaDB...")
    db_manager.csv_to_chroma('data.csv')
    
    # Test queries
    print("\nTesting queries:")
    
    # Test brand query
    print("\n1. Products by brand 'apple':")
    apple_products = db_manager.query_by_brand('apple', limit=3)
    for product in apple_products:
        print(f"- {product.get('category_code', 'Unknown')} | "
              f"CF Score: {product.get('cf_score', 'N/A'):.2f} | "
              f"Category: {product.get('cf_category', 'Unknown')}")
    
    # Test CF category query
    print("\n2. Low CF products:")
    low_cf_products = db_manager.query_by_cf_category('Low CF', limit=3)
    for product in low_cf_products:
        print(f"- Brand: {product.get('brand', 'Unknown')} | "
              f"{product.get('category_code', 'Unknown')} | "
              f"CF Score: {product.get('cf_score', 'N/A'):.2f}")
    
    # Test alternatives recommendation
    if len(db_manager.ids) > 0:
        test_product_id = db_manager.ids[0]
        print(f"\n3. Sustainable alternatives for product ID: {test_product_id}")
        alternatives = db_manager.get_sustainable_alternatives(test_product_id, limit=3)
        for alt in alternatives:
            print(f"- Brand: {alt.get('brand', 'Unknown')} | "
                  f"{alt.get('category_code', 'Unknown')} | "
                  f"CF Score: {alt.get('cf_score', 'N/A'):.2f}")
    
    print("\nChromaDB integration test completed!")

def create_sample_data():
    """Create a small sample dataset for testing"""
    data = {
        'category_code': ['electronics.laptop', 'electronics.smartphone', 'electronics.tablet',
                          'electronics.laptop', 'electronics.smartphone', 'home.appliance'],
        'brand': ['apple', 'samsung', 'apple', 'dell', 'huawei', 'bosch'],
        'price': [1299.99, 899.99, 599.99, 1099.99, 699.99, 499.99],
        'packaging_material': ['cardboard', 'plastic', 'cardboard', 'cardboard', 'plastic', 'cardboard'],
        'shipping_mode': ['air', 'road', 'air', 'sea', 'air', 'road'],
        'usage_duration': ['3 years', '2 years', '3 years', '5 years', '2 years', '7 years'],
        'repairability_score': [5, 4, 6, 8, 3, 7]
    }
    
    df = pd.DataFrame(data)
    df.to_csv('data.csv', index=False)
    print(f"Created sample data with {len(df)} records")

if __name__ == "__main__":
    main() 