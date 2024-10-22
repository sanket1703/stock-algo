import gspread
from google.oauth2.service_account import Credentials


def gsheets_auth():
    
    # Path to your service account JSON file
    SERVICE_ACCOUNT_FILE = 'utils/gsheets/security/fortune-alpha13-85b1cfd528ce.json'

    # Define the scope
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']

    # Create credentials
    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # Authorize gspread client
    return gspread.authorize(credentials)