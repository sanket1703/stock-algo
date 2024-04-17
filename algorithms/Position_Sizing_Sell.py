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
        
    def send_sell_order(self,stock_name):
        holding = get_client_holding_stock(self.db,self.client_code,stock_name)
        print(f"Sell Order placed for {holding['stock_name']} for qty {holding['qty']}")
        return holding
        
        
    def off_load_stocks(self,stocks_sell):
        for stock_sell in stocks_sell:
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            holding = self.send_sell_order(stock_sell)
            last_traded_price = get_last_traded_price(fetch_stock_data(stock_sell))
            qty = holding['qty']
            turnover = (qty*decimal.Decimal(last_traded_price))
            offload_holding(self.db,self.client_code,stock_sell)
            total_available_capital = get_client_balance(self.db,self.client_code)
            add_balance(self.db,self.client_code,decimal.Decimal(turnover))
            add_trade_log(self.db,self.client_code,current_datetime,stock_sell,Signal.SELL.value,decimal.Decimal(last_traded_price),holding['qty'],decimal.Decimal(total_available_capital))
            