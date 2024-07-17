import requests
from algobaba.dto.ABRequest import *
from algobaba.dto.ABResponse import *

# Define the endpoint
# TODO:- Make this env driven
def send_buy_order(qty,stock,client):
    order_direction = 'LE'
    url = 'http://localhost:21000/MappedOrderSimple'
    # Define the parameters
    params = ABOrderRequest(SourceSymbol=stock,TransactionType=order_direction,StrategyTag=client,Quantity=qty).to_dict()
    print(params)
    # Send the GET request
    response = requests.get(url, params=params)

    # Check the status code and get the response data
    if response.status_code == 200:
        data = response.json()
        print(data)
        return data
    else:
        print(f'Error: {response.status_code}')
        return None