from tinydb import TinyDB,Query
from database.dto.clients import Client, DailyTradeLog, Holding
from database.dto.slots import Slots
from datetime import datetime 
from utils.enums.signal import Signal
from database.dao.slots_dao import get_slots, update_slots

from stock_data.price import fetch_stock_data, get_last_traded_price
import math

def get_slots():
    db = TinyDB('database/tinydb/db.json')
    slots = TinyDB.table(db,'slots')
    current_slots = slots.all()[0]['slots']
    return current_slots
    

def update_slots(update_slots):
    db = TinyDB('database/tinydb/db.json')
    slots = TinyDB.table(db,'slots')
    query = Query()
    slots.update({'slots': update_slots})  # Replace "list_field_name" with the name of the list field
    db.close()
    return update_slots
    

def convert_to_dict(obj):
    # If obj is a class instance, convert its attributes to a dictionary
    if isinstance(obj, (Client, Slots,DailyTradeLog, Holding)):
        return {key: convert_to_dict(value) if isinstance(value, (Client, Slots,DailyTradeLog,Holding)) else value
                for key, value in obj.__dict__.items()}
    # If obj is a list, recursively convert each item in the list
    elif isinstance(obj, list):
        return [convert_to_dict(item) for item in obj]
    else:
        return obj
    
def get_client_balance(client_code):
    
    db = TinyDB('database/tinydb/db.json')
    client_table = TinyDB.table(db,'clients')
    client = Query()
    result = client_table.search(client.client_code == client_code)
    client_balance = result[0].get('current_balance')
    db.close()
    return client_balance

def update_client_balance(client_code,new_balance):
    db = TinyDB('database/tinydb/db.json')
    client_table = TinyDB.table(db,'clients')
    client = Query()
    client_table.update({'current_balance': new_balance}, client.client_code == client_code)
    db.close()
    return new_balance

def update_holding(client_code,stock_name,qty,price,date):
    db = TinyDB('database/tinydb/db.json')
    client_table = TinyDB.table(db,'clients')
    client = Query()
    result = client_table.search(client.client_code == client_code)
    holding = result[0].get('holding')
    holding[stock_name] = Holding(stock_name,qty,date,price).to_json()
    client_table.update({'holding': holding}, client.client_code == client_code)
    db.close()
    
def add_trade_log(client_code,date,stock_name,direction,price,qty,balance_before_trade):
    db = TinyDB('database/tinydb/db.json')
    client_table = TinyDB.table(db,'clients')
    client = Query()
    result = client_table.search(client.client_code == client_code)
    trade_log = result[0].get('daily_trade_log')
    new_trade_log = DailyTradeLog(date,stock_name,direction,price,qty,balance_before_trade).to_list()
    trade_log.append(new_trade_log)
    client_table.update({'daily_trade_log': trade_log}, client.client_code == client_code)
    db.close()


def reduce_balance(client,amount):
    current_balance = get_client_balance(client)
    new_balance = current_balance - amount
    update_client_balance(client,new_balance)
    
def add_balance(client,amount):
    current_balance = get_client_balance(client)
    new_balance = current_balance + amount
    update_client_balance(client,new_balance)

def send_buy_order(buy_stock,qty,client,last_traded_price):
    print(f"Order sent for: Stock {buy_stock} for Qty {qty} for Client {client} at approx price {last_traded_price}")
    return last_traded_price
    
def calculate_brokerage():
    return 10

def position_sizing(final_buy_stocks,total_available_slots_before_buy,client):
    
    for buy_stock in final_buy_stocks:
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total_available_capital = get_client_balance(client)
        amount_to_invest = total_available_capital/total_available_slots_before_buy
        
        last_traded_price = get_last_traded_price(fetch_stock_data(buy_stock))
        qty = math.floor(amount_to_invest/last_traded_price)
        price = send_buy_order(buy_stock,qty,client,last_traded_price)
        turnover = (qty*last_traded_price + calculate_brokerage())
        update_holding(client,buy_stock,qty,last_traded_price,current_datetime)
        add_trade_log(client,current_datetime,buy_stock,Signal.BUY.value,last_traded_price,qty,total_available_capital)
        
        print(f"Stock: {buy_stock} Price_buy {price} Quantity {qty} Amount to Invest {amount_to_invest}")
        reduce_balance(client,turnover)
        total_available_slots_before_buy -=1

if __name__ == '__main__':
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    stocks = ['LUPIN.NS','INDHOTEL.NS','POLYCAB.NS','PERSISTENT.NS','CUMMINSIND.NS']
    position_sizing(stocks,13,123)
    get_slots()

    