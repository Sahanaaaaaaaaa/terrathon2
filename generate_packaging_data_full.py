import pandas as pd
import random
import csv

# Define realistic options for each attribute based on product categories
packaging_materials = {
    'default': ['Cardboard', 'Plastic', 'Paper'],
    'electronics': ['Plastic', 'Cardboard', 'Foam'],
    'appliances.environment': ['Cardboard', 'Thermacol', 'Plastic'],
    'appliances.kitchen': ['Cardboard', 'Plastic', 'Thermacol'],
    'electronics.video': ['Thermacol', 'Cardboard', 'Foam'],
    'electronics.smartphone': ['Paper', 'Cardboard', 'Plastic'],
    'electronics.tablet': ['Cardboard', 'Plastic', 'Paper'],
    'furniture': ['Cardboard', 'Plastic Wrap', 'Wooden Crate'],
    'accessories': ['Paper', 'Plastic', 'Cardboard'],
    'apparel': ['Paper', 'Plastic', 'Cardboard'],
    'kids': ['Cardboard', 'Paper', 'Plastic'],
    'construction': ['Plastic', 'Cardboard', 'Wooden Crate'],
    'sport': ['Cardboard', 'Plastic', 'Paper'],
    'auto': ['Cardboard', 'Plastic', 'Foam'],
    'computers': ['Foam', 'Cardboard', 'Plastic'],
    'country_yard': ['Wooden Crate', 'Cardboard', 'Plastic']
}

shipping_modes = {
    'default': ['Road', 'Air'],
    'electronics': ['Air', 'Road'],
    'appliances': ['Road', 'Sea'],
    'furniture': ['Road', 'Sea'],
    'accessories': ['Air', 'Road'],
    'apparel': ['Air', 'Road'],
    'construction': ['Road', 'Sea'],
    'sport': ['Air', 'Road'],
    'auto': ['Road', 'Sea'],
    'computers': ['Air', 'Road'],
    'country_yard': ['Road', 'Sea']
}

# Usage duration in years based on product category
usage_duration = {
    'default': [3, 4, 5],
    'electronics.smartphone': [2, 3, 4],
    'electronics.tablet': [3, 4, 5],
    'electronics.notebook': [4, 5, 6],
    'electronics.video.tv': [5, 6, 7, 8, 9, 10],
    'electronics.audio': [3, 4, 5],
    'appliances.kitchen': [6, 7, 8, 9, 10],
    'appliances.environment': [8, 9, 10, 11, 12],
    'furniture': [10, 12, 15, 18, 20],
    'accessories': [2, 3, 4],
    'apparel': [1, 2, 3],
    'kids': [2, 3, 4],
    'construction': [8, 10, 12, 15],
    'sport': [3, 4, 5],
    'auto': [5, 6, 7, 8],
    'computers': [4, 5, 6],
    'country_yard': [3, 4, 5, 6]
}

# Repairability scores (out of 10) based on product category and sometimes brand
repairability_scores = {
    'default': [5, 6, 7],
    'electronics.smartphone': {
        'apple': [3, 4],
        'samsung': [4, 5],
        'xiaomi': [5, 6],
        'huawei': [4, 5],
        'google': [6, 7],
        'default': [4, 5, 6]
    },
    'electronics.notebook': {
        'apple': [4, 5],
        'dell': [7, 8],
        'hp': [6, 7],
        'lenovo': [6, 7],
        'asus': [5, 6],
        'acer': [5, 6],
        'default': [5, 6, 7]
    },
    'appliances.kitchen': [6, 7, 8],
    'appliances.environment': [5, 6, 7, 8],
    'furniture': [6, 7, 8, 9],
    'electronics.video': [5, 6, 7],
    'electronics.audio': [4, 5, 6],
    'accessories': [5, 6, 7],
    'apparel': [2, 3, 4],
    'kids': [3, 4, 5],
    'construction': [7, 8, 9],
    'sport': [5, 6, 7],
    'auto': [6, 7, 8],
    'computers': [5, 6, 7],
    'country_yard': [4, 5, 6]
}

def get_packaging_material(category, brand):
    # Find the most specific category match
    for cat in packaging_materials:
        if category.startswith(cat):
            return random.choice(packaging_materials[cat])
    return random.choice(packaging_materials['default'])

def get_shipping_mode(category, brand):
    # Find the most specific category match
    for cat in shipping_modes:
        if category.startswith(cat):
            return random.choice(shipping_modes[cat])
    return random.choice(shipping_modes['default'])

def get_usage_duration(category, brand):
    # Find the most specific category match
    for cat in usage_duration:
        if category.startswith(cat):
            return random.choice(usage_duration[cat])
    return random.choice(usage_duration['default'])

def get_repairability_score(category, brand):
    # Find the most specific category match
    for cat in repairability_scores:
        if category.startswith(cat):
            # Check if there are brand-specific scores
            if isinstance(repairability_scores[cat], dict):
                if brand in repairability_scores[cat]:
                    return random.choice(repairability_scores[cat][brand])
                else:
                    return random.choice(repairability_scores[cat]['default'])
            else:
                return random.choice(repairability_scores[cat])
    return random.choice(repairability_scores['default'])

# Read the unique combinations
combinations = []
with open('unique_combinations_full.txt', 'r') as f:
    for line in f:
        if line.strip():
            category, brand = line.strip().split(',')
            combinations.append((category, brand))

print(f"Processing {len(combinations)} unique combinations...")

# Generate realistic values for each combination
results = []
for category, brand in combinations:
    packaging = get_packaging_material(category, brand)
    shipping = get_shipping_mode(category, brand)
    duration = get_usage_duration(category, brand)
    repair_score = get_repairability_score(category, brand)
    
    results.append({
        'category_code': category,
        'brand': brand,
        'Packaging Material': packaging,
        'Shipping Mode': shipping,
        'Usage Duration': duration,
        'Repairability Score': repair_score
    })

# Save the results to a CSV file
with open('packaging_data_full.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['category_code', 'brand', 'Packaging Material', 'Shipping Mode', 'Usage Duration', 'Repairability Score'])
    writer.writeheader()
    writer.writerows(results)

print(f"Generated realistic values for {len(results)} combinations and saved to packaging_data_full.csv")

# Display a sample of the results
print("\nSample of generated data:")
sample_size = min(20, len(results))
for i in range(sample_size):
    row = results[i]
    print(f"{row['category_code']}, {row['brand']} -> {row['Packaging Material']}, {row['Shipping Mode']}, {row['Usage Duration']}, {row['Repairability Score']}") 