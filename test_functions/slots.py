import yfinance as yf
import pandas as pd
import pandas_ta as ta

# Example usage
if __name__ == "__main__":
    
    # Will come from Database
    slots = set()
    
    max_slots = 13
    total_available_slots = 13 - len(slots)
    
    if total_available_slots == 0:
        print("stop")
    
    # Will come from the Filtered stocks
    stocks = ['A','B','C']
    final_stocks = []
    
    for stock in stocks:
        if stock not in slots:
            final_stocks.append(stock)
        if len(final_stocks) >= total_available_slots:
            break
            
        
        
    

    

    filtered_stocks = filter_stocks(stocks)
    print("Filtered stocks based on conditions:")
    print(filtered_stocks)
