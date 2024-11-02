from datetime import datetime
from algorithms.Position_Sizing_Sell import PositionSizingSell
from brokers.motilal.login import client_login
from database.dao.client_dao import get_client_list
from stock_data.indicators import calculate_ema, calculate_supertrend
from stock_data.price import fetch_stock_data
from database.dao.slots_dao import * 
from database.dynamodb import get_database
from utils.helpers.print_client import print_client

class MidcapSellAlgorithm:
    def __init__(self):
        self.db = get_database()
        self.slots = get_slots(self.db)
        self.stocks_to_sell = []
        self.stocks_to_keep = []
        self.clients = get_client_list()
    
    def order_executor(self):
        logger.debug("Starting Sell Order Execution.")
        sell_orders = {}
        
        for client_code in self.clients:
            print(f"Starting position sizing selling for {client_code}")
            print_client(client_code)
            client = PositionSizingSell(client_code)
            Mofl = client_login(client_code)
            client_order = client.off_load_stocks(self.stocks_to_sell,Mofl)
            print(f"Client order:- {client_order}")
            if client_order == None:
                continue
            sell_orders[client_code] = client_order
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sell_orders["date"] = current_datetime
        
        print(sell_orders)
        return sell_orders

    def should_sell(self,stock):
        return True
        data = fetch_stock_data(stock)
        try:
            ema = calculate_ema(data).iloc[-1]
            last_traded_price = data['Close'].iloc[-1]
            supertrend = calculate_supertrend(data).iloc[-1]
            
            if last_traded_price < supertrend or last_traded_price < ema:
                return True
            return False
        except:
            return False
    
    def sell_logic(self):
        # slots is a list of stocks
        self.slots = get_slots(self.db)
        for stock in self.slots:
            if self.should_sell(stock):
                self.stocks_to_sell.append(stock)
            else:
                self.stocks_to_keep.append(stock)
                
        update_slots(self.db,self.stocks_to_keep)
        
        print("Current Slots")
        print(get_slots(self.db))
        
        print("Sell the following stocks")
        print(self.stocks_to_sell)
        # self.stocks_to_sell = ["ABBOTINDIA.NS"]
        return self.stocks_to_sell
    
    
    def adhoc_sell(self,sell_stock_list):
        self.stocks_to_sell = sell_stock_list