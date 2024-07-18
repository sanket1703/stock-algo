import requests
from algobaba.dto.ABRequest import *
from algobaba.dto.ABResponse import *

def is_order_completed(request_id):
    url = 'http://localhost:21000/isOrdercompleted'
    # Define the parameters
    params = ABOrderStatusRequest(request_id=request_id).to_dict()
    print(params)
    # Send the GET request
    response = requests.get(url, params=params)

    # Check the status code and get the response data
    if response.status_code == 200 and response.status == "success":
        data = response.json()
        return data.response
    else:
        print(f'Error: {response.status_code}')
        if response.status_code == 200:
            return "Trading Not Started/Out of Market hours"
        return "SystemError"

def order_status(request_id):
    url = 'http://localhost:21000/OrderStatus'
    # Define the parameters
    params = ABOrderStatusRequest(request_id=request_id).to_dict()
    print(params)
    # Send the GET request
    response = requests.get(url, params=params)

    # Check the status code and get the response data
    if response.status_code == 200 and response.status == "success":
        data = response.json()
        return data.response
    else:
        if response.status_code == 200:
            return "Trading Not Started/Out of Market hours"
        print(f'Error: {response.status_code}')
        return "SystemError"

def get_trade_price(request_id):
    url = 'http://localhost:21000/OrderAvgPrice'
    # Define the parameters
    params = ABOrderStatusRequest(request_id=request_id).to_dict()
    print(params)
    # Send the GET request
    response = requests.get(url, params=params)

    # Check the status code and get the response data
    if response.status_code == 200 and response.status == "success":
        data = response.json()
        return data.response
    else:
        if response.status_code == 200:
            return "Trading Not Started/Out of Market hours"
        print(f'Error: {response.status_code}')
        return "SystemError"
    
def get_trade_qty(request_id):
    url = 'http://localhost:21000/OrderFilledQty'
    # Define the parameters
    params = ABOrderStatusRequest(request_id=request_id).to_dict()
    print(params)
    # Send the GET request
    response = requests.get(url, params=params)

    # Check the status code and get the response data
    if response.status_code == 200 and response.status == "success":
        data = response.json()
        return data.response
    else:
        if response.status_code == 200:
            return "Trading Not Started/Out of Market hours"
        print(f'Error: {response.status_code}')
        return "SystemError"
    