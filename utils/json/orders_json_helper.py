from datetime import datetime
import jobs.exchange_tradeid_job
import json

from loguru import logger
from database.dto.orders import Order


def update_order_list(order_id, client_code, stock_code, quantity, limit_price, direction, order_type, status, message, exchange_trade_id, qty_traded, trade_price, sync_status, adhoc):
    order = Order(
        order_id=order_id,
        client_code=client_code,
        stock_code=stock_code,
        quantity=quantity,
        limit_price=limit_price,
        direction=direction,
        order_type=order_type,
        status=status,
        message=message,
        exchange_trade_id=exchange_trade_id,
        timestamp=get_current_date(),
        qty_traded=qty_traded,
        trade_price=trade_price,
        sync_status=sync_status,
        adhoc=adhoc
        # Using an ISO format timestamp
    )
    file_path = "order_book/orders.json"
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        # If file doesn't exist, initialize the data as an empty list
        data = {"orders": []}

    # Convert the Order object to JSON (dictionary)
    order_data = order.to_json()

    # Append the new order to the list of orders
    data["orders"].append(order_data)

    # Save the updated data back to the JSON file
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

    logger.info(f"Order {order.order_id} added successfully to order list.")


def update_status(order_id, status=None, message=None, order_type=None, exchange_trade_id=None, trade_price=None, trade_qty=None):
    # Load the existing orders from the JSON file
    file_path = "order_book/orders.json"
    
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        logger.error("The orders file does not exist.")
        return

    # Flag to track if the order was found
    order_found = False

    # Iterate through the orders and update the status for the matching client_code
    for order in data.get("orders", []):
        if order["OrderID"] == order_id:
            if status is not None:
                order["Status"] = status
            if message is not None:
                order["Message"] = message
            if order_type is not None:
                order["Order Type"] = order_type
            if exchange_trade_id is not None:
                order["ExchangeTradeID"] = exchange_trade_id
            if trade_price is not None:
                order["TradePrice"] = trade_price
            if trade_qty is not None:
                order["QtyTraded"] = trade_qty
            order_found = True
            break

    # If the order was found, save the updated data back to the file
    if order_found:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        logger.info(
            f"Order with OrderID {order_id} has been updated successfully.")
    else:
        logger.info(f"No order found with ClientCode {order_id}.")
    

def update_sync_status(order_id):
    file_path = "order_book/orders.json"

    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        logger.error("The orders file does not exist.")
        return

    # Flag to track if the order was found
    order_found = False

    # Iterate through the orders and update the status for the matching client_code
    for order in data.get("orders", []):
        if order["OrderID"] == order_id:
            order["SSyncStatustatus"] = "Synced"
            order_found = True
            break

    # If the order was found, save the updated data back to the file
    if order_found:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        logger.info(
            f"Order with OrderID {order_id} has been Synced successfully.")
    else:
        logger.info(f"No order found with Order ID {order_id}.")

def get_current_date():
    # Get the current date
    formatted_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    return formatted_date
