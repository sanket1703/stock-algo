from datetime import datetime
from decimal import Decimal
from loguru import logger
from brokers.motilal.order import get_trade_price, get_trade_qty, get_xchange_trade_id, is_order_completed, modify_order_to_market
from database.dao.client_dao import *
from utils.enums.signal import Signal
from brokers.motilal.login import client_login
from utils.helpers.check_time import check_end_of_market
from utils.helpers.print_client import print_client
from utils.json.helper import (get_filled_buy_orders, get_filled_sell_orders, get_orders,
    get_unfilled_buy_orders, get_unfilled_sell_orders, set_filled_buy_orders,
    set_filled_sell_orders, set_unfilled_buy_orders, set_unfilled_sell_orders)
from utils.json.orders_json_helper import update_status, update_sync_status
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

    def validate_orders(self):
        orders = get_orders()
        if(orders == []):
            logger.info("No orders placed. Nothing to process")
        for order in orders:
            client = order['ClientCode']
            order_id = order['OrderID']
            Mofsl = client_login(client)
            is_order_completed(Mofsl, client, order_id)
            if (check_end_of_market() and order["ExchangeTradeID"]==""):
                modify_order_to_market(Mofsl, client, order_id)

    def calculate_brokerage(self,client_code):
        client_brokerage = get_client_brokerage(self.db,client_code)
        # print(f"Brokerage fixed for client {self.client_code} is {client_brokerage}")
        brokerage = Decimal(0.00119171) + (Decimal(1.18)*client_brokerage/100)
        # print(f"Brokerage charge Calculated during buy {brokerage}")
        return brokerage
                
    def sync_trades(self):
        
        orders = get_orders()
        for order in orders:
            xchange_trade_id = order["ExchangeTradeID"]
            if (xchange_trade_id != "" and order["SyncStatus"] != "Synced"):
                current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                client_code = order['ClientCode']
                order_id = order['OrderID']
                stock_code = order['StockCode']
                # Mofsl = client_login(client_code)
                # trade_price = get_trade_price(Mofsl, client_code, order_id)
                trade_price = order["TradePrice"]
                # qty = get_trade_qty(Mofsl, client_code, order_id)
                qty = order["QtyTraded"]
                # TODO:- qty will return random stuff if there is some error on the AB side -> handle that
                turnover = (Decimal(qty)*Decimal(trade_price))
                
                if (order['Direction'] == "Buy" and order['IsAdhocOrder'] != "Adhoc"):
                
                    update_holding(self.db, client_code, stock_code, Decimal(
                        qty), Decimal(trade_price), current_datetime)
                    logger.debug(f"Added Holding of {qty} {stock_code}")

                    turnover =  Decimal(turnover)*(1+self.calculate_brokerage(client_code))

                    reduce_balance(self.db, client_code, Decimal(turnover))
                    logger.debug(
                        f"Reduce balance of {turnover} from buy of {stock_code}")

                    add_trade_log(self.db, client_code, current_datetime, stock_code,
                                Signal.BUY.value, Decimal(trade_price), qty, xchange_trade_id)
                    logger.debug(f"Added trade log")
                    update_sync_status(order_id)
                
                elif (order['Direction'] == "Sell" and order['IsAdhocOrder'] != "Adhoc"):
                    
                    offload_holding(self.db, client_code, stock_code)
                    logger.debug(f"Holding of {stock_code} offloaded")

                    turnover =  Decimal(turnover)*(1-self.calculate_brokerage(client_code))

                    add_balance(self.db, client_code, Decimal(turnover))
                    logger.debug(
                        f"Added balance of {turnover} from sell of {stock_code}")

                    add_trade_log(self.db, client_code, current_datetime, stock_code,
                                Signal.SELL.value, Decimal(trade_price), qty, xchange_trade_id)
                    logger.debug(f"Added trade log")
                    update_sync_status(order_id)
                    
                
                  
    def check_buy_orders(self,orders):
        un_filled_orders = get_unfilled_buy_orders()
        filled_orders = get_filled_buy_orders()
        for client_code in orders:
            if client_code == "date":
                continue
            print_client(client_code)
            client_orders = orders[client_code]
            client_filled_orders = []
            client_un_filled_orders = []
            if client_orders == None:
                continue 
            
            Mofsl = client_login(client_code)
            logger.info(f"Buy orders status check for {client_code} initiated.")
            for order_id,buy_stock in client_orders:
                if(not is_order_completed(Mofsl,client_code,order_id)):
                    logger.debug(f"{order_id}-{buy_stock} not filled")
                    client_un_filled_orders.append((order_id,buy_stock))
                else:
                    xchange_trade_id = get_xchange_trade_id(Mofsl,client_code,order_id)
                    logger.debug(f"{order_id}-{buy_stock} filled with exchange trade id:- {xchange_trade_id}")
                    client_filled_orders.append((order_id,buy_stock,xchange_trade_id))
                    
            
            # update the unfilled orders
            un_filled_orders[client_code] = client_un_filled_orders

            # update or append filled orders
            if client_code in filled_orders:
                filled_orders[client_code] = filled_orders[client_code]+ client_filled_orders
            else:
                filled_orders[client_code] = client_filled_orders
                
            logger.info(f"Buy orders status check complete for {client_code}")
            
        set_filled_buy_orders(filled_orders)
        set_unfilled_buy_orders(un_filled_orders)
        
        logger.info(f"Filled buy orders:- {filled_orders}")
        logger.info(f"Unfilled buy orders:- {un_filled_orders}")
        return filled_orders,un_filled_orders
    
    def check_sell_orders(self,orders):
        un_filled_orders = get_unfilled_sell_orders()
        filled_orders = get_filled_sell_orders()
        for client_code in orders:
            if client_code == "date":
                continue
            print_client(client_code)
            client_orders = orders[client_code]
            client_filled_orders = []
            client_un_filled_orders = []
            if client_orders == None:
                continue 
            
            Mofsl = client_login(client_code)
            logger.info(f"Sell orders status check for {client_code} initiated.")
            for order_id,sell_stock in client_orders:
                if(not is_order_completed(Mofsl,client_code,order_id)):
                    logger.debug(f"{order_id}-{sell_stock} not filled")
                    client_un_filled_orders.append((order_id,sell_stock))
                else:
                    xchange_trade_id = get_xchange_trade_id(Mofsl,client_code,order_id)
                    client_filled_orders.append((order_id,sell_stock,xchange_trade_id))
            
             # update the unfilled orders
            un_filled_orders[client_code] = client_un_filled_orders

            # update or append filled orders
            if client_code in filled_orders:
                filled_orders[client_code] = filled_orders[client_code] + client_filled_orders
            else:
                filled_orders[client_code] = client_filled_orders
                
            logger.info(f"Buy orders status check complete for {client_code}")
            
        # TODO:- failed_orders & successful_orders should be saved in the DB
        set_filled_sell_orders(filled_orders)
        set_unfilled_sell_orders(un_filled_orders)
        
        logger.info(f"Filled sell orders:- {filled_orders}")
        logger.info(f"Unfilled sell orders:- {un_filled_orders}")
        return filled_orders,un_filled_orders
                    
    
    def sync_filled_buy_trades(self,filled_orders):
        
        for client_code in filled_orders:
            if client_code == "date":
                continue
            print_client(client_code)
            logger.info(f"Buy Trade sync for {client_code} initiated.")
            client_orders = filled_orders[client_code]
            if client_orders == None:
                continue 
            
            Mofsl = client_login(client_code)
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for order_id,buy_stock,xchange_trade_id in client_orders:
                trade_price = get_trade_price(Mofsl,client_code,order_id)
                qty = get_trade_qty(Mofsl,client_code,order_id)
                #TODO:- qty will return random stuff if there is some error on the AB side -> handle that 
                turnover = (Decimal(qty)*Decimal(trade_price))
                update_holding(self.db,client_code,buy_stock,Decimal(qty),Decimal(trade_price),current_datetime)
                logger.debug(f"Added Holding of {qty} {buy_stock}")
                
                reduce_balance(self.db,client_code,Decimal(turnover))
                logger.debug(f"Reduce balance of {turnover} from buy of {buy_stock}")
                
                add_trade_log(self.db,client_code,current_datetime,buy_stock,Signal.BUY.value,Decimal(trade_price),qty,xchange_trade_id)
                logger.debug(f"Added trade log")
            
            logger.info(f"Buy Trade sync for {client_code} completed.")
        return 
    
    def sync_filled_sell_trades(self,filled_orders):
        
        for client_code in filled_orders:
            if client_code == "date":
                continue
            print_client(client_code)
            logger.info(f"Sell Trade sync for {client_code} initiated.")
            client_orders = filled_orders[client_code]
            if client_orders == None:
                continue 
            
            Mofsl = client_login(client_code)
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for order_id,sell_stock,xchange_trade_id in client_orders:
                trade_price = get_trade_price(Mofsl,client_code,order_id)
                qty = get_trade_qty(Mofsl,client_code,order_id)
                turnover = (Decimal(qty)*Decimal(trade_price))
                
                offload_holding(self.db,client_code,sell_stock)
                logger.debug(f"Holding of {sell_stock} offloaded")
                
                add_balance(self.db,client_code,Decimal(turnover))
                logger.debug(f"Added balance of {turnover} from sell of {sell_stock}")
                
                add_trade_log(self.db,client_code,current_datetime,sell_stock,Signal.SELL.value,Decimal(trade_price),qty,xchange_trade_id)
                logger.debug(f"Added trade log")
            
            logger.info(f"Sell Trade sync for {client_code} completed.")
        return
                    
    def bulk_modify_to_market(self,orders):
        # Given the order object if will modify all orders to Market
        modified_orders = {}
        failed_modified_orders = {}
        for client_code in orders:
            
            if client_code == "date":
                continue
            print_client(client_code)
            Mofsl = client_login(client_code)
            
            logger.info(f"Modify to Market Orders for {client_code} initiated.")
            client_orders = orders[client_code]
            client_modified_orders = []
            client_failed_modified_orders = []
            if client_orders == None:
                continue 
            for order_id,buy_stock in client_orders:
                if(modify_order_to_market(Mofsl,client_code,order_id)):
                    logger.debug(f"{order_id}-{buy_stock} modified to market.")
                    client_modified_orders.append((order_id,buy_stock))
                else:
                    logger.debug(f"{order_id}-{buy_stock} failed to modify to market.")
                    client_failed_modified_orders.append((order_id,buy_stock))
            
            modified_orders[client_code] = client_modified_orders
            failed_modified_orders[client_code] = client_failed_modified_orders        
                
            logger.info(f"Modify to Market Orders for {client_code} completed.")
        
        logger.info(f"Modified orders:- {modified_orders}")
        logger.info(f"Failed modified orders:- {failed_modified_orders}")
        
        return modified_orders,failed_modified_orders                
                    