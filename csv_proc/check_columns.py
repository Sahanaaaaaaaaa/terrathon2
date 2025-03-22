import pandas as pd

# Just read the first few rows to get column names
print("Reading column names from df_2.csv...")
df_sample = pd.read_csv('df_2.csv', nrows=5)

# Display column names
print("\nColumns in df_2.csv:")
for i, col in enumerate(df_sample.columns):
    print(f"{i+1}. {col}") 