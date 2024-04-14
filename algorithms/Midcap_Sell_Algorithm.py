from stock_data.indicators import calculate_ema, calculate_supertrend
from stock_data.price import fetch_stock_data
from database.dao.slots_dao import * 

class MidcapSellAlgorithm:
    def __init__(self):
        self.slots = get_slots()
        
    def get_slots():
        return

    def should_sell(self,stock):
        
        data = fetch_stock_data(stock)
        ema = calculate_ema(data).iloc[-1]
        last_traded_price = data['Close'].iloc[-1]
        supertrend = calculate_supertrend(data).iloc[-1]
        
        if last_traded_price < supertrend or last_traded_price < ema:
            return True
        
        return False
    
    def sell_logic(self):
        # slots is a list of stocks
        self.slots = get_slots()
        stocks_to_keep = []
        stocks_to_sell = []
        for stock in self.slots:
            if self.should_sell(stock):
                stocks_to_sell.append(stock)    
            else:
                stocks_to_keep.append(stock)
                
        # New Slots 
        self.stocks_to_keep = stocks_to_keep
        update_slots(self.stocks_to_keep)
        print("Current Slots")
        print(get_slots())
        self.stocks_to_sell = stocks_to_sell
        print("Sell the following stocks")
        print(self.stocks_to_sell)
        return self.stocks_to_sell
    