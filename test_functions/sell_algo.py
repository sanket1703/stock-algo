from stock_data.indicators import calculate_ema, calculate_supertrend
from stock_data.price import fetch_stock_data, get_last_traded_price

def sell_algo(slots):
    # slots is a list of stocks
    stocks_to_keep = []
    stocks_to_sell = []
    for stock in slots:
        if should_sell(stock):
            stocks_to_sell.append(stock)    
        else:
            stocks_to_keep.append(stock)
            
    # New Slots 
    slots = stocks_to_keep
    # Update in the database
    
    return stocks_to_keep
    

def should_sell(stock):
    
    data = fetch_stock_data(stock)
    ema = calculate_ema(data).iloc[-1]
    last_traded_price = data['Close'].iloc[-1]
    supertrend = calculate_supertrend(data).iloc[-1]
    
    if last_traded_price < supertrend or last_traded_price < ema:
        return True
    
    return False
    
if __name__ == "__main__":
    stocks = ['LUPIN.NS','INDHOTEL.NS','POLYCAB.NS','PERSISTENT.NS','CUMMINSIND.NS','ZYDUSLIFE.NS','RECLTD.NS','ABBOTINDIA.NS','TVSMOTOR.NS','AUBANK.NS','LTTS.NS','GUJGASLTD.NS','TRENT.NS','OFSS.NS','COFORGE.NS','ALKEM.NS','AUROPHARMA.NS','HONAUT.NS','ASTRAL.NS','BALKRISIND.NS','MPHASIS.NS']
    print(sell_algo())