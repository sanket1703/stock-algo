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
from utils.database_helper.client import clear_trade_log_clients
from utils.gsheets.helpers import add_text
from utils.gsheets.security.connect import gsheets_auth
from utils.json.helper import (get_buy_orders, get_filled_buy_orders, get_sell_orders,
    set_buy_orders, set_sell_orders)
from utils.watchlist_filter import massage_watchlist
import socket
import requests
import dns.resolver
import warnings


def buy():
    # if not check_connectivity(): 
    #     print("Please check your connection")
    #     return
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

def buy_order_validator():
    
    buy_orders = get_buy_orders()
    # if not check_connectivity(): 
    #     print("Please check your connection")
    #     return
    trade_sync = TradeSync(buy_orders)
    filled,unfilled = trade_sync.check_orders(buy_orders)
    print(f"Filled : {filled}")
    print(f"Unfilled : {unfilled}")

    if(not unfilled): return
    print("Retry for below Unfilled")
    print(f"Unfilled:- {unfilled}")
    filled,unfilled = trade_sync.check_orders(unfilled)
    
    if(not unfilled): return
    print("Market order for below unfilled")
    print(f"Unfilled:- {unfilled}")
    
    modified,unmodified = trade_sync.bulk_modify_to_market(unfilled)
    print(f"Modified orders: {modified}")
    filled,unfilled = trade_sync.check_orders(modified)
    print(f"Now filled{filled}")
    print(f"Now unfilled{unfilled}")
    print("Failed to Modify")
    print(unmodified)
    return

def filled_buy_orders_processor():
    # if not check_connectivity(): 
    #     print("Please check your connection")
    #     return
    filled_buy_orders = get_filled_buy_orders()
    trade_sync = TradeSync(filled_buy_orders)
    trade_sync.sync_filled_buy_trades(filled_buy_orders)

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
    

def check_mo_resolution():
    try:
        ip_address = socket.gethostbyname('openapi.motilaloswal.com')
        print(f"Domain resolved to IP: {ip_address}")
        return True
    except socket.gaierror:
        print("Can't resolve MO. Issue Connecting to MO.")
        return False
    
def check_connectivity():
    try:
        ip_address = socket.gethostbyname('google.com')
        print(f"Google resolved to IP: {ip_address}")
        if(not check_mo_resolution()):return False
        return True
    except socket.gaierror:
        print("Can't resolve google.Connectivity issue.")
        return False


def resolve_with_custom_dns(domain):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = ['8.8.8.8']  # Use Google's public DNS
    try:
        answers = resolver.resolve(domain)
        print(answers)
        for rdata in answers:
            print(f"Resolved IP: {rdata}")
    except Exception as e:
        print(f"Failed to resolve {domain}: {e}")


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    run("Buy")
    buy_order_validator()
    filled_buy_orders_processor()
    # print(gsheets_auth())
    # add_text()
    # update_dynamodb_balance("DEEPAK17",200)