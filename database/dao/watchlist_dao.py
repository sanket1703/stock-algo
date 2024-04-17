from tinydb import TinyDB

def get_watchlist():
    db = TinyDB('database/tinydb/db.json')
    watchlist = TinyDB.table(db,'watchlist')
    cuurent_watchlist = watchlist.all()[0]['watchlist']
    return cuurent_watchlist
    

def update_watchlist(update_watchlist):
    db = TinyDB('database/tinydb/db.json')
    watchlist = TinyDB.table(db,'watchlist')
    watchlist.update({'watchlist': update_watchlist}) 
    db.close()
    return update_watchlist