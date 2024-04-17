from tinydb import TinyDB,Query
from database.dto.clients import Client, DailyTradeLog, Holding
from database.dto.slots import Slots
from datetime import datetime 
from utils.enums.signal import Signal
from database.dao_tiny.slots_dao import get_slots, update_slots
from database.dao_tiny.watchlist_dao import *
from stock_data.price import fetch_stock_data, get_last_traded_price
import math
import boto3


def get_client_holding_stock(client_code,stock_name):
    db = TinyDB('database/tinydb/db.json')
    client_table = TinyDB.table(db,'clients')
    client = Query()
    result = client_table.search(client.client_code == client_code)
    client_balance = result[0].get('holding')[stock_name]
    db.close()
    return client_balance

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
    
def send_sell_order(stock_name,client_code):
    holding = get_client_holding_stock(client_code,stock_name)
    print(f"Sell Order placed for {holding['stock_name']}")
    
def offload_holding(client_code,stock_name):
    db = TinyDB('database/tinydb/db.json')
    client_table = TinyDB.table(db,'clients')
    client = Query()
    result = client_table.search(client.client_code == client_code)
    holding = result[0].get('holding')
    del holding[stock_name]
    client_table.update({'holding': holding}, client.client_code == client_code)
    db.close()

def get_db_snapshot():
    db = TinyDB('database/tinydb/db.json')
    client_table = TinyDB.table(db,'clients')
    slots_table = TinyDB.table(db,'slots')
    snapshot = {}
    snapshot["Clients"] = client_table.all()
    snapshot["Slots"] = slots_table.all()
    return snapshot


def get_watchlist():
    db = TinyDB('database/tinydb/db.json')
    watchlist = TinyDB.table(db,'watchlist')
    cuurent_watchlist = watchlist.all()[0]['watchlist']
    return cuurent_watchlist
    

def update_watchlist(update_watchlist):
    db = TinyDB('database/tinydb/db.json')
    watchlist = TinyDB.table(db,'watchlist')
    watchlist.update({'watchlist': update_watchlist}) 
    db.close()
    return update_watchlist


from tinydb import TinyDB

def get_watchlist():
    db = TinyDB('database/tinydb/db.json')
    watchlist = TinyDB.table(db,'watchlist')
    cuurent_watchlist = watchlist.all()[0]['watchlist']
    return cuurent_watchlist
    

def update_watchlist(update_watchlist):
    db = TinyDB('database/tinydb/db.json')
    watchlist = TinyDB.table(db,'watchlist')
    watchlist.update({'watchlist': update_watchlist}) 
    db.close()
    return update_watchlist

def get_watchlist(db):

    watchlist = db.Table('watchlist')
    curent_watchlist = watchlist.scan()['Items'][0]['watchlist']
    return curent_watchlist
    

def update_watchlist(db,update_watchlist):

    watchlist = db.Table('watchlist')
    key = {"watchlist_id":"1"}
    response = watchlist.get_item(Key=key)
    print(response)
    response['Item']['watchlist'] = update_watchlist
    watchlist.put_item(Item = response['Item'])
    
    

def get_slots(db):
    slots = db.Table('stock_slots')
    current_slots = slots.scan()['Items'][0]['stock_slots']
    return current_slots
    

def update_slots(db,update_slots):
    
    slots = db.Table('stock_slots')
    key = {"stock_slots_id":"1"}
    response = slots.get_item(Key=key)
    print(response)
    response['Item']['stock_slots'] = update_slots
    slots.put_item(Item = response['Item'])
    return update_slots

def get_client_holding_stock(client_code,stock_name):
    db = TinyDB('database/tinydb/db.json')
    client_table = TinyDB.table(db,'clients')
    client = Query()
    result = client_table.search(client.client_code == client_code)
    client_balance = result[0].get('holding')[stock_name]
    db.close()
    return client_balance

def get_client_balance(db,client_code):
    
    clients = db.Table('clients')
    response = clients.scan(FilterExpression=boto3.dynamodb.conditions.Attr('client_code').eq(client_code))
    client_balance = response['Items'][0]['current_balance']
    return client_balance

def update_client_balance(db,client_code,new_balance):
    clients = db.Table('clients')
    response = clients.scan(FilterExpression=boto3.dynamodb.conditions.Attr('client_code').eq(client_code))
    response['Items'][0]['current_balance'] = new_balance
    clients.put_item(Item=response['Items'][0])
    return new_balance

def update_holding(db,client_code,stock_name,qty,price,date):
    clients = db.Table('clients')
    response = clients.scan(FilterExpression=boto3.dynamodb.conditions.Attr('client_code').eq(client_code))
    response['Items'][0]['holding'][stock_name] = Holding(stock_name,qty,date,price).to_json()
    clients.put_item(Item=response['Items'][0])
    
    
def offload_holding(db,client_code,stock_name):
    clients = db.Table('clients')
    response = clients.scan(FilterExpression=boto3.dynamodb.conditions.Attr('client_code').eq(client_code))
    del response['Items'][0]['holding'][stock_name]
    clients.put_item(Item=response['Items'][0])
    
def add_trade_log(db,client_code,date,stock_name,direction,price,qty,balance_before_trade):
    clients = db.Table('clients')
    response = clients.scan(FilterExpression=boto3.dynamodb.conditions.Attr('client_code').eq(client_code))
    response['Items'][0]['daily_trade_log'].append(DailyTradeLog(date,stock_name,direction,price,qty,balance_before_trade).to_list())
    clients.put_item(Item=response['Items'][0])


def get_database():
    
    aws_access_key_id = 'AKIAW3MEAN3TBZIFTCE6'
    aws_secret_access_key = 'Ad2nS01Iioxl4cfqqDsXWBAoPd4SJRMqwdPpdFbj'

    # Create a DynamoDB resource object with your credentials
    dynamodb = boto3.resource(
        'dynamodb',
        region_name='ap-south-1',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key)
    
    return dynamodb

if __name__ == '__main__':
    # current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # stocks = ['LUPIN.NS','INDHOTEL.NS','POLYCAB.NS','PERSISTENT.NS','CUMMINSIND.NS']
    # position_sizing(stocks,13,123)
    # get_slots()
    # print(send_sell_order('OFSS.NS',123))
    # print(get_client_holding_stock(123,'OFSS.NS'))
    db = get_database()
    # get_client_balance(db,"")
    # update_holding()
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # update_client_balance(db,"Sanket",4)
    # update_holding(db,"Sanket","OFSS.NS",5,123,current_datetime)
    # offload_holding(db,"Sanket","OFSS.NS")
    add_trade_log(db,"Sanket",current_datetime,"OFSS.NS","Buy",1,1,1)
    # print(table)
    # print(update_watchlist(['LUPIN.NS','INDHOTEL.NS','POLYCAB.NS','PERSISTENT.NS','CUMMINSIND.NS','ZYDUSLIFE.NS','RECLTD.NS','ABBOTINDIA.NS','TVSMOTOR.NS','AUBANK.NS','LTTS.NS','GUJGASLTD.NS','OFSS.NS','COFORGE.NS','ALKEM.NS','AUROPHARMA.NS','HONAUT.NS','ASTRAL.NS','BALKRISIND.NS','MPHASIS.NS']))
    