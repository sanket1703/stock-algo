from datetime import datetime
from algorithms.Position_Sizing_Buy import PositionSizingBuy
from stock_data.indicators import calculate_ema, calculate_supertrend
from stock_data.price import fetch_stock_data, get_last_traded_price
from database.dao.slots_dao import * 
from database.dynamodb import get_database


class MidcapBuyAlgorithm:
    def __init__(self,stock_list,clients):
        self.db = get_database()
        self.stock_list = stock_list
        self.ranked_stock_list = []
        self.clients = clients
        self.final_stocks_buy = []
    
    def position_sizing(self):
        print("Starting Position sizing")
        buy_orders = {}
        for client_code in self.clients:
            client = PositionSizingBuy(client_code)
            client_order = client.position_sizing(self.final_stocks_buy,self.total_available_slots_before_buy)
            if client_order == None:
                continue
            buy_orders[client_code] = client_order
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            buy_orders["date"] = current_datetime
            
        print(buy_orders)
        return buy_orders
    
    
    
    def calculate_and_update_slots(self):
        
        slots = get_slots(self.db)
        buy_stocks = self.stock_list
        max_slots = 13
        self.total_available_slots_before_buy = max_slots - len(slots)
        
        if self.total_available_slots_before_buy == 0:
            print("There are no available slots.")
            return ([],self.total_available_slots_before_buy)
        
        for stock in buy_stocks:
            if stock not in slots:
                self.final_stocks_buy.append(stock)
                slots.append(stock)
            else:
                print(f"{stock} already present in the slots. Not Buying")
            
            if len(slots) >= max_slots:
                break
        
        total_available_slots_after_buy =  max_slots - len(slots)
        
        update_slots(self.db,list(slots))
        
        print("Final Buy signal to Algo Baba, Before total Available slots")
        print((self.final_stocks_buy,self.total_available_slots_before_buy))
        return self.final_stocks_buy,self.total_available_slots_before_buy
    
    


# Example usage
if __name__ == "__main__":
    print
