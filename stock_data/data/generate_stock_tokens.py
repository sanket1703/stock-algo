import pandas as pd
import json

# Load the CSV file into a pandas DataFrame
csv_file_path = "instruments.csv"  # Update this path if necessary
df = pd.read_csv(csv_file_path)

# Filter rows where instrument_type is "EQ" and segment is "NSE"
filtered_df = df[(df['instrument_type'] == 'EQ') & (df['segment'] == 'NSE')]

# Create a dictionary with tradingsymbol as key and exchange_token as value
instrument_dict = dict(zip(filtered_df['tradingsymbol'], filtered_df['exchange_token']))

# Save the dictionary to a JSON file named output.json
output_json_path = "output.json"
with open(output_json_path, "w") as json_file:
    json.dump(instrument_dict, json_file, indent=4)

print("Filtered data saved to output.json.")
