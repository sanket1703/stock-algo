from stock_data.price import fetch_1d_stock_data, get_last_traded_price

def place_buy_order(client_code,stock_code,qty,Mofsl):
    print("--------------------------------PlaceOrder--------------------------------")
    ltp = get_last_traded_price(fetch_1d_stock_data(stock_code))
    # Convert it into the token that motilal wants
    print(ltp)
    stock_code = stock_code
    Orderinfo = {
        "clientcode":client_code,      
        "exchange":"NSE",
        "symboltoken":1660,
        "buyorsell":"BUY",
        "ordertype":"MARKET",
        "producttype":"DELIVERY",
        "orderduration":"DAY",
        # "price":ltp,
        "quantityinlot":qty,
        "amoorder":"N",
    }
    print(f"Placing order for {client_code} with order info {Orderinfo}")
    response = Mofsl.PlaceOrder(Orderinfo)

    print(f"Order for {client_code} is {response}")
    return response['uniqueorderid']


def place_sell_order(client_code,stock_code,qty,Mofsl):
    print("--------------------------------PlaceOrder--------------------------------")
    # PlaceOrderInfo
    ltp = get_last_traded_price(fetch_1d_stock_data(stock_code))
    # Convert it into the token that motilal wants
    stock_code = stock_code
    Orderinfo = {
        "clientcode":client_code,      
        "exchange":"NSE",
        "symboltoken":stock_code,
        "buyorsell":"SELL",
        "ordertype":"LIMIT",
        "producttype":"NORMAL",
        "orderduration":"DAY",
        "price":ltp,
        "triggerprice":0,
        "quantityinlot":qty
    }
    print(f"Placing order for {client_code}")
    response = Mofsl.PlaceOrder(Orderinfo)

    print(f"Order for {client_code} is {response}")
    return response['uniqueorderid']