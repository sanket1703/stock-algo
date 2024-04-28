from flask import Flask
from flask_cors import CORS
from algorithms.Midcap_Buy_Algorithm import MidcapBuyAlgorithm
from time import sleep
from algorithms.Midcap_Buy_Algorithm import MidcapBuyAlgorithm
from algorithms.Midcap_Sell_Algorithm import MidcapSellAlgorithm
from tinydb import TinyDB, Query
from database.dto.clients import Client, DailyTradeLog, Holding
from database.dto.slots import Slots
from algorithms.Position_Sizing_Buy import PositionSizingBuy
from algorithms.Position_Sizing_Sell import PositionSizingSell
from database.dao.watchlist_dao import get_watchlist
from database.dynamodb import get_database
from database.dao.client_dao import *


app = Flask(__name__)
CORS(app)

@app.route('/buy', methods=['GET'])
def buy(stocks):
    
    # stocks = ['LUPIN.NS','INDHOTEL.NS','POLYCAB.NS','PERSISTENT.NS','CUMMINSIND.NS','ZYDUSLIFE.NS','RECLTD.NS','ABBOTINDIA.NS','TVSMOTOR.NS','AUBANK.NS','LTTS.NS','GUJGASLTD.NS','OFSS.NS','COFORGE.NS','ALKEM.NS','AUROPHARMA.NS','HONAUT.NS','ASTRAL.NS','MPHASIS.NS']
    db = get_database()
    # stocks = get_watchlist(db)
    
    mid_cap_algo = MidcapBuyAlgorithm(stocks)
    # mid_cap_algo.rank_stocks_by_ema_difference()
    mid_cap_algo.filter_stocks()

    final_stocks_buy, slots_before_buy = mid_cap_algo.slot_fill()
    clients = ["FTCT1208","Keyur"]
    
    for client in clients:
        print(f"Starting position sizing buy for {client}")
        client = PositionSizingBuy(client)
        client.position_sizing(final_stocks_buy,slots_before_buy)
    
    # snapshot = get_db_snapshot()
    return "Buy Algo Completed"
    

@app.route('/sell', methods=['GET'])
def sell():
    sell_algo = MidcapSellAlgorithm()
    stocks_to_sell = sell_algo.sell_logic()
    
    clients = ["FTCT1208","Keyur"]
    
    
    for client in clients:
        print(f"Starting position sizing selling for {client}")
        client = PositionSizingSell(client)
        client.off_load_stocks(stocks_to_sell)

    return "Sell Algo Completed"
    
if __name__ == "__main__":
    app.run(debug=True)