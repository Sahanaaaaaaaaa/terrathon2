import pandas as pd

# Read the original data
print("Reading df_2.csv...")
# Use chunks to handle large file
chunk_size = 100000
chunks = pd.read_csv('df_2.csv', chunksize=chunk_size)

# Create a set of all unique combinations from df_2
all_combinations = set()
count = 0
for chunk in chunks:
    # Create candidate keys - use proper null handling 
    chunk['brand'] = chunk['brand'].fillna('none')
    chunk['category_code'] = chunk['category_code'].fillna('none')
    
    # Add to set
    for _, row in chunk.iterrows():
        all_combinations.add((row['category_code'], row['brand']))
    
    count += len(chunk)
    print(f"Processed {count} rows...")

# Read our packaging data
packaging_data = pd.read_csv('packaging_data.csv')
packaging_combinations = set(zip(packaging_data['category_code'], packaging_data['brand']))

# Compare counts
print(f"\nTotal unique combinations in df_2.csv: {len(all_combinations)}")
print(f"Total combinations in packaging_data.csv: {len(packaging_combinations)}")

# Check for differences
print("\nAnalyzing differences...")
missing_combinations = all_combinations - packaging_combinations

print(f"Number of missing combinations: {len(missing_combinations)}")

# Print some examples of missing combinations
print("\nExamples of missing combinations:")
for i, combo in enumerate(list(missing_combinations)[:20]):
    print(f"{i+1}. {combo[0]}, {combo[1]}")

# Check if null values might be the issue
print("\nChecking for null values in combinations...")
# Use chunks again
chunks = pd.read_csv('df_2.csv', chunksize=chunk_size)
null_category = 0
null_brand = 0
null_both = 0

for chunk in chunks:
    null_category += chunk['category_code'].isna().sum()
    null_brand += chunk['brand'].isna().sum()
    null_both += ((chunk['category_code'].isna()) & (chunk['brand'].isna())).sum()

print(f"Rows with null category_code: {null_category}")
print(f"Rows with null brand: {null_brand}")
print(f"Rows with both values null: {null_both}") 