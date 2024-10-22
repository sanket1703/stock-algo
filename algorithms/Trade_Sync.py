from datetime import datetime
from decimal import Decimal

from brokers.motilal.order import get_trade_price, get_trade_qty, is_order_completed, modify_order_to_market, order_status
from database.dao.client_dao import *
from utils.enums.signal import Signal
from brokers.motilal.login import client_login
from utils.json.helper import set_filled_buy_orders, set_filled_sell_orders, set_unfilled_buy_orders
class TradeSync:
    def __init__(self,orders):
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
        un_filled_orders = {}
        filled_orders = {}
        for client_code in orders:
            if client_code == "date":
                continue
            print(f"Checking order status for {client_code}")
            client_orders = orders[client_code]
            client_filled_orders = []
            client_un_filled_orders = []
            if client_orders == None:
                continue 
            
            Mofsl = client_login(client_code)
            
            for order_id,buy_stock in client_orders:
                if(not is_order_completed(Mofsl,client_code,order_id)):
                    client_un_filled_orders.append((order_id,buy_stock))
                else:
                    client_filled_orders.append((order_id,buy_stock))
            
            # Check if client_code exists in un_filled_orders, if so, zip the lists, else add client_un_filled_orders
            if client_code in un_filled_orders:
                un_filled_orders[client_code] = list(zip(un_filled_orders[client_code], client_un_filled_orders))
            else:
                un_filled_orders[client_code] = client_un_filled_orders

            # Check if client_code exists in filled_orders, if so, zip the lists, else add client_filled_orders
            if client_code in filled_orders:
                filled_orders[client_code] = list(zip(filled_orders[client_code], client_filled_orders))
            else:
                filled_orders[client_code] = client_filled_orders
                
            print(f"Done trade sync for {client_code}")
            
        # TODO:- failed_orders & successful_orders should be saved in the DB
        set_filled_buy_orders(filled_orders)
        set_unfilled_buy_orders(un_filled_orders)
        return filled_orders,un_filled_orders
                    
    
    def sync_filled_buy_trades(self,filled_orders):
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for client_code in filled_orders:
            if client_code == "date":
                continue
            print(f"Starting trade sync for {client_code}")
            client_orders = filled_orders[client_code]
            if client_orders == None:
                continue 
            
            Mofsl = client_login(client_code)
            
            for order_id,buy_stock in client_orders:
                trade_price = get_trade_price(Mofsl,client_code,order_id)
                qty = get_trade_qty(Mofsl,client_code,order_id)
                #TODO:- qty will return random stuff if there is some error on the AB side -> handle that 
                turnover = (Decimal(qty)*Decimal(trade_price))
                update_holding(self.db,client_code,buy_stock,Decimal(qty),Decimal(trade_price),current_datetime)
                add_trade_log(self.db,client_code,current_datetime,buy_stock,Signal.BUY.value,Decimal(trade_price),qty)
                reduce_balance(self.db,client_code,Decimal(turnover))
            print(f"Updated all holdings for {client_code}")
        return 
    
    def sync_filled_sell_trades(self,filled_orders):
        
        for client_code in filled_orders:
            if client_code == "date":
                continue
            print(f"Starting trade sync for {client_code}")
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            client_orders = filled_orders[client_code]
            print(f"Client {client_code} :- {client_orders}")
            if client_orders == None:
                continue 
            
            Mofsl = client_login(client_code)
            
            for order_id,sell_stock in client_orders:
                trade_price = get_trade_price(Mofsl,client_code,order_id)
                qty = get_trade_qty(Mofsl,client_code,order_id)
                turnover = (Decimal(qty)*Decimal(trade_price))
                # Adjust for brokerage
                offload_holding(self.db,client_code,sell_stock)
                add_balance(self.db,client_code,Decimal(turnover))
                add_trade_log(self.db,client_code,current_datetime,sell_stock,Signal.SELL.value,Decimal(trade_price),qty)
        return
                    
    def bulk_modify_to_market(self,orders):
        # Given the order object if will modify all orders to Market
        modified_orders = {}
        failed_modified_orders = {}
        for client_code in orders:
            if client_code == "date":
                continue
            
            Mofsl = client_login(client_code)
            
            print(f"Checking order status for {client_code}")
            client_orders = orders[client_code]
            client_modified_orders = []
            client_failed_modified_orders = []
            if client_orders == None:
                continue 
            for order_id,buy_stock in client_orders:
                if(modify_order_to_market(Mofsl,client_code,order_id)):
                    client_modified_orders.append((order_id,buy_stock))
                else:
                    client_failed_modified_orders.append((order_id,buy_stock))
            
            modified_orders[client_code] = client_modified_orders
            failed_modified_orders[client_code] = client_failed_modified_orders        
                
            print(f"Done trade sync for {client_code}")
    
        return modified_orders,failed_modified_orders                
                    