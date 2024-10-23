import pyotp
from brokers.motilal.api.MOFSLOPENAPI import MOFSLOPENAPI
from brokers.motilal.helper.read_client_data import read_csv_to_dict
from loguru import logger

def client_login(client_code):
    clients_auth = read_csv_to_dict()
    client_auth_data= clients_auth[client_code]
    Base_Url = "https://142.79.250.93"
    ApiKey = client_auth_data['api_key']
    userid = client_code
    password = client_auth_data['password']
    Two_FA = client_auth_data['pan']
    vendorinfo = client_code
    clientcode = None
    SourceID = "Desktop"
    browsername = "chrome"
    browserversion = "104"   
    totp = client_auth_data['totp']
    totp = pyotp.TOTP(totp).now()
    Mofsl = MOFSLOPENAPI(ApiKey, Base_Url, clientcode, SourceID, browsername, browserversion)
    Mofsl.login(userid, password, Two_FA, totp, vendorinfo)
    logger.debug(f"Login Completed for {client_code}")
    return Mofsl