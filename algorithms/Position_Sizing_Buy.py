from datetime import datetime, time
from decimal import Decimal
from algobaba.buy_order import send_buy_order
from brokers.motilal.order import place_buy_order
from database.dao.client_dao import *
import boto3
from loguru import logger
from utils.enums.signal import Signal
import math
from stock_data.price import fetch_1d_stock_data, fetch_stock_data, get_last_traded_price

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
        

        
    # def send_buy_order(self,buy_stock,qty,client,last_traded_price):
    #     print(f"Order sent for: Stock {buy_stock} for Qty {qty} for Client {client} at approx price {last_traded_price}")
    #     return last_traded_price
        
    def calculate_brokerage(self):
        client_brokerage = get_client_brokerage(self.db,self.client_code)
        # print(f"Brokerage fixed for client {self.client_code} is {client_brokerage}")
        brokerage = Decimal(0.00119171) + (Decimal(1.18)*client_brokerage/100)
        # print(f"Brokerage charge Calculated during buy {brokerage}")
        return brokerage
    
    def position_sizing(self,final_buy_stocks,total_available_slots_before_buy,Mofsl):
        logger.info(f"Initiating Position sizing for {self.client_code}")
        total_available_capital = get_client_balance(self.db,self.client_code)
        if total_available_slots_before_buy == 0:
            logger.info("No slots available")
            return []
        amount_to_invest = total_available_capital/total_available_slots_before_buy
        client_order_list = []
        for buy_stock in final_buy_stocks:
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            amount_to_invest = amount_to_invest/(1+self.calculate_brokerage())
            last_traded_price = get_last_traded_price(fetch_1d_stock_data(buy_stock))
            qty = math.floor(Decimal(amount_to_invest)/Decimal(last_traded_price))
            # Last traded price is only to get an idea to estimate the quantity
            request_id = place_buy_order(self.client_code,buy_stock,qty,Mofsl)
            if request_id == '':
                logger.error(f"Buy order for {buy_stock} failed for {self.client_code}")
                continue
            client_order_list.append((request_id,buy_stock))
        return client_order_list
           
           
