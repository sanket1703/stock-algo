import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from loguru import logger
from brokers.motilal.login import client_login
from brokers.motilal.order import get_modified_time, get_order_qty
from notification.email.send_email import send_email
from stock_data.symbols import get_symbol_token


def update_color(event):
    direction = direction_var.get()
    if direction == "Buy":
        root.configure(bg="green")
    elif direction == "Sell":
        root.configure(bg="red")
    elif direction == "Modify":
        root.configure(bg="orange")
    elif direction == "Status":
        root.configure(bg="light gray")
    elif direction == "Cancel Order":
        root.configure(bg="blue")


def execute_action():
    direction = direction_var.get()
    if direction == "Buy":
        buy_action()
    elif direction == "Sell":
        sell_action()
    elif direction == "Modify":
        modify_action()
    elif direction == "Status":
        status_action()
    elif direction == "Cancel Order":
        cancel_action()


def buy_action():
    # Retrieve the values from each entry field
    client_code = client_code_entry.get()
    qty = int(quantity_entry.get())
    limit_price = limit_price_entry.get()
    stock_code_ns = stock_code_entry.get()

    # Return or print the values
    logger.debug("Client Code:", client_code)
    logger.debug("Quantity:", qty)
    logger.debug("Limit Price:", limit_price)
    logger.debug("Stock Code:", stock_code_ns)
    stock_code = get_symbol_token(stock_code_ns)
    Mofsl = client_login(client_code)
    if (limit_price == "MARKET"):
        logger.info(
            f"Placing Market buy order of {qty} {stock_code_ns} for {client_code} ")
        Orderinfo = {
            "clientcode": client_code,
            "exchange": "NSE",
            "symboltoken": stock_code,
            "buyorsell": "BUY",
            "ordertype": "MARKET",
            "producttype": "DELIVERY",
            "orderduration": "DAY",
            "quantityinlot": qty,
            "amoorder": "N"
        }
    else:
        logger.info(
            f"Placing Limit buy order of {qty} {stock_code_ns} for {client_code} ")
        Orderinfo = {
            "clientcode": client_code,
            "exchange": "NSE",
            "symboltoken": stock_code,
            "buyorsell": "BUY",
            "ordertype": "LIMIT",
            "producttype": "DELIVERY",
            "orderduration": "DAY",
            "price": round(float(limit_price), 4),
            "quantityinlot": qty,
            "amoorder": "N"
        }

    yesno = messagebox.askyesno(
        "Confirmation", "Are you sure you want to proceed?")
    if yesno:
        response = Mofsl.PlaceOrder(Orderinfo)
        logger.info(f"PlaceOrder for {client_code} Buy Response:- {response}")
        logger.info(f"PlaceOrder for Buy Message:- {response['message']}")
        message = f"Response for Buy Order {stock_code_ns}/BUY/{qty}@Rs{limit_price}:- \n{response}"
        notification("Buy", message, client_code, response['uniqueorderid'])
        show_response_window(client_code,response['status'],
                             response['message'], message, "BUY")
        reset()
        # root.destroy()
    else:
        # root.destroy()
        reset()


def sell_action():
    # Retrieve the values from each entry field
    client_code = client_code_entry.get()
    qty = int(quantity_entry.get())
    limit_price = limit_price_entry.get()
    stock_code_ns = stock_code_entry.get()

    # Return or print the values
    logger.debug("Client Code:", client_code)
    logger.debug("Quantity:", qty)
    logger.debug("Limit Price:", limit_price)
    logger.debug("Stock Code:", stock_code_ns)

    stock_code = get_symbol_token(stock_code_ns)
    Mofsl = client_login(client_code)

    if (limit_price == "MARKET"):
        logger.debug(
            f"Placing MARKET sell order of {qty} {stock_code} for {client_code} ")
        Orderinfo = {
            "clientcode": client_code,
            "exchange": "NSE",
            "symboltoken": stock_code,
            "buyorsell": "SELL",
            "ordertype": "MARKET",
            "producttype": "DELIVERY",
            "orderduration": "DAY",
            "quantityinlot": qty,
            "amoorder": "N",
        }
    else:
        logger.debug(
            f"Placing LIMIT sell order of {qty} {stock_code} for {client_code} ")
        Orderinfo = {
            "clientcode": client_code,
            "exchange": "NSE",
            "symboltoken": stock_code,
            "buyorsell": "SELL",
            "ordertype": "LIMIT",
            "producttype": "DELIVERY",
            "orderduration": "DAY",
            "quantityinlot": qty,
            "amoorder": "N",
            "price": round(float(limit_price), 4)
        }

    yesno = messagebox.askyesno(
        "Confirmation", "Are you sure you want to proceed?")
    if yesno:
        response = Mofsl.PlaceOrder(Orderinfo)
        logger.info(f"PlaceOrder for {client_code} Sell Response:- {response}")
        logger.info(f"PlaceOrder for Sell Message:- {response['message']}")
        message = f"Response for Sell Order {stock_code_ns}/SELL/{qty}@{limit_price}:- \n{response}"
        notification("Sell", message, client_code, response['uniqueorderid'])
        show_response_window(client_code,response['status'],
                             response['message'], message, "SELL")
        reset()
    else:
        reset()


