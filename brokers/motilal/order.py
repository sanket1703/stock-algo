from brokers.motilal.login import client_login
from database.dao.client_dao import get_client_holding
from database.dynamodb import get_database
import loguru
from stock_data.price import fetch_1d_stock_data, get_last_traded_price
from stock_data.symbols import get_symbol_token
from loguru import logger

def place_buy_order(client_code,stock_code,qty,Mofsl):
    logger.info(f"Placing buy order of {qty} {stock_code} for {client_code} ")
    ltp = get_last_traded_price(fetch_1d_stock_data(stock_code))
    stock_code = get_symbol_token(stock_code)
    stock_code = stock_code
    Orderinfo = {
        "clientcode":client_code,      
        "exchange":"NSE",
        "symboltoken":stock_code,
        "buyorsell":"BUY",
        "ordertype":"LIMIT",
        "producttype":"DELIVERY",
        "orderduration":"DAY",
        "price":round(ltp, 4),
        "quantityinlot":qty,
        "amoorder":"N"
    }
    response = Mofsl.PlaceOrder(Orderinfo)
    logger.debug(f"PlaceOrder for Buy Response:- {response}")
    logger.info(f"PlaceOrder for Buy Message:- {response['message']}")
    return response['uniqueorderid']


def place_sell_order(db,client_code,stock_code,Mofsl):
    qty = 1
    # qty = get_client_holding(db,client_code,stock_code)
    logger.debug(f"Placing sell order of {qty} {stock_code} for {client_code} ")
    ltp = get_last_traded_price(fetch_1d_stock_data(stock_code))
    # Convert it into the token that motilal wants
    stock_code = get_symbol_token(stock_code)
    Orderinfo = {
        "clientcode":client_code,      
        "exchange":"NSE",
        "symboltoken":stock_code,
        "buyorsell":"SELL",
        "ordertype":"LIMIT",
        "producttype":"DELIVERY",
        "orderduration":"DAY",
        "quantityinlot":qty,
         "amoorder":"N",
         "price":round(ltp, 4),
    }
    response = Mofsl.PlaceOrder(Orderinfo)
    logger.debug(f"PlaceOrder for Sell Response:- {response}")
    logger.info(f"PlaceOrder for Sell Message:- {response['message']}")
    return response['uniqueorderid']


def get_modified_time(Mofsl,client_code,order_id):
    return Mofsl.GetOrderDetailByUniqueorderID(order_id,client_code)['data'][0]['lastmodifiedtime']

def get_trade_price(Mofsl,client_code,order_id):
    orderdetails = Mofsl.GetOrderDetailByUniqueorderID(order_id,client_code)
    return orderdetails['data'][0]['averageprice']

def get_xchange_trade_id(Mofsl,client_code,order_id):
    orderdetails = Mofsl.GetOrderDetailByUniqueorderID(order_id,client_code)
    return orderdetails['data'][0]['orderid']

def get_trade_qty(Mofsl,client_code,order_id):
    return Mofsl.GetOrderDetailByUniqueorderID(order_id,client_code)['data'][0]['qtytradedtoday']

def get_order_qty(Mofsl,client_code,order_id):
    return Mofsl.GetOrderDetailByUniqueorderID(order_id,client_code)['data'][0]['orderqty']
    
def order_status(Mofsl,client_code,order_id):
    order_details = Mofsl.GetOrderDetailByUniqueorderID(order_id,client_code)
    logger.debug(f"Order details for {client_code} for {order_id}:- {order_details} ")
    if (order_details['status'] == "FAILED" or order_details['message']=='NO RECORDS FOUND'):
        logger.error(f"Could not fetch the order details. Either the order_id expired or could not call MOFSL")
        return False
    if (order_details['data'][0]['orderstatus']=="Traded"):
        logger.info(f"Order is executed and the status is 'Traded'")
        return True
    logger.info("Order is still not 'Traded")
    return False
    
    
def is_order_completed(Mofsl,client_code,order_id):
    return order_status(Mofsl,client_code,order_id)

def modify_order_to_market(Mofsl,client_code,order_id):
    # ModifyOrder
    logger.debug(f"Modifying to market for {order_id} of {client_code} ")
    ModifiedOrderInfo = {
        "clientcode":client_code,
        "uniqueorderid":order_id,
        "newordertype":"MARKET",
        "neworderduration":"DAY",   
        "newquantityinlot":get_order_qty(Mofsl,client_code,order_id),
        # "newdisclosedquantity":0,
        # "newprice":235.50,
        # "newtriggerprice":0,
        # "newgoodtilldate": 0,
        "lastmodifiedtime": get_modified_time(Mofsl,client_code,order_id),
        "qtytradedtoday": 0
    }
    response = Mofsl.ModifyOrder(ModifiedOrderInfo)
    logger.debug(f"Modify to Market Response:- {response}")
    logger.info(f"Modify to Market Message:- {response['message']}")
    
    if response['status'] ==  "SUCCESS": return True
    return False