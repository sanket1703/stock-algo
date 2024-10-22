from utils.gsheets.security.connect import gsheets_auth


def add_text():
    
    gc = gsheets_auth()
    
    spreadsheet = gc.open('Voucher Ledger')  # Or use gc.open_by_url('Your Spreadsheet URL')

    # Select a worksheet
    worksheet = spreadsheet.sheet1  # You can also use spreadsheet.get_worksheet(index)

    # Read data from a cell
    cell_value = worksheet.cell(1, 1).value  # Read value from cell A1
    print(f'Value in A1: {cell_value}')

    # Write data to a cell
    worksheet.update('A1', [['Alouette gente alouette']])  # Update cell A1 with new value