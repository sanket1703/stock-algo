import json
from datetime import datetime
from FOR_KEYUR import get_watchlist_for_keyur
from adhoc_module.broker.motilal.order import ahdoc_order_box
from algorithms.Filter_Algorithm import FilterAlgorithm
from algorithms.Midcap_Buy_Algorithm import MidcapBuyAlgorithm
from algorithms.Midcap_Buy_Algorithm import MidcapBuyAlgorithm
from algorithms.Midcap_Sell_Algorithm import MidcapSellAlgorithm
from algorithms.Trade_Sync import TradeSync
from brokers.motilal.helper.read_client_data import read_csv_to_dict
from database.dao.watchlist_dao import get_watchlist
from database.dynamodb import get_database
from database.dao.client_dao import *
from database.cleanup.database_cleanup import prepare_buy_testdata, prepare_sell_testdata
from jobs.exchange_tradeid_job import exchange_tradeid_job
from jobs.mo_login_check_job import check_login_job
from jobs.pre_order_executor_job import pre_order_executor_job
from utils.csv.helpers import save_buy_orders, save_sell_orders
from utils.helpers.check_time import check_end_of_market
from utils.helpers.take_confirmation import take_confirmation
from utils.json.helper import (get_buy_orders, get_filled_buy_orders, get_filled_sell_orders, get_sell_orders,
                               set_buy_orders, set_sell_orders)
from utils.logging.configure import configure_log
from utils.watchlist_filter import massage_watchlist
import warnings
from loguru import logger
from jobs.clean_json import clean_order_jsons_job


def buy(buy_stocks):
    prepare_buy_testdata()
    logger.info(f"Stock list for buy :\n{buy_stocks}")
    if (take_confirmation()):
        logger.info(f"Buy stock list:- {buy_stocks}")
        buy_algo = MidcapBuyAlgorithm(buy_stocks)
        buy_algo.allocate_slots()
        buy_orders = buy_algo.order_executor()
        set_buy_orders(buy_orders)
        logger.info(
            f"Consolidated Buy Orders details for each client:- {buy_orders}")
        logger.debug("Consolidated Buy Orders details saved locally.")
        return buy_orders
    else:
        return


def sell(sell_stocks):
    prepare_sell_testdata(sell_stocks)
    logger.info(f"Stock list for sell : \n{sell_stocks}")
    if (take_confirmation()):
        logger.info(f"Stock list for sell :{sell_stocks}")
        sell_algo = MidcapSellAlgorithm()
        # sell_algo.sell_logic()
        sell_algo.adhoc_sell(sell_stocks)
        sell_orders = sell_algo.order_executor()
        set_sell_orders(sell_orders)
        logger.info(
            f"Consolidated Sell Orders details for each client:- {sell_orders}")
        logger.debug("Consolidated Sell Orders details saved locally.")
        return sell_orders
    else:
        return


def buy_order_validator():

    buy_orders = get_buy_orders()
    trade_sync = TradeSync(buy_orders)
    filled, unfilled = trade_sync.check_buy_orders(buy_orders)

    if (not unfilled):
        logger.info("All Buy orders filled")
        return

    logger.info(f"Retry 1: Order validation for {unfilled}")

    filled, unfilled = trade_sync.check_buy_orders(unfilled)

    if (not unfilled):
        logger.info("All Buy orders filled")
        return

    if (check_end_of_market()):
        logger.info(f"Update to market order for {unfilled}")
        modified, unmodified = trade_sync.bulk_modify_to_market(unfilled)
        logger.info(
            f"Retry 2: Order validation for {unfilled} after Modify to Market")
        filled, unfilled = trade_sync.check_buy_orders(modified)
        return
    return


def filled_buy_orders_processor():

    filled_buy_orders = get_filled_buy_orders()
    trade_sync = TradeSync(filled_buy_orders)
    trade_sync.sync_filled_buy_trades(filled_buy_orders)


