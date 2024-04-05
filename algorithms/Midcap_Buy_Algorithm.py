from stock_data.indicators import calculate_ema, calculate_supertrend
from stock_data.price import fetch_stock_data, get_last_traded_price


class MidcapBuyAlgorithm:
    def __init__(self,stock_list):
        self.stock_list = stock_list
        self.ranked_stock_list = []

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
            self.ranked_stock_list.append(stock[0])
            
        print(self.ranked_stock_list)
        return self.ranked_stock_list
    
    def filter_stocks(self):
        """
        Filters stocks based on specified conditions.

        Args:
            stocks (list): List of stock symbols.

        Returns:
            list: Filtered list of stocks.
        """
        filtered_stocks = []
        for symbol in self.ranked_stock_list:
            data = fetch_stock_data(symbol)
            if data.empty:
                print(f"No data available for {symbol}.")
                continue
            ema = calculate_ema(data)
            last_traded_price = data['Close'].iloc[-1]
            supertrend = calculate_supertrend(data)
            print(ema.iloc[-1])
            print(last_traded_price)
            print(supertrend.iloc[-1])
            if last_traded_price > 1.03 * ema.iloc[-1] and last_traded_price > supertrend.iloc[-1]:
                filtered_stocks.append(symbol)
                
        self.filtered_stocks = filtered_stocks
        return filtered_stocks
    
    
    def slot_fill(self):
        # Will come from Database
        slots = set(['a'])
        
        max_slots = 13
        total_available_slots = max_slots - len(slots)
        
        if total_available_slots == 0:
            return
        
        # Will come from the Filtered stocks
        final_stocks = []
        for stock in self.filtered_stocks:
            if stock not in slots:
                final_stocks.append(stock)
                # Make a database entery
                slots.add(stock)
            
            if len(final_stocks) >= total_available_slots:
                break
        self.stocks_to_buy = final_stocks
        self.total_available_slots = total_available_slots
        
        return (final_stocks,total_available_slots)


# Example usage
if __name__ == "__main__":
    print
