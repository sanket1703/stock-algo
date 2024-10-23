from datetime import datetime
from algorithms.Position_Sizing_Buy import PositionSizingBuy
from brokers.motilal.helper.read_client_data import read_csv_to_dict
from brokers.motilal.login import client_login
from database.dao.client_dao import get_client_list
from database.dao.slots_dao import * 
from database.dynamodb import get_database
from loguru import logger


class MidcapBuyAlgorithm:
    def __init__(self,stock_list):
        self.db = get_database()
        self.stock_list = stock_list
        self.ranked_stock_list = []
        self.clients = get_client_list()
        self.final_stocks_buy = []
        
    def order_executor(self):
        logger.debug("Starting Buy Order Execution.")
        buy_orders = {}
        
        for client_code in self.clients:
            Mofl = client_login(client_code)
            client = PositionSizingBuy(client_code)
            client_order = client.position_sizing(self.final_stocks_buy,self.total_available_slots_before_buy,Mofl)
            if client_order == None:
                logger.error(f"No buy orders executed for {client_code}")
                continue
            buy_orders[client_code] = client_order
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            buy_orders["date"] = current_datetime
            
        logger.debug("Order Execution completed")
        return buy_orders
    
    def get_client_auth(self,client_code):
        clients_auth = read_csv_to_dict()
        return clients_auth[client_code]
    
    def allocate_slots(self):
        
        slots = get_slots(self.db)
        buy_stocks = self.stock_list
        max_slots = 13
        self.total_available_slots_before_buy = max_slots - len(slots)
        
        if self.total_available_slots_before_buy == 0:
            logger.info("No slots available.")
            return ([],self.total_available_slots_before_buy)
        
        for stock in buy_stocks:
            if stock not in slots:
                self.final_stocks_buy.append(stock)
                slots.append(stock)
            else:
                logger.info(f"{stock} already present in the slots. Not buying {stock}")
            
            if len(slots) >= max_slots:
                break
        
        total_available_slots_after_buy =  max_slots - len(slots)
        
        update_slots(self.db,list(slots))
        print("Final Buy signal to Broker, Before total Available slots")
        logger.info(f"Final buy list of Stocks :- {self.final_stocks_buy}")
        logger.info(f"Total slots which were available before allocating slots:- {self.total_available_slots_before_buy}")
        return self.final_stocks_buy,self.total_available_slots_before_buy
    
    


# Example usage
if __name__ == "__main__":
    print
