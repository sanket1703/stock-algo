from time import sleep
from flask import Flask, jsonify
from flask_cors import CORS

from algorithms.Midcap_Buy_Algorithm import MidcapBuyAlgorithm
from algorithms.Midcap_Sell_Algorithm import MidcapSellAlgorithm
from test_functions.sell_algo import sell_algo
from utils.helper import get_slots,update_slots

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
    stocks = ['LUPIN.NS','INDHOTEL.NS','POLYCAB.NS','PERSISTENT.NS','CUMMINSIND.NS']
    mid_cap_algo = MidcapBuyAlgorithm(stocks)
    mid_cap_algo.rank_stocks_by_ema_difference()
    mid_cap_algo.filter_stocks()
    mid_cap_algo.slot_fill()
    # print(sell_algo(stocks))
    return "buy" 

@app.route('/sell', methods=['GET'])
def sell():
    update_slots(['LUPIN.NS','INDHOTEL.NS','POLYCAB.NS','PERSISTENT.NS','CUMMINSIND.NS','RECLTD.NS'])
    sell_algo = MidcapSellAlgorithm()
    sell_algo.sell_logic()
    return "sell" 

if __name__ == '__main__':
    app.run(debug=True)