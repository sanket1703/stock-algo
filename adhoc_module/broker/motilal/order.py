import json
from tkinter import messagebox
from loguru import logger
from brokers.motilal.login import client_login
from stock_data.symbols import get_symbol_token
from notification.email.send_email import send_email
import tkinter as tk

def adhoc_status():
    
    client_code = client_code_entry.get()
    order_id = order_id_entry.get()
    
    logger.debug("Client Code:", client_code)
    logger.debug("Order Id:", order_id)
    
    Mofsl = client_login(client_code)
    
    order_details = Mofsl.GetOrderDetailByUniqueorderID(order_id,client_code)
    stock_code=order_details['data'][0]['symbol']
    qty=order_details['data'][0]['orderqty']
    price=order_details['data'][0]['price']
    direction=order_details['data'][0]['buyorsell']
    logger.debug(f"Order details for {client_code} for {order_id}:- {order_details} ")
    
    if (order_details['status'] == "FAILED" or order_details['message']=='NO RECORDS FOUND'):
        logger.error(f"Could not fetch the order details. Either the order_id expired or could not call MOFSL")
        message = f"{stock_code}/{direction}/{qty}@Rs{price} \n\nCould not fetch the order details. Either the order_id expired or could not call MOFSL. \n\n\n\nOrder Status:- {order_details['data'][0]['orderstatus']} \n\n\n\nError:- {order_details['data'][0]['error']} \n\n\n\n{order_details}"
        notification("Status",message,client_code,order_details['data'][0]['uniqueorderid'])
    
    if (order_details['data'][0]['orderstatus']=="Traded"):
        logger.info(f"Order is executed and the status is 'Traded'")
        message = f"{stock_code}/{direction}/{qty}@Rs{price} \n\nOrder is executed and the status is 'Traded. \n Exchange Trade Id:- {order_details['data'][0]['orderid']}\n\n\n\n {order_details}"
        notification("Status",message,client_code,order_details['data'][0]['uniqueorderid'])
    
    logger.info("Order is still not 'Traded")
    message = f"{stock_code}/{direction}/{qty}@Rs{price} \n\nOrder is still not 'Traded. \n\n\n\nOrder Status:- {order_details['data'][0]['orderstatus']} \n\n\n\nError:- {order_details['data'][0]['error']} \n\n\n\n{order_details}"
    notification("Status",message,client_code,order_details['data'][0]['uniqueorderid'])
    root.destroy()

def adhoc_buy():
    # Retrieve the values from each entry field
    client_code = client_code_entry.get()
    qty = int(qty_entry.get())
    limit_price = float(limit_price_entry.get())
    stock_code_ns = stock_code_entry.get()

    # Return or print the values
    logger.debug("Client Code:", client_code)
    logger.debug("Quantity:", qty)
    logger.debug("Limit Price:", limit_price)
    logger.debug("Stock Code:", stock_code_ns)
    
    logger.info(f"Placing buy order of {qty} {stock_code_ns} for {client_code} ")
    stock_code = get_symbol_token(stock_code_ns)
    Mofsl = client_login(client_code)
    Orderinfo = {
        "clientcode":client_code,      
        "exchange":"NSE",
        "symboltoken":stock_code,
        "buyorsell":"BUY",
        "ordertype":"LIMIT",
        "producttype":"DELIVERY",
        "orderduration":"DAY",
        "price":round(limit_price, 4),
        "quantityinlot":qty,
        "amoorder":"N"
    }
    yesno = messagebox.askyesno("Confirmation", "Are you sure you want to proceed?")
    if yesno:
        response = Mofsl.PlaceOrder(Orderinfo)
        logger.info(f"PlaceOrder for {client_code} Buy Response:- {response}")
        logger.info(f"PlaceOrder for Buy Message:- {response['message']}")
        message = f"Response for Buy Order {stock_code_ns}/BUY/{qty}@Rs{limit_price}:- \n{response}"
        notification("Buy",message,client_code,response['uniqueorderid'])
        root.destroy()
    else:
        root.destroy()
    

