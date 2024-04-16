from database.dto.clients import Holding
from database.dao.client_dao import *
from datetime import datetime
from utils.enums.signal import Signal
from stock_data.price import fetch_stock_data, get_last_traded_price

class PositionSizingSell:
    def __init__(self,client_code):
        self.client_code = client_code
        
    def send_sell_order(self,stock_name):
        holding = get_client_holding_stock(self.client_code,stock_name)
        print(f"Sell Order placed for {holding['stock_name']} for qty {holding['qty']}")
        return holding
        
        
    def off_load_stocks(self,stocks_sell):
        for stock_sell in stocks_sell:
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            holding = self.send_sell_order(stock_sell)
            last_traded_price = get_last_traded_price(fetch_stock_data(stock_sell))
            qty = holding['qty']
            turnover = (qty*last_traded_price)
            offload_holding(self.client_code,stock_sell)
            total_available_capital = get_client_balance(self.client_code)
            add_balance(self.client_code,turnover)
            add_trade_log(self.client_code,current_datetime,stock_sell,Signal.SELL.value,last_traded_price,holding['qty'],total_available_capital)
            