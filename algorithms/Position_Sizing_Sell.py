from database.dto.clients import Holding
from database.dao.client_dao import *


class PositionSizingSell:
    def __init__(self,client_code):
        self.client_code = client_code
        
    def send_sell_order(self,stock_name):
        holding = get_client_holding_stock(self.client_code,stock_name)
        print(f"Sell Order placed for {holding['stock_name']} for qty {holding['qty']}")
        
        
    def off_load_stocks(self,stocks_sell):
        for stock_sell in stocks_sell:
            self.send_sell_order(self,stock_sell)
            offload_holding(self.client_code,stock_sell)