def adhoc_sell():
    # Retrieve the values from each entry field
    client_code = client_code_entry.get()
    qty = int(qty_entry.get())
    limit_price = float(limit_price_entry.get())
    stock_code_ns = stock_code_entry.get()

    # Return or print the values
    logger.debug("Client Code:", client_code)
    logger.debug("Quantity:", qty)
    logger.debug("Limit Price:", limit_price)
    logger.debug("Stock Code:", stock_code_ns)
    
    stock_code = get_symbol_token(stock_code_ns)
    
    logger.debug(f"Placing sell order of {qty} {stock_code} for {client_code} ")
    Mofsl = client_login(client_code)
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
         "price":round(limit_price, 4),
    }
    yesno = messagebox.askyesno("Confirmation", "Are you sure you want to proceed?")
    if yesno:
        response = Mofsl.PlaceOrder(Orderinfo)
        logger.info(f"PlaceOrder for {client_code} Sell Response:- {response}")
        logger.info(f"PlaceOrder for Sell Message:- {response['message']}")
        message = f"Response for Sell Order {stock_code_ns}/SELL/{qty}@{limit_price}:- \n{response}"
        notification("Sell",message,client_code,response['uniqueorderid'])
        root.destroy()
    else:
        root.destroy()


def adhoc_order(direction):

    # Main tkinter window
    global root
    root = tk.Tk()
    root.title("Order")
    global client_code_entry, qty_entry, limit_price_entry, stock_code_entry, order_id_entry

    # Labels and entry fields for each variable
    tk.Label(root, text="Client Code:").grid(row=0, column=0, padx=10, pady=5)
    client_code_entry = tk.Entry(root)
    client_code_entry.insert(0, "WEALTH666")
    client_code_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="Quantity:").grid(row=1, column=0, padx=10, pady=5)
    qty_entry = tk.Entry(root)
    qty_entry.insert(0, "0")
    qty_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(root, text="Limit Price:").grid(row=2, column=0, padx=10, pady=5)
    limit_price_entry = tk.Entry(root)
    limit_price_entry.insert(0, "0")
    limit_price_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(root, text="Stock Code:").grid(row=3, column=0, padx=10, pady=5)
    stock_code_entry = tk.Entry(root)
    stock_code_entry.insert(0, "STOCK.NS") 
    stock_code_entry.grid(row=3, column=1, padx=10, pady=5)
    
    tk.Label(root, text="Order Id:").grid(row=4, column=0, padx=10, pady=5)
    order_id_entry = tk.Entry(root)
    order_id_entry.insert(0, "ORDERID") 
    order_id_entry.grid(row=4, column=1, padx=10, pady=5)

    # Submit button
    if direction=='Buy':
        submit_button = tk.Button(root, text="Submit", command=adhoc_buy)
    elif direction =='Sell':
        submit_button = tk.Button(root, text="Submit", command=adhoc_sell)
    elif direction =='Status':
        submit_button = tk.Button(root, text="Submit", command=adhoc_status)
    else:
        logger.error("Please pass 'Buy' or 'Sell' or 'Status'")
        return
    
    submit_button.grid(row=5, column=0, columnspan=2, pady=10) 
    root.mainloop()


def notification(direction,message_text,client,order_id):
    sender = "Keyursanket.com"
    recipient = "sanketyou8@gmail.com"
    cc = "keyurmarolia2@gmail.com"
    subject = f"[{client}] Adhoc Order {direction} - {order_id}"
    send_email(sender,recipient,cc,subject,message_text,None)

# Commented code is the way in which you can fetch orders from the JSON
    
# def extract_order_details_from_file(file_path):
#     # Read JSON data from the file
#     with open(file_path, 'r') as file:
#         data = json.load(file)
    
#     # Extract values
#     client_code = data.get("client_code")
#     stock_code = data.get("stock_code")
#     limit_price = data.get("limit_price")
#     qty = data.get("qty")
    
#     return client_code, stock_code, limit_price, qty


# def place_adhoc_sell_order():
    
#     path = "adhoc_module/order_json/sell.json"
#     client_code, stock_code, limit_price, qty = extract_order_details_from_file(path)
#     stock_code = get_symbol_token(stock_code)
    
