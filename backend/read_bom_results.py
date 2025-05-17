import os
import pandas as pd
from pathlib import Path


def read_bom_results(directory_path):
    results = {}
    all_partnumbers = []
    # Ensure the directory path exists
    if not os.path.exists(directory_path):
        print(f"Directory not found: {directory_path}")
        return results, all_partnumbers
    
    # Get all CSV files in the directory
    csv_files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]
    
    # Read each CSV file into a pandas DataFrame
    for file in csv_files:
        file_path = os.path.join(directory_path, file)
        try:
            df = pd.read_csv(file_path)
            # Store the DataFrame with the filename (without extension) as the key
            results[os.path.splitext(file)[0]] = df
            print(f"Successfully read {file} with {len(df)} rows")
            
            # Extract partnumbers for each component
            if 'partnumber' in df.columns:
                file_partnumbers = df['partnumber'].tolist()
                print(len(file_partnumbers[0]))
                all_partnumbers.extend(file_partnumbers)
                print(f"Added {len(file_partnumbers)} partnumbers from {file}")
            else:
                print(f"\nNo partnumber column found in {file}")
                
        except Exception as e:
            print(f"Error reading {file}: {e}")
    for i in all_partnumbers:
        all_partnumbers.remove(i) if len(i) < 5 else None
    return results, all_partnumbers
