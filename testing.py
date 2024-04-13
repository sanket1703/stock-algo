from tinydb import TinyDB

from database.dto.clients import Client, DailyTradeLog, Holding
from database.dto.slots import Slots


def convert_to_dict(obj):
    # If obj is a class instance, convert its attributes to a dictionary
    if isinstance(obj, (Client, Slots,DailyTradeLog, Holding)):
        return {key: convert_to_dict(value) if isinstance(value, (Client, Slots,DailyTradeLog,Holding)) else value
                for key, value in obj.__dict__.items()}
    # If obj is a list, recursively convert each item in the list
    elif isinstance(obj, list):
        return [convert_to_dict(item) for item in obj]
    else:
        return obj
    
def get_client_balance()

if __name__ == '__main__':
    db = TinyDB('database/tinydb/db.json')
    slots = TinyDB.table(db,'slots')
    client_table = TinyDB.table(db,'clients')
    
    daily_trade_log = DailyTradeLog(0,-1,100,10000,0,0,0)
    holding = Holding(1,2,3,4)
    client = Client(123,10000,daily_trade_log,holding)
    print(convert_to_dict(client))
    # client_table.insert(convert_to_dict(client))
    
    # "":"",
    # slots.insert({"slots":[]})\

    # client.insert({
    # "client_code": 1,
    # "last_available_balance" : "",
    # "daily_trade" : [{
    #     "date" : "",
    #     "stock_name" : "",
    #     "direction":"",
    #     "price":"",
    #     "charges":"",
    #     "net":"",
    #     "balance":"",
    #     }],
    # "holding": [{
    #     "stock_name":"",
    #     "qty":"",
    #     "last_buy_time_stamp":"",
    #     "last_buy_price":"",
    # }]
    # })
    