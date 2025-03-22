import pandas as pd
import os

print("Reading df_2.csv in chunks...")
# Use chunks to handle large file
chunk_size = 100000
chunks = pd.read_csv('df_2.csv', chunksize=chunk_size)

# Columns to remove
columns_to_remove = [
    'Packaging Material', 
    'Shipping Mode', 
    'Usage Duration', 
    'Repairability Score'
]

# Create a new file name
output_file = 'df_2_modified.csv'

# Process chunks and write to new file
first_chunk = True
count = 0

for i, chunk in enumerate(chunks):
    # Remove the columns
    for col in columns_to_remove:
        if col in chunk.columns:
            chunk = chunk.drop(columns=[col])
    
    # Write to file (first chunk with header, others appended)
    if first_chunk:
        chunk.to_csv(output_file, index=False)
        first_chunk = False
    else:
        chunk.to_csv(output_file, mode='a', header=False, index=False)
    
    count += len(chunk)
    print(f"Processed {count} rows...")

print(f"\nFinished processing. New file created: {output_file}")
print(f"Original file size: {os.path.getsize('df_2.csv') / (1024 * 1024):.2f} MB")
print(f"Modified file size: {os.path.getsize(output_file) / (1024 * 1024):.2f} MB") 