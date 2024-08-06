from datetime import datetime
import time
from algorithms.Filter_Algorithm import FilterAlgorithm
from algorithms.Midcap_Buy_Algorithm import MidcapBuyAlgorithm
from time import sleep
from algorithms.Midcap_Buy_Algorithm import MidcapBuyAlgorithm
from algorithms.Midcap_Sell_Algorithm import MidcapSellAlgorithm
from tinydb import TinyDB, Query
from algorithms.Trade_Sync import TradeSync
from database.dao.slots_dao import update_slots
from database.dto.clients import Client, DailyTradeLog, Holding
from database.dto.slots import Slots
from algorithms.Position_Sizing_Buy import PositionSizingBuy
from algorithms.Position_Sizing_Sell import PositionSizingSell
from database.dao.watchlist_dao import get_watchlist
from database.dynamodb import get_database
from database.dao.client_dao import *
from database_cleanup import clear_stack
from utils.csv.helpers import save_buy_orders, save_sell_orders




def buy(stocks):
    start_time_stock_data = time.time()
    stocks = ['LUPIN.NS','INDHOTEL.NS','POLYCAB.NS','PERSISTENT.NS','CUMMINSIND.NS','ZYDUSLIFE.NS','RECLTD.NS','ABBOTINDIA.NS','TVSMOTOR.NS','AUBANK.NS','LTTS.NS','GUJGASLTD.NS','OFSS.NS','COFORGE.NS','ALKEM.NS','AUROPHARMA.NS','HONAUT.NS','ASTRAL.NS','MPHASIS.NS']
    db = get_database()
    # stocks = get_filtered_watchlist()
    
    mid_cap_algo = MidcapBuyAlgorithm(stocks)
    
    # Step 1 :- Filter watchlist
    # mid_cap_algo.filter_watchlist()
    
    # Step 2 :- Filter Stocks 
    mid_cap_algo.filter_stocks()

    # Step 3 :- Calculate Slots (Do not update the Database)
    final_stocks_buy, slots_before_buy, slots = mid_cap_algo.slot_calculation() ##
    
    # Step 4 :- Get Client List from Database
    clients = ["FTCT1208","Keyur","Sanket","Smit","Sid"]
    
    end_time_stock_data = time.time()
    print(f"Execution timefor stock data: {end_time_stock_data-start_time_stock_data:.2f} seconds")
    
    buy_orders = {}
    # Step 5 :- Position Sizing + Order sending to Algo Baba
    for client_code in clients:
        # print(f"Starting position sizing buy for {client_code}")
        client = PositionSizingBuy(client_code)
        client_order = client.position_sizing(final_stocks_buy,slots_before_buy)
        if client_order == None:
            # print("Something is wrong with the client")
            continue
        buy_orders[client_code] = client_order
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        buy_orders["date"] = current_datetime
        
    print(buy_orders)
    
    # Step 6 :- Check Orders 
    trade_sync = TradeSync()
    successful_orders,failed_orders = trade_sync.check_orders(buy_orders)
    
    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time_stock_data  # Calculate the elapsed time
    print(f"Execution time: {elapsed_time:.2f} seconds")
    
    print(f"Failed orders:- {failed_orders}")
    
    
    start_time_trade_sync = time.time()
    # Step 7 :- Trade Sync
    trade_sync.sync_successful_buy_trades(successful_orders)
    
    # Step 8 :- Update the slots as everything is sucessful
    update_slots(db,list(slots))
    
    end_time_trade_sync = time.time()
    elapsed_time = end_time_trade_sync-start_time_trade_sync
    elapsed_time/=60
    print(f"Execution time: {elapsed_time:.2f} Minutes")
    
    return elapsed_time
    
