from algorithms.Midcap_Buy_Algorithm import MidcapBuyAlgorithm
from time import sleep
from flask import Flask, jsonify
from flask_cors import CORS
from algorithms.Midcap_Buy_Algorithm import MidcapBuyAlgorithm
from algorithms.Midcap_Sell_Algorithm import MidcapSellAlgorithm
from test_functions.sell_algo import sell_algo
from database.dao_tiny.slots_dao import update_slots
from tinydb import TinyDB, Query
from database.dto.clients import Client, DailyTradeLog, Holding
from database.dto.slots import Slots
from algorithms.Position_Sizing_Buy import PositionSizingBuy
from algorithms.Position_Sizing_Sell import PositionSizingSell
from database.dao.watchlist_dao import get_watchlist
from database.dynamodb import get_database


def buy():
    
    stocks = ['LUPIN.NS','INDHOTEL.NS','POLYCAB.NS','PERSISTENT.NS','CUMMINSIND.NS','ZYDUSLIFE.NS','RECLTD.NS','ABBOTINDIA.NS','TVSMOTOR.NS','AUBANK.NS','LTTS.NS','GUJGASLTD.NS','OFSS.NS','COFORGE.NS','ALKEM.NS','AUROPHARMA.NS','HONAUT.NS','ASTRAL.NS','MPHASIS.NS']
    db = get_database()
    stocks = get_watchlist(db)
    
    mid_cap_algo = MidcapBuyAlgorithm(stocks)
    mid_cap_algo.rank_stocks_by_ema_difference()
    mid_cap_algo.filter_stocks()

    final_stocks_buy, slots_before_buy = mid_cap_algo.slot_fill()
    clients = ["Sanket","Keyur"]
    
    for client in clients:
        print(f"Starting position sizing buy for {client}")
        client = PositionSizingBuy(client)
        client.position_sizing(final_stocks_buy,slots_before_buy)
    
    # snapshot = get_db_snapshot()
    return "Buy Algo Completed"
    


def sell():
    sell_algo = MidcapSellAlgorithm()
    stocks_to_sell = sell_algo.sell_logic()
    
    clients = ["Sanket","Keyur"]
    for client in clients:
        print(f"Starting position sizing selling for {client}")
        client = PositionSizingSell(client)
        client.off_load_stocks(stocks_to_sell)

    return "Sell Algo Completed"


def lambda_handler(event, context):
    if event["action"] == "Buy":
        return buy()
    elif event["action"] == "Sell":
        return sell()
    
    
    
if __name__ == "__main__":
    event = {}
    event["action"] = "Buy"
    print(lambda_handler(event,None))