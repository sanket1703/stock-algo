from database.dao.slots_dao import update_slots
from database.dynamodb import get_database
def clean_slots():
    db = get_database()
    update_slots(db,[])
    print("Slots cleared")
    
def add_slots(slots):
    db = get_database()
    update_slots(db,slots)