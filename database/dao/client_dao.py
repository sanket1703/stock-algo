from botocore.exceptions import ClientError
import decimal
from database.dto.clients import *
import boto3
import configparser

from database.dynamodb import get_database

# Initialize the configparser
config = configparser.ConfigParser()

# Read the config file
config.read('config.properties')
env = config['DEFAULT']['environment']

def get_client_list():
    db = get_database()
    clients = db.Table('clients' + env)
    response = clients.scan(ProjectionExpression='client_code')
    return [item['client_code'] for item in response['Items']]

def get_client_holding_stock(db, client_code,stock_name):
    clients = db.Table('clients' + env)
    response = clients.scan(FilterExpression=boto3.dynamodb.conditions.Attr('client_code').eq(client_code))
    client_balance = response['Items'][0]['holding'][stock_name]
    return client_balance

def get_client_balance(db,client_code):
    
    clients = db.Table('clients'+ env)
    response = clients.scan(FilterExpression=boto3.dynamodb.conditions.Attr('client_code').eq(client_code))
    client_balance = response['Items'][0]['current_balance']
    return client_balance
    
def get_client_brokerage(db,client_code):
    
    clients = db.Table('clients'+ env)
    response = clients.scan(FilterExpression=boto3.dynamodb.conditions.Attr('client_code').eq(client_code))
    brokerage = response['Items'][0]['brokerage']
    return brokerage

def update_client_balance(db,client_code,new_balance):
    clients = db.Table('clients'+ env)
    response = clients.scan(FilterExpression=boto3.dynamodb.conditions.Attr('client_code').eq(client_code))
    response['Items'][0]['current_balance'] = new_balance
    clients.put_item(Item=response['Items'][0])
    # print(f"New balance for {client_code} is Rs. {new_balance}")
    return new_balance

def update_holding(db,client_code,stock_name,qty,price,date):
    clients = db.Table('clients'+ env)
    response = clients.scan(FilterExpression=boto3.dynamodb.conditions.Attr('client_code').eq(client_code))
    response['Items'][0]['holding'][stock_name] = Holding(stock_name,qty,date,price).to_json()
    clients.put_item(Item=response['Items'][0])

def get_client_holding(db,client_code,stock_name):
    clients = db.Table('clients'+ env)
    response = clients.scan(FilterExpression=boto3.dynamodb.conditions.Attr('client_code').eq(client_code))
    return response['Items'][0]['holding'][stock_name]['qty']
   
def is_client_enabled(db,client_code):
    clients = db.Table('clients' + env)
    response = clients.scan(FilterExpression=boto3.dynamodb.conditions.Attr(
        'client_code').eq(client_code))
    return response['Items'][0]['enabled']
    
def offload_holding(db,client_code,stock_name):
    clients = db.Table('clients'+ env)
    response = clients.scan(FilterExpression=boto3.dynamodb.conditions.Attr('client_code').eq(client_code))
    del response['Items'][0]['holding'][stock_name]
    clients.put_item(Item=response['Items'][0])
    
def add_trade_log(db,client_code,date,stock_name,direction,price,qty,xchange_trade_id):
    clients = db.Table('clients'+ env)
    response = clients.scan(FilterExpression=boto3.dynamodb.conditions.Attr('client_code').eq(client_code))
    response['Items'][0]['daily_trade_log'].append(DailyTradeLog(date,stock_name,direction,price,qty,xchange_trade_id).to_list())
    clients.put_item(Item=response['Items'][0])

def add_order_log(db,client_code,date,stock_name,direction,requestId,qty):
    clients = db.Table('clients'+ env)
    response = clients.scan(FilterExpression=boto3.dynamodb.conditions.Attr('client_code').eq(client_code))
    response['Items'][0]['daily_trade_log'].append(DailyOrderLog(date,stock_name,direction,requestId,decimal.Decimal(qty)).to_list())
    clients.put_item(Item=response['Items'][0])

def reduce_balance(db,client,amount):
    current_balance = get_client_balance(db,client)
    new_balance = current_balance - amount
    update_client_balance(db,client,new_balance)
    
def add_balance(db,client,amount):
    current_balance = get_client_balance(db,client)
    new_balance = current_balance + amount
    update_client_balance(db,client,new_balance)
    
    
def get_client_balance(db,client_code):
    
    clients = db.Table('clients'+ env)
    response = clients.scan(FilterExpression=boto3.dynamodb.conditions.Attr('client_code').eq(client_code))
    client_balance = response['Items'][0]['current_balance']
    return client_balance


def update_dynamodb_balance(client_code,new_balance):
    aws_access_key_id = 'AKIAW3MEAN3TBZIFTCE6'
    aws_secret_access_key = 'Ad2nS01Iioxl4cfqqDsXWBAoPd4SJRMqwdPpdFbj'

    # Create a DynamoDB resource object with your credentials
    dynamodb = boto3.resource(
        'dynamodb',
        region_name='ap-south-1',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key)
    
    clients = dynamodb.Table('clients'+ env)
    response = clients.scan(FilterExpression=boto3.dynamodb.conditions.Attr('client_code').eq(client_code))
    response['Items'][0]['current_balance'] = new_balance
    clients.put_item(Item=response['Items'][0])
    # print(f"New balance for {client_code} is Rs. {new_balance}")
    return new_balance


def update_client_status(client_code, value):
    """Update the enabled status for a specific client."""
    db = get_database()
    print(client_code)
    try:
        clients = db.Table('clients' + env)
        response = clients.scan(FilterExpression=boto3.dynamodb.conditions.Attr('client_code').eq(client_code))
        response['Items'][0]['enabled'] = value
        clients.put_item(Item=response['Items'][0])
        print(
            f"Successfully updated client {client_code} to {'enabled' if value else 'disabled'}.")
    except ClientError as e:
        print(f"Error updating client {client_code}: {e}")


def enable_all_clients():
    """Enable all clients in the table."""
    db = get_database()
    client = db.Table('clients')
    try:
        response = client.scan(ProjectionExpression='client_code')
        print(response)
        for item in response['Items']:
            update_client_status(item['client_code'], True)
    except ClientError as e:
        print(f"Error enabling all clients: {e}")
    return 


def disable_all_clients():
    """Disable all clients in the table."""
    db = get_database()
    client = db.Table('clients')
    try:
        response = client.scan(ProjectionExpression='client_code')
        for item in response['Items']:
            update_client_status(item['client_code'], False)
    except ClientError as e:
        print(f"Error disabling all clients: {e}")
    return 


def disable_all_and_enable_selected(client_codes_to_enable):
    """Disable all clients and enable only the specified ones."""
    try:
        # First, disable all clients
        disable_all_clients()

        # Then, enable clients in the given list
        for client_code in client_codes_to_enable:
            update_client_status(client_code, True)
    except ClientError as e:
        print(f"Error updating clients: {e}")
    return 