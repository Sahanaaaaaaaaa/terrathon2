import pandas as pd

# Just read the first row to get column names
print("Reading column names from df_2.csv...")
df_sample = pd.read_csv('df_2.csv', nrows=1)

# Get the column names as a list
column_names = df_sample.columns.tolist()

# Print total number of columns
print(f"\nTotal number of columns: {len(column_names)}")

# Display column names
print("\nColumns in df_2.csv:")
for i, col in enumerate(column_names):
    print(f"{i+1}. {col}")
    
# Also check if the modified file has different columns
print("\nChecking columns in df_2_modified.csv...")
modified_sample = pd.read_csv('df_2_modified.csv', nrows=1)
modified_cols = modified_sample.columns.tolist()

print(f"\nTotal number of columns in df_2_modified.csv: {len(modified_cols)}")

# Display column names of modified file
print("\nColumns in df_2_modified.csv:")
for i, col in enumerate(modified_cols):
    print(f"{i+1}. {col}")
    
# Find columns that differ
removed_cols = [col for col in column_names if col not in modified_cols]
print(f"\nColumns removed from df_2.csv: {removed_cols}") 