from stock_data.price import fetch_stock_data, get_last_traded_price
import math

def get_available_balance(client):
    return 13000000

def reduce_balance(client,amount):
    current_balance = get_available_balance(client)
    current_balance -= amount
    update_balance(client,current_balance)
    
def add_balance(client,amount):
    current_balance = get_available_balance(client)
    current_balance += amount
    update_balance(client,current_balance)
    
def update_balance(client,amount):
    print("New Balance is")
    

def send_buy_order(buy_stock,qty,client):
    print("Order sent for: ")
    print(buy_stock,qty,client)
    price_bought = 10
    return price_bought
    
def calculate_brokerage():
    return 10

def position_sizing(final_buy_stocks,total_available_slots_before_buy,client):
    
    for buy_stock in final_buy_stocks:
        total_available_capital = get_available_balance()
        amount_to_invest = total_available_capital/total_available_slots_before_buy
        
        last_traded_price = get_last_traded_price(buy_stock)
        qty = math.floor(amount_to_invest/last_traded_price)
        price = send_buy_order(buy_stock,qty,client)
        turnover = (qty*last_traded_price + calculate_brokerage())
        print("Stock: {stock} Price_buy {price} Quantity {qty} Amount to Invest {amount_to_invest}")
        reduce_balance(client,turnover)
        total_available_slots_before_buy -=1
        
if __name__ == '__main__':
    print