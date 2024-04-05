import yfinance as yf
import pandas as pd
import pandas_ta as ta


def slot_fill(stocks):
    # Will come from Database
    slots = set(['a'])
    
    max_slots = 13
    total_available_slots = max_slots - len(slots)
    
    if total_available_slots == 0:
        return
    
    # Will come from the Filtered stocks
    final_stocks = []
    for stock in stocks:
        if stock not in slots:
            final_stocks.append(stock)
            total_available_slots-=1
            # Make a database entery
            slots.add(stock)
        
        if len(final_stocks) >= total_available_slots:
            break

    return (final_stocks,total_available_slots)
    

# Example usage
if __name__ == "__main__":  
    
    stocks = ['a','b']
    print(slot_fill(stocks))
