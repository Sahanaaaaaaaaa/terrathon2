import pandas as pd
import os
from carbon_footprint_calculator import CarbonFootprintCalculator
from chroma_db_integration import ChromaDBManager

def main():
    """Process df_2.csv and generate a sample with CF scores, stored in ChromaDB"""
    print("Starting to process df_2.csv...")
    
    # Check if the file exists
    if not os.path.exists('df_2.csv'):
        print("Error: df_2.csv not found. Please make sure the file exists.")
        return
    
    # Initialize the calculator and ChromaDB manager
    calculator = CarbonFootprintCalculator()
    db_manager = ChromaDBManager(collection_name="products_large", persistence_path="./chroma_db")
    
    # Process df_2.csv directly through ChromaDB integration
    print("Processing df_2.csv and storing in ChromaDB...")
    db_manager.csv_to_chroma('df_2.csv')
    
    # Output some statistics
    print(f"Processing complete. Total records: {len(db_manager.products_data)}")
    
    # Calculate average CF score
    cf_scores = [product.get('cf_score', 0) for product in db_manager.products_data]
    if cf_scores:
        avg_cf_score = sum(cf_scores) / len(cf_scores)
        print(f"Average CF Score: {avg_cf_score:.2f}")
    
    # Calculate CF category distribution
    cf_categories = {}
    for product in db_manager.products_data:
        category = product.get('cf_category', 'Unknown')
        cf_categories[category] = cf_categories.get(category, 0) + 1
    
    print(f"CF Category distribution:")
    for category, count in cf_categories.items():
        print(f"- {category}: {count}")
    
    # Calculate average CF score by brand
    brand_cf = {}
    for product in db_manager.products_data:
        brand = product.get('brand', 'unknown')
        if brand not in brand_cf:
            brand_cf[brand] = {'total': 0, 'count': 0}
        
        brand_cf[brand]['total'] += product.get('cf_score', 0)
        brand_cf[brand]['count'] += 1
    
    # Calculate averages and sort
    brand_averages = []
    for brand, data in brand_cf.items():
        if data['count'] > 0:
            avg = data['total'] / data['count']
            brand_averages.append((brand, avg, data['count']))
    
    # Sort by average CF score (lowest first = most sustainable)
    brand_averages.sort(key=lambda x: x[1])
    
    # Display top 10 most sustainable brands (lowest CF scores)
    print("\nTop 10 most sustainable brands:")
    for brand, avg, count in brand_averages[:10]:
        print(f"- {brand}: Avg CF Score = {avg:.2f} ({count} products)")
    
    # Display top 10 least sustainable brands (highest CF scores)
    print("\nTop 10 least sustainable brands:")
    for brand, avg, count in brand_averages[-10:]:
        print(f"- {brand}: Avg CF Score = {avg:.2f} ({count} products)")
    
    # Test a query for a specific brand
    test_brand = brand_averages[0][0]  # Most sustainable brand
    print(f"\nTesting query for brand '{test_brand}':")
    products = db_manager.query_by_brand(test_brand, limit=3)
    for product in products:
        print(f"- {product.get('category_code', 'Unknown')} | CF Score: {product.get('cf_score', 'N/A'):.2f}")
    
    print("\nProcessing and ChromaDB storage complete!")

if __name__ == "__main__":
    main() 