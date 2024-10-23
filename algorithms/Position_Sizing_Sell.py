from algobaba.buy_order import send_sell_order
from brokers.motilal.order import place_sell_order
from database.dto.clients import Holding
from database.dao.client_dao import *
from datetime import datetime
import decimal
from utils.enums.signal import Signal
from stock_data.price import fetch_stock_data, get_last_traded_price
import boto3

class PositionSizingSell:
    def __init__(self,client_code):
        self.client_code = client_code
        self.db = self.get_database()
    
    def get_database(self):
    
        aws_access_key_id = 'AKIAW3MEAN3TBZIFTCE6'
        aws_secret_access_key = 'Ad2nS01Iioxl4cfqqDsXWBAoPd4SJRMqwdPpdFbj'

        # Create a DynamoDB resource object with your credentials
        dynamodb = boto3.resource(
            'dynamodb',
            region_name='ap-south-1',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key)
        
        return dynamodb
        
    def calculate_brokerage(self):
        client_brokerage = get_client_brokerage(self.db,self.client_code)
        print(f"Brokerage fixed for client {self.client_code} is {client_brokerage}")
        brokerage = decimal.Decimal(0.00104171) + (decimal.Decimal(1.18)*client_brokerage/100)
        print(f"Brokerage Calculated during sell {brokerage}")
        return decimal.Decimal(brokerage)
        
        
    def off_load_stocks(self,stocks_sell,Mofl):
        client_order_list = []
        for stock_sell in stocks_sell:
            request_id = place_sell_order(self.db,self.client_code,stock_sell,Mofl)
            if request_id == '':
                print(f"Could not sell {stock_sell}")
                continue
            client_order_list.append((request_id,stock_sell))
        return client_order_list
