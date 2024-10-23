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
import time
from utils.csv.helpers import save_buy_orders, save_sell_orders
from utils.json.helper import (get_buy_orders, get_filled_buy_orders, get_filled_sell_orders, get_sell_orders,
    set_buy_orders, set_sell_orders)
from utils.logging.configure import configure_log
from utils.watchlist_filter import massage_watchlist
import socket
import dns.resolver
import warnings
from loguru import logger


def buy():
    # if not check_connectivity(): 
    #     print("Please check your connection")
    #     return
    prepare_buy_testdata()
    
    buy_stocks = ['IDEA.NS','MAHABANK.NS']
    logger.info(f"Buy stock list:- {buy_stocks}")
    buy_algo = MidcapBuyAlgorithm(buy_stocks)
    buy_algo.allocate_slots()
    buy_orders = buy_algo.order_executor()
    set_buy_orders(buy_orders)
    logger.info(f"Consolidated Buy Orders details for each client:- {buy_orders}")
    logger.debug("Consolidated Buy Orders details saved locally.")
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
    print(f"Buy orders :- {buy_orders}")
    trade_sync = TradeSync(buy_orders)
    filled,unfilled = trade_sync.check_buy_orders(buy_orders)
    print(f"Filled : {filled}")
    print(f"Unfilled : {unfilled}")
    
    if(not unfilled): return
    print("Retry for below Unfilled")
    print(f"Unfilled:- {unfilled}")
    time.sleep(1)
    filled,unfilled = trade_sync.check_buy_orders(unfilled)
    
    if(not unfilled): return
    print("Market order for below unfilled")
    print(f"Unfilled:- {unfilled}")
    time.sleep(1)
    modified,unmodified = trade_sync.bulk_modify_to_market(unfilled)
    print(f"Modified orders: {modified}")
    time.sleep(2)
    filled,unfilled = trade_sync.check_buy_orders(modified)
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

def sell_order_validator():
    
    sell_orders = get_sell_orders()
    trade_sync = TradeSync(sell_orders)
    filled,unfilled = trade_sync.check_sell_orders(sell_orders)
    print(f"Filled : {filled}")
    print(f"Unfilled : {unfilled}")
    time.sleep(1)
    if(not unfilled): return
    print("Retry for below Unfilled")
    print(f"Unfilled:- {unfilled}")
    filled,unfilled = trade_sync.check_sell_orders(unfilled)
    time.sleep(1)
    if(not unfilled): return
    print("Market order for below unfilled")
    print(f"Unfilled:- {unfilled}")
    
    modified,unmodified = trade_sync.bulk_modify_to_market(unfilled)
    print(f"Modified orders: {modified}")
    time.sleep(2)
    filled,unfilled = trade_sync.check_sell_orders(modified)
    print(f"Now filled{filled}")
    print(f"Now unfilled{unfilled}")
    print("Failed to Modify")
    print(unmodified)
    
    return

def filled_sell_orders_processor():
    # if not check_connectivity(): 
    #     print("Please check your connection")
    #     return
    filled_sell_orders = get_filled_sell_orders()
    trade_sync = TradeSync(filled_sell_orders)
    trade_sync.sync_filled_sell_trades(filled_sell_orders)
    
    
    
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
    
    configure_log(level="INFO")
    run("Buy")
    # buy_order_validator()
    # filled_buy_orders_processor()
    
    # input("Please press enter for sell: ")
    # print(f"Proceeding on command!")
    
    # run("Sell")
    # sell_order_validator()
    # filled_sell_orders_processor()
    # logger.debug("Test")
    # logger.info("This is an info message")
    # logger.warning("This is a warning message")
    # logger.error("This is an error message")
    # logger.critical("This is a critical message")