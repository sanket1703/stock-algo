



from stock_data.indicators import calculate_ema, calculate_supertrend
from stock_data.price import fetch_stock_data


class MidcapSellAlgorithm:
    def __init__(self):
        self
        
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
    
    def sell_logic(self,slots):
    # slots is a list of stocks
    
        stocks_to_keep = []
        stocks_to_sell = []
        for stock in slots:
            if self.should_sell(stock):
                stocks_to_sell.append(stock)    
            else:
                stocks_to_keep.append(stock)
                
        # New Slots 
        slots = stocks_to_keep
        # Update in the database
        
        return stocks_to_keep
    