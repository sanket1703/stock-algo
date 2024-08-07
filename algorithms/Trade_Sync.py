from datetime import datetime
from decimal import Decimal

from algobaba.order_details import get_trade_price, get_trade_qty, is_order_completed, order_status
from database.dao.client_dao import *
from utils.enums.signal import Signal
class TradeSync:
    def __init__(self):
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
    
    def check_orders(self,orders):
        failed_orders = {}
        successful_orders = {}
        for client in orders:
            if client == "date":
                continue
            print(f"Checking order status for {client}")
            client_orders = orders[client]
            client_failed_orders = []
            client_successful_orders = []
            if client_orders == None:
                continue 
            for request_id,buy_stock in client_orders:
                if(not is_order_completed(request_id)):
                    client_failed_orders.append((request_id,buy_stock))
                else:
                    client_successful_orders.append((request_id,buy_stock))
            
            failed_orders[client] = client_failed_orders
            successful_orders[client] = client_successful_orders        
                
            # print(f"Done trade sync for {client}")
            
        # TODO:- failed_orders & successful_orders should be saved in the DB
        return orders,failed_orders
                    
    
    def sync_successful_buy_trades(self,successful_orders):
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for client in successful_orders:
            if client == "date":
                continue
            print(f"Starting trade sync for {client}")
            client_orders = successful_orders[client]
            if client_orders == None:
                continue 
            for request_id,buy_stock in client_orders:
                trade_price = get_trade_price(request_id)
                qty = get_trade_qty(request_id)
                #TODO:- qty will return random stuff if there is some error on the AB side -> handle that 
                turnover = (Decimal(qty)*Decimal(trade_price))
                update_holding(self.db,client,buy_stock,qty,Decimal(trade_price),current_datetime)
                add_trade_log(self.db,client,current_datetime,buy_stock,Signal.BUY.value,Decimal(trade_price),qty)
                reduce_balance(self.db,client,Decimal(turnover))
        return 
    
    def sync_successful_sell_trades(self,successful_orders):
        
        for client in successful_orders:
            if client == "date":
                continue
            print(f"Starting trade sync for {client}")
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            client_orders = successful_orders[client]
            print(f"Client {client} :- {client_orders}")
            if client_orders == None:
                continue 
            for request_id,sell_stock in client_orders:
                trade_price = get_trade_price(request_id)
                qty = get_trade_qty(request_id)
                turnover = (Decimal(qty)*Decimal(trade_price))
                # Adjust for brokerage
                offload_holding(self.db,client,sell_stock)
                add_balance(self.db,client,Decimal(turnover))
                add_trade_log(self.db,client,current_datetime,sell_stock,Signal.SELL.value,Decimal(trade_price),qty)
        return
                    
                    
                