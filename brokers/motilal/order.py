from brokers.motilal.login import client_login
from database.dao.client_dao import get_client_holding
from database.dynamodb import get_database
from stock_data.price import fetch_1d_stock_data, get_last_traded_price
from stock_data.symbols import get_symbol_token
from algobaba.order_details import get_trade_price, get_trade_qty, is_order_completed

def place_buy_order(client_code,stock_code,qty,Mofsl):
    print("--------------------------------PlaceOrder--------------------------------")
    ltp = get_last_traded_price(fetch_1d_stock_data(stock_code))
    # Convert it into the token that motilal wants
    stock_code = get_symbol_token(stock_code)
    print(round(ltp, 4),stock_code)
    stock_code = stock_code
    Orderinfo = {
        "clientcode":client_code,      
        "exchange":"NSE",
        "symboltoken":stock_code,
        "buyorsell":"BUY",
        "ordertype":"LIMIT",
        "producttype":"DELIVERY",
        "orderduration":"DAY",
        "price":round(ltp-0.3, 4),
        "quantityinlot":qty,
        "amoorder":"N"
    }
    print(f"Placing buy order for {client_code} with order info {Orderinfo}")
    response = Mofsl.PlaceOrder(Orderinfo)

    print(f"Buy Order for {client_code} is {response}")
    return response['uniqueorderid']


def place_sell_order(db,client_code,stock_code,Mofsl):
    print("--------------------------------PlaceOrder--------------------------------")
    # PlaceOrderInfo
    qty = 1
    # qty = get_client_holding(db,client_code,stock_code)
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
    print(f"Placing sell order for {client_code}")
    print(Orderinfo)
    
    response = Mofsl.PlaceOrder(Orderinfo)
    print(f"Sell Order for {client_code} is {response}")
    return response['uniqueorderid']


def get_modified_time(Mofsl,client_code,order_id):
    return Mofsl.GetOrderDetailByUniqueorderID(order_id,client_code)['data'][0]['lastmodifiedtime']

def get_trade_price(Mofsl,client_code,order_id):
    orderdetails = Mofsl.GetOrderDetailByUniqueorderID(order_id,client_code)
    print(orderdetails)
    return orderdetails['data'][0]['averageprice']
    
def get_trade_qty(Mofsl,client_code,order_id):
    return Mofsl.GetOrderDetailByUniqueorderID(order_id,client_code)['data'][0]['qtytradedtoday']

def get_order_qty(Mofsl,client_code,order_id):
    return Mofsl.GetOrderDetailByUniqueorderID(order_id,client_code)['data'][0]['orderqty']
    
def order_status(Mofsl,client_code,order_id):
    order_details = Mofsl.GetOrderDetailByUniqueorderID(order_id,client_code)
    print(order_details)
    if (order_details['status'] == "FAILED" or order_details['message']=='NO RECORDS FOUND'):
        return False
    if (order_details['data'][0]['orderstatus']=="Traded" ):
        return True
    return False
    
    
def is_order_completed(Mofsl,client_code,order_id):
    return order_status(Mofsl,client_code,order_id)

def modify_order_to_market(Mofsl,client_code,order_id):
    # ModifyOrder
    print(f"--------------------------------ModifyOrder for {client_code}--------------------------------")
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
    print(f"Modify Order Response: {response}")
    if response['status'] ==  "SUCCESS": return True
    return False