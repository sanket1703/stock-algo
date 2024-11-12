import json
import os
from loguru import logger
def set_buy_orders(data):
    # Save to a file
    with open("order_book/buy_orders.json", "w") as file:
        json.dump(data, file)

def set_sell_orders(data):
    # Save to a file
    with open("order_book/sell_orders.json", "w") as file:
        json.dump(data, file)
        
def set_filled_buy_orders(data):
    # Save to a file
    with open("order_book/filled_orders/filled_buy_orders.json", "w") as file:
        json.dump(data, file)
        
def set_unfilled_buy_orders(data):
    # Save to a file
    with open("order_book/unfilled_orders/unfilled_buy_orders.json", "w") as file:
        json.dump(data, file)
 
def get_filled_buy_orders():
    # Save to a file
    if os.stat('order_book/filled_orders/filled_buy_orders.json').st_size == 0:
        logger.debug("No filled buy orders")
        return {}
    with open("order_book/filled_orders/filled_buy_orders.json", "r") as file:
        data = json.load(file)
    return data  

def get_unfilled_buy_orders():
    # Save to a file
    if os.stat('order_book/unfilled_orders/unfilled_buy_orders.json').st_size == 0:
        logger.debug("No unfilled buy orders")
        return {}
    with open("order_book/unfilled_orders/unfilled_buy_orders.json", "r") as file:
        data = json.load(file)
    return data

def set_filled_sell_orders(data):
    # Save to a file
    with open("order_book/filled_orders/filled_sell_orders.json", "w") as file:
        json.dump(data, file)
 
def get_filled_sell_orders():
    # Save to a file
    if os.stat('order_book/filled_orders/filled_sell_orders.json').st_size == 0:
        logger.debug("No filled sell orders")
        return {}
    with open("order_book/filled_orders/filled_sell_orders.json", "r") as file:
            data = json.load(file)
    return data            
        
def set_unfilled_sell_orders(data):
    # Save to a file
    with open("order_book/unfilled_orders/unfilled_sell_orders.json", "w") as file:
        json.dump(data, file)  

def get_unfilled_sell_orders():
    # Save to a file
    if os.stat('order_book/unfilled_orders/unfilled_sell_orders.json').st_size == 0:
        logger.debug("No unfilled sell orders")
        return {}
    with open("order_book/unfilled_orders/unfilled_sell_orders.json", "r") as file:
        data = json.load(file)
    return data   


def get_sell_orders():
    # Save to a file
    if os.stat('order_book/sell_orders.json').st_size == 0:
        raise ValueError("No Sell orders")
    with open("order_book/sell_orders.json", "r") as file:
        data = json.load(file)
    return data
        
def get_buy_orders():
    # Save to a file
    if os.stat('order_book/buy_orders.json').st_size == 0:
        raise ValueError("No buy orders")
    with open("order_book/buy_orders.json", "r") as file:
        data = json.load(file)
    return data


def get_orders():
    # Save to a file
    if os.stat('order_book/orders.json').st_size == 0:
        raise ValueError("No buy orders")
    with open("order_book/orders.json", "r") as file:
        data = json.load(file)
    return data["orders"]
