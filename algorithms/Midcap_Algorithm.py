from stock_data.indicators import calculate_ema, calculate_supertrend
from stock_data.price import fetch_stock_data, get_last_traded_price


class MidcapAlgorithm:
    def __init__(self,stock_list):
        self.stock_list = stock_list

    def rank_stocks_by_ema_difference(self):
        """
        Ranks stocks based on the difference between the 100-day EMA and the last traded price.

        Args:
            stocks (list): List of stock symbols.

        Returns:
            list: Ranked list of stocks based on EMA difference.
        """
        ranked_stocks = []
        for symbol in self.stock_list:
            data = fetch_stock_data(symbol)
            if data.empty:
                print(f"No data available for {symbol}.")
                continue
            ema = calculate_ema(data)
            last_traded_price = get_last_traded_price(data)
            ema_difference = abs(ema.iloc[-1] - last_traded_price)
            ranked_stocks.append((symbol, ema_difference))
        
        ranked_stocks.sort(key=lambda x: x[1])
        
        for stock in ranked_stocks:
            self.stock_list.append(stock[0])
            
        return self.stock_list
    
    def filter_stocks(self):
        """
        Filters stocks based on specified conditions.

        Args:
            stocks (list): List of stock symbols.

        Returns:
            list: Filtered list of stocks.
        """
        filtered_stocks = []
        for symbol in self.stock_list:
            data = fetch_stock_data(symbol)
            if data.empty:
                print(f"No data available for {symbol}.")
                continue
            ema = calculate_ema(data)
            last_traded_price = data['Close'].iloc[-1]
            supertrend = calculate_supertrend(data)
            if last_traded_price > 1.03 * ema.iloc[-1] and last_traded_price > supertrend.iloc[-1]:
                filtered_stocks.append(symbol)
        return filtered_stocks


# Example usage
if __name__ == "__main__":
   print