def complete():
    
    db = get_database()
    
    watch_list = get_watchlist(db)
    watch_list = ['LUPIN.NS','INDHOTEL.NS','POLYCAB.NS','PERSISTENT.NS','CUMMINSIND.NS','ZYDUSLIFE.NS','RECLTD.NS','ABBOTINDIA.NS','TVSMOTOR.NS','AUBANK.NS','LTTS.NS','GUJGASLTD.NS','OFSS.NS','COFORGE.NS','ALKEM.NS','AUROPHARMA.NS','HONAUT.NS','ASTRAL.NS','MPHASIS.NS']
    
    clients = get_client_list(db)
    clients = ["Keyur","Smit","Sanket"]
    
    filter_algo = FilterAlgorithm(watch_list)
    filter_algo.filter_watchlist()
    stocks = filter_algo.filter_stocks()
    
    buy_algo = MidcapBuyAlgorithm(stocks,clients)
    buy_algo.calculate_and_update_slots()
    buy_orders = buy_algo.position_sizing()
    
    print(buy_orders)
    save_buy_orders(buy_orders)
    
    sell_algo = MidcapSellAlgorithm(clients)
    sell_algo.sell_logic()
    sell_orders = sell_algo.position_sizing()
    
    save_sell_orders(sell_orders)
    
    buy_trade_sync = TradeSync()
    successful_buy_orders,failed_buy_orders = buy_trade_sync.check_orders(buy_orders)
    
    print(f"Failed Buy Orders :- {failed_buy_orders}")
    
    sell_trade_sync = TradeSync()
    successful_sell_orders,failed_sell_orders = sell_trade_sync.check_orders(sell_orders)
    
    print(f"Failed Buy Orders :- {failed_sell_orders}")
    
    buy_trade_sync.sync_successful_buy_trades(successful_buy_orders)
    
    sell_trade_sync.sync_successful_sell_trades(successful_sell_orders)
    
    return 0
        


def sell():
    stocks = ['BHEL.NS','LTTS.NS']
    update_slots(get_database(),stocks)
    sell_algo = MidcapSellAlgorithm()
    stocks_to_sell = sell_algo.sell_logic()
    print(stocks_to_sell)
    clients = ["FTCT1208","Keyur","Sanket","Smit","Sid"]
    sell_orders = {}
    for client_code in clients:
        print(f"Starting position sizing selling for {client_code}")
        client = PositionSizingSell(client_code)
        client_order = client.off_load_stocks(stocks_to_sell)
        print(f"Client order:- {client_order}")
        if client_order == None:
            # print("Something is wrong with the client")
            continue
        sell_orders[client_code] = client_order
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sell_orders["date"] = current_datetime
        
    print(f"Sell orders:- {sell_orders}")
    trade_sync = TradeSync()
    successful_sell_orders,failed_orders = trade_sync.check_orders(sell_orders)
    print(f"Successful sell :- {successful_sell_orders}")
    trade_sync.sync_successful_sell_trades(successful_sell_orders)  

    return 0


def lambda_handler(event, context):
    if event["action"] == "Buy":
        stocks = ['LUPIN.NS','INDHOTEL.NS','POLYCAB.NS','PERSISTENT.NS','CUMMINSIND.NS','ZYDUSLIFE.NS','RECLTD.NS','ABBOTINDIA.NS','TVSMOTOR.NS','AUBANK.NS','LTTS.NS','GUJGASLTD.NS','OFSS.NS','COFORGE.NS','ALKEM.NS','AUROPHARMA.NS','HONAUT.NS','ASTRAL.NS','MPHASIS.NS']
        return buy(stocks)
    elif event["action"] == "Sell":
        return sell()
    elif event["action"] == "Complete":
        return complete()
        

def runner(n,direction):
    event = {}
    event["action"] = direction
    total_time = 0
    it = 0
    for i in range(1, n+1):
        print(i)
        it+=1
        total_time += lambda_handler(event,None)
        print(total_time/it)
    print(it)
    print(total_time/it)
    
if __name__ == "__main__":
    clear_stack()
    runner(1,"Complete")