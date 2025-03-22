import pandas as pd

# Read the generated data
df = pd.read_csv('packaging_data.csv')

# Print basic statistics
print(f"Total number of combinations: {len(df)}")

# Display counts of each packaging material
print("\nPackaging Material Distribution:")
print(df['Packaging Material'].value_counts())

# Display counts of each shipping mode
print("\nShipping Mode Distribution:")
print(df['Shipping Mode'].value_counts())

# Display average usage duration by high-level category
print("\nAverage Usage Duration by Category:")
df['high_level_category'] = df['category_code'].apply(lambda x: x.split('.')[0])
print(df.groupby('high_level_category')['Usage Duration'].mean().sort_values(ascending=False))

# Display average repairability by high-level category
print("\nAverage Repairability Score by Category:")
print(df.groupby('high_level_category')['Repairability Score'].mean().sort_values(ascending=False))

# Check specific categories
categories_to_check = [
    'electronics.smartphone', 
    'electronics.tablet', 
    'electronics.notebook',
    'appliances.kitchen',
    'furniture'
]

print("\nSamples from specific categories:")
for category in categories_to_check:
    cat_data = df[df['category_code'].str.startswith(category)]
    if not cat_data.empty:
        print(f"\n{category} ({len(cat_data)} entries):")
        print(cat_data.head(5).to_string(index=False)) 