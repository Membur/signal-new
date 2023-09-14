import pandas as pd

# Load the CSV file
file_path = 'convertcsv.csv'
df = pd.read_csv(file_path)

# Check if the columns "_key" and "cik_str" exist in the DataFrame
if "_key" in df.columns and "cik_str" in df.columns:
    # Drop the "_key" and "cik_str" columns
    df.drop(columns=["_key", "cik_str"], inplace=True)

    # Save the modified DataFrame back to the CSV file
    df.to_csv(file_path, index=False)
    print("Columns '_key' and 'cik_str' have been removed and the file has been saved.")
else:
    print("Columns '_key' and 'cik_str' not found in the DataFrame.")

# Print the resulting DataFrame
print(df.columns)
