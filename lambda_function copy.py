from datetime import datetime
import time
from algorithms.Midcap_Buy_Algorithm import MidcapBuyAlgorithm
from algorithms.Midcap_Sell_Algorithm import MidcapSellAlgorithm
from tinydb import TinyDB, Query
from algorithms.Trade_Sync import TradeSync
from database.dao.slots_dao import update_slots
from database.dto.clients import Client, DailyTradeLog, Holding
from database.dto.slots import Slots
from algorithms.Position_Sizing_Buy import PositionSizingBuy
from algorithms.Position_Sizing_Sell import PositionSizingSell
from database.dao.watchlist_dao import get_watchlist
from database.dynamodb import get_database
from database.dao.client_dao import *
import concurrent.futures
import botocore
from botocore.exceptions import ClientError



def optimize(client_code, final_stocks_buy, slots_before_buy):
    client = PositionSizingBuy(client_code)
    client_order = client.position_sizing(final_stocks_buy, slots_before_buy)
    print(f"Client order for {client_code}: {client_order}")
    if client_order is None:
        return None
    
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return (client_code, client_order, current_datetime)

def buy(stocks):
    start_time_stock_data = time.time()
    stocks = ['LUPIN.NS','INDHOTEL.NS','POLYCAB.NS','PERSISTENT.NS','CUMMINSIND.NS','ZYDUSLIFE.NS','RECLTD.NS','ABBOTINDIA.NS','TVSMOTOR.NS','AUBANK.NS','LTTS.NS','GUJGASLTD.NS','OFSS.NS','COFORGE.NS','ALKEM.NS','AUROPHARMA.NS','HONAUT.NS','ASTRAL.NS','MPHASIS.NS']
    # db = get_database_with_backoff()
    
    mid_cap_algo = MidcapBuyAlgorithm(stocks)
    mid_cap_algo.filter_stocks()
    final_stocks_buy, slots_before_buy = mid_cap_algo.slot_fill()
    clients = ["FTCT1208","Keyur"]
    
    end_time_stock_data = time.time()
    print(f"Execution time for stock data: {end_time_stock_data - start_time_stock_data:.2f} seconds")
    
    orders = {}
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(optimize, client_code, final_stocks_buy, slots_before_buy) for client_code in clients]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                client_code, client_order, current_datetime = result
                orders[client_code] = client_order
                orders["date"] = current_datetime
    
    print(orders)
    
    trade_sync = TradeSync()
    failed_orders = trade_sync.verify_trades(orders)
    
    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time_stock_data  # Calculate the elapsed time
    print(f"Execution time: {elapsed_time:.2f} seconds")
    
    return elapsed_time

def sell():
    sell_algo = MidcapSellAlgorithm()
    stocks_to_sell = sell_algo.sell_logic()
    
    clients = ["FTCT1208","Keyur","Sanket","Vivek","Smit","Sid"]
    
    for client in clients:
        print(f"Starting position sizing selling for {client}")
        client = PositionSizingSell(client)
        client.off_load_stocks(stocks_to_sell)

    return "Sell Algo Completed"

def lambda_handler(event, context):
    if event["action"] == "Buy":
        stocks = ['LUPIN.NS','INDHOTEL.NS','POLYCAB.NS','PERSISTENT.NS','CUMMINSIND.NS','ZYDUSLIFE.NS','RECLTD.NS','ABBOTINDIA.NS','TVSMOTOR.NS','AUBANK.NS','LTTS.NS','GUJGASLTD.NS','OFSS.NS','COFORGE.NS','ALKEM.NS','AUROPHARMA.NS','HONAUT.NS','ASTRAL.NS','MPHASIS.NS']
        return buy(stocks)
    elif event["action"] == "Sell":
        return sell()

if __name__ == "__main__":
    event = {"action": "Buy"}
    print(lambda_handler(event, None))
