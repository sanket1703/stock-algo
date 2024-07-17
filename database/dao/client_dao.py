from database.dto.clients import *
import boto3

def get_client_holding_stock(db, client_code,stock_name):
    clients = db.Table('clients')
    response = clients.scan(FilterExpression=boto3.dynamodb.conditions.Attr('client_code').eq(client_code))
    client_balance = response['Items'][0]['holding'][stock_name]
    return client_balance

def get_client_balance(db,client_code):
    
    clients = db.Table('clients')
    response = clients.scan(FilterExpression=boto3.dynamodb.conditions.Attr('client_code').eq(client_code))
    client_balance = response['Items'][0]['current_balance']
    return client_balance
    
def get_client_brokerage(db,client_code):
    
    clients = db.Table('clients')
    response = clients.scan(FilterExpression=boto3.dynamodb.conditions.Attr('client_code').eq(client_code))
    brokerage = response['Items'][0]['brokerage']
    return brokerage

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

def add_order_log(db,client_code,date,stock_name,direction,requestId,qty):
    clients = db.Table('clients')
    response = clients.scan(FilterExpression=boto3.dynamodb.conditions.Attr('client_code').eq(client_code))
    response['Items'][0]['daily_trade_log'].append(DailyOrderLog(date,stock_name,direction,requestId,qty).to_list())
    clients.put_item(Item=response['Items'][0])

def reduce_balance(db,client,amount):
    current_balance = get_client_balance(db,client)
    new_balance = current_balance - amount
    update_client_balance(db,client,new_balance)
    
def add_balance(db,client,amount):
    current_balance = get_client_balance(db,client)
    new_balance = current_balance + amount
    update_client_balance(db,client,new_balance)

