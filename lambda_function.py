from FOR_KEYUR import get_watchlist_for_keyur
from algorithms.Filter_Algorithm import FilterAlgorithm
from algorithms.Midcap_Buy_Algorithm import MidcapBuyAlgorithm
from algorithms.Midcap_Buy_Algorithm import MidcapBuyAlgorithm
from algorithms.Midcap_Sell_Algorithm import MidcapSellAlgorithm
from algorithms.Trade_Sync import TradeSync
from brokers.motilal.helper.read_client_data import read_csv_to_dict
from database.dao.watchlist_dao import get_watchlist
from database.dynamodb import get_database
from database.dao.client_dao import *
from database_cleanup import prepare_buy_testdata, prepare_sell_testdata
from utils.csv.helpers import save_buy_orders, save_sell_orders
from utils.json.helper import get_buy_orders, get_sell_orders, set_buy_orders, set_sell_orders
from utils.watchlist_filter import massage_watchlist

def buy():
    prepare_buy_testdata()
    buy_stocks = ['IDEA.NS']
    buy_algo = MidcapBuyAlgorithm(buy_stocks)
    buy_algo.allocate_slots()
    buy_orders = buy_algo.order_executor()
    print(f"Buy orders:- {buy_orders}")
    set_buy_orders(buy_orders)
    return buy_orders
    
    
def sell():
    prepare_sell_testdata()
    sell_stocks = ['IDEA.NS']
    sell_algo = MidcapSellAlgorithm()
    # sell_algo.sell_logic()
    sell_algo.adhoc_sell(sell_stocks)
    sell_orders = sell_algo.position_sizing()
    print(f"Sell orders:- {sell_orders}")
    set_sell_orders(sell_orders)
    return sell_orders

def trade_sync_buy():
    
    buy_orders = get_buy_orders()
    trade_sync = TradeSync(buy_orders)
    filled,unfilled = trade_sync.check_orders(buy_orders)
    print(f"Filled : {filled}")
    print(f"Unfilled : {unfilled}")
    trade_sync.sync_filled_buy_trades(filled)
    print("Trade Synced for filled orders")
    
    if(not unfilled): return
    print("Retry for below Unfilled")
    print(f"Unfilled:- {unfilled}")
    filled,unfilled = trade_sync.check_orders(unfilled)
    trade_sync.sync_filled_buy_trades(filled)
    print("Try 2: Trade Synced for filled orders")
    
    if(not unfilled): return
    print("Market order for below unfilled")
    print(f"Unfilled:- {unfilled}")
    modified,unmodified = trade_sync.bulk_modify_to_market(unfilled)
    print(f"Modified orders: {modified}")
    filled,unfilled = trade_sync.check_orders(modified)
    print(f"Now filled{filled}")
    print(f"Now unfilled{filled}")
    trade_sync.sync_filled_buy_trades(filled)
    print("Failed even after Modify")
    print(unfilled)
    return

def trade_sync_sell():
    
    sell_orders = get_sell_orders()
    trade_sync = TradeSync(sell_orders)
    filled,unfilled = trade_sync.check_orders(sell_orders)
    print(f"Try 1: Unfilled : {unfilled}")
    trade_sync.sync_filled_sell_trades(filled)
    print("Try 1: Trade Synced for filled orders")
    
    if(not unfilled): return
    print("Try 2: Retry for below Unfilled")
    print(f"Try 2: Unfilled:- {unfilled}")
    
    filled,unfilled = trade_sync.check_orders(unfilled)
    trade_sync.sync_filled_sell_trades(filled)
    print("Try 2: Trade Synced for filled orders")
    
    if(not unfilled): return
    print("Try 3: Market order for below unfilled")
    print(f"Try 3: Unfilled:- {unfilled}")
    modified,unmodified = trade_sync.bulk_modify_to_market(unfilled)
    
    filled,unfilled = trade_sync.check_orders(modified)
    trade_sync.sync_filled_sell_trades(filled)
    print("Failed even after Modify")
    print(unfilled)
    return
    
    
    
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
    buy_algo.allocate_slots()
    buy_orders = buy_algo.order_executor(all_client_data)
    
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
    
# if __name__ == "__main__":
#     run("Buy")

if __name__ == "__main__":
    
    # client_code = "WEALTH666"
    # client_auth = get_client_auth(client_code)
    # Mofsl = client_login(client_auth,client_code)
    # print(Mofsl.GetTradeDetailByUniqueorderID("1000002WEALTH666",client_code))
    
    # run("Sell")
    # trade_sync_sell()
    
    # run("Buy")
    trade_sync_buy()