import json

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
    with open("order_book/filled_buy_orders.json", "w") as file:
        json.dump(data, file)
        
def set_unfilled_buy_orders(data):
    # Save to a file
    with open("order_book/unfilled_buy_orders.json", "w") as file:
        json.dump(data, file)
 
def get_filled_buy_orders():
    # Save to a file
    with open("order_book/filled_buy_orders.json", "r") as file:
        data = json.load(file)
    return data  

def get_unfilled_buy_orders():
    # Save to a file
    with open("order_book/unfilled_buy_orders.json", "r") as file:
        data = json.load(file)
    return data

def set_filled_sell_orders(data):
    # Save to a file
    with open("order_book/filled_sell_orders.json", "w") as file:
        json.dump(data, file)
 
def get_unfilled_sell_orders():
    # Save to a file
    with open("order_book/filled_sell_orders.json", "r") as file:
        data = json.load(file)
    return data            
        
def get_sell_orders():
    # Save to a file
    with open("order_book/sell_orders.json", "r") as file:
        data = json.load(file)
    return data
        
def get_buy_orders():
    # Save to a file
    with open("order_book/buy_orders.json", "r") as file:
        data = json.load(file)
    return data