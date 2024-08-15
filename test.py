

from algobaba.buy_order import *
from algobaba.order_details import *
from database.dao.client_dao import get_client_holding
from database.dao.watchlist_dao import get_watchlist
from database.dynamodb import get_database
import yfinance as yf
import pandas as pd

from stock_data.price import one_year_return

if __name__ == "__main__":
    # send_buy_order(2,'ABB.NS','SANKET')
    get_watchlist(get_database())