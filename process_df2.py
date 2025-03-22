import pandas as pd
from carbon_footprint_calculator import CarbonFootprintCalculator

def main():
    """Process df_2.csv and generate a sample with CF scores"""
    print("Starting to process df_2.csv...")
    
    # Initialize the calculator
    calculator = CarbonFootprintCalculator()
    
    # Process df_2.csv
    result_df = calculator.process_dataset('df_2.csv')
    
    # Save the results
    output_file = 'df_2_with_cf_scores.csv'
    result_df.to_csv(output_file, index=False)
    
    print(f"Processing complete. Results saved to {output_file}")
    print(f"Sample size: {len(result_df)} rows")
    print(f"Average CF Score: {result_df['cf_score'].mean():.2f}")
    print(f"CF Category distribution:")
    print(result_df['cf_category'].value_counts())
    
    # Also generate the brand CF statistics
    print("\nCalculating average CF score by brand...")
    brand_cf = result_df.groupby('brand')['cf_score'].agg(['mean', 'count']).sort_values('mean')
    brand_cf.columns = ['Avg CF Score', 'Count']
    
    # Display top 10 most sustainable brands (lowest CF scores)
    print("\nTop 10 most sustainable brands:")
    print(brand_cf.head(10))
    
    # Display top 10 least sustainable brands (highest CF scores)
    print("\nTop 10 least sustainable brands:")
    print(brand_cf.tail(10))
    
    # Save brand statistics
    brand_cf.to_csv('brand_cf_statistics.csv')
    print("\nBrand statistics saved to brand_cf_statistics.csv")

if __name__ == "__main__":
    main() 