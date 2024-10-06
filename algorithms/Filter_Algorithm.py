

from stock_data.indicators import calculate_ema, calculate_supertrend
from stock_data.price import fetch_stock_data


class FilterAlgorithm:
    def __init__(self,watchlist):
        self.stock_list = []
        self.ranked_stock_list = []
        self.watch_list = watchlist
    
    def filter_watchlist(self):
        '''
            50 Stocks will be fetched from the DB. These are Nifty 50 Stocks updated every quarter. These stocks will be filtered based on certain parameters
            and then they will be further processed.
        '''
        
        self.stock_list = self.watch_list
        return
    
    def filter_stocks(self):
        """
        Filters stocks based on specified conditions.

        Args:
            stocks (list): List of stock symbols.

        Returns:
            list: Filtered list of stocks.
        """
        self.ranked_stock_list = self.stock_list
        filtered_stocks = []
        for symbol in self.ranked_stock_list:
            data = fetch_stock_data(symbol)
            if data.empty:
                print(f"No data available for {symbol}.")
                continue
            ema = calculate_ema(data)
            last_traded_price = data['Close'].iloc[-1]
            supertrend = calculate_supertrend(data)
            # print(symbol)
            # print(ema.iloc[-1])
            # print(last_traded_price)
            # print(supertrend.iloc[-1])
            #filtered_stocks.append(symbol)
            if last_traded_price > 1.03 * ema.iloc[-1] and last_traded_price > supertrend.iloc[-1]:
                filtered_stocks.append(symbol)
                
        # print("Final Buy Stocks")
        self.filtered_stocks = filtered_stocks
        # print(self.filtered_stocks)
        return self.filtered_stocks