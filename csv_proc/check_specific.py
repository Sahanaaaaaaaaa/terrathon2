import pandas as pd

# Read the generated data
df = pd.read_csv('packaging_data.csv')

# Check specific categories
categories_to_check = [
    'electronics.smartphone', 
    'electronics.tablet', 
    'electronics.notebook',
    'appliances.kitchen.coffee_machine',
    'furniture.kitchen.table'
]

for category in categories_to_check:
    cat_data = df[df['category_code'] == category]
    if cat_data.empty:
        # Try with startswith
        cat_data = df[df['category_code'].str.startswith(category)]
    
    if not cat_data.empty:
        print(f"\n{category} ({len(cat_data)} entries):")
        print(cat_data[['brand', 'Packaging Material', 'Shipping Mode', 'Usage Duration', 'Repairability Score']].head(10).to_string(index=False)) 