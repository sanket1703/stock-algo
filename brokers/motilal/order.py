from decimal import Decimal
from brokers.motilal.login import client_login
from database.dao.client_dao import get_client_holding
from database.dynamodb import get_database
import loguru
from notification.email.send_email import send_email
from stock_data.price import fetch_1d_stock_data, get_last_traded_price
from stock_data.symbols import get_symbol_token
from loguru import logger

from utils.helpers.get_config import get_test_mode
from utils.json.orders_json_helper import update_order_list, update_status

def place_buy_order(client_code,stock_code_nse,qty,Mofsl):
    logger.info(
        f"Placing buy order of {qty} {stock_code_nse} for {client_code} ")
    ltp = get_last_traded_price(fetch_1d_stock_data(stock_code_nse))
    stock_code = get_symbol_token(stock_code_nse)
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

    if(response["status"]!="SUCCESS"):
        notification_error("BUY",response,client_code)
        if('uniqueorderid' in response):
            update_order_list(response['uniqueorderid'], client_code,
                              stock_code_nse, qty, ltp, "Buy", "Limit", "Not Placed", response['message'], "",0, 0, "", "FA13")
            return response['uniqueorderid']
        else: 
            update_order_list(response['uniqueorderid'], client_code,
                              stock_code_nse, qty, ltp, "Buy", "Limit", "FAILED", response['message'], "", 0, 0, "","FA13")
            return ''
    else:
        update_order_list(response['uniqueorderid'], client_code,
                      stock_code_nse, qty, ltp, "Buy", "Limit", "Placed", response['message'], "", 0, 0, "","FA13")
    return response['uniqueorderid']

def notification_error(direction,message_text,client):
    sender = "Keyursanket.com"
    recipient = "sanketyou8@gmail.com"
    cc = "keyurmarolia2@gmail.com"
    subject = f"[{client}] Place {direction} Order FAILED."
    message = f"Error Response \n\n{message_text}"
    send_email(sender,recipient,cc,subject,message,None)


def place_sell_order(client_code, stock_code_nse, Mofsl):
    
    # if (get_test_mode()):qty=1
    # else: qty = get_client_holding(get_database(),client_code,stock_code)
    
    
    ltp = get_last_traded_price(fetch_1d_stock_data(stock_code_nse))
    # Convert it into the token that motilal wants
    stock_code = get_symbol_token(stock_code_nse)
    qty = get_client_holding(get_database(), client_code, stock_code_nse)
    logger.debug(
        f"Placing sell order of {qty} {stock_code_nse} for {client_code} ")
    Orderinfo = {
        "clientcode":client_code,      
        "exchange":"NSE",
        "symboltoken":stock_code,
        "buyorsell":"SELL",
        "ordertype":"LIMIT",
        "producttype":"DELIVERY",
        "orderduration":"DAY",
        "quantityinlot":int(qty),
         "amoorder":"N",
         "price":round(ltp, 4),
    }
    response = Mofsl.PlaceOrder(Orderinfo)
    logger.debug(f"PlaceOrder for Sell Response:- {response}")
    logger.info(f"PlaceOrder for Sell Message:- {response['message']}")
    if(response["status"]!="SUCCESS"):
        notification_error("SELL",response,client_code)
        if('uniqueorderid' in response):
            update_order_list(response['uniqueorderid'], client_code,
                              stock_code_nse, int(qty), ltp, "Sell", "Limit", "Not Placed", response['message'], "", 0, 0, "","FA13")

            return response['uniqueorderid']
        else:
            update_order_list("", client_code,
                              stock_code_nse, int(qty), ltp, "Sell", "Limit", "FAILED", response['message'], "", 0, 0, "","FA13")

            return ''
    else:
        update_order_list(response['uniqueorderid'], client_code,
                      stock_code_nse, int(qty), ltp, "Sell", "Limit", "Placed", response['message'], "",0,0,"","FA13")

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
    

def is_order_completed(Mofsl, client_code, order_id):
    order_details = Mofsl.GetOrderDetailByUniqueorderID(order_id,client_code)
    logger.debug(f"Order details for {client_code} for {order_id}:- {order_details} ")
    if (order_details['status'] == "FAILED" or order_details['message']=='NO RECORDS FOUND'):
        update_status(order_id=order_id, message=order_details['message'])
        logger.error(f"Could not fetch the order details. Either the order_id expired or could not call MOFSL")
        return False
    
    if (order_details["status"] == "SUCCESS"):
        if (order_details['data'][0]['error']!=""):
            update_status(order_id=order_id,
                          message=order_details['data'][0]['error'])
            return False
    
    if (order_details['data'][0]['orderstatus']=="Traded"):
        logger.info(f"Order is executed and the status is 'Traded'")
        update_status(order_id=order_id, 
                      status="Traded",
                      message=order_details['message'], 
                      exchange_trade_id=order_details['data'][0]['orderid'], 
                      trade_price=order_details['data'][0]['averageprice'],
                      trade_qty=order_details['data'][0]['qtytradedtoday'])
        return True
    
    logger.info("Order is still not 'Traded")
    return False

def modify_order_to_market(Mofsl,client_code,order_id):
    # ModifyOrder
    logger.debug(f"Modifying to market for {order_id} of {client_code} ")
    qty = get_order_qty(Mofsl, client_code, order_id)
    ModifiedOrderInfo = {
        "clientcode":client_code,
        "uniqueorderid":order_id,
        "newordertype":"MARKET",
        "neworderduration":"DAY",   
        "newquantityinlot":qty,
        "newdisclosedquantity":qty,
        # "newprice":235.50,
        # "newtriggerprice":0,
        # "newgoodtilldate": 0,
        "lastmodifiedtime": get_modified_time(Mofsl,client_code,order_id),
        "qtytradedtoday": get_trade_qty(Mofsl, client_code, order_id)
    }
    response = Mofsl.ModifyOrder(ModifiedOrderInfo)
    logger.debug(f"Modify to Market Response:- {response}")
    logger.info(f"Modify to Market Message:- {response['message']}")
    
    if response['status'] ==  "SUCCESS": 
        update_status(order_id, message=response['message'], order_type="Market")
        return True
    
    if(response["status"]!="SUCCESS"):
        notification_error("MODIFY MARKET",response,client_code)
        update_status(order_id, message=response['message'])
        return False