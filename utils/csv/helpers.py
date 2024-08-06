import csv
import os

def save_buy_orders(orders):

# Extract the date for the filenames
    date_str = orders['date'].split(' ')[0]

    # Define the parent folder name
    parent_folder = "Daily Buy Orders"

    # Create the parent folder
    os.makedirs(parent_folder, exist_ok=True)

    # Iterate over the names and their records
    for name, records in orders.items():
        if name != 'date':
            # Create a directory for each name within the parent folder
            name_folder = os.path.join(parent_folder, name)
            os.makedirs(name_folder, exist_ok=True)
            
            # Define the CSV file path
            csv_file = os.path.join(name_folder, f'{name}_{date_str}.csv')
            
            # Open the CSV file for writing
            with open(csv_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                
                # Write the header
                writer.writerow(['Order Id', 'Stock', 'Date'])
                
                # Write the data
                for record in records:
                    writer.writerow(list(record) + [orders['date']])
            
            print(f'Data has been written to {csv_file}')
            
def save_sell_orders(orders):

# Extract the date for the filenames
    date_str = orders['date'].split(' ')[0]

    # Define the parent folder name
    parent_folder = "Daily Sell Orders"

    # Create the parent folder
    os.makedirs(parent_folder, exist_ok=True)

    # Iterate over the names and their records
    for name, records in orders.items():
        if name != 'date':
            # Create a directory for each name within the parent folder
            name_folder = os.path.join(parent_folder, name)
            os.makedirs(name_folder, exist_ok=True)
            
            # Define the CSV file path
            csv_file = os.path.join(name_folder, f'{name}_{date_str}.csv')
            
            # Open the CSV file for writing
            with open(csv_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                
                # Write the header
                writer.writerow(['Order Id', 'Stock', 'Date'])
                
                # Write the data
                for record in records:
                    writer.writerow(list(record) + [orders['date']])
            
            print(f'Data has been written to {csv_file}')