def modify_action():
    # Retrieve the values from each entry field
    client_code = client_code_entry.get()
    limit_price = limit_price_entry.get()
    stock_code_ns = stock_code_entry.get()
    order_id = order_id_entry.get()

    # Return or print the values
    logger.debug("Client Code:", client_code)
    logger.debug("Order Id:", order_id)
    logger.debug("Limit Price:", limit_price)
    logger.debug("Stock Code:", stock_code_ns)

    stock_code = get_symbol_token(stock_code_ns)
    Mofsl = client_login(client_code)
    qty = get_order_qty(Mofsl, client_code, order_id)
    if (limit_price == "MARKET"):
        logger.debug(
            f"Updating order {order_id} to MARKET for {stock_code} for {client_code} ")
        
        ModifiedOrderInfo = {
        "clientcode": client_code,
        "uniqueorderid": order_id,
        "newordertype": "MARKET",
        "neworderduration": "DAY",
        "newquantityinlot": qty,
        "newdisclosedquantity": 1,
        # "newprice": round(float(limit_price), 4),
        # "newtriggerprice":0,
        # "newgoodtilldate": 0,
        "lastmodifiedtime": get_modified_time(Mofsl, client_code, order_id),
        "qtytradedtoday": 0

    }
    else:
        logger.debug(
            f"Placing LIMIT sell order of {qty} {stock_code} for {client_code} ")
        
        ModifiedOrderInfo = {
        "clientcode": client_code,
        "uniqueorderid": order_id,
        "newordertype": "LIMIT",
        "neworderduration": "DAY",
        "newquantityinlot": qty,
        "newdisclosedquantity": 1,
        "newprice": round(float(limit_price), 4),
        # "newtriggerprice":0,
        # "newgoodtilldate": 0,
        "lastmodifiedtime": get_modified_time(Mofsl, client_code, order_id),
        "qtytradedtoday": 0

    }

    yesno = messagebox.askyesno(
        "Confirmation", "Are you sure you want to proceed?")
    if yesno:
        response = Mofsl.ModifyOrder(ModifiedOrderInfo)
        print(response)
        logger.debug(f"Modify to Market Response:- {response}")
        logger.info(f"Modify to Market Message:- {response['message']}")
        message = f"Response for Modify Order {stock_code_ns}/MODIFY/{qty}@{limit_price}:- \n{response}"
        notification("MODIFY", message, client_code, order_id)
        show_response_window(client_code,response['status'],
                             response['message'], message, "MODIFY")
        reset()
    else:
        reset()


def cancel_action():
    client_code = client_code_entry.get()
    order_id = order_id_entry.get()

    # Return or print the values
    logger.debug("Client Code:", client_code)
    logger.debug("Order Id", order_id)

    Mofsl = client_login(client_code)

    logger.debug(f"Cancel {order_id} of {client_code} ")

    yesno = messagebox.askyesno(
        "Confirmation", "Are you sure you want to proceed?")
    if yesno:
        response = Mofsl.CancelOrder(order_id, client_code)
        print(response)
        logger.debug(f"Cancel Order Response:- {response}")
        logger.info(f"Cancel Order Message:- {response['message']}")
        message = f"Cancel {order_id}:- \n{response}"
        notification("CANCEL", message, client_code, order_id)
        show_response_window(client_code, response['status'],
                             response['message'], message, "CANCEL")
        reset()
    else:
        reset()




