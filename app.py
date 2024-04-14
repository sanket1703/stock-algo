from time import sleep
from flask import Flask, jsonify
from flask_cors import CORS

from algorithms.Midcap_Buy_Algorithm import MidcapBuyAlgorithm
from algorithms.Midcap_Sell_Algorithm import MidcapSellAlgorithm
from test_functions.sell_algo import sell_algo
from utils.helper import get_slots,update_slots

from tinydb import TinyDB, Query


from database.dto.clients import Client, DailyTradeLog, Holding
from database.dto.slots import Slots
from algorithms.Position_Sizing_Buy import PositionSizingBuy
from algorithms.Position_Sizing_Sell import PositionSizingSell

app = Flask(__name__)
CORS(app)  # Allow CORS for all routes

# Sample route to test CORS
@app.route('/test', methods=['GET'])
def test():
    stocks = ['LUPIN.NS','INDHOTEL.NS','POLYCAB.NS','PERSISTENT.NS','CUMMINSIND.NS','ZYDUSLIFE.NS','RECLTD.NS','ABBOTINDIA.NS','TVSMOTOR.NS','AUBANK.NS','LTTS.NS','GUJGASLTD.NS','OFSS.NS','COFORGE.NS','ALKEM.NS','AUROPHARMA.NS','HONAUT.NS','ASTRAL.NS','BALKRISIND.NS','MPHASIS.NS']
    # stocks = ['INDHOTEL.NS']
    # mid_cap_algo = MidcapAlgorithm(stocks)
    # mid_cap_algo.rank_stocks_by_ema_difference()
    # print(mid_cap_algo.filter_stocks())
    # print(mid_cap_algo.slot_fill())
    print(sell_algo(stocks))
    return "2" 

@app.route('/buy', methods=['GET'])
def buy():
    stocks = ['LUPIN.NS','INDHOTEL.NS','POLYCAB.NS','PERSISTENT.NS','CUMMINSIND.NS','ZYDUSLIFE.NS','RECLTD.NS','ABBOTINDIA.NS','TVSMOTOR.NS','AUBANK.NS','LTTS.NS','GUJGASLTD.NS','OFSS.NS','COFORGE.NS','ALKEM.NS','AUROPHARMA.NS','HONAUT.NS','ASTRAL.NS','BALKRISIND.NS','MPHASIS.NS']
    # stocks = ['LUPIN.NS','INDHOTEL.NS','POLYCAB.NS','PERSISTENT.NS','CUMMINSIND.NS']
    mid_cap_algo = MidcapBuyAlgorithm(stocks)
    input("Please Enter to continue: ")
    mid_cap_algo.rank_stocks_by_ema_difference()
    input("Please Enter to continue: ")
    mid_cap_algo.filter_stocks()
    input("Please Enter to continue: ")
    final_stocks_buy, slots_before_buy = mid_cap_algo.slot_fill()
    # print(sell_algo(stocks))
    input("Please Enter to continue: ")
    clients = [123]
    
    for client in clients:
        client = PositionSizingBuy(client)
        client.position_sizing(final_stocks_buy,slots_before_buy)
    return "buy" 

@app.route('/sell', methods=['GET'])
def sell():
    update_slots(['LUPIN.NS','INDHOTEL.NS','POLYCAB.NS','PERSISTENT.NS','CUMMINSIND.NS','RECLTD.NS'])
    sell_algo = MidcapSellAlgorithm()
    stocks_to_sell = sell_algo.sell_logic()
    
    clients = [123]
    for client in clients:
        client = PositionSizingSell(client)
        client.off_load_stocks(stocks_to_sell)
        
        
    
    return "sell" 

if __name__ == '__main__':
    db = TinyDB('database/tinydb/db.json')
    app.run(debug=True)