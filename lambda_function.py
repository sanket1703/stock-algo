from datetime import datetime
import time
from FOR_KEYUR import get_watchlist_for_keyur
from algorithms.Filter_Algorithm import FilterAlgorithm
from algorithms.Midcap_Buy_Algorithm import MidcapBuyAlgorithm
from time import sleep
from algorithms.Midcap_Buy_Algorithm import MidcapBuyAlgorithm
from algorithms.Midcap_Sell_Algorithm import MidcapSellAlgorithm
from tinydb import TinyDB, Query
from algorithms.Trade_Sync import TradeSync
from brokers.motilal.helper.read_client_data import read_csv_to_dict
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
from utils.watchlist_filter import massage_watchlist




def buy():
    # Given by Keyur
    buy_stocks = ['LUPIN.NS','INDHOTEL.NS']
    buy_stocks = buy_stocks
    
    db = get_database()
    clients = get_client_list(db)
    all_client_data = read_csv_to_dict()
    print(f"Client Data :- {all_client_data}")
    buy_algo = MidcapBuyAlgorithm(buy_stocks,clients)
    buy_algo.calculate_and_update_slots()
    buy_orders = buy_algo.position_sizing(all_client_data)
    print(f"Buy orders:- {buy_orders}")
    
def complete():
    
    db = get_database()

    watch_list = get_watchlist(db)

    watch_list = get_watchlist_for_keyur()

    watch_list = massage_watchlist(watch_list)

    clients = get_client_list(db)
    
    all_client_data = read_csv_to_dict()
    
    filter_algo = FilterAlgorithm(watch_list)
    filter_algo.filter_watchlist()
    stocks = filter_algo.filter_stocks()
    
    buy_algo = MidcapBuyAlgorithm(stocks,clients)
    buy_algo.calculate_and_update_slots()
    buy_orders = buy_algo.position_sizing(all_client_data)
    
    print(f"Buy Orders :- {buy_orders}")
    save_buy_orders(buy_orders)
    
    sell_algo = MidcapSellAlgorithm(clients)
    sell_algo.sell_logic()
    sell_orders = sell_algo.position_sizing()
    
    print(f"Sell Orders :- {sell_orders}")
    save_sell_orders(sell_orders)
    
    buy_trade_sync = TradeSync()
    successful_buy_orders,failed_buy_orders = buy_trade_sync.check_orders(buy_orders)
    
    print(f"Failed Buy Orders :- {failed_buy_orders}")
    
    sell_trade_sync = TradeSync()
    successful_sell_orders,failed_sell_orders = sell_trade_sync.check_orders(sell_orders)
    
    print(f"Failed Sell Orders :- {failed_sell_orders}")
    
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
        return buy()
    elif event["action"] == "Sell":
        return sell()
    elif event["action"] == "Complete":
        return complete()
        

def run(direction):
    event = {}
    event["action"] = direction
    lambda_handler(event,None)
    
if __name__ == "__main__":
    clear_stack()
    run("Buy")