def status_action():
    client_code = client_code_entry.get()
    order_id = order_id_entry.get()

    logger.debug("Client Code:", client_code)
    logger.debug("Order Id:", order_id)

    Mofsl = client_login(client_code)

    order_details = Mofsl.GetOrderDetailByUniqueorderID(order_id, client_code)
    stock_code = order_details['data'][0]['symbol']
    qty = order_details['data'][0]['orderqty']
    price = order_details['data'][0]['price']
    direction = order_details['data'][0]['buyorsell']
    logger.debug(
        f"Order details for {client_code} for {order_id}:- {order_details} ")

    if (order_details['status'] == "FAILED" or order_details['message'] == 'NO RECORDS FOUND'):
        logger.error(
            f"Could not fetch the order details. Either the order_id expired or could not call MOFSL")
        message = f"{stock_code}/{direction}/{qty}@Rs{price} \n\nCould not fetch the order details. Either the order_id expired or could not call MOFSL. \n\n\n\nOrder Status:- {order_details['data'][0]['orderstatus']} \n\n\n\nError:- {order_details['data'][0]['error']} \n\n\n\n{order_details}"

        notification("Status", message, client_code,
                     order_details['data'][0]['uniqueorderid'])
        show_response_window(client_code, order_details['status'],
                             message, message, "STATUS")
        reset()

    elif (order_details['data'][0]['orderstatus'] == "Traded"):
        logger.info(f"Order is executed and the status is 'Traded'")
        message = f"{stock_code}/{direction}/{qty}@Rs{price} \n\nOrder is executed and the status is 'Traded. \n\nExchange Trade Id:- {order_details['data'][0]['orderid']}\n\n\n\n {order_details}"
        notification("Status", message, client_code,
                     order_details['data'][0]['uniqueorderid'])
        show_response_window(client_code, order_details['status'],
                             message, message, "STATUS")

        reset()
    else:
        logger.info("Order is still not 'Traded")
        message = f"{stock_code}/{direction}/{qty}@Rs{price} \n\nOrder is still not 'Traded. \n\n\n\nOrder Status:- {order_details['data'][0]['orderstatus']} \n\n\n\nError:- {order_details['data'][0]['error']} \n\n\n\n{order_details}"

        notification("Status", message, client_code,
                     order_details['data'][0]['uniqueorderid'])
        show_response_window(client_code, order_details['status'],
                             message, message, "STATUS")
        reset()


def show_response_window(client_code, status, message, details, direction):
    title = f"{direction} Response"
    content = f"Client Code:   {client_code}\n\nDirection:   {direction}\n\nStatus:    {status}\n\nMessage:    {message}\n\nDetails:   {details}"
    messagebox.showinfo(title, content)

def reset():
    client_code_entry.delete(0, tk.END)
    client_code_entry.insert(0, "WEALTH666")
    quantity_entry.delete(0, tk.END)
    quantity_entry.insert(0, "0")
    stock_code_entry.delete(0, tk.END)
    stock_code_entry.insert(0, "IDEA.NS")
    order_id_entry.delete(0, tk.END)
    order_id_entry.insert(0, "")
    limit_price_entry.delete(0, tk.END)
    limit_price_entry.insert(0, "")

def ahdoc_order_box():

    # Display the response message in a pop-up window

    # Setting up the main window
    global root
    root = tk.Tk()

    root.title("Order Terminal")
    root.geometry("400x300")

    # Labels and Entry Fields
    tk.Label(root, text="Client Code:").grid(
        row=0, column=0, padx=10, pady=5, sticky="w")
    global client_code_entry
    client_code_entry = tk.Entry(root)
    client_code_entry.insert(0, "WEALTH666")
    client_code_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="Quantity:").grid(
        row=1, column=0, padx=10, pady=5, sticky="w")
    global quantity_entry
    quantity_entry = tk.Entry(root)
    quantity_entry.insert(0, "0")
    quantity_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(root, text="Limit Price:").grid(
        row=2, column=0, padx=10, pady=5, sticky="w")
    global limit_price_entry
    limit_price_entry = tk.Entry(root)
    limit_price_entry.insert(0, 0)
    limit_price_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(root, text="Stock Code:").grid(
        row=3, column=0, padx=10, pady=5, sticky="w")
    global stock_code_entry
    stock_code_entry = tk.Entry(root)
    stock_code_entry.insert(0, "IDEA.NS")
    stock_code_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(root, text="Order ID:").grid(
        row=4, column=0, padx=10, pady=5, sticky="w")
    global order_id_entry
    order_id_entry = tk.Entry(root)
    order_id_entry.grid(row=4, column=1, padx=10, pady=5)

    # Dropdown for Direction
    tk.Label(root, text="Direction:").grid(
        row=5, column=0, padx=10, pady=5, sticky="w")
    global direction_var
    direction_var = tk.StringVar()
    direction_dropdown = ttk.Combobox(root, textvariable=direction_var, values=[
        "Buy", "Sell", "Modify", "Status", "Cancel Order"])
    direction_dropdown.grid(row=5, column=1, padx=10, pady=5)
    direction_dropdown.bind("<<ComboboxSelected>>", update_color)

    # Submit Button
    submit_button = tk.Button(root, text="Submit", command=execute_action)
    submit_button.grid(row=6, column=0, columnspan=2, pady=20)

    # Run the application
    root.mainloop()


def notification(direction, message_text, client, order_id):
    sender = "Keyursanket.com"
    recipient = "sanketyou8@gmail.com"
    cc = "keyurmarolia2@gmail.com"
    subject = f"[{client}] Adhoc Order {direction} - {order_id}"
    send_email(sender, recipient, cc, subject, message_text, None)


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
