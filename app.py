from time import sleep
from flask import Flask, jsonify
from flask_cors import CORS

from algorithms.Midcap_Buy_Algorithm import MidcapBuyAlgorithm
from algorithms.Midcap_Sell_Algorithm import MidcapSellAlgorithm
from test_functions.sell_algo import sell_algo
from database.dao.slots_dao import update_slots

from tinydb import TinyDB, Query


from database.dto.clients import Client, DailyTradeLog, Holding
from database.dto.slots import Slots
from algorithms.Position_Sizing_Buy import PositionSizingBuy
from algorithms.Position_Sizing_Sell import PositionSizingSell
from database.dao.watchlist_dao import get_watchlist

app = Flask(__name__)
CORS(app)  # Allow CORS for all routes

@app.route('/snapshot', methods=['GET'])
def get_db_snapshot():
    db = TinyDB('database/tinydb/db.json')
    client_table = TinyDB.table(db,'clients')
    slots_table = TinyDB.table(db,'slots')
    snapshot = {}
    snapshot["Slots"] = slots_table.all()
    snapshot["Clients"] = client_table.all()
    
    return snapshot

# Sample route to test CORS
@app.route('/test', methods=['GET'])
def test():
    stocks =  get_watchlist()
    # mid_cap_algo = MidcapAlgorithm(stocks)
    # mid_cap_algo.rank_stocks_by_ema_difference()
    # print(mid_cap_algo.filter_stocks())
    # print(mid_cap_algo.slot_fill())
    print(sell_algo(stocks))
    return "2" 

@app.route('/buy', methods=['GET'])
def buy():
    stocks = ['LUPIN.NS','INDHOTEL.NS','POLYCAB.NS','PERSISTENT.NS','CUMMINSIND.NS','ZYDUSLIFE.NS','RECLTD.NS','ABBOTINDIA.NS','TVSMOTOR.NS','AUBANK.NS','LTTS.NS','GUJGASLTD.NS','OFSS.NS','COFORGE.NS','ALKEM.NS','AUROPHARMA.NS','HONAUT.NS','ASTRAL.NS','BALKRISIND.NS','MPHASIS.NS']
    stocks =  get_watchlist()
    # stocks = ['LUPIN.NS','INDHOTEL.NS','POLYCAB.NS','PERSISTENT.NS','CUMMINSIND.NS']
    mid_cap_algo = MidcapBuyAlgorithm(stocks)
    # input("Please Enter to continue: ")
    mid_cap_algo.rank_stocks_by_ema_difference()
    # input("Please Enter to continue: ")
    mid_cap_algo.filter_stocks()
    # input("Please Enter to continue: ")
    final_stocks_buy, slots_before_buy = mid_cap_algo.slot_fill()
    # print(sell_algo(stocks))
    # input("Please Enter to continue: ")
    clients = ["Sanket","Keyur","Yasho"]
    
    for client in clients:
        print(f"Starting position sizing buy for {client}")
        client = PositionSizingBuy(client)
        client.position_sizing(final_stocks_buy,slots_before_buy)
    
    snapshot = get_db_snapshot()
    return snapshot

@app.route('/sell', methods=['GET'])
def sell():
    update_slots([ 'OFSS.NS'])
    sell_algo = MidcapSellAlgorithm()
    stocks_to_sell = sell_algo.sell_logic()
    
    clients = ["Sanket","Keyur","Yasho"]
    for client in clients:
        print(f"Starting position sizing selling for {client}")
        client = PositionSizingSell(client)
        client.off_load_stocks(stocks_to_sell)
    snapshot = get_db_snapshot()
    return snapshot

if __name__ == '__main__':
    db = TinyDB('database/tinydb/db.json')
    app.run(debug=True)