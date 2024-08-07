import requests
from algobaba.dto.ABRequest import *
from algobaba.dto.ABResponse import *

port = 21000

def is_order_completed(request_id):
    url = f'http://localhost:{port}/isOrderCompleted'
    # print(url)
    # Define the parameters
    params = ABOrderStatusRequest(request_id=request_id).to_dict()
    # print(params)
    # Send the GET request
    response = requests.get(url, params=params)
    # print(response)
    # Check the status code and get the response data
    if response.status_code == 200 and response.json()["status"] == "success":
        data = response.json()
        return data["response"]== "true"

def order_status(request_id):
    url = f'http://localhost:{port}/OrderStatus'
    # Define the parameters
    # print(url)
    params = ABOrderStatusRequest(request_id=request_id).to_dict()
    # print(params)
    # Send the GET request
    response = requests.get(url, params=params)

    # Check the status code and get the response data
    if response.status_code == 200 and response.json()["status"] == "success":
        data = response.json()
        return data["status"]
    else:
        if response.status_code == 200:
            return "Trading Not Started/Out of Market hours"
        print(f'Error: {response.status_code}')
        return "SystemError"

def get_trade_price(request_id):
    url = f'http://localhost:{port}/OrderAvgPrice'
    # Define the parameters
    # print(url)
    params = ABOrderStatusRequest(request_id=request_id).to_dict()
    # print(params)
    # Send the GET request
    response = requests.get(url, params=params)

    # Check the status code and get the response data
    if response.status_code == 200 and response.json()["status"] == "success":
        data = response.json()
        return data['response']
    else:
        if response.status_code == 200:
            return "Trading Not Started/Out of Market hours"
        print(f'Error: {response.status_code}')
        return "SystemError"
    
def get_trade_qty(request_id):
    url = f'http://localhost:{port}/OrderFilledQty'
    # Define the parameters
    # print(url)
    params = ABOrderStatusRequest(request_id=request_id).to_dict()
    # print(params)
    # Send the GET request
    response = requests.get(url, params=params)

    # Check the status code and get the response data
    if response.status_code == 200 and response.json()["status"] == "success":
        data = response.json()
        return int(data['response'])
    else:
        if response.status_code == 200:
            return "Trading Not Started/Out of Market hours"
        print(f'Error: {response.status_code}')
        return "SystemError"
    