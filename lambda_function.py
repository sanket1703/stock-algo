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
from utils.json.helper import (get_buy_orders, get_filled_buy_orders, get_filled_sell_orders, get_sell_orders,
    set_buy_orders, set_sell_orders)
from utils.logging.configure import configure_log
from utils.watchlist_filter import massage_watchlist
import warnings
from loguru import logger


def buy():
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
    logger.info(f"Sell stock list:- {sell_stocks}")
    sell_algo = MidcapSellAlgorithm()
    # sell_algo.sell_logic()
    sell_algo.adhoc_sell(sell_stocks)
    sell_orders = sell_algo.order_executor()
    set_sell_orders(sell_orders)
    logger.info(f"Consolidated Sell Orders details for each client:- {sell_orders}")
    logger.debug("Consolidated Sell Orders details saved locally.")
    return sell_orders

def buy_order_validator():
    
    buy_orders = get_buy_orders()
    trade_sync = TradeSync(buy_orders)
    filled,unfilled = trade_sync.check_buy_orders(buy_orders)
    
    if(not unfilled): 
        logger.info("All Buy orders filled")
        return
    
    logger.info(f"Retry 1: Order validation for {unfilled}")

    filled,unfilled = trade_sync.check_buy_orders(unfilled)
    
    if(not unfilled): 
        logger.info("All Buy orders filled")
        return
    
    logger.info(f"Update to market order for {unfilled}")
    
    modified,unmodified = trade_sync.bulk_modify_to_market(unfilled)

    logger.info(f"Retry 2: Order validation for {unfilled} after Modify to Market")
    filled,unfilled = trade_sync.check_buy_orders(modified)
    return

def filled_buy_orders_processor():

    filled_buy_orders = get_filled_buy_orders()
    trade_sync = TradeSync(filled_buy_orders)
    trade_sync.sync_filled_buy_trades(filled_buy_orders)

def sell_order_validator():
    
    sell_orders = get_sell_orders()
    trade_sync = TradeSync(sell_orders)
    filled,unfilled = trade_sync.check_sell_orders(sell_orders)
    
    if(not unfilled): 
        logger.info("All Buy orders filled")
        return
    
    logger.info(f"Retry 1: Order validation for {unfilled}")

    filled,unfilled = trade_sync.check_sell_orders(unfilled)

    if(not unfilled): 
        logger.info("All Sell orders filled")
        return
    
    logger.info(f"Update to market order for {unfilled}")
    
    modified,unmodified = trade_sync.bulk_modify_to_market(unfilled)

    logger.info(f"Retry 2: Order validation for {unfilled} after Modify to Market")
    filled,unfilled = trade_sync.check_sell_orders(modified)
    return

def filled_sell_orders_processor():

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