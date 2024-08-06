
from algobaba.buy_order import *
from algobaba.order_details import *
from database.dao.client_dao import get_client_holding
from database.dao.watchlist_dao import get_watchlist
from database.dynamodb import get_database
import yfinance as yf
import pandas as pd

from stock_data.price import one_year_return

if __name__ == "__main__":
    
    stocks = [
    "RVNL", "IRFC", "SUZLON", "KALYANKJIL", "TRENT", "BHEL", "PRESTIGE", "RECLTD", "BSE", 
    "MCX", "ZOMATO", "ADANIPOWER", "OFSS", "HAL", "DIXON", "PFC", "BEL", "APARINDS", "NCC", 
    "BAJAJ-AUTO", "CUMMINSIND", "NHPC", "HINDCOPPER", "PNB", "ZYDUSLIFE", "GICRE", "POLICYBZR", 
    "TVSMOTOR", "ADANIGREEN", "VBL", "LUPIN", "GLENMARK", "JSL", "KEI", "DLF", "ABB", "LTF", 
    "AUROPHARMA", "INDIANB", "LODHA", "CANBK", "INDHOTEL", "KPITTECH", "UNIONBANK", "ANGELONE", 
    "SUPREMEIND", "BSOFT", "APOLLOTYRE", "CYIENT", "POONAWALLA"
]
    returns = {}
    for stock in stocks:
        try:
            ret = one_year_return(stock + ".NS")  # Adding ".NS" for NSE
            if ret is not None:
                returns[stock] = ret
        except Exception as e:
            print(f"Error fetching data for {stock}: {e}")

    # Create a DataFrame for better visualization
    returns_df = pd.DataFrame(list(returns.items()), columns=['Stock', '1-Year Return'])

    # Check if returns_df is empty
    if returns_df.empty:
        print("No valid returns data found.")
    else:
        # Calculate the total return to find weightage
        total_return = returns_df['1-Year Return'].sum()

        # Calculate weightage
        returns_df['Weightage'] = (returns_df['1-Year Return'] / total_return)*100

        # Display the results
        print(returns_df)

    # Show the DataFrame
    returns_df