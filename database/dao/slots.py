from tinydb import TinyDB, Query

def get_slots():
    db = TinyDB('database/tinydb/db.json')
    slots = TinyDB.table(db,'slots')
    slots.update({'slots':['B']})
    # slots.insert({'slots': ['A']})
    print(slots.all())
    print(db)
    
def update_slots(slots):
    db = TinyDB('database/tinydb/db.json')
    slots = TinyDB.table(db,'slots')
    slots.update({'slots':['B']})
    # slots.insert({'slots': ['A']})
    print(slots.all())
    print(db)