#     logger.debug(f"Placing sell order of {qty} {stock_code} for {client_code} ")
#     Mofsl = client_login(client_code)
#     Orderinfo = {
#         "clientcode":client_code,      
#         "exchange":"NSE",
#         "symboltoken":stock_code,
#         "buyorsell":"SELL",
#         "ordertype":"LIMIT",
#         "producttype":"DELIVERY",
#         "orderduration":"DAY",
#         "quantityinlot":qty,
#          "amoorder":"N",
#          "price":round(limit_price, 4),
#     }
#     response = Mofsl.PlaceOrder(Orderinfo)
#     logger.info(f"PlaceOrder for {client_code} Sell Response:- {response}")
#     logger.info(f"PlaceOrder for Sell Message:- {response['message']}")
#     message = f"Response for Sell Order:- \n{response}"
#     notification("Sell",message,client_code,response['uniqueorderid'])
#     return response['uniqueorderid']

# def place_adhoc_buy_order():
#     path = "adhoc_module/order_json/buy.json"
#     client_code, stock_code, limit_price, qty = extract_order_details_from_file(path)
#     logger.info(f"Placing buy order of {qty} {stock_code} for {client_code} ")
#     stock_code = get_symbol_token(stock_code)
#     Mofsl = client_login(client_code)
#     Orderinfo = {
#         "clientcode":client_code,      
#         "exchange":"NSE",
#         "symboltoken":stock_code,
#         "buyorsell":"BUY",
#         "ordertype":"LIMIT",
#         "producttype":"DELIVERY",
#         "orderduration":"DAY",
#         "price":round(limit_price, 4),
#         "quantityinlot":qty,
#         "amoorder":"N"
#     }
#     response = Mofsl.PlaceOrder(Orderinfo)
#     logger.info(f"PlaceOrder for {client_code} Buy Response:- {response}")
#     logger.info(f"PlaceOrder for Buy Message:- {response['message']}")
#     message = f"Response for Buy Order:- \n{response}"
#     notification("Buy",message,client_code,response['uniqueorderid'])
#     return response['uniqueorderid']

# def adhoc_order_status():
#     path = "adhoc_module/order_json/order_status.json"
#     client_code, order_id = extract_order_status_data_from_file(path)
#     Mofsl = client_login(client_code)
    
#     order_details = Mofsl.GetOrderDetailByUniqueorderID(order_id,client_code)
#     logger.debug(f"Order details for {client_code} for {order_id}:- {order_details} ")
    
#     if (order_details['status'] == "FAILED" or order_details['message']=='NO RECORDS FOUND'):
#         logger.error(f"Could not fetch the order details. Either the order_id expired or could not call MOFSL")
#         message = f"Could not fetch the order details. Either the order_id expired or could not call MOFSL. \n\n\n\nOrder Status:- {order_details['data'][0]['orderstatus']} \n\n\n\nError:- {order_details['data'][0]['error']} \n\n\n\n{order_details}"
#         notification("Status",message,client_code,order_details['data'][0]['uniqueorderid'])
    
#     if (order_details['data'][0]['orderstatus']=="Traded"):
#         logger.info(f"Order is executed and the status is 'Traded'")
#         message = f"Order is executed and the status is 'Traded. \n Exchange Trade Id:- {order_details['data'][0]['orderid']}\n\n\n\n {order_details}"
#         notification("Status",message,client_code,order_details['data'][0]['uniqueorderid'])
    
#     logger.info("Order is still not 'Traded")
#     message = f"Order is still not 'Traded. \n\n\n\nOrder Status:- {order_details['data'][0]['orderstatus']} \n\n\n\nError:- {order_details['data'][0]['error']} \n\n\n\n{order_details}"
#     notification("Status",message,client_code,order_details['data'][0]['uniqueorderid'])



def extract_order_status_data_from_file(file_path):
    
    with open(file_path, 'r') as file:
        data = json.load(file)

    client_code = data.get("client_code")
    order_id = data.get("order_id")

    return client_code, order_id