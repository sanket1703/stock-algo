import csv
import os

def read_csv_to_dict():
    # Define the path to the CSV file
    csv_file_path = os.path.join("Clients", "client_data.csv")
    csv_file_path = "brokers/motilal/helper/Clients/client_data.csv"
    # Initialize an empty dictionary to store client data with client_code as keys
    client_data_dict = {}

    try:
        # Open the CSV file for reading
        with open(csv_file_path, mode='r') as file:
            # Use DictReader to automatically map headers to values
            csv_reader = csv.DictReader(file)
            
            # Iterate over each row in the CSV
            for row in csv_reader:
                # Use client_code as the key, and store the rest of the fields in a sub-dictionary
                client_code = row['client_code']
                
                # Populate the client information dictionary for this client_code
                client_data_dict[client_code] = {
                    'name': row['name'],
                    'password': row['password'],
                    'totp': row['totp'],
                    'api_key': row['api_key'],
                    'pan': row['pan']
                }

        return client_data_dict

    except FileNotFoundError:
        return f"File not found: {csv_file_path}"
    except Exception as e:
        return f"An error occurred: {e}"