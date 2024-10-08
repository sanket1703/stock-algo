import pyotp
from brokers.motilal.api.MOFSLOPENAPI import MOFSLOPENAPI

def client_login(client_data,client_code ):
    print(f"Client Data {client_data}")
    Base_Url = "https://openapi.motilaloswaluat.com"
    ApiKey = client_data['api_key']
    userid = client_code
    password = client_data['password']
    Two_FA = client_data['pan']
    vendorinfo = client_code
    clientcode = None
    SourceID = "Desktop"
    browsername = "chrome"
    browserversion = "104"   
    totp = client_data['totp']
    totp = pyotp.TOTP(totp).now()
    Mofsl = MOFSLOPENAPI(ApiKey, Base_Url, clientcode, SourceID, browsername, browserversion)
    print("--------------------------------Login--------------------------------")
    Mofsl.login(userid, password, Two_FA, totp, vendorinfo)
    return Mofsl