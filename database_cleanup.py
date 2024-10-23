from database.dao.slots_dao import update_slots
from database.dynamodb import get_database
from utils.database_helper.client import clear_trade_log_clients
from utils.database_helper.slots import add_slots, clean_slots
from loguru import logger

   
def prepare_sell_testdata():
    add_slots(list(['LUPIN.NS']))
    
def prepare_buy_testdata():
    logger.debug("Preparing buy test data")
    clear_trade_log_clients()
    clean_slots()
    logger.info("Test data prepared. Ready to buy.")
