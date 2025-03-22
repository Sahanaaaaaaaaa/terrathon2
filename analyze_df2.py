import pandas as pd

# Read the first few rows to understand the structure
print("Reading sample of data...")
sample = pd.read_csv('df_2.csv', nrows=5)
print("Columns:", sample.columns.tolist())

# Extract unique combinations of category_code and brand
print("\nReading full file to extract unique combinations...")
# Use chunks to handle large file
unique_combinations = set()
chunk_size = 100000
chunks = pd.read_csv('df_2.csv', chunksize=chunk_size, usecols=['category_code', 'brand'])

count = 0
for chunk in chunks:
    # Remove any NaN values
    chunk = chunk.dropna(subset=['category_code', 'brand'])
    
    # Get unique combinations in this chunk
    for _, row in chunk.drop_duplicates(['category_code', 'brand']).iterrows():
        unique_combinations.add((row['category_code'], row['brand']))
    
    count += len(chunk)
    print(f"Processed {count} rows...")
    
    # Limit to first 1000 combinations for practicality
    if len(unique_combinations) >= 1000:
        break

# Convert to a list and sort
unique_list = sorted(list(unique_combinations))

# Print number of unique combinations
print(f"\nFound {len(unique_list)} unique category_code and brand combinations")

# Print first 100 combinations
print("\nFirst 100 combinations:")
for i, (category, brand) in enumerate(unique_list[:100]):
    print(f"{i+1}. {category} - {brand}")

# Save all combinations to a file
with open('unique_combinations.txt', 'w') as f:
    for category, brand in unique_list:
        f.write(f"{category},{brand}\n")

print("\nAll combinations saved to 'unique_combinations.txt'") 