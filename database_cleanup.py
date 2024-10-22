from database.dao.slots_dao import update_slots
from database.dynamodb import get_database
from utils.database_helper.client import clear_trade_log_clients
from utils.database_helper.slots import add_slots, clean_slots

   
def prepare_sell_testdata():
    add_slots(list(['LUPIN.NS']))
    
def prepare_buy_testdata():
    clear_trade_log_clients()
    clean_slots()
