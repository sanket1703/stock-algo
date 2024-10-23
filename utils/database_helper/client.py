from database.dynamodb import get_database
import decimal
from database.dto.clients import *
import boto3
from database.dao.client_dao import get_client_list
from loguru import logger

def clear_trade_log_clients():
    client_list = get_client_list()
    db = get_database()
    for client in client_list:
        clients = db.Table('clients')
        response = clients.scan(FilterExpression=boto3.dynamodb.conditions.Attr('client_code').eq(client))
        response['Items'][0]['daily_trade_log']=[]
        clients.put_item(Item=response['Items'][0])
        logger.debug(f"Cleared trade log for {client}")
    