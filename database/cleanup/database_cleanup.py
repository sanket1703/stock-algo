from utils.database_helper.client import clear_trade_log_clients
from utils.database_helper.slots import add_slots, clean_slots
from loguru import logger

   
def prepare_sell_testdata(sell_stocks):
    logger.debug("Preparing sell test data")
    add_slots(sell_stocks)
    logger.info("Test data prepared. Ready to sell.")
    
def prepare_buy_testdata():
    logger.debug("Preparing buy test data")
    clear_trade_log_clients()
    clean_slots()
    logger.info("Test data prepared. Ready to buy.")
