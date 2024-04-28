from datetime import datetime
from decimal import Decimal
from database.dao.client_dao import *
import boto3

from utils.enums.signal import Signal
import math
from stock_data.price import fetch_stock_data, get_last_traded_price

class PositionSizingBuy:
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
        
    def send_buy_order(self,buy_stock,qty,client,last_traded_price):
        print(f"Order sent for: Stock {buy_stock} for Qty {qty} for Client {client} at approx price {last_traded_price}")
        return last_traded_price
        
    def calculate_brokerage(self,amount_to_invest):
        client_brokerage = get_client_brokerage(self.db,self.client_code)
        print(f"Brokerage fixed for client {self.client_code} is {client_brokerage}")
        brokerage = amount_to_invest*Decimal(client_brokerage)
        print(f"Brokerage Calculated during buy {brokerage}")
        return brokerage
    
    def position_sizing(self,final_buy_stocks,total_available_slots_before_buy):
    
        for buy_stock in final_buy_stocks:
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            total_available_capital = get_client_balance(self.db,self.client_code)
            amount_to_invest = total_available_capital/total_available_slots_before_buy
            amount_to_invest -= self.calculate_brokerage(amount_to_invest)
            last_traded_price = get_last_traded_price(fetch_stock_data(buy_stock))
            qty = math.floor(Decimal(amount_to_invest)/Decimal(last_traded_price))
            price = self.send_buy_order(buy_stock,qty,self.client_code,last_traded_price)
            turnover = (qty*last_traded_price)
            update_holding(self.db,self.client_code,buy_stock,qty,Decimal(last_traded_price),current_datetime)
            add_trade_log(self.db,self.client_code,current_datetime,buy_stock,Signal.BUY.value,Decimal(last_traded_price),qty,Decimal(total_available_capital))
            
            print(f"Stock: {buy_stock} Price_buy {price} Quantity {qty} Amount to Invest {amount_to_invest}")
            reduce_balance(self.db,self.client_code,Decimal(turnover))
            total_available_slots_before_buy -=1    