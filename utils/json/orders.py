from datetime import datetime
import jobs.exchange_tradeid_job
import json

from loguru import logger
from database.dto.orders import Order


def update_order_list(order_id, client_code, stock_code, quantity, limit_price, direction, order_type, status, message, exchange_trade_id):
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
        timestamp=get_current_date()  # Using an ISO format timestamp
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

    logger.debug(f"Order {order.order_id} added successfully.")


def update_status(client_code, status, message, order_type, exchange_trade_id):
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
        if order["ClientCode"] == client_code:
            order["Status"] = status
            order["Message"] = message
            order["Order Type"] = order_type
            order["ExchangeTradeID"] = exchange_trade_id
            order_found = True
            break

    # If the order was found, save the updated data back to the file
    if order_found:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
        logger.info(
            f"Order with ClientCode {client_code} has been updated successfully.")
    else:
        logger.info(f"No order found with ClientCode {client_code}.")
    
    

def get_current_date():
    # Get the current date
    formatted_date = datetime.now().strftime("%-d %B %Y")

    # Determine the suffix for the day
    day = datetime.now().day
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]

    # Add suffix to the day
    formatted_date_with_suffix = formatted_date.replace(
        f"{day}", f"{day}{suffix}")

    return formatted_date_with_suffix
