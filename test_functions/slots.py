import yfinance as yf
import pandas as pd
import pandas_ta as ta
import json


def slot_fill(buy_stocks):
    # Will come from Database
    slots = get_slots()
    
    max_slots = 5
    total_available_slots = max_slots - len(slots)
    
    if total_available_slots == 0:
        return
    
    # Will come from the Filtered stocks
    final_buy_stocks = []
    for stock in buy_stocks:
        if stock not in slots:
            final_buy_stocks.append(stock)
            slots.append(stock)
        
        if len(final_buy_stocks) + len(slots) > max_slots:
            break
    
    update_slots(list(slots))
    total_available_slots =  max_slots - len(slots)
    
    return (final_buy_stocks,total_available_slots)
    

def get_slots():
    with open('slots.json', 'r') as f:
        return json.load(f)
    
def update_slots(slots):
    with open('slots.json', 'w') as f:
        json.dump(slots, f)
    

# Example usage
if __name__ == "__main__":  
    update_slots([])
    # print(slot_fill(['a','b','c','d','e','f']))
