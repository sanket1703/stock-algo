from tinydb import TinyDB,Query
from database.dto.clients import *

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