def sell_order_validator():

    sell_orders = get_sell_orders()
    trade_sync = TradeSync(sell_orders)
    filled, unfilled = trade_sync.check_sell_orders(sell_orders)

    if (not unfilled):
        logger.info("All Buy orders filled")
        return

    logger.info(f"Retry 1: Order validation for {unfilled}")

    filled, unfilled = trade_sync.check_sell_orders(unfilled)

    if (not unfilled):
        logger.info("All Sell orders filled")
        return

    if (check_end_of_market()):
        logger.info(f"Update to market order for {unfilled}")
        modified, unmodified = trade_sync.bulk_modify_to_market(unfilled)
        logger.info(
            f"Retry 2: Order validation for {unfilled} after Modify to Market")
        filled, unfilled = trade_sync.check_sell_orders(modified)
        return
    return


def filled_sell_orders_processor():

    filled_sell_orders = get_filled_sell_orders()
    trade_sync = TradeSync(filled_sell_orders)
    trade_sync.sync_filled_sell_trades(filled_sell_orders)


def lambda_handler(event, context):
    if event["action"] == "Buy":
        return buy(event["stocks"])
    elif event["action"] == "Sell":
        return sell(event["stocks"])

def order_executor(direction, stocks):
    event = {}
    event["action"] = direction
    event["stocks"] = stocks
    lambda_handler(event, None)


def shouldValidate():
    # Condition 1: Check if the current time is before 3:25 PM
    # current_time = datetime.now().time()
    # if current_time >= datetime.strptime("15:25", "%H:%M").time():
    #     return False

    # Load unfilled buy and sell orders from JSON files
    with open('order_book/unfilled_orders/unfilled_buy_orders.json', 'r') as buy_file:
        unfilled_buy_orders = json.load(buy_file)

    with open('order_book/unfilled_orders/unfilled_sell_orders.json', 'r') as sell_file:
        unfilled_sell_orders = json.load(sell_file)

    # Condition 2 & 3: Check if there is at least one non-empty list in either buy or sell orders
    any_buy_orders_non_empty = any(
        orders for client, orders in unfilled_buy_orders.items() if client != "date"
    )
    any_sell_orders_non_empty = any(
        orders for client, orders in unfilled_sell_orders.items() if client != "date"
    )

    # Return True if there is at least one non-empty list in either buy or sell orders
    return any_buy_orders_non_empty or any_sell_orders_non_empty


def validate_orders():
    while (shouldValidate()):
        buy_order_validator()
        sell_order_validator()

def sync_orders():
    filled_buy_orders_processor()
    filled_sell_orders_processor()
    exchange_tradeid_job()

def pre_run_checklist():
    check_login_job()
    clean_order_jsons_job()

if __name__ == "__main__":

    ######################################
    #########   Configurations    ########
    ######################################

    warnings.filterwarnings("ignore")
    configure_log(level="DEBUG")
    
    ######################################
    #########      Full Run       ########
    ######################################
    
    pre_run_checklist()

    buy_list = ["IDEA.NS", "GTLINFRA.NS"]
    order_executor("Buy", buy_list)

    sell_list = ["IDEA.NS", "GTLINFRA.NS"]
    order_executor("Sell", sell_list)
    
    # validate_orders()

    # sync_orders()
    
    ######################################
    ##   Before Execution (ONLY ONCE)   ##
    ######################################
    
    # pre_order_executor_job()

    ######################################
    #######     Buy Suite     ############
    ######################################
    
    # buy_list = ["IDEA.NS", "GTLINFRA.NS"]
    # order_executor("Buy", buy_list)
    # buy_order_validator()
    # filled_buy_orders_processor()

    ######################################
    #######     Sell Suite     ###########
    #####################################
    
    # sell_list = []
    # order_executor("Sell", sell_list)
    # sell_order_validator()
    # filled_sell_orders_processor()

    #####################################
    #######        Jobs       ###########
    #####################################

    # exchange_tradeid_job()
    # check_login_job()
    # clean_order_jsons_job()

    ######################################
    #########      Adhoc Jobs    #########
    ######################################
    
    # ahdoc_order_box()
