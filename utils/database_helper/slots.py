from database.dao.slots_dao import update_slots
from database.dynamodb import get_database
from loguru import logger
def clean_slots():
    db = get_database()
    update_slots(db,[])
    logger.info("Cleared slots on the database.")
    
def add_slots(slots):
    db = get_database()
    update_slots(db,slots)