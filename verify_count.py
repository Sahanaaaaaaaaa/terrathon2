import pandas as pd

# Read the file
df = pd.read_csv('packaging_data_full.csv')

# Print row count
print(f"Row count in packaging_data_full.csv: {len(df)}")

# Verify unique combinations
unique_combos = df[['category_code', 'brand']].drop_duplicates()
print(f"Unique category_code and brand combinations: {len(unique_combos)}") 