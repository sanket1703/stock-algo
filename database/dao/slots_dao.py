from tinydb import TinyDB, Query

def get_slots():
    db = TinyDB('database/tinydb/db.json')
    slots = TinyDB.table(db,'slots')
    current_slots = slots.all()[0]['slots']
    return current_slots
    

def update_slots(update_slots):
    db = TinyDB('database/tinydb/db.json')
    slots = TinyDB.table(db,'slots')
    query = Query()
    slots.update({'slots': update_slots}) 
    db.close()
    return update_slots