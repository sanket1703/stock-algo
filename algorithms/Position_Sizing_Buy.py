from datetime import datetime
from database.dao.client_dao import *

from utils.enums.signal import Signal
import math
from stock_data.price import fetch_stock_data, get_last_traded_price

class PositionSizingBuy:
    def __init__(self,client_code):
        self.client_code = client_code
        
    def send_buy_order(self,buy_stock,qty,client,last_traded_price):
        print(f"Order sent for: Stock {buy_stock} for Qty {qty} for Client {client} at approx price {last_traded_price}")
        return last_traded_price
    
    def position_sizing(self,final_buy_stocks,total_available_slots_before_buy):
    
        for buy_stock in final_buy_stocks:
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            total_available_capital = get_client_balance(self.client_code)
            amount_to_invest = total_available_capital/total_available_slots_before_buy
            
            last_traded_price = get_last_traded_price(fetch_stock_data(buy_stock))
            qty = math.floor(amount_to_invest/last_traded_price)
            price = self.send_buy_order(buy_stock,qty,self.client_code,last_traded_price)
            # Add brokerage here
            turnover = (qty*last_traded_price)
            update_holding(self.client_code,buy_stock,qty,last_traded_price,current_datetime)
            add_trade_log(self.client_code,current_datetime,buy_stock,Signal.BUY.value,last_traded_price,qty,total_available_capital)
            
            print(f"Stock: {buy_stock} Price_buy {price} Quantity {qty} Amount to Invest {amount_to_invest}")
            reduce_balance(self.client_code,turnover)
            total_available_slots_before_buy -=1    